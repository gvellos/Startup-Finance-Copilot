from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Get the OpenRouter API key
api_key = os.getenv("OPENROUTER_API_KEY")

class RiskAdvisorAgent:
    def __init__(self, model_name="meta-llama/llama-4-maverick:free"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model_name = model_name

    def analyze_risks(self, startup_data: dict) -> str:
        prompt = f"""
        Είσαι σύμβουλος ρίσκου για startups. Ανάλυσε τους πιθανούς κινδύνους για την παρακάτω startup και πρότεινε στρατηγικές περιορισμού κινδύνου καθώς και plan B για τα χειρότερα σενάρια:

        Όνομα: {startup_data['name']}
        Τομέας: {startup_data['industry']}
        Επιχειρηματικό μοντέλο: {startup_data['business_model']}
        Στόχος χρηματοδότησης: ${startup_data['goal']}

        Θέλω:
        - Αναγνώριση βασικών επιχειρηματικών κινδύνων
        - Ανάλυση “τι θα γίνει αν” (what-if) για cashflow, team, αγορά
        - Προτεινόμενα mitigation strategies και εναλλακτικές πορείες
        """

        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]

        response = self.client.chat.completions.create(
            extra_headers={"HTTP-Referer": "<YOUR_SITE_URL>", "X-Title": "<YOUR_SITE_NAME>"},
            model=self.model_name,
            messages=messages
        )

        return response.choices[0].message.content