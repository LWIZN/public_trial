import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
ret, frame_src = cap.read()
print(ret)
cv2.imshow('picture', frame_src)
cv2.imwrite('./DCIM' + str(0)+'.jpg', frame_src)
cap.release()
cv2.destroyAllWindows()
