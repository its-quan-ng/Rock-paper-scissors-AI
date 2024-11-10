import cv2
import random
import hand_detection_lib as handlib
import os

detector = handlib.handDetector()
cap = cv2.VideoCapture(0)
desired_width = 890
desired_height = 600
def draw_results(frame, user_draw):
    # Cho phép máy tính sinh ra lựa chọn ngẫu nhiên
    com_draw = random.randint(0,2)

    # vẽ hình, viết chữ theo user_draw
    frame = cv2.putText(frame, 'You', (50,50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0,255,0), 2, cv2.LINE_AA)
    user_img_path = os.path.join("pix", str(user_draw) + ".png")
    print(f"Attempting to load image at: {user_img_path}")
    s_img = cv2.imread(user_img_path)
    if s_img is None:
        print(f"Error: Could not load image at {user_img_path}")
        return
    x_offset = 50
    y_offset = 100
    frame[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1]] = s_img

    # vẽ hình, viết chữ theo com_draw
    frame = cv2.putText(frame, 'Computer', (400,50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)
    com_img_path = os.path.join("pix", str(com_draw) + ".png")
    print(f"Attempting to load image at: {com_img_path}")
    s_img = cv2.imread(com_img_path)
    if s_img is None:
        print(f"Error: Could not load image at {com_img_path}")
        return
    x_offset = 400
    y_offset = 100
    frame[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1]] = s_img

    # Kiểm tra và hiển thị kết quả
    if user_draw == com_draw:
        result = "DRAW!"
    elif (user_draw == 0 and com_draw == 1) or (user_draw == 1 and com_draw == 2) or (user_draw == 2 and com_draw == 0):
        result = "YOU WIN!"
    else:
        result = "YOU LOSE!"

    frame = cv2.putText(frame,  result, (50, 550),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2, cv2.LINE_AA)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (desired_width, desired_height))
    # truyền hình ảnh vào detector
    frame, hand_lms = detector.findHands(frame)
    n_fingers = detector.count_finger(hand_lms)

    # user
    user_draw = -1
    if n_fingers == 0:
        user_draw = 1
    elif n_fingers == 2:
        user_draw = 2
    elif n_fingers == 5:
        user_draw = 0
    elif n_fingers != -1:
        print("Chỉ chấp nhận Kéo búa bao")
    else:
        print("Không có bàn tay trong hình")

    key = cv2.waitKey(1)
    cv2.imshow("Rock-paper-scissors", frame)

    if(key == ord('q')):
        break
    elif key == ord(" "):
        draw_results(frame, user_draw)
        cv2.imshow("Rock-paper-scissors", frame)
        cv2.waitKey()


cap.release()
cv2.destroyAllWindows()

