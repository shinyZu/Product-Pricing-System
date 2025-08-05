class PriceEntry {
    int minQty;
    double price;

    public PriceEntry(int minQty, double price) {
        this.minQty = minQty;
        this.price = price;
    }
}

class ProductRequest {
    int productId;
    int quantity;
    int customerId;

    public ProductRequest(int productId, int quantity, int customerId) {
        this.productId = productId;
        this.quantity = quantity;
        this.customerId = customerId;
    }
}


class ProductResponse {
    String productId;
    double price;
    String priceType;

    public ProductResponse(String productId, double price, String priceType) {
        this.productId = productId;
        this.price = price;
        this.priceType = priceType;
    }

    @Override
    public String toString() {
        return "{ product_id: " + productId + ", price: " + price + ", price_type: " + priceType + " }";
    }
}

class PriceSoutions{

	Map<String, List<PriceEntry>> customerPrices = new HashMap<>();
Map<String, List<PriceEntry>> tierPrices = new HashMap<>();
Map<String, List<PriceEntry>> groupPrices = new HashMap<>();
Map<Integer, List<PriceEntry>> normalPrices = new HashMap<>();

Map<Integer, String> customerTiers = new HashMap<>();
Map<Integer, List<String>> customerGroups = new HashMap<>();

customerPrices.put("2_2", Arrays.asList(new PriceEntry(3, 5))); // customer 2, product 2
tierPrices.put("Silver_1", Arrays.asList(new PriceEntry(2, 95))); // Silver tier, product 1
groupPrices.put("G1_1", Arrays.asList(new PriceEntry(2, 100)));
normalPrices.put(1, Arrays.asList(new PriceEntry(1, 120)));
normalPrices.put(2, Arrays.asList(new PriceEntry(1, 10)));

customerTiers.put(2, "Silver");
customerTiers.put(6, "Gold");

customerGroups.put(2, Arrays.asList("G1"));
customerGroups.put(6, new ArrayList<>());

public static ProductResponse getBestPrice(ProductRequest req) {
    int productId = req.productId;
    int quantity = req.quantity;
    int customerId = req.customerId;

    String customerKey = customerId + "_" + productId;

    // 1. Customer Price
    if (customerPrices.containsKey(customerKey)) {
        for (PriceEntry entry : customerPrices.get(customerKey)) {
            if (quantity >= entry.minQty) {
                return new ProductResponse("P00" + productId, entry.price, "CUSTOMER");
            }
        }
    }

    // 2. Tier Price
    if (customerTiers.containsKey(customerId)) {
        String tier = customerTiers.get(customerId);
        String tierKey = tier + "_" + productId;
        if (tierPrices.containsKey(tierKey)) {
            for (PriceEntry entry : tierPrices.get(tierKey)) {
                if (quantity >= entry.minQty) {
                    return new ProductResponse("P00" + productId, entry.price, "TIER");
                }
            }
        }
    }

    // 3. Group Price
    if (customerGroups.containsKey(customerId)) {
        for (String group : customerGroups.get(customerId)) {
            String groupKey = group + "_" + productId;
            if (groupPrices.containsKey(groupKey)) {
                for (PriceEntry entry : groupPrices.get(groupKey)) {
                    if (quantity >= entry.minQty) {
                        return new ProductResponse("P00" + productId, entry.price, "GROUP");
                    }
                }
            }
        }
    }

    // 4. Normal Price
    if (normalPrices.containsKey(productId)) {
        for (PriceEntry entry : normalPrices.get(productId)) {
            if (quantity >= entry.minQty) {
                return new ProductResponse("P00" + productId, entry.price, "NORMAL");
            }
        }
    }

    return new ProductResponse("P00" + productId, 0, "NOT_FOUND");
}

public static void main(String[] args) {
    List<ProductRequest> requests = Arrays.asList(
        new ProductRequest(1, 4, 2),
        new ProductRequest(2, 3, 6),
        new ProductRequest(1, 3, 6),
        new ProductRequest(3, 2, 6)  // not found case
    );

    for (ProductRequest req : requests) {
        System.out.println(getBestPrice(req));
    }
}


}
