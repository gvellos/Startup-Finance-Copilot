from openai import OpenAI
import os
# Correct Code
from dotenv import load_dotenv# Load environment variables
load_dotenv()

# Get the OpenRouter API key
api_key = os.getenv("OPENROUTER_API_KEY")

class PitchDeckAgent:
    def __init__(self, model_name="meta-llama/llama-4-maverick:free"):
        # Initialize the OpenAI client (OpenRouter)
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model_name = model_name

    def generate_pitch_deck(self, startup_info: dict) -> str:
        # Construct the prompt for generating the pitch deck
        prompt = f"""
        Είσαι ειδικός σύμβουλος startup. Με βάση τα παρακάτω στοιχεία, φτιάξε μια παρουσίαση pitch deck:
        - Όνομα: {startup_info['name']}
        - Πρόβλημα: {startup_info['problem']}
        - Λύση: {startup_info['solution']}
        - Αγορά: {startup_info['market']}
        - Business model: {startup_info['business_model']}
        - Στόχος: {startup_info['goal']}
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

        # Return the response content (pitch deck)
        return response.choices[0].message.content
