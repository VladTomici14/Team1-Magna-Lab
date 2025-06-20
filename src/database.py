import mysql.connector
from mysql.connector import Error
import datetime
import os # Import the os module to access environment variables
from dotenv import load_dotenv # Import load_dotenv

class ParkingDatabaseManager:
    """
    Manages interactions with the team1_parking MySQL database.
    Provides methods to append, delete, and verify vehicle records.
    """

    def __init__(self, host, user, password, database):
        """
        Initializes the database manager with connection details.

        Args:
            host (str): The database host (e.g., 'localhost' or Raspberry Pi's IP).
            user (str): The database username.
            password (str): The password for the database user.
            database (str): The name of the database (e.g., 'team1_parking').
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def _connect(self):
        """
        Establishes a connection to the MySQL database.
        Returns the connection and cursor objects if successful, otherwise None.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(buffered=True)
                print(f"Successfully connected to MySQL database: {self.database}")
                return self.connection, self.cursor
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return None, None
        return None, None

    def _disconnect(self):
        """
        Closes the database cursor and connection.
        """
        try:
            if self.cursor:
                self.cursor.close()
                print("MySQL cursor closed.")
            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("MySQL connection closed.")
        except Error as e:
            print(f"Error closing MySQL connection: {e}")

    def append_to_database(self, plate_number, is_authorized=True):
        """
        Appends a new vehicle record to the 'vehicles' table.

        Args:
            plate_number (str): The unique plate number of the vehicle.
            is_authorized (bool, optional): Whether the vehicle is authorized.
                                            Defaults to True.

        Returns:
            bool: True if the record was successfully added, False otherwise.
        """
        connection, cursor = self._connect()
        if not connection:
            return False

        try:
            # Check if plate number already exists to prevent duplicates
            query_check = "SELECT vehicle_id FROM vehicles WHERE plate_number = %s"
            cursor.execute(query_check, (plate_number,))
            if cursor.fetchone():
                print(f"Error: Vehicle with plate number '{plate_number}' already exists.")
                return False

            query_insert = """
            INSERT INTO vehicles (plate_number, added_at, is_authorized)
            VALUES (%s, %s, %s)
            """
            # Use datetime.datetime.now() to get the current timestamp
            # which matches the DATETIME format in MySQL
            current_time = datetime.datetime.now()
            cursor.execute(query_insert, (plate_number, current_time, is_authorized))
            connection.commit()
            print(f"Successfully added vehicle: Plate='{plate_number}', Authorized={is_authorized}")
            return True
        except Error as e:
            print(f"Error appending vehicle to database: {e}")
            return False
        finally:
            self._disconnect()

    def delete_from_database(self, plate_number):
        """
        Deletes a vehicle record from the 'vehicles' table based on plate number.

        Args:
            plate_number (str): The plate number of the vehicle to delete.

        Returns:
            bool: True if the record was successfully deleted, False otherwise.
        """
        connection, cursor = self._connect()
        if not connection:
            return False

        try:
            query_delete = "DELETE FROM vehicles WHERE plate_number = %s"
            cursor.execute(query_delete, (plate_number,))
            connection.commit()
            if cursor.rowcount > 0:
                print(f"Successfully deleted vehicle with plate number: '{plate_number}'")
                return True
            else:
                print(f"No vehicle found with plate number: '{plate_number}' to delete.")
                return False
        except Error as e:
            print(f"Error deleting vehicle from database: {e}")
            return False
        finally:
            self._disconnect()

    def verify_from_database(self, plate_number):
        """
        Verifies if a plate number exists in the 'vehicles' table
        and returns its details.

        Args:
            plate_number (str): The plate number to verify.

        Returns:
            dict or None: A dictionary containing vehicle details
                          (vehicle_id, plate_number, added_at, is_authorized)
                          if found, otherwise None.
        """
        connection, cursor = self._connect()
        if not connection:
            return None

        try:
            query_select = "SELECT vehicle_id, plate_number, added_at, is_authorized FROM vehicles WHERE plate_number = %s"
            cursor.execute(query_select, (plate_number,))
            result = cursor.fetchone()

            if result:
                vehicle_details = {
                    "vehicle_id": result[0],
                    "plate_number": result[1],
                    "added_at": result[2],
                    "is_authorized": bool(result[3]) # Convert tinyint(1) to Python boolean
                }
                print(f"Vehicle found: {vehicle_details}")
                return vehicle_details
            else:
                print(f"Vehicle with plate number '{plate_number}' not found.")
                return None
        except Error as e:
            print(f"Error verifying vehicle from database: {e}")
            return None
        finally:
            self._disconnect()

# --- Example Usage ---
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve database credentials from environment variables
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    # Basic check to ensure environment variables are loaded
    if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
        print("Error: One or more database environment variables are not set. "
              "Please check your .env file.")
    else:
        db_manager = ParkingDatabaseManager(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

        print("\n--- Appending a new vehicle ---")
        db_manager.append_to_database("ABC-123", is_authorized=True)
        db_manager.append_to_database("XYZ-789", is_authorized=False)
        db_manager.append_to_database("LMN-456") # Defaults to is_authorized=True

        print("\n--- Trying to append an existing vehicle (should fail) ---")
        db_manager.append_to_database("ABC-123")

        print("\n--- Verifying vehicles ---")
        vehicle1 = db_manager.verify_from_database("ABC-123")
        if vehicle1:
            print(f"ABC-123 is authorized: {vehicle1['is_authorized']}")

        vehicle2 = db_manager.verify_from_database("XYZ-789")
        if vehicle2:
            print(f"XYZ-789 is authorized: {vehicle2['is_authorized']}")

        db_manager.verify_from_database("NON-EXISTENT")

        print("\n--- Deleting a vehicle ---")
        db_manager.delete_from_database("XYZ-789")

        print("\n--- Verifying deleted vehicle (should not be found) ---")
        db_manager.verify_from_database("XYZ-789")

        print("\n--- Deleting a non-existent vehicle (should indicate not found) ---")
        db_manager.delete_from_database("NON-EXISTENT")
