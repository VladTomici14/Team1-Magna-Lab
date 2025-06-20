import cv2
import os
from dotenv import load_dotenv
import serial  # Import the serial library

# Assuming recognizer.py and validator.py are in the same directory or accessible via PYTHONPATH
from recognizer import NumberPlateRecognizer
from validator import RomanianLicensePlateValidator

# Import the ParkingDatabaseManager class from your database.py (or parking_db_app.py) file
from database import ParkingDatabaseManager

# TODO: think about adding a conf.local file for each platform

# ----- only importing the picamera2 if we're running on a pi -----
try:
    from picamera2 import Picamera2
except ImportError:
    Picamera2 = None


class PiCamera2Stream:
    def __init__(self, resolution=(640, 480), platform="pi"):
        self.platform = platform
        self.resolution = resolution
        self.serial_port = None  # Initialize serial_port attribute

        # Constructors for image processing and plate validation classes
        self.numberPlateRecognizer = NumberPlateRecognizer()
        self.validator = RomanianLicensePlateValidator()

        # Load environment variables for database connection
        load_dotenv()
        DB_HOST = os.getenv("DB_HOST")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_NAME = os.getenv("DB_NAME")

        # Initialize the database manager
        if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
            print("Error: One or more database environment variables are not set. Please check your .env file.")
            self.db_manager = None  # Set to None to indicate no database connection
        else:
            self.db_manager = ParkingDatabaseManager(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

        if self.platform == "pi":
            # ----- initialising the picamera2 for the raspberry pi -----
            if not Picamera2:
                raise ImportError("[ERROR] picamera2 module not found. Are you running this on a Pi with Bookworm?")

            self.picam2 = Picamera2()
            self.picam2.preview_configuration.main.size = resolution
            self.picam2.preview_configuration.main.format = "RGB888"
            self.picam2.configure("preview")
            self.picam2.start()
            print(f"[Picamera2] Camera started with resolution {resolution}")

            # ----- Initializing serial communication for Raspberry Pi -----
            try:
                # Configure the serial port. Adjust baudrate as needed for your device.
                self.serial_port = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
                print(f"[Serial] Connected to /dev/ttyUSB0 at 9600 baud.")
            except serial.SerialException as e:
                print(f"[ERROR] Could not open serial port /dev/ttyUSB0: {e}")
                self.serial_port = None  # Ensure it's None if connection fails
            except FileNotFoundError:
                print(f"[ERROR] Serial port /dev/ttyUSB0 not found. Check if the device is connected.")
                self.serial_port = None

        elif self.platform == "mac":
            # ----- initialising the webcam for the macOS system -----
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
            print(f"[Webcam] Initialized with resolution {resolution}")

        # TODO: add linux / windows platforms for this class (depends on who's interested in running the code locally)

        else:
            # ----- returning an error if the platform is not supported -----
            raise ValueError("[ERROR] Unsupported platform. Use 'pi' or 'mac'.")

    def _send_serial_message(self, message):
        """
        Sends a message over the initialized serial port.
        """
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(message.encode('utf-8'))  # Encode message to bytes
                print(f"[Serial] Sent message: '{message}'")
            except serial.SerialException as e:
                print(f"[ERROR] Error sending serial message: {e}")
        else:
            print("[Serial] Serial port not open or not initialized. Message not sent.")

    def start_stream(self):
        """
        Starts the camera stream and displays the video feed in a window.
        """
        print("Press 'q' to quit.")
        while True:
            frame = None  # Initialize frame outside the if/else to ensure it's always defined for cv2.imshow

            if self.platform == "pi":
                frame = self.picam2.capture_array()  # captures a single image frame from the active preview stream.

                # NOTE: The current setup uses a static image path ("../images/car1.jpg") for recognition
                # You might want to pass the 'frame' directly to the recognizer if it processes raw image data.
                # For demonstration, I'll assume your recognizer can handle 'frame' or that you're using
                # the static image for testing the plate recognition part.
                # If your recognizer needs a file path, you'd need to save the frame to a temporary file first.

                # Assuming recognizer.recognizePlateNumber can take the captured 'frame' directly or an image path
                # I'm keeping the original call for now. If it expects a file path, this will need adjustment.
                # If your recognizer can take an OpenCV image (numpy array), you would change this to:
                # plate_region, extracted_text = self.numberPlateRecognizer.recognizePlateNumber(frame)

                # For this example, let's assume `recognizer` can process the `frame` directly.
                # If it expects an image path, you'd need to save the frame temporarily.
                # As `car1.jpg` is a fixed path, I'll add a placeholder to demonstrate the flow.
                # You'll need to adapt `recognizer.py` or how you feed images to it.
                # For a real-time system, you'd pass the `frame` (numpy array) directly.

                # Temporarily using a placeholder for extracted_text for testing db integration
                # In a real scenario, this would come from the actual recognition process.
                # For now, let's simulate a recognized plate for testing DB integration:
                # extracted_text = "B01ABC" # Example of a recognized plate for testing

                # Original call, assuming it works with your setup or is for a different part of the flow
                plate_region, extracted_text = self.numberPlateRecognizer.recognizePlateNumber("../images/car1.jpg",
                                                                                               frame)

                if extracted_text is not None and extracted_text != "":  # Ensure text is not empty
                    extracted_text = extracted_text.strip().upper()  # Clean and standardize
                    print(f"Recognized Text: {extracted_text}")

                    if self.validator.verifyPlateFormat(extracted_text):
                        print(f"Plate '{extracted_text}' is in VALID format.")

                        # --- Database Verification and Auto-Add ---
                        if self.db_manager:
                            vehicle_info = self.db_manager.verify_from_database(extracted_text)
                            if vehicle_info:
                                print(
                                    f"*** Plate '{extracted_text}' FOUND in database! Authorization: {vehicle_info['is_authorized']} ***")
                                # Send serial message if found and authorized (you can add a condition here if needed)
                                self._send_serial_message("open_entry")
                            else:
                                # If plate not found in DB, check if it starts with "TM" and add it
                                print(f"--- Plate '{extracted_text}' NOT FOUND in database. ---")
                                if extracted_text.startswith("TM"):
                                    print(
                                        f"Plate '{extracted_text}' starts with 'TM'. Attempting to add to database...")
                                    if self.db_manager.append_to_database(extracted_text, is_authorized=True):
                                        print(
                                            f"*** Plate '{extracted_text}' successfully ADDED to database with authorization TRUE. ***")
                                        # Send serial message after successful auto-add
                                        self._send_serial_message("open_entry")
                                    else:
                                        print(f"!!! Failed to add plate '{extracted_text}' to database. !!!")
                                else:
                                    print(
                                        f"Plate '{extracted_text}' does not start with 'TM'. Not automatically adding to database.")
                        else:
                            print("Database manager not initialized. Cannot verify or add plate to DB.")
                    else:
                        print(f"Plate '{extracted_text}' is in INVALID format.")
                elif extracted_text == "":
                    print("No text extracted from plate region.")
                else:
                    print("Plate recognition failed or no text extracted.")


            elif self.platform == "mac":
                ret, frame = self.camera.read()

                if not ret:
                    print("[ERROR] Failed to capture image from webcam.")
                    break

                # On macOS, you would also apply your recognition and validation logic here
                # plate_region, extracted_text = self.numberPlateRecognizer.recognizePlateNumber(frame)
                # ... and then perform database verification as above ...

            # Only show frame if it's available
            if frame is not None:
                cv2.imshow("Camera stream", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        """
        Cleans up the resources used by the camera stream.
        """
        cv2.destroyAllWindows()

        if self.platform == "pi":
            self.picam2.stop()
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
                print("[Serial] Serial port closed.")
        elif self.platform == "mac":  # Added elif for clarity
            self.camera.release()


if __name__ == "__main__":
    # ----- initialising the camera stream class based on the target resolution and running platform -----
    # Make sure your recognizer.py and validator.py are correctly set up and accessible.
    # If running on a Pi, ensure picamera2 is installed and functional.
    # If using 'mac', ensure your webcam is accessible (usually index 0).

    # For testing on a Pi:
    stream = PiCamera2Stream(resolution=(800, 600), platform="pi")

    # For testing on a Mac (if you have a webcam and cv2 is installed):
    # stream = PiCamera2Stream(resolution=(800, 600), platform="mac")

    # ----- starting the camera stream -----
    stream.start_stream()
