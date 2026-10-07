import cv2
import mediapipe as mp
import random

# Create the MediaPipe Hand Landmarker
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="models/hand_landmarker.task"
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

landmarker = HandLandmarker.create_from_options(options)

# Falling ball
ball_x = 300
ball_y = 50
ball_radius = 20
ball_speed = 8

# Game variables
score = 0
lives = 3
game_over = False

# Paddle
paddle_width = 120
paddle_height = 30
paddle_x = 300
paddle_y = 0

# Open webcam
cap = cv2.VideoCapture(0)

# Reduce camera resolution for better performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

timestamp_ms = 0

while True:
    success, frame = cap.read()

    if not success:
        break

    # Mirror the camera image
    frame = cv2.flip(frame, 1)

    height, width, _ = frame.shape
    paddle_y = height - 60

    # Convert OpenCV BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to MediaPipe image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp_ms += 33
    result = landmarker.detect_for_video(mp_image, timestamp_ms)

    # -------------------------
    # AI HAND CONTROL
    # -------------------------
    if result.hand_landmarks:

        hand_landmarks = result.hand_landmarks[0]

        # Index fingertip
        index_tip = hand_landmarks[8]

        index_x = int(index_tip.x * width)
        index_y = int(index_tip.y * height)

        # Paddle follows index finger
        paddle_x = index_x - paddle_width // 2

        # Keep paddle inside the window
        paddle_x = max(0, min(paddle_x, width - paddle_width))

        # Draw hand landmarks
        for landmark in hand_landmarks:
            x = int(landmark.x * width)
            y = int(landmark.y * height)

            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )

        # Highlight index fingertip
        cv2.circle(
            frame,
            (index_x, index_y),
            12,
            (0, 0, 255),
            -1
        )

    # -------------------------
    # GAME
    # -------------------------

    # Draw paddle
    cv2.rectangle(
        frame,
        (paddle_x, paddle_y),
        (paddle_x + paddle_width,
         paddle_y + paddle_height),
        (255, 0, 0),
        -1
    )

    # Only run the game while it is not over
    if not game_over:

        # Move ball
        ball_y += ball_speed

        # Check for catch
        if (
            paddle_x <= ball_x <= paddle_x + paddle_width
            and paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height
        ):
            score += 1

            ball_y = ball_radius
            ball_x = random.randint(
                ball_radius,
                width - ball_radius
            )

        # Ball missed
        if ball_y - ball_radius > height:
            lives -= 1

            if lives <= 0:
                lives = 0
                game_over = True
            else:
                ball_y = ball_radius
                ball_x = random.randint(
                    ball_radius,
                    width - ball_radius
                )

        # Draw ball
        cv2.circle(
            frame,
            (ball_x, ball_y),
            ball_radius,
            (0, 255, 255),
            -1
        )

    # Display score
    cv2.putText(
        frame,
        f"Score: {score}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    # Display lives
    cv2.putText(
        frame,
        f"Lives: {lives}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    # -------------------------
    # GAME OVER
    # -------------------------
    if game_over:

        cv2.putText(
            frame,
            "GAME OVER",
            (width // 2 - 150, height // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 0, 255),
            4
        )

        cv2.putText(
            frame,
            "Press R to Restart",
            (width // 2 - 160, height // 2 + 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

    cv2.imshow("AI Hand Game", frame)

    # Read keyboard
    key = cv2.waitKey(1) & 0xFF

    # Press Q to quit
    if key == ord("q"):
        break

    # Press R to restart after Game Over
    if game_over and key == ord("r"):
        score = 0
        lives = 3
        game_over = False

        ball_y = ball_radius
        ball_x = random.randint(
            ball_radius,
            width - ball_radius
        )

cap.release()
landmarker.close()
cv2.destroyAllWindows()