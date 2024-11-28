import pyodbc as pydb

connection_to_database= {
    "DRIVER":"{ODBC Driver 17 for SQL Server}",
    "SERVER":"MSSQL Port 1433,1433",
    "DATABASE":"PetLinker",
    "UID":"flask_user",
    "PWD":"Flask!User1234"
}
def connect_to_database():
    connection = pydb.connect(
     f"DRIVER={connection_to_database['DRIVER']};"
     f"SERVER={connection_to_database['SERVER']};"
     f"DATABASE={connection_to_database['DATABASE']};"
     f"UID={connection_to_database['UID']};"
     f"PWD={connection_to_database['PWD']};"   
    )
    return connection