import cloudscraper
from bs4 import BeautifulSoup

url = "https://growjo.com/"
scraper = cloudscraper.create_scraper()

response = scraper.get(url)
print(response.status_code)  # Should be 200

soup=BeautifulSoup(response.text,'html.parser')

import pandas as pd

table=soup.find("table",class_="jss31")
rows=table.find_all("tr")
rows_data=[]
for i in rows[1:]:
  data=i.find_all("td")
  # Extract data for the desired columns based on their position in the row
  company_name = data[1].text.strip()  # Company is the second column (index 1)
  industry = data[5].text.strip()      # Industry is the sixth column (index 5)
  country = data[3].text.strip()       # Country is the fourth column (index 3)
  revenue = data[7].text.strip()       # Revenue is the eighth column (index 7)
  growth = data[8].text.strip()        # Growth % is the ninth column (index 8)

  rows_data.append([company_name, industry, country, revenue, growth])

# Define the headers for the desired columns
headers = ['Company Name', 'Industry', 'Country', 'Revenue', 'Growth %']

# Create a pandas DataFrame
df = pd.DataFrame(rows_data, columns=headers)

# Display the DataFrame
print(df)

# Save the DataFrame to a CSV file
df.to_csv('data/startups_raw.csv', index=False)

print("✅ DataFrame saved to growjo_companies.csv")
