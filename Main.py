# main.py
"""Intelligent Expense Categorizer
Menu-driven interface for the whole application."""

from expense import ExpenseTracker
from Charts import ExpenseCharts


def show_menu():
    print("\n" + "=" * 50)
    print("INTELLIGENT EXPENSE CATEGORIZER")
    print("=" * 50)
    print("1. Add an expense")
    print("2. View all expenses")
    print("3. Show spending by category (pie chart)")
    print("4. Show monthly spending (bar chart)")
    print("5. Show summary statistics")
    print("6. Exit")
    print("=" * 50)


def add_expense_flow(tracker):
    print("\n--- Add Expense ---")
    description = input("  Description (e.g., 'pizza with friends'): ").strip()
    if not description:
        print("  Description cannot be empty.")
        return

    try:
        amount = float(input("  Amount: ").strip())
        if amount <= 0:
            print("  Amount must be positive.")
            return
    except ValueError:
        print("  Invalid amount. Please enter a number.")
        return

    date = input("  Date (YYYY-MM-DD): ").strip()
    # Basic validation
    import datetime
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("  Invalid date format. Use YYYY-MM-DD.")
        return

    expense = tracker.add_expense(description, amount, date)
    print(f"\n  ✔ Expense added and auto-categorized as: {expense.category}")


def show_summary(tracker):
    """Print summary statistics using NumPy."""
    import numpy as np

    if not tracker.expenses:
        print("\n  No expenses yet.")
        return

    amounts = np.array([e.amount for e in tracker.expenses])
    print("\n--- Summary Statistics ---")
    print(f"  Number of expenses : {len(amounts)}")
    print(f"  Total spent        : {np.sum(amounts):.2f}")
    print(f"  Average per expense: {np.mean(amounts):.2f}")
    print(f"  Largest expense    : {np.max(amounts):.2f}")
    print(f"  Smallest expense   : {np.min(amounts):.2f}")

    print("\n  Spending per category:")
    for cat, total in sorted(tracker.category_totals().items(),
                              key=lambda x: -x[1]):
        print(f"    {cat:<15} {total:>8.2f}")


def main():
    tracker = ExpenseTracker()
    charts = ExpenseCharts(tracker)

    while True:
        show_menu()
        choice = input("  Enter choice (1-6): ").strip()

        if choice == "1":
            add_expense_flow(tracker)
        elif choice == "2":
            tracker.show_all()
        elif choice == "3":
            charts.category_pie_chart()
        elif choice == "4":
            charts.monthly_bar_chart()
        elif choice == "5":
            show_summary(tracker)
        elif choice == "6":
            print("\n  Goodbye!\n")
            break
        else:
            print("  Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()