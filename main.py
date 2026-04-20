import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================
# 1. LOAD DATA
# ==============================================================
dataset = pd.read_csv("online_retail.csv")

# ==============================================================
# 2. BASIC INFO
# ==============================================================
print("Head:\n", dataset.head())
print("\nShape:", dataset.shape)

print("\nMissing values BEFORE cleaning:")
print(dataset.isnull().sum())

print("\nMissing %:")
print(dataset.isnull().mean() * 100)

# ==============================================================
# 3. CLEANING
# ==============================================================

# Remove missing Description
dataset = dataset.dropna(subset=["Description"])

# Remove invalid rows
dataset = dataset[dataset["Quantity"] > 0]
dataset = dataset[dataset["UnitPrice"] > 0]

dataset.reset_index(drop=True, inplace=True)

print("\nAfter cleaning Description & invalid values:")
print(dataset.isnull().sum())

# Convert CustomerID
dataset["CustomerID"] = dataset["CustomerID"].astype("Int64")

# ==============================================================
# 4. SPLIT DATA (IMPORTANT)
# ==============================================================

df_with_customer = dataset.dropna(subset=["CustomerID"]).copy()
df_without_customer = dataset[dataset["CustomerID"].isnull()].copy()

print("\nDataset Split:")
print("Total:", dataset.shape)
print("With CustomerID:", df_with_customer.shape)
print("Without CustomerID:", df_without_customer.shape)

# ==============================================================
# 5. TOTAL SALES
# ==============================================================

dataset["Total_Sales"] = dataset["Quantity"] * dataset["UnitPrice"]
df_with_customer["Total_Sales"] = df_with_customer["Quantity"] * df_with_customer["UnitPrice"]
df_without_customer["Total_Sales"] = df_without_customer["Quantity"] * df_without_customer["UnitPrice"]

# ==============================================================
# 6. ANALYSIS
# ==============================================================

# Top Products (FULL dataset)
top_products = (
    dataset.groupby("Description")["Total_Sales"]
    .sum()
    .sort_values(ascending=True)
    .tail(10)
)

# Top Customers (ONLY valid customers)
top_customers = (
    df_with_customer.groupby("CustomerID")["Total_Sales"]
    .sum()
    .sort_values(ascending=True)
    .tail(10)
)

# Country Sales (FULL dataset)
country_sales = (
    dataset.groupby("Country")["Total_Sales"]
    .sum()
    .sort_values(ascending=True)
    .tail(10)
)

# ==============================================================
# 7. VISUALIZATION (SAME STYLE AS YOURS)
# ==============================================================

plt.style.use('seaborn-v0_8')
plt.rcParams.update({'font.size': 12})

# ---------------- Top Products ----------------
plt.figure(figsize=(10,7), dpi=120)

colors = plt.cm.Blues([0.5 + i*0.05 for i in range(len(top_products))])
plt.barh(top_products.index.astype(str), top_products.values, color=colors)

for i, v in enumerate(top_products.values):
    plt.text(v - (v * 0.05), i, f'{v:.0f}',
             va='center', ha="right", color='white', fontweight='bold')

plt.title("Top 10 Products by Sales", fontsize=20, fontweight='bold')
plt.xlabel("Total Sales", fontsize=17, fontweight='bold')
plt.ylabel("Products", fontsize=17, fontweight='bold')

plt.grid(axis='x', linestyle='--', alpha=0.3)
plt.tight_layout()

plt.savefig("top_products.png", bbox_inches='tight', dpi=300)
plt.show()

# ---------------- Top Customers ----------------
plt.figure(figsize=(10,6), dpi=120)

colors = plt.cm.Blues([0.5 + i*0.05 for i in range(len(top_customers))])
plt.barh(top_customers.index.astype(str), top_customers.values, color=colors)

offset = max(top_customers.values) * 0.02

for i, v in enumerate(top_customers.values):
    plt.text(v - offset, i, f'{v:.0f}',
             va='center', ha='right', color='white', fontweight='bold')

plt.title("Top 10 Customers by Sales", fontsize=20, fontweight='bold')
plt.xlabel("Total Sales", fontsize=17, fontweight='bold')
plt.ylabel("Customer ID", fontsize=17, fontweight='bold')

plt.grid(axis='x', linestyle='--', alpha=0.3)
plt.tight_layout()

plt.savefig("top_customers.png", bbox_inches='tight', dpi=300)
plt.show()

# ---------------- Country Sales ----------------
plt.figure(figsize=(10,8), dpi=120)

colors = plt.cm.Blues([0.5 + (i / len(country_sales)) * 0.5 for i in range(len(country_sales))])
plt.barh(country_sales.index, country_sales.values, color=colors, height=0.6)

max_val = max(country_sales.values)

for i, v in enumerate(country_sales.values):
    plt.text(v + (max_val * 0.01), i, f'{v:.0f}',
             va='center', ha='left',
             color='black', fontweight='bold')

plt.title("Top 10 Countries by Sales", fontsize=20, fontweight='bold')
plt.xlabel("Total Sales", fontsize=17, fontweight='bold')
plt.ylabel("Country", fontsize=17, fontweight='bold')

plt.grid(axis='x', linestyle='--', alpha=0.3)
plt.subplots_adjust(left=0.35)
plt.tight_layout()

plt.savefig("country_sales.png", bbox_inches='tight', dpi=300)
plt.show()

# ==============================================================
# 8. FINAL INSIGHTS
# ==============================================================

print("\nFINAL INSIGHTS:")
print("1. A small number of customers generate most revenue.")
print("2. Certain products generate significantly higher revenue.")
print("3. Sales are concentrated in a few countries.")
print("4. Missing CustomerID represents unknown or guest customers.")
print("5. Customer analysis is performed only on valid CustomerID data.")