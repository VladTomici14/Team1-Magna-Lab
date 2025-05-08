import cv2

from recognizer import *
from validator import *

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

        self.numberPlateRecognizer = NumberPlateRecognizer()
        self.validator = RomanianLicensePlateValidator()

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

    def start_stream(self):
        """
        Starts the camera stream and displays the video feed in a window.
        """
        print("Press 'q' to quit.")
        while True:

            if self.platform == "pi":
                frame = self.picam2.capture_array()

                plate_region, extracted_text = self.numberPlateRecognizer.recognizePlateNumber("../images/car1.jpg", frame)

                if extracted_text is not None and validator.verifyPlateFormat(extracted_text):
                    print(extracted_text)

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
        """
        Cleans up the resources used by the camera stream.
        """
        cv2.destroyAllWindows()

        if self.platform == "pi":
            self.camera.stop()
        else:
            self.camera.release()


if __name__ == "__main__":
    # ----- initialising the camera stream class based on the target resolution and running platform -----
    stream = PiCamera2Stream(resolution=(800, 600), platform="pi")

    # ----- starting the camera stream -----
    stream.start_stream()
