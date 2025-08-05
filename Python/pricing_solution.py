# pricing_solution.py
# Author: Shiny Isurandi
# Purpose: Interview Assessment – Python Pricing Logic

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
    ("Silver", 2): [{"min_qty": 4, "price": 100}],
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
    5: "Premium",
    6: "Premium"
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


# Main function to run everything
def main():
    # Input orders
    input_data = [
        {"product_id": 1, "quantity": 4, "customer_id": 2},
        {"product_id": 2, "quantity": 3, "customer_id": 6},
        {"product_id": 2, "quantity": 2, "customer_id": 1},
        {"product_id": 1, "quantity": 2, "customer_id": 1},
        {"product_id": 1, "quantity": 2, "customer_id": 5},
        {"product_id": 2, "quantity": 3, "customer_id": 5},
        {"product_id": 2, "quantity": 1, "customer_id": 5},
        {"product_id": 3, "quantity": 4, "customer_id": 6}
    ]

    # Output results
    result = []
    for item in input_data:
        result.append(get_best_price(item["product_id"], item["quantity"], item["customer_id"]))

    # Print results
    print(result)


# Run the script
if __name__ == "__main__":
    main()
