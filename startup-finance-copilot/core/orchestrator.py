from agents.pitch_deck_agent import PitchDeckAgent
from agents.financial_projection_agent import FinancialProjectionAgent

class StartupCopilot:
    def __init__(self):
        self.pitch_agent = PitchDeckAgent()
        self.financial_agent = FinancialProjectionAgent()

    def run(self, startup_data):
        print("➡️ Δημιουργία Pitch Deck...")
        pitch = self.pitch_agent.generate_pitch_deck(startup_data)

        print("➡️ Δημιουργία Οικονομικών Προβλέψεων...")
        financials = self.financial_agent.generate_financials(startup_data)

        # Μελλοντικά: χρήση και άλλων πρακτόρων

        return {
            "pitch_deck": pitch,
            "financials": financials,
        }
