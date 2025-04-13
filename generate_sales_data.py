import pandas as pd
import random
from datetime import datetime, timedelta

# Produtos simulados
products = [
    {"Product": "Laptop", "Category": "Electronics", "Price": 1200},
    {"Product": "Smartphone", "Category": "Electronics", "Price": 800},
    {"Product": "Headphones", "Category": "Electronics", "Price": 150},
    {"Product": "Desk", "Category": "Furniture", "Price": 500},
    {"Product": "Office Chair", "Category": "Furniture", "Price": 350},
    {"Product": "Notebook", "Category": "Stationery", "Price": 15},
    {"Product": "Pen", "Category": "Stationery", "Price": 5},
    {"Product": "Backpack", "Category": "Accessories", "Price": 90},
    {"Product": "Water Bottle", "Category": "Accessories", "Price": 30}
]

regions = ["North", "South", "East", "West"]
sellers = ["Carla Ferreira", "Julio Lima", "Felipe Goncalves"]

start_date = datetime(2024, 1, 1)
data = []

for _ in range(300):  # número de registros
    product = random.choice(products)
    quantity = random.randint(1, 10)
    date = start_date + timedelta(days=random.randint(0, 89))
    region = random.choice(regions)
    seller = random.choice(sellers)
    unit_price = product["Price"]
    total = quantity * unit_price
    margin = round(total * random.uniform(0.4, 0.7), 2)  # margem entre 40% e 70%

    data.append({
        "Date": date.strftime("%Y-%m-%d"),
        "Product": product["Product"],
        "Category": product["Category"],
        "Region": region,
        "Quantity": quantity,
        "Unit Price": unit_price,
        "Total": total,
        "Gross Margin": margin,
        "Seller": seller
    })

df = pd.DataFrame(data)
df.to_csv("data/sales_data.csv", index=False)
print("✅ Novo CSV com vendedor e margem criado com sucesso.")
