from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Get the OpenRouter API key
api_key = os.getenv("OPENROUTER_API_KEY")

class FinancialProjectionAgent:
    def __init__(self, model_name="meta-llama/llama-4-maverick:free"):
        # Initialize the OpenAI client (OpenRouter)
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model_name = model_name

    def generate_financials(self, startup_data: dict) -> str:
        # Construct the prompt for generating financial projections
        prompt = f"""
        Δημιούργησε μια οικονομική πρόβλεψη για τα επόμενα 3 χρόνια για την startup με τα εξής χαρακτηριστικά:
        
        Όνομα: {startup_data['name']}
        Τομέας: {startup_data['industry']}
        Επιχειρηματικό μοντέλο: {startup_data['business_model']}
        Στόχος χρηματοδότησης: ${startup_data['goal']}
        
        Παρουσίασε:
        - Εκτιμώμενα έσοδα ανά έτος
        - Εκτιμώμενα κόστη (ανάπτυξης, μάρκετινγκ, λειτουργικά)
        - EBITDA
        - Ανάλυση ανά έτος

        Η απάντηση να είναι σε μορφή παρουσίασης/δομημένου κειμένου.
        """
        
        # Define the message format
        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]

        # Make the request to OpenRouter for the response
        response = self.client.chat.completions.create(
            extra_headers={"HTTP-Referer": "<YOUR_SITE_URL>", "X-Title": "<YOUR_SITE_NAME>"},
            model=self.model_name,
            messages=messages
        )

        # Return the response content (financial projections)
        return response.choices[0].message.content
