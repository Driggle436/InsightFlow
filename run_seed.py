#!/usr/bin/env python3
"""
Master Seed Data Runner
Load different datasets for testing InsightFlow with various business types
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.seed_data import generate_sales_data as electronics_sales, generate_reviews as electronics_reviews, generate_crm_data as electronics_crm
from database.seed_fashion import generate_sales_data as fashion_sales, generate_reviews as fashion_reviews, generate_crm_data as fashion_crm
from database.seed_grocery import generate_sales_data as grocery_sales, generate_reviews as grocery_reviews, generate_crm_data as grocery_crm
from database.seed_saas import generate_sales_data as saas_sales, generate_reviews as saas_reviews, generate_crm_data as saas_crm
from database.seed_automotive import generate_sales_data as auto_sales, generate_reviews as auto_reviews, generate_crm_data as auto_crm


DATASETS = {
    "electronics": {
        "name": "Electronics (Laptops, Phones, Tablets)",
        "funcs": [electronics_sales, electronics_reviews, electronics_crm],
    },
    "fashion": {
        "name": "Fashion (Clothing, Shoes, Accessories)",
        "funcs": [fashion_sales, fashion_reviews, fashion_crm],
    },
    "grocery": {
        "name": "Grocery (Food, Produce, Dairy)",
        "funcs": [grocery_sales, grocery_reviews, grocery_crm],
    },
    "saas": {
        "name": "SaaS (Cloud, Security, CRM, Analytics)",
        "funcs": [saas_sales, saas_reviews, saas_crm],
    },
    "automotive": {
        "name": "Automotive (Cars, SUVs, Trucks, EVs)",
        "funcs": [auto_sales, auto_reviews, auto_crm],
    },
}


def load_dataset(dataset_key):
    """Load a specific dataset"""
    if dataset_key not in DATASETS:
        print(f"❌ Unknown dataset: {dataset_key}")
        print(f"Available datasets: {', '.join(DATASETS.keys())}")
        return False
    
    dataset = DATASETS[dataset_key]
    print("\n" + "=" * 70)
    print(f"📦 LOADING: {dataset['name']}")
    print("=" * 70)
    
    try:
        for i, func in enumerate(dataset['funcs'], 1):
            print(f"  [{i}/3] {func.__name__}...", end=" ", flush=True)
            func()
            print("✓")
        
        print("=" * 70)
        print(f"✅ {dataset['name']} loaded successfully!")
        print("=" * 70 + "\n")
        return True
    except Exception as e:
        print(f"\n❌ Error loading {dataset['name']}: {e}\n")
        return False


def list_datasets():
    """List all available datasets"""
    print("\n" + "=" * 70)
    print("Available Datasets for InsightFlow")
    print("=" * 70)
    for key, info in DATASETS.items():
        print(f"  • {key:15} → {info['name']}")
    print("=" * 70 + "\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_seed.py <dataset>")
        print("       python run_seed.py list")
        list_datasets()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_datasets()
    else:
        success = load_dataset(command)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
