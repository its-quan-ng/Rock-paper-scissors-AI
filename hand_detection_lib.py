import cv2
import mediapipe as mp

class handDetector():
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img):
        # convert bgr to rgb (do nhận từ camera là bgr)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # để đưa vào mediapipe
        results = self.hands.process(imgRGB)
        hand_lms = []

        if results.multi_hand_landmarks:
            # nếu có tay, vẽ landmarks cho bàn tay (s)
            for handlm in results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handlm, self.mpHands.HAND_CONNECTIONS)

            # trích ra các tọa độ khớp của các ngón tay
            firstHand = results.multi_hand_landmarks[0]
            h,w,_ = img.shape
            for id, lm in enumerate(firstHand.landmark):
                real_x, real_y = int(lm.x * w), int(lm.y * h)
                hand_lms.append([id, real_x, real_y])
        return img, hand_lms

    def count_finger(self, hand_lms):
        finger_start_index = [4,8,12,16,20]
        n_finger=0

        if len(hand_lms)>0:
            # kiểm tra ngón cái
            if hand_lms[finger_start_index[0]][1] < hand_lms[finger_start_index[0]-1][1]:
                n_finger+=1

            # Kiểm tra 4 ngón còn lại
            for idx in range(1,5):
                if hand_lms[finger_start_index[idx]][2] < hand_lms[finger_start_index[idx]-2][2]:
                    n_finger+=1

            return n_finger
        else:
            return -1
