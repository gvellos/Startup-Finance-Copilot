# EUFundingAgent.py
from utils.EUFundingScraper import EUFundingScraper

class EUFundingAgent:
    def __init__(self):
        self.scraper = EUFundingScraper()

    def search_funding_opportunities(self, keyword, max_results=5):
        """
        Αναζητά ευκαιρίες χρηματοδότησης για ένα δεδομένο keyword.
        
        Args:
            keyword (str): Ο όρος αναζήτησης (π.χ. 'AI', 'green energy').
            max_results (int): Μέγιστος αριθμός αποτελεσμάτων.

        Returns:
            list[dict]: Λίστα από ευκαιρίες με τίτλο, deadline, περιγραφή.
        """
        print(f"[EUFundingAgent] Ξεκινώ αναζήτηση για: '{keyword}'...")
        try:
            results = self.scraper.search(keyword, max_results=max_results)
            print(f"[EUFundingAgent] Βρέθηκαν {len(results)} αποτελέσματα.")
            return results
        except Exception as e:
            print(f"[EUFundingAgent] Σφάλμα κατά την αναζήτηση: {e}")
            return []

# Παράδειγμα χρήσης
if __name__ == "__main__":
    agent = EUFundingAgent()
    funding_results = agent.search_funding_opportunities("artificial intelligence", max_results=10)

    for i, result in enumerate(funding_results, 1):
        print(f"\nFunding Opportunity {i}")
        print(f"Title: {result['title']}")
        print(f"Deadline: {result['deadline']}")
        print(f"Description: {result['description']}")
