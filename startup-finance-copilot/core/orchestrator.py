from agents.pitch_deck_agent import PitchDeckAgent
from agents.financial_projection_agent import FinancialProjectionAgent
from agents.valuation_agent import ValuationAgent

class StartupCopilot:
    def __init__(self):
        self.pitch_agent = PitchDeckAgent()
        self.financial_agent = FinancialProjectionAgent()
        self.valuation_agent = ValuationAgent()


    def run(self, startup_data):
        print("➡️ Δημιουργία Pitch Deck...")
        pitch = self.pitch_agent.generate_pitch_deck(startup_data)

        print("➡️ Δημιουργία Οικονομικών Προβλέψεων...")
        financials = self.financial_agent.generate_financials(startup_data)

        # Μελλοντικά: χρήση και άλλων πρακτόρων
        print("➡️ Υπολογισμός Αποτίμησης...")
        valuation = self.valuation_agent.compute_valuation(
            revenue_forecast=[120000, 250000, 400000],
            ebitda_margin=0.25,
            discount_rate=0.15,
            multiple=8
        )

        valuation = self.valuation_agent.load_inputs_from_excel("startup-finance-copilot/data/valuation_input.xlsx")



        return {
            "pitch_deck": pitch,
            "financials": financials,
            "valuation": valuation,

        }
