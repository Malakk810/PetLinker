import pyodbc

class PetActivityService:
    def __init__(self):
        try:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};'
                'SERVER=FaridaAli\\SQLEXPRESS;'  
                'DATABASE=PetLinker;'
                'UID=flask_user;'
                'PWD=Flask!User1234;'
                'TrustServerCertificate=yes'
            )
            self.cursor = self.conn.cursor()
            self.activity_service = PetActivityService()  
        except pyodbc.Error as e:
            print(f"Error connecting to the database: {e}")
            raise

    def insert_sample_activities(self):
        activity_data = [
            ("Dog Cafe Social", "Cafe", "Cairo", "A pet-friendly cafe with social events every weekend.", "2024-12-03 16:00:00", "011-1234-5678", 5),
            ("Paws in the Park", "Park", "Alexandria", "An open park where pets can run and play freely.", "2024-12-02 07:00:00", "010-2345-6789", 4),
            ("Pet Training Workshop", "Workshop", "Giza", "A training session for dogs hosted by certified trainers.", "2024-12-04 10:00:00", "012-3456-7890", 5),
        ]

        
        self.cursor.executemany("""
        INSERT INTO activities (activity_name, activity_type, location, description, date_time, contact_info, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, activity_data)

        self.conn.commit()

    def find_pet_activities(self, location, activity_type=None):
        if not location:
            return "Location data missing. Please enter a valid location."

        query = """
        SELECT activity_name, activity_type, location, description, date_time, contact_info, rating 
        FROM activities 
        WHERE location LIKE ?
        """
        params = [f"%{location}%"]

        if activity_type:
            query += " AND activity_type LIKE ?"
            params.append(f"%{activity_type}%")

        self.cursor.execute(query, params)
        activities = self.cursor.fetchall()

        if not activities:
            return "No pet activities or events found in this area. Check back later or try a different location."

        return [
            {
                'activity_name': activity[0],
                'activity_type': activity[1],
                'location': activity[2],
                'description': activity[3],
                'date_time': activity[4].strftime("%Y-%m-%d %H:%M:%S"),
                'contact_info': activity[5],
                'rating': activity[6]
            }
            for activity in activities
        ]

    def find_upcoming_events(self, location):
        query = """
        SELECT activity_name, date_time, description 
        FROM activities
        WHERE location LIKE ? AND activity_type = 'Event' AND date_time >= CURRENT_TIMESTAMP
        """
        self.cursor.execute(query, (f"%{location}%",))
        events = self.cursor.fetchall()

        if not events:
            return "No upcoming events in this area."

        return [
            {
                'activity_name': event[0],
                'date_time': event[1].strftime("%Y-%m-%d %H:%M:%S"),
                'description': event[2]
            }
            for event in events
        ]

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
