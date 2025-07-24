# ------------------------ Stage 1: Data Cleaning ------------------------

import pandas as pd

# Load the scraped raw data
df = pd.read_csv("data/startups_raw.csv")

# Drop any rows with missing values
df.dropna(inplace=True)

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Convert revenue values like "$12M", "$450K", etc.
def convert_revenue(rev):
    try:
        rev = rev.replace('$', '').replace(',', '').strip()
        if 'M' in rev:
            return float(rev.replace('M', '')) * 1_000_000
        elif 'K' in rev:
            return float(rev.replace('K', '')) * 1_000
        else:
            return float(rev)
    except:
        return None

# Convert growth values like "45%" to float
def convert_growth(growth):
    try:
        return float(growth.replace('%', '').strip())
    except:
        return None

# Apply conversions
df['Revenue'] = df['Revenue'].apply(convert_revenue)
df['Growth %'] = df['Growth %'].apply(convert_growth)

# Drop rows with invalid values after conversion
df.dropna(subset=["Revenue", "Growth %"], inplace=True)

# Save cleaned data
df.to_csv("data/startups_clean.csv", index=False)
print("✅ Cleaning done. Data saved to 'data/startups_clean.csv'")

# ------------------------ Stage 2: Visualization & Summary ------------------------

import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("data/startups_clean.csv")

# ------------------ Plot 1: Top 5 Industries by Company Count ------------------
industry_counts = df['Industry'].value_counts().head(5)

plt.figure(figsize=(8, 5))
sns.barplot(x=industry_counts.values, y=industry_counts.index, palette="viridis")
plt.title("Top 5 Industries by Company Count")
plt.xlabel("Number of Companies")
plt.ylabel("Industry")
plt.tight_layout()
plt.savefig("visuals/top_5_industries.png")
plt.close()

# ------------------ Plot 2: Revenue Distribution ------------------
plt.figure(figsize=(8, 5))
sns.histplot(df['Revenue'], bins=10, kde=True, color='skyblue')
plt.title("Revenue Distribution")
plt.xlabel("Revenue ($)")
plt.ylabel("Number of Companies")
plt.tight_layout()
plt.savefig("visuals/revenue_distribution.png")
plt.close()

# ------------------ Plot 3: Growth % Distribution ------------------
plt.figure(figsize=(8, 5))
sns.histplot(df['Growth %'], bins=10, kde=True, color='salmon')
plt.title("Growth % Distribution")
plt.xlabel("Growth (%)")
plt.ylabel("Number of Companies")
plt.tight_layout()
plt.savefig("visuals/growth_distribution.png")
plt.close()

# ------------------ Summary Statistics ------------------
summary = {
    "Total Companies": len(df),
    "Average Revenue": round(df['Revenue'].mean(), 2),
    "Median Revenue": round(df['Revenue'].median(), 2),
    "Average Growth (%)": round(df['Growth %'].mean(), 2),
    "Median Growth (%)": round(df['Growth %'].median(), 2),
}

# Print summary to console
print("\n📊 Summary Report:")
for key, value in summary.items():
    print(f"{key}: {value}")

# Save summary to text file
with open("visuals/summary.txt", "w") as f:
    for key, value in summary.items():
        f.write(f"{key}: {value}\n")

print("\n✅ Summary report and charts saved in 'visuals/' folder.")
