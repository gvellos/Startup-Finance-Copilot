from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
import pandas as pd


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

class ValuationAgent:
    def __init__(self, model_name="meta-llama/llama-4-maverick:free"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model_name = model_name

    def compute_valuation(self, revenue_forecast: list, ebitda_margin: float, discount_rate: float, multiple: float) -> dict:
        # Υπολογισμός EBITDA
        ebitda = [rev * ebitda_margin for rev in revenue_forecast]

        # DCF (Discounted Cash Flow)
        dcf = [ebitda[i] / ((1 + discount_rate) ** (i + 1)) for i in range(len(ebitda))]
        dcf_valuation = round(np.sum(dcf), 2)

        # Multiples-based valuation
        terminal_value = round(ebitda[-1] * multiple, 2)

        # Συνδυασμός: μέση αποτίμηση
        average_valuation = round((dcf_valuation + terminal_value) / 2, 2)

        # Prompt προς LLM που περιλαμβάνει τα πραγματικά αποτελέσματα
        prompt = f"""
        Είσαι οικονομικός σύμβουλος startup και ο πελάτης σου ζητάει αναφορά αποτίμησης.
        
        Χρησιμοποίησε τα εξής δεδομένα:
        - Έσοδα 3ετίας: {revenue_forecast}
        - EBITDA Margin: {ebitda_margin}
        - Discount Rate: {discount_rate}
        - EBITDA Multiple: {multiple}

        Τα πραγματικά υπολογισμένα μεγέθη είναι:
        - EBITDA ανά έτος: {ebitda}
        - DCF Value (παρούσα αξία ταμειακών ροών): {dcf_valuation}
        - Terminal Value (EBITDA × multiple): {terminal_value}
        - Μέση Αποτίμηση: {average_valuation}

        Εξήγησε τα αποτελέσματα σε μορφή παρουσίασης για μη τεχνικό κοινό (VCs, founders).
        """

        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )

        summary = response.choices[0].message.content

        return {
            "dcf_valuation": dcf_valuation,
            "terminal_value": terminal_value,
            "average_valuation": average_valuation,
            "summary": summary
        }

    

    def load_inputs_from_excel(self, filepath: str):
        try:
            # Φόρτωση revenue forecast
            df_revenue = pd.read_excel(filepath, sheet_name="RevenueForecast")
            if "Revenue" not in df_revenue.columns:
                raise ValueError("Το φύλλο 'RevenueForecast' πρέπει να περιέχει στήλη 'Revenue'.")
            revenue_forecast = df_revenue["Revenue"].dropna().tolist()
            if not revenue_forecast:
                raise ValueError("Η λίστα εσόδων είναι κενή.")
            
            # Φόρτωση assumptions
            df_assumptions = pd.read_excel(filepath, sheet_name="Assumptions")
            assumptions = df_assumptions.set_index("Parameter")["Value"]

            # Ανάγνωση τιμών με fallback
            ebitda_margin = float(assumptions.get("EBITDA Margin", 0.2))
            discount_rate = float(assumptions.get("Discount Rate", 0.1))
            multiple = float(assumptions.get("Multiple", 7))

            print("📄 Excel φορτώθηκε με επιτυχία.")

        except FileNotFoundError:
            print("❌ Το αρχείο Excel δεν βρέθηκε. Χρησιμοποιούνται default τιμές.")
            revenue_forecast = [100000, 200000, 300000]
            ebitda_margin = 0.2
            discount_rate = 0.1
            multiple = 7

        except Exception as e:
            print(f"⚠️ Σφάλμα κατά την ανάγνωση Excel: {e}")
            revenue_forecast = [100000, 200000, 300000]
            ebitda_margin = 0.2
            discount_rate = 0.1
            multiple = 7

        return self.compute_valuation(
            revenue_forecast,
            ebitda_margin,
            discount_rate,
            multiple
        )



