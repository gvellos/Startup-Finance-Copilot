from agents.pitch_deck_agent import PitchDeckAgent
from agents.financial_projection_agent import FinancialProjectionAgent
from agents.risk_advisor_agent import RiskAdvisorAgent

class StartupCopilot:
    def __init__(self):
        self.pitch_agent = PitchDeckAgent()
        self.financial_agent = FinancialProjectionAgent()
        self.risk_agent = RiskAdvisorAgent()

    def run(self, startup_data):
        print("➡️ Δημιουργία Pitch Deck...")
        pitch = self.pitch_agent.generate_pitch_deck(startup_data)

        print("➡️ Δημιουργία Οικονομικών Προβλέψεων...")
        financials = self.financial_agent.generate_financials(startup_data)

        print("➡️ Ανάλυση Ρίσκων και Στρατηγικές Plan B...")
        risk_analysis = self.risk_agent.analyze_risks(startup_data)

        return {
            "pitch_deck": pitch,
            "financials": financials,
            "risk_analysis": risk_analysis,
        }
