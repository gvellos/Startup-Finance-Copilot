from agents.pitch_deck_agent import PitchDeckAgent


def main():
    # Example startup information
    startup_info = {
        "name": "Startup XYZ",
        "problem": "Lack of efficient communication in remote teams.",
        "solution": "An AI-powered tool for improving communication and collaboration.",
        "market": "Remote working teams, startups, and enterprises.",
        "business_model": "Subscription-based SaaS model.",
        "goal": "Raise $500,000 in seed funding to develop the platform."
    }

    # Initialize the PitchDeckAgent
    agent = PitchDeckAgent()

    # Generate the pitch deck
    pitch_deck = agent.generate_pitch_deck(startup_info)

    # Output the generated pitch deck
    print("Generated Pitch Deck:")
    print(pitch_deck)

if __name__ == "__main__":
    main()
