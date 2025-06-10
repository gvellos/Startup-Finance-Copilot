# agents/financial_projection_agent.py

import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

class FinancialProjectionAgent:
    def __init__(self, model_name="meta-llama/llama-4-maverick:free"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model_name = model_name



    def generate_financials(self, startup_data: dict,excel_path: str) -> str:
        df = pd.read_excel(excel_path)
        df.to_string(index=False)
        excel_data = pd.read_excel(excel_path)

        prompt = f"""
        Έχεις τα οικονομικά στοιχεία της startup:

        {excel_data}

        Χρησιμοποιώντας αυτά και τα παρακάτω χαρακτηριστικά της startup, δημιούργησε οικονομική πρόβλεψη για τα επόμενα 3 χρόνια:

        Όνομα: {startup_data['name']}
        Τομέας: {startup_data['industry']}
        Επιχειρηματικό μοντέλο: {startup_data['business_model']}
        Στόχος χρηματοδότησης: ${startup_data['goal']}

        Παρουσίασε:
        - Εκτιμώμενα έσοδα ανά έτος
        - Εκτιμώμενα κόστη (ανάπτυξης, μάρκετινγκ, λειτουργικά)
        - EBITDA
        - Ανάλυση ανά έτος
        """

        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]

        response = self.client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "Startup Finance Copilot"
            },
            model=self.model_name,
            messages=messages
        )

        return response.choices[0].message.content
