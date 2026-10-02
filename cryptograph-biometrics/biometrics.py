# biometrics.py
# Implements webcam face enrollment/matching and fingerprint verification.
# Faces are stored as individual named PNGs under the faces/ directory.

import cv2
import numpy as np
import os
import time

# Directory where named face templates are stored
FACES_DIR = "faces"
TEMPLATE_FINGERPRINT_PATH = "template_fingerprint.png"


def generate_mock_fingerprint(output_path, seed=42, noise=False):
    """
    Generates a simulated fingerprint image by drawing concentric ellipses,
    representing ridges. Perfect for demonstrating structural comparisons.
    """
    img = np.ones((400, 400, 3), dtype=np.uint8) * 255
    np.random.seed(seed)
    center = (200 + np.random.randint(-15, 16), 220 + np.random.randint(-15, 16))
    base_angle = np.random.randint(0, 180)
    spacing = np.random.randint(6, 10)
    for r in range(20, 180, spacing):
        axes = (r, int(r * 1.3))
        cv2.ellipse(img, center, axes, base_angle, 0, 360, (0, 0, 0), 2)
    for _ in range(15):
        x = np.random.randint(100, 300)
        y = np.random.randint(100, 300)
        length = np.random.randint(10, 25)
        angle_rad = np.random.rand() * np.pi * 2
        x2 = int(x + length * np.cos(angle_rad))
        y2 = int(y + length * np.sin(angle_rad))
        cv2.line(img, (x, y), (x2, y2), (0, 0, 0), 3)
    if noise:
        np.random.seed(int(time.time()) % 10000 + seed)
        noise_mask = np.random.rand(400, 400) < 0.05
        img[noise_mask] = (0, 0, 0)
    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    cv2.imwrite(output_path, img)


def _sanitize_name(name: str) -> str:
    """Strips and lowercases a name for use as a filename."""
    return name.strip().replace(" ", "_").lower()


class BiometricVerifier:
    def __init__(self):
        os.makedirs(FACES_DIR, exist_ok=True)
        if not os.path.exists(TEMPLATE_FINGERPRINT_PATH):
            generate_mock_fingerprint(TEMPLATE_FINGERPRINT_PATH, seed=101, noise=False)

    # ------------------------------------------------------------------
    # Named Face Registry Helpers
    # ------------------------------------------------------------------

    def _face_path(self, name: str) -> str:
        return os.path.join(FACES_DIR, f"{_sanitize_name(name)}.png")

    def list_registered_faces(self) -> list:
        """Returns sorted list of registered display-names."""
        names = []
        if not os.path.isdir(FACES_DIR):
            return names
        for fname in os.listdir(FACES_DIR):
            if fname.lower().endswith(".png"):
                display = os.path.splitext(fname)[0].replace("_", " ").title()
                names.append(display)
        return sorted(names)

    def is_face_registered(self) -> bool:
        return len(self.list_registered_faces()) > 0

    def is_name_registered(self, name: str) -> bool:
        return os.path.exists(self._face_path(name))

    def delete_face(self, name: str) -> bool:
        path = self._face_path(name)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    # ------------------------------------------------------------------
    # Fingerprint Verification
    # ------------------------------------------------------------------

    def verify_fingerprint(self, test_image_path):
        if not os.path.exists(test_image_path):
            return False, None, 0.0, "Test fingerprint image file not found."
        img1 = cv2.imread(TEMPLATE_FINGERPRINT_PATH, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(test_image_path, cv2.IMREAD_GRAYSCALE)
        if img1 is None or img2 is None:
            return False, None, 0.0, "Error reading fingerprint images."
        diff = img1.astype(float) - img2.astype(float)
        mse = np.mean(diff ** 2)
        score = max(0.0, 100.0 - (mse / 250.0))
        h, w = img1.shape
        match_img = np.zeros((h, w * 2 + 10, 3), dtype=np.uint8)
        bgr1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
        bgr2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        match_img[:, :w] = bgr1
        match_img[:, w:w+10] = [128, 128, 128]
        match_img[:, w+10:] = bgr2
        threshold_score = 75.0
        success = score >= threshold_score
        color = (0, 255, 0) if success else (0, 0, 255)
        match_img = cv2.copyMakeBorder(match_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=color)
        output_dir = os.path.dirname(test_image_path) or "."
        match_output_path = os.path.join(output_dir, "fingerprint_matches.png")
        cv2.imwrite(match_output_path, match_img)
        explanation = (
            f"Comparing structural ridge patterns:\n"
            f"Mean Squared Error (MSE): {mse:.2f}\n"
            f"Calculated Pattern Match Score: {score:.2f}%\n"
            f"Required Match Threshold: {threshold_score:.2f}%\n"
        )
        if success:
            explanation += "STATUS: Verification SUCCESSFUL! Fingerprint ridges match."
        else:
            explanation += "STATUS: Verification FAILED! Intruder detected."
        return success, match_output_path, score, explanation

    # ------------------------------------------------------------------
    # Webcam Face Registration (Named)
    # ------------------------------------------------------------------

    def register_face_via_webcam(self, name, on_frame_callback, on_complete_callback, on_error_callback):
        """
        Opens webcam, captures a face, saves it as faces/<name>.png.
        Calls on_complete_callback(True, display_name) on success.
        """
        if not name or not name.strip():
            on_error_callback("A name is required to register a face.")
            return

        save_path = self._face_path(name)
        display_name = name.strip().title()

        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        if face_cascade.empty():
            on_error_callback("Failed to load face detection cascade classifier.")
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            on_error_callback("Cannot open webcam. Please make sure no other app is using it.")
            return

        face_captured = False
        running = True
        try:
            while running:
                ret, frame = cap.read()
                if not ret:
                    on_error_callback("Failed to grab webcam frame.")
                    break
                frame = cv2.flip(frame, 1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
                    cv2.putText(frame, f"CAPTURING: {display_name}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 2)
                    face_crop = gray[y:y+h, x:x+w]
                    face_resized = cv2.resize(face_crop, (128, 128), interpolation=cv2.INTER_AREA)
                    cv2.imwrite(save_path, face_resized)
                    face_captured = True
                    running = False
                    break
                if face_captured:
                    on_frame_callback(frame)
                    time.sleep(0.5)
                    on_complete_callback(True, display_name)
                    break
                if not on_frame_callback(frame):
                    running = False
                    break
                time.sleep(0.03)
        finally:
            cap.release()
            try:
                cv2.destroyAllWindows()
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Webcam Face Verification (Named Multi-Face)
    # ------------------------------------------------------------------

    def scan_face_via_webcam(self, on_frame_callback, on_complete_callback, on_error_callback):
        """
        Compares live face against ALL registered templates.
        Calls on_complete_callback(True, matched_name) on success.
        """
        registered = self.list_registered_faces()
        if not registered:
            on_error_callback("No registered faces found. Please register a face first.")
            return

        # Pre-load and preprocess all registered face templates
        templates = {}
        for display_name in registered:
            path = self._face_path(display_name)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                eq = cv2.equalizeHist(img)
                templates[display_name] = cv2.GaussianBlur(eq, (3, 3), 0)

        if not templates:
            on_error_callback("Could not load any registered face templates.")
            return

        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        if face_cascade.empty():
            on_error_callback("Failed to load face detection cascade classifier.")
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            on_error_callback("Cannot open webcam. Please make sure no other app is using it.")
            return

        detection_duration_needed = 2.5
        last_detected_time = None
        cumulative_detected_time = 0.0
        current_match_name = None

        running = True
        try:
            while running:
                ret, frame = cap.read()
                if not ret:
                    on_error_callback("Failed to grab webcam frame.")
                    break
                frame = cv2.flip(frame, 1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))

                current_time = time.time()
                face_matched = False
                best_match_name = None
                color_hud = (0, 0, 255)

                for (x, y, w, h) in faces:
                    face_crop = gray[y:y+h, x:x+w]
                    face_resized = cv2.resize(face_crop, (128, 128), interpolation=cv2.INTER_AREA)
                    face_eq = cv2.equalizeHist(face_resized)
                    face_processed = cv2.GaussianBlur(face_eq, (3, 3), 0)

                    best_ncc = -1.0
                    best_mse = float('inf')
                    best_name = None
                    for tname, timg in templates.items():
                        diff = timg.astype(float) - face_processed.astype(float)
                        mse = np.mean(diff ** 2)
                        ncc_result = cv2.matchTemplate(face_processed, timg, cv2.TM_CCOEFF_NORMED)
                        ncc = ncc_result[0][0]
                        if ncc > best_ncc:
                            best_ncc = ncc
                            best_mse = mse
                            best_name = tname

                    if best_name and best_mse < 2000 and best_ncc >= 0.78:
                        face_matched = True
                        best_match_name = best_name
                        color_hud = (0, 255, 0)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), color_hud, 2)
                        cv2.putText(frame, f"CONFIRMED: {best_name} (NCC:{best_ncc:.2f})",
                                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color_hud, 2)
                    else:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), color_hud, 2)
                        lbl = best_name if best_name else "?"
                        cv2.putText(frame, f"UNKNOWN (NCC:{best_ncc:.2f} MSE:{best_mse:.0f})",
                                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color_hud, 2)

                if face_matched:
                    current_match_name = best_match_name
                    if last_detected_time is None:
                        last_detected_time = current_time
                    else:
                        elapsed = current_time - last_detected_time
                        cumulative_detected_time += elapsed
                        last_detected_time = current_time
                else:
                    last_detected_time = None
                    current_match_name = None
                    cumulative_detected_time = max(0.0, cumulative_detected_time - 0.05)

                progress = min(1.0, cumulative_detected_time / detection_duration_needed)
                bar_width = int(progress * (frame.shape[1] - 100))
                cv2.rectangle(frame, (50, frame.shape[0] - 50),
                              (frame.shape[1] - 50, frame.shape[0] - 40), (100, 100, 100), -1)
                if bar_width > 0:
                    cv2.rectangle(frame, (50, frame.shape[0] - 50),
                                  (50 + bar_width, frame.shape[0] - 40), (0, 255, 0), -1)
                bar_text = f"VERIFYING: {int(progress * 100)}%"
                cv2.putText(frame, bar_text, (50, frame.shape[0] - 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0, 255, 255) if progress < 1.0 else (0, 255, 0), 2)

                if progress >= 1.0:
                    cv2.putText(frame, f"ACCESS GRANTED: {current_match_name}",
                                (max(0, int(frame.shape[1]/2) - 200), int(frame.shape[0]/2)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)
                    on_frame_callback(frame)
                    time.sleep(1.0)
                    running = False
                    on_complete_callback(True, current_match_name)
                    break

                if not on_frame_callback(frame):
                    running = False
                    break
                time.sleep(0.03)
        finally:
            cap.release()
            try:
                cv2.destroyAllWindows()
            except Exception:
                pass


if __name__ == "__main__":
    verifier = BiometricVerifier()
    generate_mock_fingerprint("test_positive.png", seed=101, noise=True)
    generate_mock_fingerprint("test_negative.png", seed=202, noise=False)
    print("Testing positive match...")
    success, match_path, score, explanation = verifier.verify_fingerprint("test_positive.png")
    print(explanation)
    assert success == True, "Fingerprint positive verification failed!"
    print("\nTesting negative match...")
    success, match_path, score, explanation = verifier.verify_fingerprint("test_negative.png")
    print(explanation)
    assert success == False, "Fingerprint negative verification succeeded when it should fail!"
    print("\nBiometric verification module tests passed!")
