import sqlite3

DATABASE = 'petlinker.db'


class MarketplaceService:
    def initialize_database(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Create the marketplaces table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS marketplaces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_name TEXT NOT NULL,
                location TEXT NOT NULL,
                contact_info TEXT,
                products TEXT,
                description TEXT,
                opening_hours TEXT,
                payment_methods TEXT,
                rating INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def insert_sample_data(self):
        marketplace_data = [
            ("Pet Supplies Plus", "Cairo", "011-1234-5678", "Dog Food, Cat Toys",
             "A leading pet supply store offering a wide range of pet foods and accessories.",
             "Mon-Fri 9:00 AM - 9:00 PM", "Cash, Credit/Debit Card", 4),
            ("Furry Friends Market", "Alexandria", "010-2345-6789", "Leashes, Pet Beds",
             "Specializes in high-quality pet products and pet care items.",
             "Mon-Sat 10:00 AM - 8:00 PM", "Cash, PayPal", 5),
        ]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.executemany('''
            INSERT INTO marketplaces (store_name, location, contact_info, products, description, opening_hours, payment_methods, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', marketplace_data)
        conn.commit()
        conn.close()

    def get_pet_marketplaces(self, location=None):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        if location:
            cursor.execute('''
                SELECT store_name, location, contact_info, products, description, opening_hours, payment_methods, rating
                FROM marketplaces
                WHERE location LIKE ?
            ''', (f"%{location}%",))
        else:
            cursor.execute('''
                SELECT store_name, location, contact_info, products, description, opening_hours, payment_methods, rating
                FROM marketplaces
            ''')

        marketplaces = cursor.fetchall()
        conn.close()

        if not marketplaces:
            return "No pet marketplaces found. Try expanding your search radius."

        return [{"store_name": row[0], "location": row[1], "contact_info": row[2], "products": row[3],
                 "description": row[4], "opening_hours": row[5], "payment_methods": row[6], "rating": row[7]} for row in marketplaces]
