import cv2
import face_recognition
 
imgKobe = face_recognition.load_image_file('images\kobe-bryant.jpg')
imgKobe = cv2.cvtColor(imgKobe,cv2.COLOR_BGR2RGB)
imgTest = face_recognition.load_image_file('images\LeBron_James.jpg')
imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)
 
faceLoc = face_recognition.face_locations(imgKobe)[0]
encodeKobe = face_recognition.face_encodings(imgKobe)[0]
cv2.rectangle(imgKobe,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
cv2.imshow("kobe",imgKobe);cv2.waitKey(0)

 
faceLocTest = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
cv2.imshow("lebron",imgTest);cv2.waitKey(0) 

results = face_recognition.compare_faces([encodeKobe],encodeTest)
faceDis = face_recognition.face_distance([encodeKobe],encodeTest)
print(results,faceDis)
cv2.putText(imgTest,f'{results} {round(faceDis[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
 
cv2.imshow('kobe',imgKobe)
cv2.imshow('lebron',imgTest)
cv2.waitKey(0)