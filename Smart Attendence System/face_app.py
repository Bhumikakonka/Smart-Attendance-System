import face_recognition
import cv2
import numpy as np
import os
import xlwt
from xlwt import Workbook
from datetime import date
import xlrd, xlwt
from xlutils.copy import copy as xl_copy

# -------------------------------------------------------
# Windows-compatible version (no RPi.GPIO / LCD / Buzzer)
# -------------------------------------------------------

CurrentFolder = os.getcwd()

# -------------------------------------------------------
# ADD YOUR STUDENTS HERE
# Each student needs a photo (.png) in the same folder
# -------------------------------------------------------
person1_name = "bhumika"
person1_image = face_recognition.load_image_file(CurrentFolder + '/bhumika.png')
person1_face_encoding = face_recognition.face_encodings(person1_image)[0]

person2_name = "Sneha"
person2_image = face_recognition.load_image_file(CurrentFolder + '/sneha.png')
person2_face_encoding = face_recognition.face_encodings(person2_image)[0]

person3_name = "Rahul"
person3_image = face_recognition.load_image_file(CurrentFolder + '/rahul.png')
person3_face_encoding = face_recognition.face_encodings(person3_image)[0]

# Add more students by copying the 3 lines above and changing name/image/variable

known_face_encodings = [
    person1_face_encoding,
    person2_face_encoding,
    person3_face_encoding,
]
known_face_names = [
    person1_name,
    person2_name,
    person3_name,
]

# -------------------------------------------------------
# Open webcam
# -------------------------------------------------------
video_capture = cv2.VideoCapture(0)

# -------------------------------------------------------
# Ask for lecture/subject name
# -------------------------------------------------------
inp = input('Please enter current subject / lecture name: ')
print(f"\n[INFO] Lecture: {inp}")
print("[INFO] Camera is running. Press Q to quit and save attendance.\n")

# -------------------------------------------------------
# Open Excel file and create new sheet for this lecture
# -------------------------------------------------------
rb = xlrd.open_workbook('attendence_excel.xls', formatting_info=True)
wb = xl_copy(rb)
sheet1 = wb.add_sheet(inp)
sheet1.write(0, 0, 'Name/Date')
sheet1.write(0, 1, str(date.today()))
row = 1
col = 0

# -------------------------------------------------------
# Face recognition loop
# -------------------------------------------------------
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
already_attendance_taken = ""

while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        rgb_small_frame = np.ascontiguousarray(rgb_small_frame)
        face_encodings_list = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings_list:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            if already_attendance_taken != name and name != "Unknown":
                sheet1.write(row, col, name)
                col += 1
                sheet1.write(row, col, "Present")
                row += 1
                col = 0
                wb.save('attendence_excel.xls')
                already_attendance_taken = name
                print(f"[ATTENDANCE TAKEN] {name} marked Present")
            elif name == "Unknown":
                print("[INFO] Unknown face detected")
            else:
                print(f"[INFO] {name} already marked, waiting for next student")

    process_this_frame = not process_this_frame

    # Draw boxes on screen
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Smart Attendance System - Press Q to quit', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n[INFO] Attendance saved to attendence_excel.xls")
        break

video_capture.release()
cv2.destroyAllWindows()