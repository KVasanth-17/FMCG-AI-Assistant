import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# --- 1. PRODUCT MASTER ---
products = [
    {"product_id": "BEV-001", "product_name": "Spark Lemon 500ml", "brand": "Spark", "category": "Carbonated", "sub_category": "Sparkling Water", "pack_size_ml": 500, "unit_price": 2.50},
    {"product_id": "BEV-002", "product_name": "Spark Berry 500ml", "brand": "Spark", "category": "Carbonated", "sub_category": "Sparkling Water", "pack_size_ml": 500, "unit_price": 2.50},
    {"product_id": "BEV-003", "product_name": "AquaPure 1L", "brand": "AquaPure", "category": "Water", "sub_category": "Still Water", "pack_size_ml": 1000, "unit_price": 1.50},
    {"product_id": "BEV-004", "product_name": "AquaPure 500ml", "brand": "AquaPure", "category": "Water", "sub_category": "Still Water", "pack_size_ml": 500, "unit_price": 1.00},
    {"product_id": "BEV-005", "product_name": "Energy Surge", "brand": "Surge", "category": "Energy", "sub_category": "Energy Drink", "pack_size_ml": 330, "unit_price": 3.00},
    {"product_id": "BEV-006", "product_name": "Energy Surge Zero", "brand": "Surge", "category": "Energy", "sub_category": "Energy Drink", "pack_size_ml": 330, "unit_price": 3.00},
    {"product_id": "BEV-007", "product_name": "Orchard Apple 1L", "brand": "Orchard", "category": "Juice", "sub_category": "Fruit Juice", "pack_size_ml": 1000, "unit_price": 4.00},
    {"product_id": "BEV-008", "product_name": "Orchard Orange 1L", "brand": "Orchard", "category": "Juice", "sub_category": "Fruit Juice", "pack_size_ml": 1000, "unit_price": 4.00},
    {"product_id": "BEV-009", "product_name": "DairyRich Iced Coffee", "brand": "DairyRich", "category": "Dairy", "sub_category": "Iced Coffee", "pack_size_ml": 250, "unit_price": 3.50},
    {"product_id": "BEV-010", "product_name": "DairyRich Chocolate Milk", "brand": "DairyRich", "category": "Dairy", "sub_category": "Flavored Milk", "pack_size_ml": 250, "unit_price": 2.00},
    {"product_id": "BEV-011", "product_name": "Fizz Cola 330ml", "brand": "Fizz", "category": "Carbonated", "sub_category": "Cola", "pack_size_ml": 330, "unit_price": 1.80},
    {"product_id": "BEV-012", "product_name": "Fizz Diet Cola 330ml", "brand": "Fizz", "category": "Carbonated", "sub_category": "Cola", "pack_size_ml": 330, "unit_price": 1.80},
    {"product_id": "BEV-013", "product_name": "SportHydrate Blue", "brand": "SportHydrate", "category": "Water", "sub_category": "Sports Drink", "pack_size_ml": 750, "unit_price": 2.80},
    {"product_id": "BEV-014", "product_name": "SportHydrate Red", "brand": "SportHydrate", "category": "Water", "sub_category": "Sports Drink", "pack_size_ml": 750, "unit_price": 2.80},
    {"product_id": "BEV-015", "product_name": "Mango Tango 500ml", "brand": "Orchard", "category": "Juice", "sub_category": "Fruit Juice", "pack_size_ml": 500, "unit_price": 2.20},
]
df_products = pd.DataFrame(products)

# --- 2. STORE MASTER ---
regions = ["North", "South", "East", "West"]
formats = ["Supermarket", "Hypermarket", "Convenience", "Wholesale"]
stores = []
for i in range(1, 31):
    stores.append({
        "store_id": f"STR-{i:03d}",
        "store_name": f"Store {i}",
        "region": random.choice(regions),
        "city": f"City {random.randint(1, 15)}",
        "store_format": random.choice(formats)
    })
df_stores = pd.DataFrame(stores)

# --- 3 & 4. SALES & INVENTORY GENERATION ---
weeks = 24
start_date = datetime(2024, 1, 1)
date_list = [start_date + timedelta(weeks=i) for i in range(weeks)]

sales_data = []
inventory_data = []

promotion_types = ["Price Cut", "BOGO", "Display Feature", "Bundle"]

for store in stores:
    for product in products:
        # Initial inventory for week 1
        current_stock = np.random.randint(50, 200)
        
        for week_date in date_list:
            # Determine Promotions
            is_promo = np.random.choice([True, False], p=[0.2, 0.8])
            promo_type = random.choice(promotion_types) if is_promo else None
            discount_pct = round(random.uniform(0.1, 0.3), 2) if is_promo else 0.0
            
            # Base Demand
            base_demand = np.random.randint(10, 50)
            
            # Promotion Spike Logic
            if is_promo:
                demand_multiplier = random.uniform(1.5, 3.5)
                actual_demand = int(base_demand * demand_multiplier)
            else:
                actual_demand = base_demand
                
            # Inventory Logic
            units_received = np.random.randint(20, 100) if current_stock < 50 else np.random.randint(0, 30)
            available_stock = current_stock + units_received
            
            # Stockout Logic
            units_sold = min(actual_demand, available_stock)
            stockout_flag = (units_sold == available_stock) and (actual_demand > available_stock)
            closing_stock = available_stock - units_sold
            
            # Revenue Calculation
            revenue = round(units_sold * product["unit_price"] * (1 - discount_pct), 2)
            
            # Append Sales Data
            sales_data.append({
                "week_start_date": week_date.strftime("%Y-%m-%d"),
                "product_id": product["product_id"],
                "store_id": store["store_id"],
                "region": store["region"],
                "units_sold": units_sold,
                "revenue": revenue,
                "promotion_flag": is_promo,
                "promotion_type": promo_type,
                "discount_pct": discount_pct
            })
            
            # Append Inventory Data
            inventory_data.append({
                "week_start_date": week_date.strftime("%Y-%m-%d"),
                "product_id": product["product_id"],
                "store_id": store["store_id"],
                "opening_stock": current_stock,
                "units_received": units_received,
                "units_sold": units_sold,
                "closing_stock": closing_stock,
                "stockout_flag": stockout_flag
            })
            
            # Carry over stock to next week
            current_stock = closing_stock

df_sales = pd.DataFrame(sales_data)
df_inventory = pd.DataFrame(inventory_data)

# --- EXPORT TO CSV ---
df_products.to_csv("product_master.csv", index=False)
df_stores.to_csv("store_master.csv", index=False)
df_sales.to_csv("sales_and_promotions.csv", index=False)
df_inventory.to_csv("inventory.csv", index=False)

print("✅ Success! 4 CSV files generated in the current directory.")