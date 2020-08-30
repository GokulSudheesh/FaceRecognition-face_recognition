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

img_filename = "unknown_image1.jpg"
unknown_image = face_recognition.load_image_file(img_filename)
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
img = cv2.imread(img_filename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face_detections = face_cascade.detectMultiScale(gray, 1.3, 5)

for (x, y, w, h) in face_detections:
    name = "Unknown"
    for key in faces.keys():
        result = face_recognition.compare_faces([faces[key]], unknown_encoding)[0]
        if result:
            name = key
            print(key)
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.rectangle(img, (x, y - 40), (x + w, y), (255, 0, 0), -1)
    cv2.putText(img, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255, 255, 255), 2)
    #cv2.imwrite("face_recog1.jpg", img)
cv2.imshow('Face Recognizer', img)
cv2.waitKey(0)