
import cv2
from handTracker import HandTracker

# Webcam Setup

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    cap.release()
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    raise SystemExit

tracker = HandTracker()

# Drawing Settings

drawColor = (255, 0, 255)  # Purple
headerHeight = 70
brushThickness = 8

xp, yp = 0, 0
canvas = None

# Toolbar width boundaries
toolbar_widths = [100, 200, 300, 400, 500]

try:
    while True:
        success, img = cap.read()

        if not success:
            print("Failed to read webcam frame.")
            break

        img = cv2.flip(img, 1)
        h, w = img.shape[:2]

        # Create persistent canvas
        if canvas is None:
            canvas = img.copy()
            canvas[:] = 0

    
        # Draw Toolbar
        
        toolbar_items = [
            (0, 100, (0, 0, 255), "RED"),
            (100, 200, (0, 255, 0), "GREEN"),
            (200, 300, (255, 0, 0), "BLUE"),
            (300, 400, (0, 255, 255), "YELLOW"),
            (400, 500, (0, 0, 0), "BLACK"),
            (500, w, (200, 200, 200), "CLEAR"),
        ]

        for x1, x2, color, label in toolbar_items:
            x2 = min(x2, w)

            cv2.rectangle(
                img, (x1, 0), (x2, headerHeight),
                color, cv2.FILLED
            )

            text_color = (
                (0, 0, 0)
                if label in ("YELLOW", "CLEAR")
                else (255, 255, 255)
            )

            cv2.putText(
                img, label, (x1 + 8, 43),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55, text_color, 2
            )

        
        # Hand Detection
        
        hands, img = tracker.findHands(img)

        if hands:
            hand = hands[0]
            lmList = hand["lmList"]

            # Index fingertip
            x, y, z = lmList[8]

            fingers = tracker.detector.fingersUp(hand)

            # Selection mode: index + middle fingers
            if fingers[1] == 1 and fingers[2] == 1:
                xp, yp = 0, 0

                if y < headerHeight:
                    if x < 100:
                        drawColor = (0, 0, 255)       # Red
                    elif x < 200:
                        drawColor = (0, 255, 0)       # Green
                    elif x < 300:
                        drawColor = (255, 0, 0)       # Blue
                    elif x < 400:
                        drawColor = (0, 255, 255)     # Yellow
                    elif x < 500:
                        drawColor = (0, 0, 0)         # Black ink
                    else:
                        canvas[:] = 0                 # Clear canvas

                cv2.circle(
                    img, (x, y), 10,
                    drawColor, cv2.FILLED
                )

            # Drawing mode: index finger up, middle finger down
            elif fingers[1] == 1 and fingers[2] == 0:
                if y > headerHeight:
                    if xp == 0 and yp == 0:
                        xp, yp = x, y

                    # Continuous, anti-aliased stroke
                    cv2.line(
                        canvas,
                        (xp, yp),
                        (x, y),
                        drawColor,
                        brushThickness,
                        cv2.LINE_AA
                    )

                    # Smooth stroke ends
                    cv2.circle(
                        canvas,
                        (x, y),
                        brushThickness // 2,
                        drawColor,
                        cv2.FILLED,
                        cv2.LINE_AA
                    )

                    xp, yp = x, y
                else:
                    xp, yp = 0, 0

            else:
                xp, yp = 0, 0

        else:
            xp, yp = 0, 0

        
        # Combine Canvas and Webcam
        
        img = cv2.add(img, canvas)

        cv2.imshow("Air Painting - Smart Screen", img)

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
