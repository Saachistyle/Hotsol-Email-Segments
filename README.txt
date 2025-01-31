File Download Instructions:
    1. Download the Shopify Orders data and name it "Shopify Orders List.csv"
    2. Download the Klaviyo Main List and name it "Klaviyo Main List.csv"
    3. Download the most updated Customers AI list and name it "Customers AI List.csv"

Sample Data:
    These files contain sample data for demonstration purposes.

    1. Shopify Orders: 2024 Orders
    2. Klaviyo: Downloaded 12/20/24
    3. Customers.ai: Downloaded 12/23/24

How To Run:
    Execute the script process_customers.py in your preferred Python environment: 
        - Mac: "python3 process_customers.py"
        - Windows: "python process_customers.py"

    This will automatically process all datasets, filter unique customers, segment them, and generate final reports.

Output Folders:
    1. Segments: Contains CSV files with customers segmented by product interest.
    2. Segments for Olid Hotsol: Contains customized customer segment combinations.

Summary of Process:
    1. Cleans and standardizes customer data.
    2. Filters out duplicate customers present in Klaviyo and Shopify.
    3. Categorizes customers based on product interest.
    4. Saves segmented customer data as CSV files.
    5. Generates final Excel reports for easy review.