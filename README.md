Supply Chain Management (SCM) Simulation
This project is a comprehensive, object-oriented simulation of a supply chain management system developed in Python. It features a graphical user interface (GUI) built with Tkinter and integrates a local Large Language Model (LLM) to provide intelligent, data-driven insights.

Key Features
Object-Oriented Design: The entire supply chain is modeled using Python classes (e.g., Supplier, Manufacturer, Product, Order), demonstrating strong OOP principles.

AI-Powered Insights: A locally-run LLM (via llama-cpp-python) is integrated to perform tasks like:

Generating marketing slogans for products.

Analyzing customer reviews for sentiment and key takeaways.

Answering general questions about supply chain management.

Graphical User Interface (GUI): A user-friendly login screen and main application interface built with Tkinter.

Database Integration: Uses SQLite to persist user and product data, making the simulation's state durable between sessions.

Advanced Design Patterns: Implements the Proxy Pattern (ProductProxy) to control access to Product objects, for instance, by restricting certain actions (like updating quantity) to admin-level users.

Complete SCM Flow: Simulates the entire lifecycle from raw material supply to manufacturing, warehousing, distribution, retail, and final customer orders.

How to Run This Project
Prerequisites
You need to have Python installed on your system. You will also need to install the required libraries.

1. Clone the Repository
First, clone this repository to your local machine:

git clone https://github.com/ali3442/SCM-Simulation-Project.git
cd SCM-Simulation-Project

2. Install Dependencies
This project requires a few Python libraries. You can install them using pip:

pip install Pillow multipledispatch llama-cpp-python

(Note: tkinter and sqlite3 are part of the standard Python library and do not need to be installed separately.)

3. Set Up the AI Model
This simulation is configured to use a local Large Language Model (LLM) in GGUF format.

Download a Model: You need to download a GGUF model. The one used during development was DeepSeek-Coder-V2-Lite-Instruct-IQ3_M.gguf. You can find this or similar models on Hugging Face or LLM studio.

Update the Model Path: Open the main_project_FINAL_VERSION.py file and update the model_path variable in the AIService class instance to point to the location where you saved your downloaded model.

# Find this line in main_project_FINAL_VERSION.py
ai_service = AIService(
    model_path=r"C:\path\to\your\downloaded\model.gguf" # <-- CHANGE THIS
    )

4. Run the Application
Once the dependencies are installed and the model path is set, you can run the application by executing the GUI script:

python gui_FINAL_VERSION.py

Login Email: admin@gmail.com

Login Password: 123456789

Project Structure
gui_FINAL_VERSION.py: The main entry point for the application. Launches the Tkinter GUI.

main_project_FINAL_VERSION.py: Contains the core logic, classes, and the main simulation flow.

products_database_FINAL_VERSION.py: Handles all database operations for products.

user_database_FINAL_VERSION.py: Handles all database operations for users.

backgroundIMG.jpg: The background image used in the GUI.

Here is how the program should run with you:
 
![457494173-638ce0e1-585b-42a2-a037-7b01fe9b4170](https://github.com/user-attachments/assets/8d3baa92-31df-4e9a-813e-9dee628718ed)

![457494085-67ed18c1-a31f-42ad-826a-c7089b1bfca1](https://github.com/user-attachments/assets/c2db7866-e56e-4ae7-887b-5d96778f885f)
![Screenshot 2025-05-06 203009](https://github.com/user-attachments/assets/2a6a76ce-284d-4f7e-b663-74b24424aa8c)
![Screenshot 2025-05-06 203022](https://github.com/user-attachments/assets/781bb6f4-60fe-4a23-b947-fdef63582a24)


![Screenshot 2025-05-06 203033](https://github.com/user-attachments/assets/a7f8eda3-5ee0-4717-91d4-29f346946074)
![Screenshot 2025-05-06 203100](https://github.com/user-attachments/assets/b8274b37-61a5-4166-8e32-ea38a56bcc64)

![Screenshot 2025-05-06 203111](https://github.com/user-attachments/assets/c69a4a49-a8e1-4b0d-99ad-38e46883e508)

![Screenshot 2025-05-06 203123](https://github.com/user-attachments/assets/46fa328a-db5a-4b1e-80ca-862d30375a30)




