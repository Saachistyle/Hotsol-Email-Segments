import pandas as pd
import os
import re

### STEP 1: LOAD & FILTER UNIQUE CUSTOMERS ###
print("🔹 Step 1: Cleaning and filtering unique customers...")

# Load datasets
customers_ai_file = 'Customers AI List.csv'
klaviyo_file = 'Klaviyo Main List.csv'
shopify_file = 'Shopify Orders List.csv'

customers_ai_df = pd.read_csv(customers_ai_file)
klaviyo_df = pd.read_csv(klaviyo_file)
shopify_df = pd.read_csv(shopify_file)

# Standardize email formats
customers_ai_df['EMAIL'] = customers_ai_df['EMAIL'].str.strip().str.lower()
klaviyo_df['Email'] = klaviyo_df['Email'].str.strip().str.lower()
shopify_df['Email'] = shopify_df['Email'].str.strip().str.lower()

# Remove customers present in Klaviyo or Shopify
unique_customers = set(customers_ai_df['EMAIL']) - set(klaviyo_df['Email']) - set(shopify_df['Email'])
unique_customers_ai_df = customers_ai_df[customers_ai_df['EMAIL'].isin(unique_customers)]

### STEP 2: SEGMENT CUSTOMERS BASED ON PRODUCT INTEREST ###
print("🔹 Step 2: Segmenting customers by product interest...")

# Standardize column names
unique_customers_ai_df.rename(columns={
    'ADDRESS_CITY': 'City',
    'ADDRESS_LINE_1': 'Address',
    'ADDRESS_STATE': 'State',
    'EMAIL': 'Email',
    'PHONE': 'Mobile',
    'age': 'Age'
}, inplace=True)

# Ensure necessary columns exist
required_columns = ['first_name', 'last_name', 'Email', 'Mobile', 'Address', 'State', 'Age', 'gender']
for col in required_columns:
    if col not in unique_customers_ai_df.columns:
        unique_customers_ai_df[col] = None

# Standardize phone numbers
def standardize_phone(phone):
    if pd.isna(phone) or not re.search(r'\d', str(phone)):
        return ""
    phone = re.sub(r'\D', '', str(phone))
    if len(phone) == 10:
        return f"1 ({phone[:3]}) {phone[3:6]}-{phone[6:]}"
    elif len(phone) == 11 and phone.startswith("1"):
        return f"1 ({phone[1:4]}) {phone[4:7]}-{phone[7:]}"
    return phone

unique_customers_ai_df['Mobile'] = unique_customers_ai_df['Mobile'].apply(standardize_phone)

# Define product categories
item_categories = [
    "Kimono", "Capelet", "Fur", "Slides", "Beret", "Wrap", "Face Mask",
    "Gift Cards", "Wrapin", "Masks", "Reversibles", "Bandana", "Kaftan",
    "Cardigan", "Cashmere", "Necklace", "Bracelet", "Earring", "Ring", "Cape",
    "Poncho", "Duster", "Jacket", "Shirt", "Tunic", "Vest", "Ruana", "Scarf",
    "Crochet", "Silks", "Bags", "Shoe", "Mule", "Shawl", "Dress", "Apple Watch Band",
    "Beanie", "Bolero", "Choker", "Cuff", "Gift Card", "Bag", "Sweater"
]

# Categorize customers based on `LANDING_PAGE_URL`
def categorize_url(url):
    if pd.isna(url):
        return "Uncategorized"
    url = url.lower()
    for category in item_categories:
        if category.lower() in url:
            return category
    return "Uncategorized"

unique_customers_ai_df['Category'] = unique_customers_ai_df['LANDING_PAGE_URL'].apply(categorize_url)

# Create folders for segments
segments_folder = 'Segments'
olid_folder = 'Segments for Olid Hotsol'
os.makedirs(segments_folder, exist_ok=True)
os.makedirs(olid_folder, exist_ok=True)

# Save individual segment files
segments = {category: unique_customers_ai_df[unique_customers_ai_df['Category'] == category] for category in set(unique_customers_ai_df['Category'])}
for category, segment_df in segments.items():
    filename = os.path.join(segments_folder, f"{category.replace(' ', '_').lower()}.csv")
    segment_df.to_csv(filename, index=False)
    print(f"✅ Saved segment: {filename}")

# Custom segment combinations for Olid Hotsol
olid_combinations = {
    "FUR APPAREL": ["Fur"],
    "CARDIGAN": ["Cardigan"],
    "BRACELETS": ["Bracelet"],
    "Scarves & Wraps": ["Scarf", "Wrap"],
    "KIMONO": ["Kimono"],
    "ALL APPAREL": ["Kimono", "Capelet", "Wrap", "Kaftan", "Cardigan", "Cape", "Poncho", "Duster", "Jacket", "Shirt", "Tunic", "Vest", "Ruana", "Scarf", "Dress", "Beanie", "Bolero", "Sweater"],
    "JEWELERY": ["Necklace", "Bracelet", "Earring", "Ring", "Choker", "Cuff"],
    "CAPELETS": ["Capelet"]
}

for name, categories in olid_combinations.items():
    combined_df = unique_customers_ai_df[unique_customers_ai_df['Category'].isin(categories)]
    filename = os.path.join(olid_folder, f"{name.replace(' ', '_').lower()}.csv")
    combined_df.to_csv(filename, index=False)
    print(f"✅ Saved custom segment for Olid Hotsol: {filename}")

### STEP 3: CONVERT SEGMENTS TO EXCEL ###
print("🔹 Step 3: Creating Excel reports from segments...")

def create_excel_from_folder(input_folder, output_excel_file):
    csv_files = sorted([file for file in os.listdir(input_folder) if file.endswith('.csv')])
    
    with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
        for file_name in csv_files:
            file_path = os.path.join(input_folder, file_name)
            df = pd.read_csv(file_path)
            sheet_name = os.path.splitext(file_name)[0][:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"✅ Added {file_name} to {output_excel_file}")
    
    print(f"✅ All segments saved to {output_excel_file}")


print("🎉 Process completed successfully!")
