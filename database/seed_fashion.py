import random
from datetime import date, timedelta
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import get_connection

random.seed(42)

regions = ["North", "South", "East", "West"]
products = ["Winter Jackets", "Jeans", "T-Shirts", "Sneakers", "Dresses", "Hoodies", "Shorts", "Boots"]

def generate_sales_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM sales_transactions")
    connection.commit()

    start_date = date.today() - timedelta(days=59)
    rows = []

    regional_factors = {"North": 1.3, "South": 0.95, "East": 0.9, "West": 0.85}
    product_demand = {"Winter Jackets": 90, "Jeans": 200, "T-Shirts": 250, "Sneakers": 180, "Dresses": 150, "Hoodies": 140, "Shorts": 120, "Boots": 100}

    for day_number in range(60):
        current_date = start_date + timedelta(days=day_number)
        for region in regions:
            for product in products:
                base_orders = int(product_demand[product] * regional_factors[region])
                base_orders += random.randint(-30, 30)
                if day_number >= 50 and region == "North":
                    base_orders = int(base_orders * 0.68)
                orders = max(5, base_orders)

                price = {"Winter Jackets": 129.99, "Jeans": 69.99, "T-Shirts": 24.99, "Sneakers": 119.99, "Dresses": 89.99, "Hoodies": 54.99, "Shorts": 39.99, "Boots": 149.99}[product]
                revenue = orders * price
                base_marketing = 12000 if product in ["Winter Jackets", "Dresses", "Boots"] else 8000
                marketing_spend = base_marketing + random.uniform(-3000, 3000)

                rows.append((current_date, region, product, orders, round(revenue, 2), round(marketing_spend, 2)))

    query = "INSERT INTO sales_transactions (date, region, product, orders, revenue, marketing_spend) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, rows)
    connection.commit()
    print(f"✓ Inserted {len(rows)} fashion sales records")
    cursor.close()
    connection.close()

def generate_reviews():
    from datetime import datetime
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM customer_reviews")
    connection.commit()

    reviews = [
        ("Winter Jackets", 5, "Perfect fit and very warm. Great quality fabric."),
        ("Winter Jackets", 2, "Sizing runs small, had to exchange."),
        ("Jeans", 5, "Best fitting jeans I've ever bought. Very comfortable."),
        ("Jeans", 3, "Color faded after first wash."),
        ("T-Shirts", 5, "High quality cotton, colors don't fade."),
        ("T-Shirts", 2, "Shrunk after washing, disappointing quality."),
        ("Sneakers", 5, "Extremely comfortable, perfect for running."),
        ("Sneakers", 1, "Sole separated after 2 weeks, returned."),
        ("Dresses", 5, "Elegant design, fits perfectly. Love it!"),
        ("Dresses", 4, "Pretty dress but shorter than expected."),
        ("Hoodies", 5, "So cozy and the fabric is premium quality."),
        ("Hoodies", 2, "Zipper broke after first use."),
        ("Shorts", 4, "Great for summer, comfortable and breathable."),
        ("Shorts", 3, "Pockets are too small for phone."),
        ("Boots", 5, "Stylish and super comfortable even for long wear."),
        ("Boots", 2, "Shipping took 3 weeks, customer service unhelpful."),
        ("Winter Jackets", 4, "Warm and stylish, good value."),
        ("Jeans", 5, "Perfect dark wash, very durable."),
        ("T-Shirts", 4, "Nice fit, colors are vibrant."),
        ("Sneakers", 4, "Good shoes, delivery was fast."),
    ]

    query = "INSERT INTO customer_reviews (review_date, product, rating, review_text) VALUES (%s, %s, %s, %s)"
    data = [(datetime.now(), product, rating, text) for product, rating, text in reviews]
    cursor.executemany(query, data)
    connection.commit()
    print(f"✓ Inserted {len(data)} fashion reviews")
    cursor.close()
    connection.close()

def generate_crm_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM crm_customers")
    connection.commit()

    rows = []
    customer_id = 1000
    churn_rates = {"North": 0.08, "South": 0.14, "East": 0.10, "West": 0.18}

    for region in regions:
        for _ in range(200):
            churn = random.random() < churn_rates[region]
            signup = date.today() - timedelta(days=random.randint(30, 365))
            rows.append((customer_id, region, churn, signup))
            customer_id += 1

    query = "INSERT INTO crm_customers (customer_id, region, churn, signup_date) VALUES (%s, %s, %s, %s)"
    cursor.executemany(query, rows)
    connection.commit()
    print(f"✓ Inserted {len(rows)} fashion CRM records")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    print("=" * 70)
    print("LOADING: FASHION RETAIL DATA (Clothing, Shoes, Accessories)")
    print("=" * 70)
    generate_sales_data()
    generate_reviews()
    generate_crm_data()
    print("✅ Fashion dataset loaded successfully!\n")
