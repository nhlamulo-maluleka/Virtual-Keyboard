import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(maxHands=1)

textView = ""
delayCounter = 0

keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '<'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', ',', 'Space']]

def init():
    indent = 140
    props = []

    for index, list in enumerate(keys):
        ypos = index*100 + 370
        inner = []
        for x in range(len(list)):
            xpos = x*100 + indent
            inner.append(((xpos, ypos), (xpos + 90, ypos + 70), (xpos + 30, ypos + 50), keys[index][x]))
        
        props.append(inner)
    
    return props

def draw(img, props):
    for list in props:
        for pt1, pt2, tpos, char in list:
            cv.rectangle(img, pt1, pt2, (123, 97, 121), cv.FILLED)
            cv.rectangle(img, pt1, pt2, (0, 97, 121), 2)
            cv.putText(img, char, tpos if char != "Space" else (tpos[0]-20, tpos[1]-10), cv.FONT_HERSHEY_PLAIN, 3 if char != "Space" else 1.5, (255, 255, 0), 2)

def hoverBtn(img, prop):
    pt1, pt2, tpos, char = prop

    cv.rectangle(img, pt1, pt2, (20, 20, 20), cv.FILLED)
    cv.rectangle(img, pt1, pt2, (255, 0, 0), 2)
    cv.putText(img, char, tpos if char != "Space" else (tpos[0]-20, tpos[1]-10), cv.FONT_HERSHEY_PLAIN, 3 if char != "Space" else 1.5, (255, 255, 255), 2)    

def checkPoints(buttonList, hand1, hand2 = None):
    btn = None

    for vect in buttonList:
        for button in vect:
            start, end = button[0], button[1]
            if hand2 == None:
                if start[0] < hand1[0] < end[0] and start[1] < hand1[1] < end[1]:
                    btn = button
            else:
                 if (start[0] < hand1[0] < end[0] and start[0] < hand2[0] < end[0]) and\
                     (start[1] < hand1[1] < end[1] and start[1] < hand2[1] < end[1]):
                    btn = button

    return btn

# Start the App
props = init()

while True:
    success, frame = cap.read()
    frame = cv.flip(frame, 1)
    hands, img = detector.findHands(frame, flipType=False)    

    draw(img, props)

    if hands:
        hand = hands[0]
        pt1, pt2 = hand["lmList"][4], hand["lmList"][8]
        length, info, img = detector.findDistance(pt1, pt2, img)
        
        # Hovering
        handObj = checkPoints(props, pt2)

        if handObj:
            hoverBtn(img, handObj)

        if length < 45 and delayCounter == 0:
            handObj = checkPoints(props, pt1, pt2)
            if handObj:
                delayCounter = 1
                if handObj[-1] == "Space":
                    textView += " "
                elif handObj[-1] == "<":
                    textView = textView[:-1]
                else:
                    textView += handObj[-1]
        else:
            delayCounter = 0 if delayCounter > 10 else delayCounter + 1
        
    cv.putText(img, textView, (200, 100), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    cv.imshow("Preview", img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break
