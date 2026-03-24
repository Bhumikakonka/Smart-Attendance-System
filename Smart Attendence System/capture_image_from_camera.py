import cv2

cam_port = 0
cam = cv2.VideoCapture(cam_port)

inp = input('Enter person name: ')

print("Press SPACE to capture photo, press ESC to quit")

while True:
    result, image = cam.read()
    if result:
        cv2.imshow('Camera - Press SPACE to capture', image)
        key = cv2.waitKey(1)
        if key == 32:  # SPACE key
            filename = inp + ".png"
            cv2.imwrite(filename, image)
            print("Image saved as:", filename)
            break
        elif key == 27:  # ESC key
            print("Cancelled")
            break
    else:
        print("No image detected. Please try again.")
        break

cam.release()
cv2.destroyAllWindows()