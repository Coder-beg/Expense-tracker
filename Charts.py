# charts.py
# Generating Matplotlib charts from expense data

import os
import matplotlib.pyplot as plt


class ExpenseCharts:
    """Creates charts for expense data."""

    def __init__(self, tracker, output_dir="charts"):
        self.tracker = tracker
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def category_pie_chart(self, show=True):
        """Pie chart of spending by category."""
        totals = self.tracker.category_totals()
        if not totals:
            print("  No data to plot.")
            return

        labels = list(totals.keys())
        values = list(totals.values())

        plt.figure(figsize=(7, 5))
        plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.title("Spending by Category")
        plt.tight_layout()
        path = os.path.join(self.output_dir, "category_pie.png")
        plt.savefig(path)
        print(f"  Chart saved to {path}")
        if show:
            plt.show()
        plt.close()

    def monthly_bar_chart(self, show=True):
        """Bar chart of total spending per month."""
        monthly = self.tracker.monthly_totals()
        if not monthly:
            print("  No data to plot.")
            return

        months = list(monthly.keys())
        values = list(monthly.values())

        plt.figure(figsize=(8, 5))
        plt.bar(months, values, color="steelblue")
        plt.title("Monthly Spending")
        plt.xlabel("Month")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = os.path.join(self.output_dir, "monthly_bar.png")
        plt.savefig(path)
        print(f"  Chart saved to {path}")
        if show:
            plt.show()
        plt.close()