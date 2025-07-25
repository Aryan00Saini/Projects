import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'faces'
images = []
names = []

file_list = os.listdir(path)
for file_name in file_list:
    img = cv2.imread(f'{path}/{file_name}')
    images.append(img)
    names.append(os.path.splitext(file_name)[0])

def encode_faces(images):
    encoded_faces = []
    for img in images:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img_rgb)
        if encodings:
            encoded_faces.append(encodings[0])
        else:
            print("No face found in one of the images.")
    return encoded_faces

def save_attendance(name):
    if not os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'w') as file:
            file.write('Name,Time\n')

    with open('Attendance.csv', 'r+') as file:
        lines = file.readlines()
        present_names = []
        for line in lines:
            entry = line.split(',')
            present_names.append(entry[0])

        if name not in present_names:
            current_time = datetime.now().strftime('%H:%M:%S')
            file.write(f'{name},{current_time}\n')

print("Encoding all faces")
known_encodings = encode_faces(images)
print("All faces encoded!")

video = cv2.VideoCapture(0)

while True:
    success, frame = video.read()

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(frame_rgb)
    face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

    for i in range(len(face_encodings)):
        face_encoding = face_encodings[i]
        face_location = face_locations[i]

        matches = face_recognition.compare_faces(known_encodings, face_encoding)  

        name = "Unknown" 

        found_match = False  
        for match_index in range(len(matches)):
            if matches[match_index]: 
                found_match = True

                distance = face_recognition.face_distance(known_encodings, face_encoding)

                best_match_index = 0  
                min_distance = distance[0]
                for i in range(1, len(distance)):
                    if distance[i] < min_distance:
                        min_distance = distance[i]
                        best_match_index = i
                name = names[best_match_index]
                save_attendance(name)
                break  

        y1, x2, y2, x1 = face_location
        left, top, right, bottom = x1, y1, x2, y2
        color = (0, 255, 0) 

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        message = "Present"
        cv2.putText(frame, f"{name}-{message}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow('Face Recognition Attendance', frame)
    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()




