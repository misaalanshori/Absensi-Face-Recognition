import face_recognition
import cv2
import numpy as np
import datetime
import os
import pickle

try:
    while True:
        print("Input data face recognition")
        name = input("Nama: ")
        print("Pengambilan gambar, tekan \"y\" untuk mengambil foto")


        cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
        while(True):
            ret,frame = cap.read() # return a single frame in variable `frame`
            cv2.imshow('img1',frame) #display the captured image
            if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
                cv2.imwrite('temp.jpg',frame)
                try:
                    temp_image = face_recognition.load_image_file("temp.jpg")
                    temp_face_encoding = face_recognition.face_encodings(temp_image)[0]
                except IndexError:
                    os.remove("temp.jpg")
                    cv2.destroyAllWindows()
                    print("Wajah tidak terdeteksi, Silahkan ulangi\n\n\n")
                    break
                tempArray = [name, temp_face_encoding]

                now = datetime.datetime.now()

                with open("userData/" + name + now.strftime("%Y-%m-%d %H:%M:%S") + ".userData", "wb") as fp:
                    pickle.dump(tempArray, fp)

                os.remove("temp.jpg")

                cv2.destroyAllWindows()
                print("Input Data Selesai!\n\n\n")
                break

        cap.release()
except KeyboardInterrupt:
    print("\nQuitting...")
    quit()