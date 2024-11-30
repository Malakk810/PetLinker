import pyodbc

# Configure the database connection
DATABASE = 'PetLinker'  # This should be your database name
SERVER = 'FaridaAli\SQLEXPRESS'  # Your server name
UID = 'flask_user'  # Your database username
PWD = 'Flask!User1234'  # Your database password

# Establish the ODBC connection string
CONNECTION_STRING = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD};TrustServerCertificate=yes'

class MarketplaceService:
    def __init__(self):
        # Initialize the connection
        self.conn = pyodbc.connect(CONNECTION_STRING)
        self.cursor = self.conn.cursor()

    def insert_sample_data(self):
        marketplace_data = [
            ("Pet Supplies Plus", "Cairo", "011-1234-5678", "Dog Food, Cat Toys",
             "A leading pet supply store offering a wide range of pet foods and accessories.",
             "Mon-Fri 9:00 AM - 9:00 PM", "Cash, Credit/Debit Card", 4),
            ("Furry Friends Market", "Alexandria", "010-2345-6789", "Leashes, Pet Beds",
             "Specializes in high-quality pet products and pet care items.",
             "Mon-Sat 10:00 AM - 8:00 PM", "Cash, PayPal", 5),
        ]

        # Execute the insertion queries
        self.cursor.executemany('''
            INSERT INTO marketplaces (store_name, location, contact_info, products, description, opening_hours, payment_methods, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', marketplace_data)

        # Commit and close the connection
        self.conn.commit()

    def get_pet_marketplaces(self, location=None):
        if location:
            self.cursor.execute('''
                SELECT store_name, location, contact_info, products, description, opening_hours, payment_methods, rating
                FROM marketplaces
                WHERE location LIKE ?
            ''', (f"%{location}%",))
        else:
            self.cursor.execute('''
                SELECT store_name, location, contact_info, products, description, opening_hours, payment_methods, rating
                FROM marketplaces
            ''')

        # Fetch all the results
        marketplaces = self.cursor.fetchall()

        if not marketplaces:
            return "No pet marketplaces found. Try expanding your search radius."

        # Return a list of dictionaries with the results
        return [{"store_name": row[0], "location": row[1], "contact_info": row[2], "products": row[3],
                 "description": row[4], "opening_hours": row[5], "payment_methods": row[6], "rating": row[7]} for row in marketplaces]

    def close_connection(self):
        # Close the cursor and the connection
        self.cursor.close()
        self.conn.close()
