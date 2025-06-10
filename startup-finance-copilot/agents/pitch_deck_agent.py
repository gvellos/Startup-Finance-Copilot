import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain_chroma import Chroma
from utils.vectorizer import file_to_chroma
from .financial_projection_agent import FinancialProjectionAgent
from .EUFundingAgent import EUFundingAgent
from .risk_advisor_agent import RiskAdvisorAgent
import re


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

class PitchDeckAgent:
    def __init__(self, model_name="meta-llama/llama-4-maverick:free"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model_name = model_name
        self.financial_agent = FinancialProjectionAgent()
        self.funding_agent = EUFundingAgent()
        self.risk_advisor = RiskAdvisorAgent()

    def extract_startup_data(self, context: str) -> dict:
        """
        Εξάγει βασικά στοιχεία startup από το κείμενο του αρχείου.
        (Μπορεί αργότερα να αντικατασταθεί με LLM extraction ή parsing.)
        """
        data = {
            "name": "Unknown",
            "industry": "Unknown",
            "business_model": "Unknown",
            "goal": 100000
        }

        if "Όνομα:" in context:
            data["name"] = context.split("Όνομα:")[1].split("\n")[0].strip()
        if "Τομέας:" in context:
            data["industry"] = context.split("Τομέας:")[1].split("\n")[0].strip()
        if "Business Model:" in context:
            data["business_model"] = context.split("Business Model:")[1].split("\n")[0].strip()
        if "Στόχος:" in context:
            try:
                goal_str = context.split("Στόχος:")[1].split("\n")[0].strip().replace("$", "").replace(",", "")
                data["goal"] = int(goal_str)
            except:
                pass
        if "Project:" in context:
            data["project"] = context.split("Project:")[1].split("\n")[0].strip()

        return data
    
    def extract_project(self, context: str) -> dict:
        data = {
            "project": "Ai"
        }

        match = re.search(r'Project:\s*(.+)', context)
        if match:
            data["project"] = match.group(1).strip()

        print(f"Extracted project data: {data}")
        return data

    def generate_pitch_deck(self, txt_path: str, excel_path: str) -> str:
        """
        Δημιουργεί pitch deck βάσει δεδομένων από αρχείο κειμένου και RAG τεχνική.
        """
        vectorstore: Chroma = file_to_chroma(txt_path)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        question = "Φτιάξε ένα pitch deck για τη startup με βάση τις πληροφορίες που υπάρχουν στο αρχείο."
        docs = retriever.get_relevant_documents(question)
        context = "\n".join([doc.page_content for doc in docs])

        # ➤ Εξαγωγή δομημένων δεδομένων για το financial agent
        startup_data = self.extract_startup_data(context)
        startup_project = self.extract_project(context)
        startup_project = startup_project["project"]

        # ➤ Κλήση του financial agent για δημιουργία προβλέψεων
        financials = self.financial_agent.generate_financials(startup_data, excel_path)

        risk_advice = self.risk_advisor.analyze_risks(startup_data)

        eu_funding = self.funding_agent.search_funding_opportunities(startup_project, max_results=10)

        # ➤ Δημιουργία prompt για το pitch deck με τις οικονομικές προβλέψεις ενσωματωμένες
        prompt = f"""
Είσαι ειδικός σύμβουλος startup. Με βάση τα παρακάτω στοιχεία, φτιάξε μια παρουσίαση pitch deck:

{context}

Οργάνωσε την παρουσίαση με βασικά σημεία:
- Όνομα
- Πρόβλημα
- Λύση
- Αγορά
- Business Model
- Ανταγωνιστικό Πλεονέκτημα
- Ομάδα
- Στόχος/Χρηματοδότηση
- Οικονομικές Προβλέψεις

### Οικονομικές Προβλέψεις:
{financials}
### Ευκαιρίες Χρηματοδότησης:
{eu_funding}
### Ανάλυση Κινδύνων:
{risk_advice}
"""

        # ➤ Αποστολή προς OpenRouter
        messages = [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ]

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "Startup Finance Copilot"
            }
        )

        return response.choices[0].message.content
