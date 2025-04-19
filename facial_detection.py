import torch
import cv2
from face_alignment import FaceAlignment, LandmarksType
import numpy as np
from threading import Thread
from encouragement_app import EncouragementApp


class BoredomDetector:
    def __init__(self, model_path):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.face_alignment_model = FaceAlignment(LandmarksType.TWO_D, flip_input=False, device=self.device)

        self.model = torch.load(model_path, weights_only=False)
        self.model.to(self.device)
        self.model.eval()
        self.encouragement_window = None
        self.running = False
        self.capture = None
        self.thread = None

    def detect_boredom(self, frame):
        faces = self.face_alignment_model.get_landmarks_from_image(frame)
        if faces:
            resized_face = cv2.resize(frame, (64, 64))
            resized_face = resized_face.transpose(2, 0, 1)
            resized_face = torch.tensor(resized_face, dtype=torch.float32).unsqueeze(0).to(self.device)

            with torch.no_grad():
                output = self.model(resized_face)

            valence = output[0][0].item()
            arousal = output[0][1].item()

            if valence < 0.3 and arousal < 0.3:
                if not self.encouragement_window.master:
                    self.encouragement_window.master = EncouragementApp()
                return "Bored", valence, arousal
            else:
                return "Not Bored", valence, arousal
        else:
            return "No face detected", None, None

    def _run(self):
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            state, valence, arousal = self.detect_boredom(frame)

            if valence is not None and arousal is not None:
                cv2.putText(frame, f"State: {state}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Valence: {valence:.2f}, Arousal: {arousal:.2f}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Emotion Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.capture.release()
        cv2.destroyAllWindows()

    def start(self):
        if not self.running:
            self.capture = cv2.VideoCapture(0)
            self.running = True
            self.thread = Thread(target=self._run)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()


# Example usage
if __name__ == '__main__':
    model_path = 'C:/Users/13105/Documents/Productivity-App-Hackathon/torchscript_model_0_66_49_wo_gl.pth'
    detector = BoredomDetector(model_path)
    detector.start()
