from abc import ABC, abstractmethod
from multipledispatch import dispatch
from llama_cpp import Llama
from tkinter import messagebox, Toplevel, Label, Button
from PIL import Image, ImageTk
from products_database_FINAL_VERSION import insert_product, fetch_all_products , close_product_connection
from datetime import datetime
from user_database_FINAL_VERSION import insert_user, fetch_all_users , close_user_connection


class AIService:
    _instance = None

    def __new__(cls, model_path):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_path):
        if self._initialized:
            return
        self.model_path = model_path
        self.llm = Llama(model_path=self.model_path, n_ctx=8192, n_gpu_layers=20, n_threads=6, verbose=False)

        self._initialized = True
    
    def cleanup(self):
        if self.llm is not None:  
            del self.llm
            self.llm = None
    
    def generate_insight(self, prompt, max_tokens=512):
        try:
            output = self.llm(
                prompt,
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9 )
            
            return output['choices'][0]['text'].strip()
        except Exception as e:
            print(f"AI Error: {str(e)}")
            return "AI service unavailable"

ai_service = AIService(
    model_path=r"C:\Users\alika\.lmstudio\models\lmstudio-community\DeepSeek-Coder-V2-Lite-Instruct-GGUF\DeepSeek-Coder-V2-Lite-Instruct-IQ3_M.gguf")

class Entity(ABC):
    def __init__(self, entity_id, name):
        self._entity_id = entity_id
        self._name = name
        
    def get_id(self):
        return self._entity_id
    def get_name(self):
        return self._name
    @abstractmethod
    def get_info(self): 
        pass


class Supplier(Entity):
    def __init__(self, entity_id, name, contact_info, products_supplied, rating):
        super().__init__(entity_id, name)
        self.__contact_info = contact_info
        self.__products_supplied = products_supplied
        self.__rating = rating 
        
    def supply_product(self, manufacturer, product_name, amount):
        try:
            for product in self.__products_supplied:
                if product.get_name() == product_name:
                    if product.get_quantity() < amount:
                        print(f"Not enough stock of {product_name}! Available: {product.get_quantity()}")
                        return
                    product.update_quantity(-amount)
                    manufacturer.manufacture_product(product, amount)
                    print(f"{self.get_name()} supplied {amount} units of {product_name} to {manufacturer.get_name()}.")
                    return
            print(f"{self.get_name()} does not have {product_name} in stock.")
        except Exception as e:
            print(f"Error while supplying product: {e}")

    def get_info(self):
        return f"Supplier: {self.get_name()} | Contact: {self.__contact_info} | Rating: {self.__rating}"
  
  
class Manufacturer(Entity):
    def __init__(self, entity_id, name, raw_materials, production_capacity,products_produced):
        super().__init__(entity_id, name)
        self.__raw_materials = raw_materials
        self.__products_produced = products_produced or []
        self.__production_capacity = production_capacity
    def get_raw_materials(self):
        return self.__raw_materials

    def get_production_capacity(self):
        return self.__production_capacity

    def get_products_produced(self):
        return self.__products_produced

    def manufacture_product(self, product, amount):
        if amount > self.__production_capacity:
            print(f"Insufficient production capacity! Max limit: {self.__production_capacity}")
            print(" ___________________________________________________________________________ \n")
            return
        product.update_quantity(amount)
        if product.get_name() not in self.__products_produced:
            self.__products_produced.append(product.get_name())
        print(f"Successfully manufactured {amount} units of {product.get_name()}!")
        print(" ___________________________________________________________________________ \n")

    def get_info(self):
        return f"Manufacturer:{self.get_name()} | Raw Materials: {self.__raw_materials} | Products Manufactured: {self.__products_produced} | Production Capacity: {self.__production_capacity} units"
from datetime import datetime

class Product(Entity):
    def __init__(self, entity_id, name, category, price, quantity, expiration_date, manufacturer):
        super().__init__(entity_id, name)
        self.__category = category
        self.__price = price
        self.__quantity = quantity
        self.__expiration_date = expiration_date
        self.__manufacturer = manufacturer

    def get_info(self):
        return (
            f"Product: {self.get_name()} | Category: {self.__category} | "
            f"Price: {self.__price} EGP | Quantity: {self.__quantity} | "
            f"Expiration Date: {self.__expiration_date}"
        )


    def insert_to_db(self):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            product_id = str(self.get_id())  # Convert to integer
            insert_product(product_id, self.get_name(), self.__expiration_date)
            print(f"[DB] Product '{self.get_name()}' automatically inserted into database.")
        except Exception as e:
            print(f"[DB ERROR] Failed to insert product into database: {e}")



    def ai_slogan(self):
        prompt = f"Generate a catchy, short marketing slogan (max 10 words) for a product called {self.get_name()} , which belongs to the category ' ({self.__category})' and is priced at {self.__price} EGP."
        print(" ___________________________________________________________________________ \n")
        return ai_service.generate_insight(prompt, max_tokens=512)

    def get_quantity(self):
        return self.__quantity

    def update_quantity(self, amount):
        if amount < 0 and abs(amount) > self.__quantity:
            print(f"Cannot remove {abs(amount)} units, available quantity: {self.__quantity}")
            print(" ___________________________________________________________________________ \n")
        else:
            self.__quantity += amount
            print(f"Updated quantity for {self.get_name()}: {self.__quantity}")
            print(" ___________________________________________________________________________ \n")

    def get_info(self):
        return (
            f"Product: {self.get_name()} | Category: {self.__category} | "
            f"Price: {self.__price} EGP | Quantity: {self.__quantity} | "
            f"Expiration Date: {self.__expiration_date}"
        )


class ProductProxy:
    def __init__(self, entity_id: str, name: str, category: str, price: float, 
                 quantity: int, expiration_date: str, manufacturer: Manufacturer):
        self._real_product = Product(
            entity_id, name, category, price, quantity, expiration_date, manufacturer
        )


    def insert_to_db(self):
        self._real_product.insert_to_db()
    
    def get_name(self):
        return self._real_product.get_name()
    
    def get_id(self):
        return self._real_product.get_id()

    def get_name(self):
        return self._real_product.get_name()

    def get_info(self):
        return self._real_product.get_info()
    
    def get_quantity(self):
        return self._real_product.get_quantity()

    def get_category(self):
        return self._real_product._Product__category

    def get_price(self):
        return self._real_product._Product__price
    
    def update_quantity(self, amount, user_role="user"):
        if user_role != "admin":
            print("Permission denied: Only admin can update quantity.")
            print(" ___________________________________________________________________________ \n")
        else:
            self._real_product.update_quantity(amount)
    
    def insert_to_db(self):
        self._real_product.insert_to_db()
    
    def get_info(self):
        return self._real_product.get_info()
        
    def ai_slogan(self):
        print("Accessing AI through Proxy...")
        return self._real_product.ai_slogan()

class Warehouse(Entity):
    def __init__(self, entity_id, name, warehouse_capacity, warehouse_location):
        super().__init__(entity_id, name)
        self.__warehouse_capacity = warehouse_capacity
        self.__inventory = []
        self.__warehouse_location = warehouse_location
    
    @dispatch(Product)
    def store_product(self, product):
        if len(self.__inventory) < self.__warehouse_capacity:
            self.__inventory.append(product)
            print(f"Stored {product.get_name()} in the warehouse.")
            print(" ___________________________________________________________________________ \n")
        else:
            print("Warehouse is full!")
            print(" ___________________________________________________________________________ \n")

    @dispatch(str, int)
    def store_product(self, product_name, quantity):
        if len(self.__inventory) < self.__warehouse_capacity:
            product = Product(entity_id="TEMP", name=product_name,category="General", price=0,quantity=quantity, expiration_date=None, manufacturer=None)
            self.__inventory.append(product)
            print(f"Stored {quantity} units of {product_name} in the warehouse.")
            print(" ___________________________________________________________________________ \n")
        else:
            print("Warehouse is full!")
            print(" ___________________________________________________________________________ \n")
    def retrieve_product(self, product_name):
        for product in self.__inventory:
            if product.get_name() == product_name:
                self.__inventory.remove(product)
                print(f"{product_name} has been retrieved from the warehouse.")
                print(" ___________________________________________________________________________ \n")
                return
        print(f"{product_name} not found in warehouse.")
        print(" ___________________________________________________________________________ \n")

    def check_inventory(self):
        print("Warehouse Inventory:")
        if not self.__inventory:
            print("- Empty -")
            print(" ___________________________________________________________________________ \n")
        for item in self.__inventory:
            print(f"- {item.get_info()}")
            print(" ___________________________________________________________________________ \n")

    def get_info(self):
        return f"Warehouse: {self.get_name()} | Location: {self.__warehouse_location} | Inventory Count: {len(self.__inventory)}"


class Distributor(Entity):
    def __init__(self, entity_id, name, distributor_network):
        super().__init__(entity_id, name)
        self.__distributor_network = distributor_network
        self.__inventory = {}

    def add_to_inventory(self, product_name, quantity):
        if product_name in self.__inventory:
            self.__inventory[product_name] += quantity
        else:
            self.__inventory[product_name] = quantity
        print(f"Added {quantity} units of {product_name} to inventory.")
        print(" ___________________________________________________________________________ \n")

    def distribute_product(self, product_name, quantity):
        if product_name in self.__inventory and self.__inventory[product_name] >= quantity:
            self.__inventory[product_name] -= quantity
            print(f"Distributed {quantity} units of {product_name}. Remaining: {self.__inventory[product_name]}")
            print(" ___________________________________________________________________________ \n")
        else:
            print(f"Not enough {product_name} in stock!")
            print(" ___________________________________________________________________________ \n")

    def get_info(self):
        return f"Distributor: {self.get_name()} | Network: {self.__distributor_network} | Inventory Count: {len(self.__inventory)}"


class Retailer(Entity):
    def __init__(self, entity_id, name, location, stock):
        super().__init__(entity_id, name)
        self.__location = location
        self.__stock = stock

    def get_retailer_location(self):
        return self.__location

    def get_retailer_stock(self):
        return self.__stock

    def order_product(self, quantity, product_name):
        if quantity <= 0:
            print("Invalid quantity. Must be greater than zero.")
            return
        self.__stock[product_name] = self.__stock.get(product_name, 0) + quantity
        print(f"Ordered {quantity} units of {product_name}. Updated stock: {self.__stock[product_name]}")
        print(" ___________________________________________________________________________ \n")

    def sell_product(self, quantity, product_name):
        if product_name not in self.__stock:
            print(f"{product_name} is not available in stock.")
            return
        self.__stock[product_name] -= quantity
        print(f"Sold {quantity} units of {product_name}. Remaining stock: {self.__stock[product_name]}")
        print(" ___________________________________________________________________________ \n")

    def check_stock(self, product_name):
        stock_quantity = self.__stock.get(product_name, 0)
        print(f"Stock for {product_name}: {stock_quantity}")
        print(" ___________________________________________________________________________ \n")
        return stock_quantity

    def get_info(self):
        return f"Retailer: {self.get_name()} |ID: {self.get_id()} | Location: {self.__location} | Stock: {self.__stock}"
    
    
class Order(Entity):
    def __init__(self,entity_id, name, product, status, order_date, final_price, quantity, payment_method, items):
        super().__init__(entity_id, name)
        self.product = product
        self.status = status  
        self.order_date = order_date
        self.final_price = final_price
        self.quantity = quantity
        self.payment_method = payment_method
        self.items = items  
    
    def ai_order_analysis(self):

        prompt = f"""Analyze this order:
        - Product: {self.product.get_name()}
        - Quantity: {self.quantity}
        - Status: {self.status}
        - Payment: {type(self.payment_method).__name__}
        Provide the analysis of the order only :"""
        return ai_service.generate_insight(prompt, max_tokens=512)
        
    
    def place_order(self):
        if self.status.lower() == "pending":
            self.status = "Placed"
            print(f"Order {self.get_id()} has been placed successfully!")
            print(" ___________________________________________________________________________ \n")
        else:
            print(f"Order {self.get_id()} cannot be placed. Current status: {self.status}")
            print(" ___________________________________________________________________________ \n")
    
    def update_order_status(self, new_status):
        self.status = new_status
        print(f"Order {self.get_id()} status updated to: {self.status}")
        print(" ___________________________________________________________________________ \n")
    
    def track_order(self):
        if self.status.lower() in ["shipped", "out for delivery"]:
            return f"Your order {self.get_id()} is currently {self.status}"
        elif self.status.lower() == "delivered":
            return f"Your order {self.get_id()} has been delivered successfully!"
        elif self.status.lower() == "canceled":
            return f"Your order {self.get_id()} has been canceled."
        else:
            return f"Order {self.get_id()} is still in progress. Current status: {self.status}"
    
    def calculate_final_price(self, discount, tax):
        discounted_price = self.final_price - discount
        tax_amount = (discounted_price * tax) / 100
        self.final_price = discounted_price + tax_amount 
        print(" ___________________________________________________________________________ \n")
        return self.final_price

    @staticmethod
    def create_payment(method):
        if method.lower() == "visa":
            return Visa()
        
        elif method.lower() == "cash":
            return Cash()
        elif method.lower() == "ewallet":
            return EWallet()
        else:
            raise ValueError("Invalid payment method. Choose from: Visa, Cash, EWallet")

    def payment(self):
         return self.payment_method.process_payment(self.get_id())

    def get_info(self):
        payment_method_info = type(self.payment_method).__name__  
        return f"Order ID: {self.get_id()} | Status: {self.status} | Final Price: {self.final_price} | Quantity: {self.quantity} | Payment Method: {payment_method_info}"


class Visa:
    def process_payment(self, order_id):  
        return f"Payment via Visa for order {order_id} processed."

class Cash:
    def process_payment(self, order_id):  
        return f"Cash payment for order {order_id} received."

class EWallet:
    def process_payment(self, order_id):  
        return f"EWallet payment for order {order_id} completed."
  
 
class User(Entity):
    def __init__(self, entity_id: str, name: str, role: str, email: str, pword: str = "123456" ):
        super().__init__(entity_id, name)
        self.__role = role
        self.__email = email
        self.logged_in = False
        self.favorite_products = [] 
        self.orders = []
        self.__pword = pword  

        try:
            insert_user(self.__email, self.__pword)
            print(f"[DB] user with email '{self.__email}' automatically inserted into database.")
        except Exception as e:
            print(f"[DB ERROR] Failed to insert user into database: {e}")
        
    def add_order(self, order):
        self.orders.append(order)
        print(f"Order {order.get_id()} has been added to user {self.get_name()}.")
        print(" ___________________________________________________________________________ \n")
    
    def login(self):
        if not self.logged_in:
            self.logged_in = True
            print(f"{self.get_name()} has logged in successfully! \n ___________________________________________________________________")
        else:
            print(f"{self.get_name()} is already logged in.\n ___________________________________________________________________")

    def logout(self):
        if self.logged_in:
            self.logged_in = False
            print(f"{self.get_name()} has logged out.\n __________________________________________________________________________")
        else:
            print(f"{self.get_name()} is not logged in.")
            print(" ___________________________________________________________________________ \n")

    def view_dashboard(self):
        print(f"Welcome {self.get_name()}! Here is your dashboard:")
        if self.logged_in:
            print("Status: Logged in \n ")
        else:
            print("Status: Not logged in \n ")
        print(f"1. Name: {self.get_name()}")
        print(f"2. Role: {self.__role}")
        print("3. Account Settings: /account/settings")
        if self.orders:
            print(f"4. ordered: ")
            for order in self.orders:
             print(f" {order.get_info()}")
        else:
            print("4. No ordered Products.")
        if self.favorite_products:
            print("5. Favorite Products:")
            for product in self.favorite_products:
                print(f"{product.get_name()}")
        else:
            print("5. Favorite Products: No products added.")
        print(" ___________________________________________________________________________ \n")


    def add_to_favorite(self, product):
        try:
            if isinstance(product, ProductProxy):
                product_name = product.get_name() 
            else:
                product_name = product.get_name()     
            if product not in self.favorite_products:
                self.favorite_products.append(product)
                print(f"Added {product_name} to your favorite products.") 
                print(" ___________________________________________________________________________ \n")
            else:
                print(f"{product_name} is already in your favorite list.")
                print(" ___________________________________________________________________________ \n")
        except Exception as e:
            print(f"Error adding to favorites: {str(e)}")
            
    def get_info(self):
        return f"User: {self.get_name()} | Role: {self.__role} | Email: {self.__email}"


class Delivery:
    def __init__(self, delivery_id, order, delivery_status="Preparing"):
        self.delivery_id = delivery_id
        self.order = order
        self.delivery_status = delivery_status

    def update_status(self, new_status):
        self.delivery_status = new_status
        print(f"Delivery {self.delivery_id} status updated to {self.delivery_status} \n ___________________________________________________________________________ \n")

    def get_status(self):
        return f"Order {self.order.get_id()} is currently {self.delivery_status}"
    
class Review:
    def __init__(self, reviewer_name, rating, comment):
        self.reviewer_name = reviewer_name
        self.rating = rating
        self.comment = comment

    def get_review(self):
        return f"{self.reviewer_name} rated {self.rating}/5: {self.comment}"
    
    
    def ai_review_analysis(self):
        prompt = (
            f"Analyze this product review:\n"
            f"- Reviewer: {self.reviewer_name}\n"
            f"- Rating: {self.rating}/5\n"
            f"- Comment: {self.comment}\n\n"
            "Please provide:\n"
            "1. Short overall sentiment (positive/negative/neutral).\n"
            "2. Only three bullet-point takeaways.\n"
            "3. Only one suggestion to improve the product based on this feedback.\n"
        )
        print(" ____________________________________________________________________________ \n")
        return  ai_service.generate_insight(prompt, max_tokens=256)

    
class Ask_AI_about_Supply_Chain_Management:
    def __init__(self):
        self.ai_service = ai_service

    def ask_question(self):
        while True:
            question = input("Ask the AI model about anything in Supply Chain Management:\n> ")
            if question.lower() in ["exit", "no", "quit", "stop","n","لا"]:
                print("Ending the Q&A session. Thank you!")
                break

            prompt = f"Answer the following question about Supply Chain Management:\n{question}"
            print(f"\nAI Answer:\n{self.ai_service.generate_insight(prompt)}\n")
            print(" ___________________________________________________________________________ \n")
            again = input("Would you like to ask another question? (yes/no):\n> ")
            if again.strip().lower() not in ["yes", "y", "yeah", "sure","نعم", "ايوه"]:
                print("Ending the Q&A session. Thank you!")
                print(" ___________________________________________________________________________ \n")
                break

print(" _________________________________________________________________________________________________________________ \n")


class LoginLogic:
    def __init__(self, entry1, entry2, root_page):
        self.entry1 = entry1
        self.entry2 = entry2
        self.page = root_page
    
    def login(self):
        username = self.entry1.get().strip().lower()
        password = self.entry2.get().strip()
        if username == "admin@gmail.com" and password == "123456789":
            messagebox.showinfo(title="LOG IN", message="HELLO USER")
            self.page.withdraw()
            self.run_supply_chain_demo()
        else:
            messagebox.showerror(title="LOG IN", message="Wrong E-mail or Password \n \n      Please try again!")
            
    def run_supply_chain_demo(self):
        try:

            ask = Ask_AI_about_Supply_Chain_Management()        
            ask.ask_question()
           
            quantum_manufacturer = Manufacturer(
                entity_id="M001",
                name="Quantum Manufacturers Ltd",
                raw_materials=["Silicon", "Rare Earth Metals"],
                production_capacity=10000,
                products_produced=[])


            quantum_processor = Product(
                entity_id="1001",
                name="Quantum Processor QX-9000",
                category="Advanced Computing",
                price=45000,
                quantity=0,
                expiration_date="2026-12-31",
                manufacturer=quantum_manufacturer)


            quantum_proxy = ProductProxy(
                entity_id="1002",  
                name="Quantum Co-Processor QP-200",
                category="Advanced Computing",
                price=22000,
                quantity=0,
                expiration_date="2027-06-30",
                manufacturer=quantum_manufacturer)
            
            
            tech_supplier = Supplier(
                entity_id="S001",
                name="Advanced Components Inc.",
                contact_info="supply@advanced.com",
                products_supplied=[quantum_processor, quantum_proxy._real_product],
                rating=4.9)

            
            main_warehouse = Warehouse(
                entity_id="W001",
                name="Central Tech Warehouse",
                warehouse_capacity=50000,
                warehouse_location="Singapore")

           
            global_distributor = Distributor(
                entity_id="D001",
                name="Global Tech Distributors",
                distributor_network="Asia-Pacific Network")

            
            premium_retailer = Retailer(
                entity_id="R001",
                name="Future Tech Store",
                location="Singapore Downtown",
                stock={})

            # Users
            admin_user = User(
                entity_id="U001",
                name="Admin User",
                role="admin",
                email="admin@tech.com")

            customer_user = User(
                entity_id="U002",
                name="Premium Customer",
                role="premium",
                email="customer@tech.com")

           
            visa_payment = Order.create_payment("visa")
            ewallet_payment = Order.create_payment("ewallet")

    
            quantum_order = Order(
                entity_id="O001",
                name="Quantum Computing Package",
                product=quantum_proxy,
                status="Pending",
                order_date=datetime.now().date(),
                final_price=0,
                quantity=5,
                payment_method=visa_payment,
                items=[quantum_processor, quantum_proxy._real_product])

         
            quantum_delivery = Delivery(
                delivery_id="DLV001",
                order=quantum_order,
                delivery_status="Preparing")

         
            quantum_review = Review(
                reviewer_name="Tech Expert",
                rating=5,
                comment="Groundbreaking performance with excellent energy efficiency" )


            def test_supply_chain_flow():
           
           
                tech_supplier.supply_product(quantum_manufacturer, "Quantum Processor QX-9000", 1000)
                tech_supplier.supply_product(quantum_manufacturer, "Quantum Co-Processor QP-200", 1500)
                
                
                quantum_manufacturer.manufacture_product(quantum_processor, 800)
                quantum_manufacturer.manufacture_product(quantum_proxy._real_product, 1200)
                
                
                main_warehouse.store_product(quantum_processor)
                main_warehouse.store_product("Quantum Cooling System", 500)
                main_warehouse.retrieve_product("Quantum Processor QX-9000")
                main_warehouse.check_inventory()
               
               
                global_distributor.add_to_inventory("Quantum Processor QX-9000", 600)
                global_distributor.distribute_product("Quantum Processor QX-9000", 400)
          
          
                premium_retailer.order_product(300, "Quantum Processor QX-9000")
                premium_retailer.sell_product(50, "Quantum Processor QX-9000")
                premium_retailer.check_stock("Quantum Processor QX-9000")


                customer_user.login()
                customer_user.add_to_favorite(quantum_processor)
                customer_user.add_to_favorite(quantum_proxy)
                customer_user.add_order(quantum_order)
                customer_user.view_dashboard()
                customer_user.logout()


                admin_user.login()
                quantum_proxy.update_quantity(1000, "admin")
                admin_user.logout()


                quantum_order.place_order()
                quantum_order.update_order_status("Shipped")
                quantum_order.calculate_final_price(discount=15000, tax=7)
                print(f"Payment Status: {quantum_order.payment()}")
                print(f"Order Tracking: {quantum_order.track_order()}")
                print(f"AI Order Analysis:\n{quantum_order.ai_order_analysis()}")


                print("\nProxy Operations:")
                print(f"Proxy Initial Quantity: {quantum_proxy.get_quantity()}")
                quantum_proxy.update_quantity(500, "user")  
                quantum_proxy.update_quantity(500, "admin") 
                print(f"Proxy New Quantity: {quantum_proxy.get_quantity()}")
                print(f"Proxy AI Slogan: {quantum_proxy.ai_slogan()}")
                
                
                print("\nDatabase Operations:")
                quantum_processor.insert_to_db()
                quantum_proxy.insert_to_db() 
                insert_user("new_user@tech.com", "secure123")
                print("All Products:", fetch_all_products())
                print(" _________________________________________________________________________________________________________________________________________________________________________________ \n")
                print("All Users:", fetch_all_users())
                print(" _________________________________________________________________________________________________________________________________________________________________________________ \n")
                
                quantum_delivery.update_status("In Transit")
                print(f"\nDelivery Status: {quantum_delivery.get_status()}")
                print(" ____________________________________________________________________________ \n")
                print("\nAI Slogan & review analysis:")
                print(f"Product Slogan: {quantum_processor.ai_slogan()}")
                print(f"Review Analysis:\n{quantum_review.ai_review_analysis()}")
                
            
                
                

            test_supply_chain_flow()
            
        finally:
             if ai_service.llm is not None:
                ai_service.cleanup()
        close_product_connection()
        close_user_connection()
        self.page.destroy()