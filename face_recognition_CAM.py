import face_recognition
import cv2
import os
import pickle

faces_dir = "./faces"

def gen_face_encodings():
    faces = {}
    for img in os.listdir(faces_dir):
        img_path = os.path.join(faces_dir, img)
        label = img.split(".")[0]
        image = face_recognition.load_image_file(img_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        faces[label] = face_encoding

    with open("face_encodings.pickle", "wb") as f:
        pickle.dump(faces, f)
    return faces

#faces = gen_face_encodings()
# If you have a saved pickle file:
pickle_in = open("face_encodings.pickle","rb")
faces = pickle.load(pickle_in)

cap=cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    face_locations = face_recognition.face_locations(frame)
    unknown_face_encodings = face_recognition.face_encodings(frame, face_locations)
    face_names = []

    for (y1, x1, y2, x2), face_encoding in zip(face_locations, unknown_face_encodings):
        name = "Unknown"
        for key in faces.keys():
            result = face_recognition.compare_faces([faces[key]], face_encoding)
            #print(result)
            if result[0]:
                name = key
                print(key)
        cv2.rectangle(frame, (x2-20, y1-20), (x1+20, y2+20), (255, 0, 0), 2)
        cv2.rectangle(frame, (x2-20, y1-45), (x1+20, y1-15), (255, 0, 0), -1)
        cv2.putText(frame, name, (x2 -20, y1 -20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255), 2)
    cv2.imshow('Face Recognizer', frame)
    if(cv2.waitKey(1) & 0XFF==ord('q')):
        cv2.imwrite("facerecog.jpg", frame)
        break
cap.release()
cv2.destroyAllWindows()