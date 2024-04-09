import os
import cv2
import numpy as np
import math
import sys
import face_recognition
import threading

def face_confidence(face_distance, face_match_threshold=0.6):
    range_ = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range_ * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val +((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

class FaceRecognition:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f'faces/{image}')
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)

    def run_recognition(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = 'Unknown'
            confidence = 'Unknown'

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                confidence = face_confidence(face_distances[best_match_index])

            face_names.append((name, confidence))

        for (top, right, bottom, left), (name, confidence) in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)

            # Adjust text position to keep it within the frame width
            text_width, text_height = cv2.getTextSize(f'{name} ({confidence})', cv2.FONT_HERSHEY_DUPLEX, 0.8, 1)[0]
            text_left = max(left, 0)
            text_bottom = min(bottom - 6, frame.shape[0])
            cv2.putText(frame, f'{name} ({confidence})', (text_left, text_bottom), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            print(f'{name} ({confidence})')



def capture_faces():
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        sys.exit('Source not found')

    while True:
        ret, frame = video_capture.read()

        # Perform face recognition
        fr.run_recognition(frame)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    fr = FaceRecognition()
    threading.Thread(target=capture_faces).start()
