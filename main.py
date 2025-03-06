import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResults = False
startGame = False
imgAI = cv2.imread('Resources/1.png', cv2.IMREAD_UNCHANGED)
scores = [0, 0]

while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResults is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResults = True
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    playerMove = None
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1  # Rock
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2  # Paper
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3  # Scissors

                    randomNumber = random.randint(1, 3)  # AI's move: 1 (Rock), 2 (Paper), 3 (Scissors)

                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Determine the winner
                    if playerMove is not None:
                        aiWins = (playerMove % 3) + 1 == randomNumber
                        playerWins = (randomNumber % 3) + 1 == playerMove

                        if aiWins:
                            scores[0] += 1  # AI wins
                        elif playerWins:
                            scores[1] += 1  # Player wins

    imgBG[234:654, 795:1195] = imgScaled

    if stateResults:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)

    if key == ord('q'):
        startGame = True
        initialTime = time.time()
        stateResults = False

    if key == 27:  # Press 'Esc' to exit the game
        break

cv2.destroyAllWindows()
cap.release()
