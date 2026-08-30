import random
from datetime import date, timedelta
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import get_connection

random.seed(42)

regions = ["North", "South", "East", "West"]
products = ["Organic Vegetables", "Fresh Bread", "Dairy Products", "Meat", "Beverages", "Snacks", "Frozen Foods", "Bakery Items"]

def generate_sales_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM sales_transactions")
    connection.commit()

    start_date = date.today() - timedelta(days=59)
    rows = []

    regional_factors = {"North": 1.1, "South": 1.0, "East": 1.15, "West": 0.9}
    product_demand = {"Organic Vegetables": 350, "Fresh Bread": 280, "Dairy Products": 400, "Meat": 300, "Beverages": 450, "Snacks": 320, "Frozen Foods": 280, "Bakery Items": 240}

    for day_number in range(60):
        current_date = start_date + timedelta(days=day_number)
        for region in regions:
            for product in products:
                base_orders = int(product_demand[product] * regional_factors[region])
                base_orders += random.randint(-50, 50)
                if day_number >= 50 and region == "East":
                    base_orders = int(base_orders * 0.70)
                orders = max(10, base_orders)

                price = {"Organic Vegetables": 8.99, "Fresh Bread": 4.99, "Dairy Products": 6.99, "Meat": 15.99, "Beverages": 5.99, "Snacks": 3.99, "Frozen Foods": 7.99, "Bakery Items": 5.49}[product]
                revenue = orders * price
                base_marketing = 6000
                marketing_spend = base_marketing + random.uniform(-1500, 1500)

                rows.append((current_date, region, product, orders, round(revenue, 2), round(marketing_spend, 2)))

    query = "INSERT INTO sales_transactions (date, region, product, orders, revenue, marketing_spend) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, rows)
    connection.commit()
    print(f"✓ Inserted {len(rows)} grocery sales records")
    cursor.close()
    connection.close()

def generate_reviews():
    from datetime import datetime
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM customer_reviews")
    connection.commit()

    reviews = [
        ("Organic Vegetables", 5, "Fresh and crisp, exactly what I expected."),
        ("Organic Vegetables", 2, "Some items were wilted upon arrival."),
        ("Fresh Bread", 5, "Baked fresh daily, absolutely delicious."),
        ("Fresh Bread", 3, "Arrived stale, expiration date was near."),
        ("Dairy Products", 5, "Great quality dairy, very fresh."),
        ("Dairy Products", 2, "Expired before expected date."),
        ("Meat", 5, "Premium cuts, excellent quality."),
        ("Meat", 1, "Poor quality and smell, returned immediately."),
        ("Beverages", 5, "Great variety and competitive prices."),
        ("Beverages", 4, "Good selection but delivery was delayed."),
        ("Snacks", 5, "Healthy options, very satisfied."),
        ("Snacks", 3, "Some items were damaged in packaging."),
        ("Frozen Foods", 4, "Convenient and good quality."),
        ("Frozen Foods", 2, "Thawed during delivery in summer heat."),
        ("Bakery Items", 5, "Incredibly fresh and tasty pastries."),
        ("Bakery Items", 4, "Good quality, but limited selection."),
        ("Organic Vegetables", 4, "Mostly fresh, occasional bruised item."),
        ("Fresh Bread", 4, "Tasty but loaves are getting smaller."),
        ("Dairy Products", 5, "Excellent freshness, love the organic options."),
        ("Meat", 4, "Good cuts, fair pricing."),
    ]

    query = "INSERT INTO customer_reviews (review_date, product, rating, review_text) VALUES (%s, %s, %s, %s)"
    data = [(datetime.now(), product, rating, text) for product, rating, text in reviews]
    cursor.executemany(query, data)
    connection.commit()
    print(f"✓ Inserted {len(data)} grocery reviews")
    cursor.close()
    connection.close()

def generate_crm_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM crm_customers")
    connection.commit()

    rows = []
    customer_id = 1000
    churn_rates = {"North": 0.12, "South": 0.16, "East": 0.08, "West": 0.14}

    for region in regions:
        for _ in range(200):
            churn = random.random() < churn_rates[region]
            signup = date.today() - timedelta(days=random.randint(30, 365))
            rows.append((customer_id, region, churn, signup))
            customer_id += 1

    query = "INSERT INTO crm_customers (customer_id, region, churn, signup_date) VALUES (%s, %s, %s, %s)"
    cursor.executemany(query, rows)
    connection.commit()
    print(f"✓ Inserted {len(rows)} grocery CRM records")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    print("=" * 70)
    print("LOADING: GROCERY/FOOD DATA (Produce, Dairy, Meat, Beverages)")
    print("=" * 70)
    generate_sales_data()
    generate_reviews()
    generate_crm_data()
    print("✅ Grocery dataset loaded successfully!\n")
