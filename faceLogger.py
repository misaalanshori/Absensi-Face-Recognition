import face_recognition
import cv2
import numpy as np
import os
import glob
import pickle
import datetime

#Based on facerec_from_webcam_faster.py
#Reads file from userData folder

video_capture = cv2.VideoCapture(0)

known_face_encodings = []
known_face_names = []

print("Loading user data...")
userDataPath = os.path.join(os.getcwd(), 'userData') # Sets location for userData
for filename in glob.glob(os.path.join(userDataPath, '*.userData')): # Loads *.userData files
    with open(filename, "rb") as fp: # Unpickling and appending to Known Lists
        temp = pickle.load(fp)
        known_face_names.append(temp[0])
        known_face_encodings.append(temp[1])
        print("Loaded data for " + "\"{}\"".format(temp[0]))
print("\nLoaded {} total user".format(len(known_face_names)))




# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

tempDict = {}

userList = known_face_names

for i in userList: # Temporary Dictionary for storing user visibility during 1 minute
    tempDict[i] = []
tempDict["control"] = 0

minuteFrame = {}

for i in userList: # Creates a Dictionary for storing user data for that 1 minute
    minuteFrame[i] = []

dataFrames = []

pastSecond = 0 # Storing the second during the last loop


now = datetime.datetime.now() # Store date and time when script was started
startingDateTime = now.strftime("%Y-%m-%d %H:%M:%S")

print("Script started at {}\nQuit by pressing \"q\" on the preview window".format(startingDateTime))

while True:
    now = datetime.datetime.now()
    currentSecond = int(now.strftime("%S")) # Get current second in time
    currentMinute = int(now.strftime("%M"))
    datentime = now.strftime("%Y-%m-%d %H:%M:%S")
    # print(str(pastSecond) + "  " + str(currentSecond))
    # Grab a single frame of video
    ret, frame = video_capture.read()

    small_frame = frame
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name)

    for q in face_names:
        if q in userList:
            tempDict[q].append(1)
            # print(q + "  True")
    tempDict["control"] += 1
    
    if pastSecond > currentSecond:
        if pastSecond != currentSecond:
            for i in userList: # Converts the tempDict 
                value = sum(tempDict[i])/tempDict["control"]
                boolVal = False
                if value >= 0.3:
                    boolVal = True
                minuteFrame[i] = [boolVal, value]
            minuteFrame["frame"] = frame
            minuteFrame["datetime"] = datentime
            for key in minuteFrame:
                if key != "frame":
                    print("\n\n" + key)
                    print(minuteFrame[key])
            print("=============================")
            dataFrames.append(minuteFrame)

            if currentMinute % 2 == 0:
                filename = "Session - " + startingDateTime + ".session"
                with open(os.path.join("sessions", filename), "wb") as fp:
                    pickle.dump(dataFrames, fp)


            minuteFrame = {}
            for i in userList: # Resets the tempDict
                tempDict[i] = []
            tempDict["control"] = 0

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        # top *= 4
        # right *= 4
        # bottom *= 4
        # left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    pastSecond = currentSecond
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
filename = "Session - " + startingDateTime + ".session"
with open(os.path.join("sessions", filename), "wb") as fp:
    pickle.dump(dataFrames, fp)