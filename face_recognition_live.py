import cv2
import face_recognition
import os
import imutils
from collections import deque
import time
from datetime import datetime

# === Load known faces ===
known_face_encodings = []
known_face_names = []

known_faces_dir = 'known_faces'
for filename in os.listdir(known_faces_dir):
    if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
        image_path = os.path.join(known_faces_dir, filename)
        name = os.path.splitext(filename)[0]
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)

# === Setup camera and buffer ===
video_capture = cv2.VideoCapture(0)
fps = int(video_capture.get(cv2.CAP_PROP_FPS)) or 10
buffer_seconds = 30
buffer_size = buffer_seconds * fps

pre_buffer = deque(maxlen=buffer_size)
post_buffer = []
recording = False
post_frames_remaining = 0

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_writer = None

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=640)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Always keep the last 30 seconds
    pre_buffer.append(frame.copy())

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    found_vinicius = False

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = face_distances.argmin()
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        if name.lower() == "vinicius":
            found_vinicius = True

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    # Start recording if vinicius is detected
    if found_vinicius and not recording:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'vinicius_detected_{timestamp}.mp4'
        output_writer = cv2.VideoWriter(filename, fourcc, fps, (frame.shape[1], frame.shape[0]))
        print(f"[INFO] Detected 'vinicius'. Saving 30s before and starting 30s after to: {filename}")
        
        # Write pre-buffer
        for buffered_frame in pre_buffer:
            output_writer.write(buffered_frame)
        
        recording = True
        post_frames_remaining = buffer_size

    # If in recording mode, write current frame to post-buffer
    if recording:
        output_writer.write(frame)
        post_frames_remaining -= 1
        if post_frames_remaining <= 0:
            recording = False
            output_writer.release()
            output_writer = None
            print("[INFO] Finished saving 30s after detection.")

    cv2.putText(frame, "Press 'q' to quit", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow('Live Face Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video_capture.release()
if output_writer:
    output_writer.release()
cv2.destroyAllWindows()
