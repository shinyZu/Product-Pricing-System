# pricing_solution.py
# Author: Shiny Isurandi
# Purpose: Interview Assessment – Python Pricing Logic 
# Version: Interactive

# Sample Pricing Data
customer_prices = {
    # (customer_id, product_id): [list of price rules]
    (2, 2): [
        {"min_qty": 3, "price": 9},
        {"min_qty": 4, "price": 7},
        {"min_qty": 5, "price": 5}
    ],
    (3,1): [{"min_qty": 3, "price": 5}],
    (6,2): [{"min_qty": 3, "price": 5}],
    
}

tier_prices = {
    # (tier, product_id): [list of price rules]
    ("Silver", 1): [
        {"min_qty": 2, "price": 95},
        {"min_qty": 3, "price": 85},
        {"min_qty": 4, "price": 75}
    ],
    ("Gold", 1): [{"min_qty": 3, "price": 60}],
    ("Premium", 1): [{"min_qty": 2, "price": 50}],
}

group_prices = {
    # (group, product_id): [list of price rules]
    ("G1", 1): [{"min_qty": 2, "price": 100}],
    ("G2", 2): [{"min_qty": 3, "price": 90}]
}

normal_prices = {
    # product_id: [list of price rules]
    1: [{"min_qty": 1, "price": 120}],
    2: [{"min_qty": 1, "price": 10}]
}

# Customer information
customer_tiers = {
    # customer_id: tier_name
    1: "Silver",
    2: "Silver",
    3: "Gold",
    4: "Gold",
    5: "Premium"
}

customer_groups = {
    # customer_id: [list of groups]
    1: ["G1", "G2"],
    2: ["G1"],
    3: ["G2"],
    4: ["G2"],
    5: ["G1", "G2"],
    6: []
}

# Function to find the best price
def get_best_price(product_id, quantity, customer_id):
    # 1. CUSTOMER PRICE
    key = (customer_id, product_id)
    if(key in customer_prices):
        valid_prices = [price_entry for price_entry in customer_prices[key] if price_entry["min_qty"] <= quantity]
        if valid_prices:
            best_price = min(valid_prices, key=lambda x: x["price"])
            return {
                "product_id": f"P00{product_id}", 
                "price": best_price["price"], 
                "price_type": "CUSTOMER"
            }

    # 2. TIER PRICE
    tier = customer_tiers.get(customer_id)
    if tier:
       key = (tier, product_id)
       if key in tier_prices:
           valid_prices = [price_entry for price_entry in tier_prices[key] if price_entry["min_qty"] <= quantity]
           if valid_prices:
               best_price = min(valid_prices, key=lambda x: x["price"])
               return {
                    "product_id": f"P00{product_id}", 
                    "price": best_price["price"], 
                    "price_type": "TIER"
               }

    # 3. GROUP PRICE
    groups = customer_groups.get(customer_id, [])
    for group in groups:
        key = (group, product_id)
        if key in group_prices:
            valid_prices = [price_entry for price_entry in group_prices[key] if price_entry["min_qty"] <= quantity]
            if valid_prices:
                best_price = min(valid_prices, key=lambda x: x["price"])
                return {
                    "product_id": f"P00{product_id}", 
                    "price": best_price["price"], 
                    "price_type": "GROUP"
                }
    
    # 4. NORMAL PRICE
    if product_id:
        if product_id in normal_prices:
            valid_prices = [price_entry for price_entry in normal_prices[product_id] if price_entry["min_qty"] <= quantity]
            if valid_prices:
                best_price = min(valid_prices, key=lambda x: x["price"])
                return {
                    "product_id": f"P00{product_id}", 
                    "price": best_price["price"], 
                    "price_type": "NORMAL"
                }
    

     # No valid price found
    return {
        "product_id": f"P00{product_id}", 
        "price": None, 
        "price_type": "NOT_FOUND"
    }



# Main function to run interactively
def main():
    print("---------------------------------------------------")
    print("🔍 Welcome to the Interactive Product Pricing System!")
    print("---------------------------------------------------")
    
    while True:
        try:
            product_id = int(input("Enter Product ID (e.g., 1 or 2): "))
            quantity = int(input("Enter Quantity: "))
            customer_id = int(input("Enter Customer ID (1–6): "))

            result = get_best_price(product_id, quantity, customer_id)

            print("\n✅ Pricing Result:")
            print(f"   Product ID : {result['product_id']}")
            print(f"   Price      : {result['price']}")
            print(f"   Price Type : {result['price_type']}\n")

        except ValueError:
            print("⚠️ Invalid input. Please enter numbers only.\n")

        again = input("Would you like to check another price? (yes/no): ").lower()
        if again not in ("yes", "y"):
            print(".\n\n👋 Exiting the Pricing System. Thank you!.")
            break


# Run script
if __name__ == "__main__":
    main()
