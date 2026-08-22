import random
from datetime import date, timedelta

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import get_connection


random.seed(42)


regions = [
    "North",
    "South",
    "East",
    "West",
]

products = [
    "Laptop",
    "Phone",
    "Tablet",
    "Headphones",
]


def generate_sales_data():
    connection = get_connection()
    cursor = connection.cursor()

    start_date = date.today() - timedelta(days=59)

    rows = []

    for day_number in range(60):
        current_date = start_date + timedelta(days=day_number)

        for region in regions:
            for product in products:

                base_orders = random.randint(80, 150)

                # Create a deliberate business problem
                # during the last 10 days.
                if day_number >= 50:
                    base_orders *= 0.92

                orders = int(base_orders)

                price = {
                    "Laptop": 800,
                    "Phone": 500,
                    "Tablet": 350,
                    "Headphones": 120,
                }[product]

                revenue = orders * price

                marketing_spend = random.uniform(
                    5000,
                    15000,
                )

                rows.append(
                    (
                        current_date,
                        region,
                        product,
                        orders,
                        round(revenue, 2),
                        round(marketing_spend, 2),
                    )
                )

    query = """
        INSERT INTO sales_transactions
        (
            date,
            region,
            product,
            orders,
            revenue,
            marketing_spend
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.executemany(query, rows)

    connection.commit()

    print(f"Inserted {len(rows)} sales records.")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_sales_data()