from core.orchestrator import StartupCopilot

startup_data = {
    "name": "Startup XYZ",
    "problem": "Αναποτελεσματική συνεργασία σε απομακρυσμένες ομάδες",
    "solution": "Πλατφόρμα με AI για βελτίωση επικοινωνίας",
    "market": "Αγορά remote εργασίας",
    "business_model": "SaaS",
    "goal": "500000",
    "industry": "SaaS για remote teams"
}

copilot = StartupCopilot()
results = copilot.run(startup_data)

print("\n🧾 Pitch Deck:\n")
print(results["pitch_deck"])

print("\n📊 Financial Projections:\n")
print(results["financials"])
