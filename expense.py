# expense.py

# Two main classes:
# - Expense: represents a single expense record.
# - ExpenseTracker: manages a collection of expenses and saves/loads them.


import os
import pandas as pd
from Categorizer import ExpenseCategorizer

class Expense:
    # Represents a single expense

    def __init__(self, description, amount, date, category=None):
        self.description = description
        self.amount = float(amount)
        self.date = date  # string in 'YYYY-MM-DD' format
        # Auto-categorize if no category is given
        if category is None:
            self.category = ExpenseCategorizer().categorize(description)
        else:
            self.category = category

    def to_dict(self):
        return {
            "date": self.date,
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
        }

    def __str__(self):
        return f"{self.date} | {self.description:<25} | {self.amount:>8.2f} | {self.category}"


class ExpenseTracker:
    """Manages a list of expenses and handles saving/loading to CSV."""

    def __init__(self, csv_path="expenses.csv"):
        self.csv_path = csv_path
        self.expenses = []
        self.categorizer = ExpenseCategorizer()
        self.load()

    def add_expense(self, description, amount, date):
        """Create a new expense, auto-categorize it, and store it."""
        expense = Expense(description, amount, date)
        self.expenses.append(expense)
        self.save()
        return expense

    def load(self):
        """Load expenses from CSV if the file exists."""
        if os.path.exists(self.csv_path):
            df = pd.read_csv(self.csv_path)
            self.expenses = []
            for _, row in df.iterrows():
                self.expenses.append(
                    Expense(
                        row["description"],
                        row["amount"],
                        row["date"],
                        row["category"],
                    )
                )

    def save(self):
        """Save all expenses to CSV."""
        if not self.expenses:
            return
        df = pd.DataFrame([e.to_dict() for e in self.expenses])
        df.to_csv(self.csv_path, index=False)

    def get_dataframe(self):
        """Return all expenses as a Pandas DataFrame."""
        if not self.expenses:
            return pd.DataFrame(columns=["date", "description", "amount", "category"])
        return pd.DataFrame([e.to_dict() for e in self.expenses])

    def total_spent(self):
        """Return the total amount spent (uses NumPy)."""
        import numpy as np
        if not self.expenses:
            return 0.0
        amounts = np.array([e.amount for e in self.expenses])
        return float(np.sum(amounts))

    def category_totals(self):
        """Return a dict {category: total_amount}."""
        import numpy as np
        df = self.get_dataframe()
        if df.empty:
            return {}
        result = {}
        for category, group in df.groupby("category"):
            result[category] = float(np.sum(group["amount"].values))
        return result

    def monthly_totals(self):
        """Return a dict {month: total_amount}."""
        df = self.get_dataframe()
        if df.empty:
            return {}
        df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
        return df.groupby("month")["amount"].sum().to_dict()

    def show_all(self):
        """Print all expenses."""
        if not self.expenses:
            print("\n  No expenses recorded yet.\n")
            return
        print("\n  " + "-" * 70)
        print(f"  {'DATE':<12} {'DESCRIPTION':<25} {'AMOUNT':>8}  CATEGORY")
        print("  " + "-" * 70)
        for e in self.expenses:
            print("  " + str(e))
        print("  " + "-" * 70)
        print(f"  TOTAL SPENT: {self.total_spent():.2f}")
        print()