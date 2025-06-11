import cv2
from src.recognizer import *
from src.validator import *

try:
    from picamera2 import Picamera2
except ImportError:
    Picamera2 = None


class PiCamera2Stream:
    def __init__(self, resolution=(640, 480), platform="pi"):
        self.platform = platform
        self.resolution = resolution

        self.numberPlateRecognizer = NumberPlateRecognizer()
        self.validator = RomanianLicensePlateValidator()

        if self.platform == "pi":
            if not Picamera2:
                raise ImportError("[ERROR] picamera2 module not found. Are you running this on a Pi with Bookworm?")

            self.picam2 = Picamera2()
            self.picam2.preview_configuration.main.size = resolution
            self.picam2.preview_configuration.main.format = "RGB888"
            self.picam2.configure("preview")
            self.picam2.start()
            print(f"[Picamera2] Camera started with resolution {resolution}")


        else:
            raise ValueError("[ERROR] Unsupported platform. Use 'pi' or 'mac'.")

    def start_stream(self):
        print("Press 'q' to quit.")
        while True:
            if self.platform == "pi":
                frame = self.picam2.capture_array()

                plate_region, extracted_text = self.numberPlateRecognizer.recognizePlateNumber(None,frame)

                if extracted_text:
                    print(f"[Plate] Detected: {extracted_text}")
                    if self.validator.verifyPlateFormat(extracted_text):
                        print("[Valid Plate] Format verified.")

            else:
                ret, frame = self.camera.read()
                if not ret:
                    print("[ERROR] Failed to capture image from webcam.")
                    break

            cv2.imshow("Camera stream", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        cv2.destroyAllWindows()
        if self.platform == "pi":
            self.picam2.stop()
        else:
            self.camera.release()


if __name__ == "__main__":
    stream = PiCamera2Stream(resolution=(800, 600), platform="pi")
    stream.start_stream()



