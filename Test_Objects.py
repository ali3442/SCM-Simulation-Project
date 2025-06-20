


# 1. Initialize Core Entities
# ---------------------------
manufacturer = Manufacturer(
    manufacturer_id=1,
    manufacturer_name="Tech Manufacturers Inc",
    raw_materials=["silicon", "plastic", "copper"],
    production_capacity=10000,
    products_produced=[]
)

product = Product(
    product_id=1001,
    name="Quantum Processor",
    category="Electronics",
    price=2500,
    quantity=500,
    expiration_date="2025-12-31",
    manufacturer=manufacturer
)

supplier = Supplier(
    supplier_id=2001,
    supplier_name="Global Components Ltd",
    contact_info="supply@globalcomponents.com",
    products_supplied=[product],
    rating=4.8
)

# 2. Warehouse Operations
# -----------------------
warehouse = Warehouse(
    warehouse_id=3001,
    warehouse_location="Dubai Logistics Zone",
    warehouse_capacity=5000
)

# Test both overloaded store_product methods
warehouse.store_product(product)  # Method 1: Product object
warehouse.store_product("Cooling Fans", 1500)  # Method 2: String + quantity

# 3. Distribution Network
# -----------------------
distributor = Distributor(
    distributor_id=4001,
    name="Middle East Distributors",
    distributor_network=["Emirates Electronics", "Gulf Tech Supplies"]
)

# 4. Retail Operations
# --------------------
retailer = Retailer(
    retailer_id=5001,
    name="Future Electronics Store",
    location="Dubai Mall",
    stock={"Quantum Processor": 150}
)

# 5. Order Processing
# -------------------
# Create different payment method orders
order1 = Order(
    order_id=6001,
    product=product,
    status="Pending",
    order_date="2024-03-20",
    final_price=25000,
    quantity=10,
    payment_method=Order.create_payment("visa"),
    items=[product]
)

order2 = Order(
    order_id=6002,
    product=product,
    status="Pending",
    order_date="2024-03-20",
    final_price=12500,
    quantity=5,
    payment_method=Order.create_payment("ewallet"),
    items=[product]
)

# 6. User Interactions
# --------------------
user = User(
    user_id=7001,
    name="Ahmed Al-Farsi",
    role="Purchasing Manager",
    email="ahmed@company.com"
)

# 7. Delivery System
# ------------------
delivery = Delivery(
    delivery_id=8001,
    order=order1,
    delivery_status="Preparing"
)

# 8. Review System
# ----------------
review = Review(
    reviewer_name="Sara Mohammed",
    rating=5,
    comment="Excellent shipping speed and product quality"
)

# Example Test Scenarios
# ----------------------
def test_supply_chain_flow():
    # Test Supplier-Manufacturer interaction
    supplier.supply_product(manufacturer, "Quantum Processor", 200)
    
    # Test manufacturing process
    manufacturer.manufacture_product(product, 300)
    
    # Test warehouse operations
    warehouse.retrieve_product("Quantum Processor")
    warehouse.check_inventory()
    
    # Test distribution network
    distributor.add_to_inventory("Quantum Processor", 1000)
    distributor.distribute_product("Quantum Processor", 500)
    
    # Test retail operations
    retailer.order_product(200, "Quantum Processor")
    retailer.sell_product(50, "Quantum Processor")
    retailer.check_stock("Quantum Processor")
    
    # Test order processing
    order1.place_order()
    order1.update_order_status("Shipped")
    print(order1.track_order())
    order1.calculate_final_price(discount=500, tax=5)
    print(order1.payment())
    
    # Test user interactions
    user.login()
    user.add_to_favorite(product)
    user.add_order(order1)
    user.view_dashboard()
    user.logout()
    
    
    # Test delivery system
    delivery.update_status("In Transit")
    print(delivery.get_status())
    
    # Test review system
    print(review.get_review())
    print(review.ai_review_analysis())
    
    # Test AI interactions
    print("\nAI Slogan Test:")
    print(product.ai_slogan())
    print("\nAI Order Analysis:")
    print(order1.ai_order_analysis())

# Execute the test
test_supply_chain_flow()