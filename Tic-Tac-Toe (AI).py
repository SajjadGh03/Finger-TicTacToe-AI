import cv2
import mediapipe as mp
import time
import random


WIDTH, HEIGHT = 640, 480
GRID_SIZE = 3
cell_w = WIDTH // GRID_SIZE
cell_h = HEIGHT // GRID_SIZE
HOLD_TIME = 2.5


board = [["" for _ in range(3)] for _ in range(3)]

game_over = False

PLAYER = "X"
AI = "O"

# Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
# Camera Set.
cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)


def draw_grid(img):
    for i in range(1, GRID_SIZE):
        cv2.line(img, (0, i * cell_h), (WIDTH, i * cell_h), (200, 200, 200), 4)
        cv2.line(img, (i * cell_w, 0), (i * cell_w, HEIGHT), (200, 200, 200), 4)

def draw_marks(img):
    for r in range(3):
        for c in range(3):
            if board[r][c]:
                x = c * cell_w + cell_w // 2
                y = r * cell_h + cell_h // 2
                color = (0, 0, 255) if board[r][c] == PLAYER else (255, 0, 0)
                cv2.putText(img, board[r][c], (x - 40, y + 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 2.5, color, 6)

def check_winner(b):

    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != "":
            return b[i][0]

        if b[0][i] == b[1][i] == b[2][i] != "":
            return b[0][i]


    if b[0][0] == b[1][1] == b[2][2] != "":
        return b[0][0]

    if b[0][2] == b[1][1] == b[2][0] != "":
        return b[0][2]

    return None

def empty_cells(b):
    return [(r, c) for r in range(3) for c in range(3) if b[r][c] == ""]

def ai_move():
    # try to win
    for r, c in empty_cells(board):
        board[r][c] = AI
        if check_winner(board) == AI:
            return
        board[r][c] = ""

    # defence
    for r, c in empty_cells(board):
        board[r][c] = PLAYER
        if check_winner(board) == PLAYER:
            board[r][c] = AI
            return
        board[r][c] = ""

    # random move
    r, c = random.choice(empty_cells(board))
    board[r][c] = AI

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    frame[:] = (30, 30, 30)
    draw_grid(frame)
    draw_marks(frame)

    winner = check_winner(board)
    if winner:
        game_over = True
        text = "You Win!" if winner == PLAYER else "AI Wins!"
        cv2.putText(frame, text,
                    (WIDTH // 2 - 170, HEIGHT // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (0, 255, 0), 5)

    if result.multi_hand_landmarks and not game_over:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            tip = hand_landmarks.landmark[8]
            x = int(tip.x * WIDTH)
            y = int(tip.y * HEIGHT)
            cv2.circle(frame, (x, y), 8, (0, 255, 255), -1)

            row, col = y // cell_h, x // cell_w

            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == "":
                if hover_cell != (row, col):
                    hover_cell = (row, col)
                    hover_start_time = time.time()
                else:
                    elapsed = time.time() - hover_start_time
                    angle = min(int((elapsed / HOLD_TIME) * 360), 360)

                    cv2.ellipse(frame, (x, y), (25, 25),
                                0, 0, angle, (0, 255, 255), 4)

                    if elapsed >= HOLD_TIME:
                        board[row][col] = PLAYER
                        hover_cell = None
                        hover_start_time = None

                        if not check_winner(board) and empty_cells(board):
                            ai_move()
            else:
                hover_cell = None
                hover_start_time = None

    cv2.imshow("Finger Tic Tac Toe - Single Player", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
