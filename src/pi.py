from picamera2 import Picamera2
import cv2

class PiCamera2Stream:
    def __init__(self, resolution=(640, 480)):
        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.size = resolution
        self.picam2.preview_configuration.main.format = "BGR888"  # OpenCV-friendly
        self.picam2.configure("preview")
        self.picam2.start()
        print(f"Camera started with resolution {resolution}")

    def start_stream(self):
        print("Press 'q' to quit.")
        while True:
            frame = self.picam2.capture_array()
            cv2.imshow("PiCamera2", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        cv2.destroyAllWindows()
        self.picam2.stop()
