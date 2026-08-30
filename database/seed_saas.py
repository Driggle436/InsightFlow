import random
from datetime import date, timedelta
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import get_connection

random.seed(42)

regions = ["North", "South", "East", "West"]
products = ["Cloud Hosting Plan", "Database License", "Security Suite", "Analytics Dashboard", "API Gateway", "CRM Software", "Project Management", "Backup Service"]

def generate_sales_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM sales_transactions")
    connection.commit()

    start_date = date.today() - timedelta(days=59)
    rows = []

    regional_factors = {"North": 1.15, "South": 0.85, "East": 0.95, "West": 1.35}
    product_demand = {"Cloud Hosting Plan": 85, "Database License": 65, "Security Suite": 95, "Analytics Dashboard": 75, "API Gateway": 60, "CRM Software": 100, "Project Management": 110, "Backup Service": 80}

    for day_number in range(60):
        current_date = start_date + timedelta(days=day_number)
        for region in regions:
            for product in products:
                base_orders = int(product_demand[product] * regional_factors[region])
                base_orders += random.randint(-15, 15)
                if day_number >= 50 and region == "West":
                    base_orders = int(base_orders * 0.80)
                orders = max(5, base_orders)

                price = {"Cloud Hosting Plan": 299.99, "Database License": 599.99, "Security Suite": 399.99, "Analytics Dashboard": 249.99, "API Gateway": 449.99, "CRM Software": 999.99, "Project Management": 349.99, "Backup Service": 199.99}[product]
                revenue = orders * price
                base_marketing = 15000 if product in ["CRM Software", "Project Management", "Database License"] else 10000
                marketing_spend = base_marketing + random.uniform(-4000, 4000)

                rows.append((current_date, region, product, orders, round(revenue, 2), round(marketing_spend, 2)))

    query = "INSERT INTO sales_transactions (date, region, product, orders, revenue, marketing_spend) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, rows)
    connection.commit()
    print(f"✓ Inserted {len(rows)} SaaS sales records")
    cursor.close()
    connection.close()

def generate_reviews():
    from datetime import datetime
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM customer_reviews")
    connection.commit()

    reviews = [
        ("Cloud Hosting Plan", 5, "Excellent uptime and responsive support. Highly reliable."),
        ("Cloud Hosting Plan", 2, "Downtime during critical deployment, lost business."),
        ("Database License", 5, "Powerful features, great documentation."),
        ("Database License", 3, "Complex setup, steep learning curve."),
        ("Security Suite", 5, "Comprehensive protection, peace of mind."),
        ("Security Suite", 1, "Multiple security breaches despite service claims."),
        ("Analytics Dashboard", 5, "Beautiful visualizations, easy to understand metrics."),
        ("Analytics Dashboard", 4, "Good dashboard but real-time updates lag."),
        ("API Gateway", 5, "Smooth integration, excellent rate limiting."),
        ("API Gateway", 2, "API documentation could be better."),
        ("CRM Software", 5, "Transformed our sales process, great ROI."),
        ("CRM Software", 3, "Too many features we don't need, overwhelming."),
        ("Project Management", 5, "Team collaboration improved significantly."),
        ("Project Management", 2, "Mobile app frequently crashes."),
        ("Backup Service", 5, "Reliable and automated, never lost data."),
        ("Backup Service", 4, "Good service but restore times could be faster."),
        ("Cloud Hosting Plan", 4, "Solid infrastructure, good value for price."),
        ("Security Suite", 4, "Good protection, occasional false alerts."),
        ("Analytics Dashboard", 5, "Exactly what we needed for business intelligence."),
        ("CRM Software", 4, "Effective sales tool, good customization options."),
    ]

    query = "INSERT INTO customer_reviews (review_date, product, rating, review_text) VALUES (%s, %s, %s, %s)"
    data = [(datetime.now(), product, rating, text) for product, rating, text in reviews]
    cursor.executemany(query, data)
    connection.commit()
    print(f"✓ Inserted {len(data)} SaaS reviews")
    cursor.close()
    connection.close()

def generate_crm_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM crm_customers")
    connection.commit()

    rows = []
    customer_id = 1000
    churn_rates = {"North": 0.09, "South": 0.13, "East": 0.08, "West": 0.12}

    for region in regions:
        for _ in range(200):
            churn = random.random() < churn_rates[region]
            signup = date.today() - timedelta(days=random.randint(30, 365))
            rows.append((customer_id, region, churn, signup))
            customer_id += 1

    query = "INSERT INTO crm_customers (customer_id, region, churn, signup_date) VALUES (%s, %s, %s, %s)"
    cursor.executemany(query, rows)
    connection.commit()
    print(f"✓ Inserted {len(rows)} SaaS CRM records")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    print("=" * 70)
    print("LOADING: SAAS/SOFTWARE DATA (Cloud, Security, CRM, Analytics)")
    print("=" * 70)
    generate_sales_data()
    generate_reviews()
    generate_crm_data()
    print("✅ SaaS dataset loaded successfully!\n")
