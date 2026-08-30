import random
from datetime import date, timedelta
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import get_connection

random.seed(42)

regions = ["North", "South", "East", "West"]
products = ["Sedan", "SUV", "Truck", "Hybrid", "Electric Vehicle", "Van", "Coupe", "Crossover"]

def generate_sales_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM sales_transactions")
    connection.commit()

    start_date = date.today() - timedelta(days=59)
    rows = []

    regional_factors = {"North": 0.9, "South": 1.1, "East": 1.0, "West": 1.05}
    product_demand = {"Sedan": 45, "SUV": 65, "Truck": 55, "Hybrid": 35, "Electric Vehicle": 40, "Van": 25, "Coupe": 20, "Crossover": 50}

    for day_number in range(60):
        current_date = start_date + timedelta(days=day_number)
        for region in regions:
            for product in products:
                base_orders = int(product_demand[product] * regional_factors[region])
                base_orders += random.randint(-10, 10)
                if day_number >= 50 and region == "South":
                    base_orders = int(base_orders * 0.65)
                orders = max(2, base_orders)

                price = {"Sedan": 28000, "SUV": 42000, "Truck": 38000, "Hybrid": 32000, "Electric Vehicle": 45000, "Van": 35000, "Coupe": 25000, "Crossover": 40000}[product]
                revenue = orders * price
                base_marketing = 20000 if product in ["SUV", "Electric Vehicle", "Truck"] else 15000
                marketing_spend = base_marketing + random.uniform(-5000, 5000)

                rows.append((current_date, region, product, orders, round(revenue, 2), round(marketing_spend, 2)))

    query = "INSERT INTO sales_transactions (date, region, product, orders, revenue, marketing_spend) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, rows)
    connection.commit()
    print(f"✓ Inserted {len(rows)} automotive sales records")
    cursor.close()
    connection.close()

def generate_reviews():
    from datetime import datetime
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM customer_reviews")
    connection.commit()

    reviews = [
        ("Sedan", 5, "Excellent fuel efficiency and comfortable ride."),
        ("Sedan", 2, "Multiple mechanical issues within first month."),
        ("SUV", 5, "Spacious and perfect for family trips."),
        ("SUV", 3, "Good vehicle but lower than advertised MPG."),
        ("Truck", 5, "Powerful and reliable, great for work."),
        ("Truck", 1, "Engine problems after 3000 miles."),
        ("Hybrid", 5, "Amazing fuel economy, quiet operation."),
        ("Hybrid", 4, "Good car but battery concerns long-term."),
        ("Electric Vehicle", 5, "Fantastic acceleration, very green. Love it!"),
        ("Electric Vehicle", 2, "Range falls short in cold weather conditions."),
        ("Van", 5, "Perfect family vehicle, lots of storage."),
        ("Van", 3, "Steering feels stiff, uncomfortable long drives."),
        ("Coupe", 4, "Sporty and fun to drive. Great performance."),
        ("Coupe", 2, "Backseat cramped, impractical for long trips."),
        ("Crossover", 5, "Best of both worlds, comfort and capability."),
        ("Crossover", 4, "Excellent value, minor paint quality issues."),
        ("Sedan", 4, "Reliable daily driver, good value."),
        ("SUV", 4, "Solid SUV, handles well on highways."),
        ("Truck", 4, "Great truck for work and weekend use."),
        ("Electric Vehicle", 5, "Revolutionized my commute, no regrets."),
    ]

    query = "INSERT INTO customer_reviews (review_date, product, rating, review_text) VALUES (%s, %s, %s, %s)"
    data = [(datetime.now(), product, rating, text) for product, rating, text in reviews]
    cursor.executemany(query, data)
    connection.commit()
    print(f"✓ Inserted {len(data)} automotive reviews")
    cursor.close()
    connection.close()

def generate_crm_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM crm_customers")
    connection.commit()

    rows = []
    customer_id = 1000
    churn_rates = {"North": 0.11, "South": 0.09, "East": 0.10, "West": 0.07}

    for region in regions:
        for _ in range(200):
            churn = random.random() < churn_rates[region]
            signup = date.today() - timedelta(days=random.randint(30, 365))
            rows.append((customer_id, region, churn, signup))
            customer_id += 1

    query = "INSERT INTO crm_customers (customer_id, region, churn, signup_date) VALUES (%s, %s, %s, %s)"
    cursor.executemany(query, rows)
    connection.commit()
    print(f"✓ Inserted {len(rows)} automotive CRM records")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    print("=" * 70)
    print("LOADING: AUTOMOTIVE DATA (Sedans, SUVs, Trucks, EVs)")
    print("=" * 70)
    generate_sales_data()
    generate_reviews()
    generate_crm_data()
    print("✅ Automotive dataset loaded successfully!\n")
