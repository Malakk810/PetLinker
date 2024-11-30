import pyodbc

# Database connection settings
DATABASE = 'PetLinker'  # Your database name
SERVER = 'FaridaAli\SQLEXPRESS'  # Your server name
UID = 'flask_user'  # Your database username
PWD = 'Flask!User1234'  # Your database password

# Connection string for SQL Server
CONNECTION_STRING = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD};TrustServerCertificate=yes'

class PetActivityService:
    def __init__(self):
        # Establish the ODBC connection
        self.conn = pyodbc.connect(CONNECTION_STRING)
        self.cursor = self.conn.cursor()

    def insert_sample_activities(self):
        activity_data = [
            ("Dog Cafe Social", "Cafe", "Cairo", "A pet-friendly cafe with social events every weekend.", "Sat, 4:00 PM", "011-1234-5678", 5),
            ("Paws in the Park", "Park", "Alexandria", "An open park where pets can run and play freely.", "Daily, 7:00 AM - 8:00 PM", "010-2345-6789", 4),
            ("Pet Training Workshop", "Workshop", "Giza", "A training session for dogs hosted by certified trainers.", "Sun, 10:00 AM", "012-3456-7890", 5),
            ("Pet Parade Event", "Event", "Cairo", "An annual event with pet competitions, prizes, and a pet community meetup.", "Jan 15, 10:00 AM", "011-5678-9012", 5),
            ("Cat Lounge Cafe", "Cafe", "Alexandria", "A cozy cafe dedicated to cat lovers with a relaxing ambiance.", "Daily, 9:00 AM - 9:00 PM", "010-6789-0123", 5)
        ]

        # Insert each activity into the 'activities' table
        self.cursor.executemany("""
        INSERT INTO activities (activity_name, activity_type, location, description, date_time, contact_info, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, activity_data)

        # Commit changes
        self.conn.commit()

    def find_pet_activities(self, location, activity_type=None):
        if not location:
            return "Location data missing. Please enter a valid location."

        query = "SELECT activity_name, activity_type, location, description, date_time, contact_info, rating FROM activities WHERE location LIKE ?"
        params = [f"%{location}%"]

        if activity_type:
            query += " AND activity_type LIKE ?"
            params.append(f"%{activity_type}%")

        self.cursor.execute(query, params)
        activities = self.cursor.fetchall()

        if not activities:
            return "No pet activities or events found in this area. Check back later or try a different location."

        result = []
        for activity in activities:
            result.append({
                'activity_name': activity[0],
                'activity_type': activity[1],
                'location': activity[2],
                'description': activity[3],
                'date_time': activity[4],
                'contact_info': activity[5],
                'rating': activity[6]
            })
        return result

    def find_upcoming_events(self, location):
        query = """
        SELECT activity_name, date_time, description FROM activities
        WHERE location LIKE ? AND activity_type = 'Event' AND date_time >= CURRENT_TIMESTAMP
        """
        self.cursor.execute(query, (f"%{location}%",))
        events = self.cursor.fetchall()

        if not events:
            return "No upcoming events in this area."

        result = []
        for event in events:
            result.append({
                'activity_name': event[0],
                'date_time': event[1],
                'description': event[2]
            })
        return result

    def close_connection(self):
        # Close the cursor and connection when done
        self.cursor.close()
        self.conn.close()

