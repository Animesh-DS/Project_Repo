import cv2

print("Attempting to connect to camera...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
print(f"Hardware connection successful: {cap.isOpened()}")

if cap.isOpened():
    ret, frame = cap.read()
    print(f"Image captured successfully: {ret}")
    cap.release()