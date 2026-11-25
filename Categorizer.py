# categorizer.py
# Rule-based text classifier for expenses.
# Using keyword matching to assign a category.

class ExpenseCategorizer:
    """Classifies expense descriptions into categories using keyword rules."""

    def __init__(self):
        # Each category maps to a list of keywords.
        # You can easily add more keywords or categories here.
        self.rules = {
            "Food": [
                "pizza", "burger", "lunch", "dinner", "breakfast",
                "cafe", "coffee", "restaurant", "biryani", "meal",
                "snack", "food", "groceries", "grocery"
            ],
            "Transport": [
                "uber", "careem", "bus", "train", "fuel", "petrol",
                "taxi", "rickshaw", "metro", "ticket", "parking"
            ],
            "Education": [
                "book", "books", "fee", "tuition", "course", "stationery",
                "notebook", "pen", "exam", "university", "school"
            ],
            "Shopping": [
                "shirt", "shoes", "clothes", "shopping", "mall",
                "amazon", "daraz", "dress", "jacket", "bag"
            ],
            "Bills": [
                "electricity", "water", "gas", "internet", "wifi",
                "phone", "mobile", "bill", "recharge"
            ],
            "Health": [
                "medicine", "doctor", "hospital", "pharmacy",
                "gym", "dentist", "clinic"
            ],
            "Entertainment": [
                "movie", "cinema", "netflix", "spotify", "game",
                "concert", "youtube", "subscription"
            ],
        }
        self.default_category = "Other"

    def categorize(self, description):
        """
        Return the best matching category for a description.
        Matching is case-insensitive and checks each keyword.
        """
        text = description.lower()

        # Score each category by how many keywords appear
        scores = {}
        for category, keywords in self.rules.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[category] = score

        if not scores:
            return self.default_category

        # Return the category with the highest score
        return max(scores, key=scores.get)

    def list_categories(self):
        """Return all known categories."""
        return list(self.rules.keys()) + [self.default_category]