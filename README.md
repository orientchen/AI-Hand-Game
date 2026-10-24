# AI Hand Game

A webcam-based interactive game in Python that uses **MediaPipe hand landmark detection** to control a paddle with your index finger. Move your hand horizontally to catch falling balls, earn points, and avoid losing all three lives.

## How it works

1. OpenCV captures frames from your webcam and mirrors them for intuitive hand movement.
2. MediaPipe Hand Landmarker detects up to one hand and estimates its landmarks.
3. The horizontal position of landmark **8** (the index fingertip) controls the paddle.
4. A ball falls down the screen. Catching it with the paddle earns one point and starts another ball at a random horizontal position.
5. Missing a ball costs one life. The game ends when all three lives are lost.

The hand detection uses a **pretrained** MediaPipe model; the game does not train a new AI model.

## Repository files

| File | Purpose |
|---|---|
| `camera_test.py` | Checks that OpenCV can open the webcam and display video. |
| `hand_test.py` | Runs the hand-controlled catching game. |
| `models/hand_landmarker.task` | Pretrained MediaPipe hand landmark model required by the game. |

## Requirements

- Python 3
- A working webcam
- A desktop environment capable of displaying OpenCV windows
- Python packages: `opencv-python`, `mediapipe`

Install dependencies in a terminal:

```bash
python -m pip install opencv-python mediapipe
```

The code uses the MediaPipe Tasks API (`mp.tasks`). Use a MediaPipe version that provides this API.

## Run the game

Clone the repository and enter its directory:

```bash
git clone https://github.com/orientchen/AI-Hand-Game.git
cd AI-Hand-Game
```

First, check the webcam:

```bash
python camera_test.py
```

Press **Q** to close the webcam test. Then launch the game:

```bash
python hand_test.py
```

Run the game **from the repository root**, because it loads the model from the relative path `models/hand_landmarker.task`.

## Controls

| Control | Action |
|---|---|
| Move index finger left or right | Move the paddle horizontally. |
| **Q** | Quit the game. |
| **R** | Restart after the game is over. |

The webcam image is mirrored, so moving your finger to the left or right moves the paddle in the same apparent direction. If the hand is not detected, the paddle remains at its last position.

## Gameplay rules

- Start with **3 lives** and a score of **0**.
- Catch a falling ball with the paddle to gain **1 point**.
- Missing a ball costs **1 life**.
- At **0 lives**, the screen displays **GAME OVER**.
- Press **R** to restart or **Q** to quit.

## Technical details

The program uses MediaPipe Hand Landmarker in `VIDEO` mode, with `num_hands=1`. It converts each OpenCV frame from BGR to RGB before detection. The normalized x-coordinate of the index fingertip is multiplied by the frame width to obtain a pixel position. The paddle's x-coordinate is then adjusted and clamped to remain inside the video window.

The game uses a requested camera resolution of **640 × 480**, a ball radius of **20 pixels**, a falling speed of **8 pixels per frame**, and a paddle size of **120 × 30 pixels**. Actual frame dimensions may depend on the webcam.

## Learning objectives

This project demonstrates:

- Real-time webcam input with OpenCV
- AI-based hand landmark detection using a pretrained model
- Mapping normalized landmark coordinates to image pixels
- Human–computer interaction through hand gestures and movement
- Basic game loops, collision detection, scoring, and state management

## Troubleshooting

- **Webcam does not open:** Close other applications using the camera and verify operating-system camera permissions. Run `camera_test.py` first.
- **Model file not found:** Make sure `models/hand_landmarker.task` exists and run `python hand_test.py` from the repository root.
- **Hand not detected:** Improve lighting and keep your hand visible in the camera frame.
- **OpenCV window does not appear:** Run the program in a local desktop environment with webcam and graphical-window access. A remote/headless environment may not support `cv2.imshow()` or direct webcam access.

## Project status

The repository currently contains a webcam test and a playable single-ball catching game. It does not include a separate training pipeline or automated tests.
