import cv2
import face_recognition
print("face_recognition is working.")
import os
import imutils

# === Load known faces ===
known_face_encodings = []
known_face_names = []

known_faces_dir = 'known_faces'

for filename in os.listdir(known_faces_dir):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        image_path = os.path.join(known_faces_dir, filename)
        name = os.path.splitext(filename)[0]  # Use file name (without extension) as person's name

        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)
        else:
            print(f"Warning: No face found in {filename}")

# === Load video ===
video_capture = cv2.VideoCapture('cam_video.MOV')

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=640)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = face_distances.argmin()
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        # Draw rectangle and label
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    cv2.imshow('Face Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
