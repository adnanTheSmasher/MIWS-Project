import pygame
import HandTrackingModule as htm
import quizGameLogic as logic
import threading
import time
import sys

pygame.init()

# ========================================================
# GLOBAL VARIABLE
# ========================================================

_running = True
_gesture = None
_gesture_thread = None


# ========================================================
# GLOBAL VARIABLE - END
# ========================================================

# ========================================================
# GAME STATES
# ========================================================
_GAME_STATE = 'menu'
_currentQuestion = 0
_score = 0
_totalQuestions = 0
# ========================================================
# GAME STATES - END
# ========================================================



# ========================================================
# BUTTONS
# ========================================================

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, hover=False):
        mousePos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mousePos) or hover:
            color = HOVER_BUTTON_COLOR
        else:
            color = BUTTON_COLOR
        
        pygame.draw.rect(screen, color, self.rect)

        text_surface = font_button.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False

font_button = pygame.font.SysFont("Arial", 30)

# Buttons
start_btn = Button(540, 350, 200, 60, "Start")
quit_btn = Button(540, 450, 200, 60, "Quit")
play_again_btn = Button(540, 450, 200, 60, "Play Again")
quit_result_btn = Button(540, 550, 200, 60, 'Quit')

# ========================================================
# BUTTONS - END
# ========================================================


# ========================================================
# PYGAME VARIABLES
# ========================================================

# 🎨 Colors (edit later for styling)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 255)
HOVER_BUTTON_COLOR = (0, 200, 255) 
GREEN = (0, 0, 255), 

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Game")

font_title = pygame.font.SysFont("Arial", 60)

# ========================================================
# PYGAME VARIABLES - END
# ========================================================


# ========================================================
# QUIZ QUESTIONS
# ========================================================
# QUESTIONS = [
#     {"category": "Artificial Intelligence", "question": "Which algorithm is inspired by the human brain?",           "options": ["Decision Tree", "Neural Network", "Linear Regression", "K-Means"],                                                        "answer": 1},
#     {"category": "Artificial Intelligence", "question": "Which search uses a heuristic to find the shortest path?", "options": ["BFS", "DFS", "A* Search", "Greedy Search"],                                                                               "answer": 2},
#     {"category": "Artificial Intelligence", "question": "What does 'ML' stand for?",                                "options": ["Machine Logic", "Meta Learning", "Machine Learning", "Model Language"],                                                    "answer": 2},
#     {"category": "Artificial Intelligence", "question": "MediaPipe detects how many hand landmarks?",               "options": ["10", "15", "21", "33"],                                                                                                    "answer": 2},
#     {"category": "Computer Science",        "question": "Which data structure uses LIFO order?",                    "options": ["Queue", "Array", "Stack", "Linked List"],                                                                                  "answer": 2},
#     {"category": "Computer Science",        "question": "What is the time complexity of Binary Search?",            "options": ["O(n)", "O(n^2)", "O(log n)", "O(1)"],                                                                                     "answer": 2},
#     {"category": "Computer Science",        "question": "What does HTTP stand for?",                                "options": ["HyperText Transfer Protocol", "High Tech Transfer Process", "Host Transfer Text Protocol", "HyperText Transmission Path"], "answer": 0},
#     {"category": "Computer Science",        "question": "Which language is used for web styling?",                  "options": ["JavaScript", "Python", "HTML", "CSS"],                                                                                    "answer": 3},
#     {"category": "Python",                  "question": "What keyword defines a function in Python?",               "options": ["func", "define", "def", "function"],                                                                                       "answer": 2},
#     {"category": "Python",                  "question": "Which library is used for computer vision in Python?",     "options": ["NumPy", "Pandas", "OpenCV", "Matplotlib"],                                                                                "answer": 2},
#     {"category": "Python",                  "question": "What does len() return?",                                  "options": ["Last element", "List type", "Length of object", "Logic value"],                                                           "answer": 2},
#     {"category": "General Knowledge",       "question": "Which planet is called the Red Planet?",                  "options": ["Venus", "Jupiter", "Mars", "Saturn"],                                                                                      "answer": 2},
#     {"category": "General Knowledge",       "question": "What is the chemical symbol for Gold?",                   "options": ["Go", "Gd", "Au", "Ag"],                                                                                                    "answer": 2},
#     {"category": "General Knowledge",       "question": "How many continents are on Earth?",                       "options": ["5", "6", "7", "8"],                                                                                                        "answer": 2},
#     {"category": "General Knowledge",       "question": "What is the largest ocean on Earth?",                     "options": ["Atlantic", "Indian", "Arctic", "Pacific"],                                                                                "answer": 3},
#     {"category": "General Knowledge",       "question": "What is the approximate speed of light?",                 "options": ["300 km/s", "3,000 km/s", "300,000 km/s", "30,000 km/s"],                                                                  "answer": 2},
# ]
QUESTIONS = [
    {"category": "Artificial Intelligence", "question": "Which algorithm is inspired by the human brain?",           "options": ["Decision Tree", "Neural Network", "Linear Regression", "K-Means"],                                                        "answer": 1},
    {"category": "Artificial Intelligence", "question": "Which search uses a heuristic to find the shortest path?", "options": ["BFS", "DFS", "A* Search", "Greedy Search"],                                                                               "answer": 2},
]
# ========================================================
# QUIZ QUESTIONS - END
# ========================================================





# ========================================================
# Start CV2
# ========================================================
def StartCV2():
    global _gesture_thread
    logic.setup()
    _gesture_thread = threading.Thread(target=logic.loopForGesture, daemon=True)
    _gesture_thread.start()
# ========================================================
# Start CV2 - END
# ========================================================


# ========================================================
# MAIN LOOP
# ========================================================

def MainLoop():
    global _running, _gesture, _GAME_STATE, _currentQuestion, _score, _totalQuestions

    clock = pygame.time.Clock()

    while _running:
        screen.fill(BLACK)
        gesture = logic.getGesture()

        # =================== MENU =================== 
        if _GAME_STATE == 'menu':
            # Title
            title_text = font_title.render("Are You Ready", True, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH // 2, 200))
            screen.blit(title_text, title_rect)
            # Draw buttons
            # start_btn.draw(screen)
            # quit_btn.draw(screen)
            
            if gesture:
                print(gesture)
                right = gesture.get("fingers_right", -1)
                progress = gesture.get("progress", 0)
                hover_start = False
                hover_quit = False

                if progress >= 30:
                    if right == 1:
                        _GAME_STATE = "quiz"
                        _currentQuestion = 0
                        _score = 0
                        _totalQuestions = len(QUESTIONS)

                    elif right == 2:
                        _running = False
                    logic.resetProgress()

                if right == 1:
                    hover_start = True
                elif right == 2:
                    hover_quit = True
                start_btn.draw(screen, hover_start)
                quit_btn.draw(screen, hover_quit)

    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _running = False



                if start_btn.is_clicked(event):
                    print("Start Game")
                    _GAME_STATE = "quiz"
                    _currentQuestion = 0
                    _score = 0
                    _totalQuestions = len(QUESTIONS)

                if quit_btn.is_clicked(event):
                    _running = False
                    #logic.stop()

        elif _GAME_STATE == 'quiz':
            q = QUESTIONS[_currentQuestion]

            #Questions
            questionText = font_button.render(q['question'], True, WHITE)
            screen.blit(questionText, (100, 100))

            optionButtons = []

            for i, option in enumerate(q["options"]):
                btn = Button(200, 250 + i*80, 800, 60, option)
                btn.draw(screen=screen)
                optionButtons.append(btn)
                hoverIndex = -1
            
            hover_index = -1

            if gesture:
                right = gesture.get("fingers_right", -1)
                progress = gesture.get('progress', 0)
                hover_index = right - 1

            optionButtons = []

            for i, option in enumerate(q["options"]):
                btn = Button(200, 250 + i*80, 800, 60, option)

                is_hover = (i == hover_index)

                btn.draw(screen, is_hover)
                optionButtons.append(btn)

                

                if progress >= 30:
                    selected = right - 1

                    if 0 <= selected < 4:
                        if selected == q["answer"]:
                            _score += 1

                        _currentQuestion += 1

                        if _currentQuestion >= len(QUESTIONS):
                            _GAME_STATE = "results"
                    logic.resetProgress() 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _running = False
                
                for i, btn in enumerate(optionButtons):
                    if btn.is_clicked(event):
                        if i == q["answer"]:
                            _score += 1
                        _currentQuestion+=1
                if _currentQuestion >= len(QUESTIONS):
                    _GAME_STATE = "results"
        
        elif _GAME_STATE == "results":
            title_text = font_title.render("QUIZ FINISHED", True, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH//2, 150))
            screen.blit(title_text, title_rect)

            #score Display
            score_text = font_title.render(f"Score: {_score} / {_totalQuestions}", True, GREEN)
            score_rect = score_text.get_rect(center=(WIDTH//2, 250))
            screen.blit(score_text, score_rect)

            
            # Draw Button 
            play_again_btn.draw(screen=screen)
            quit_result_btn.draw(screen)

            # Gesture part dalna hai
            if gesture:
                right = gesture.get("fingers_right", -1)
                progress = gesture.get("progress", 0)

                if progress >= 30:
                    if right == 1:
                        _GAME_STATE = "quiz"
                        _currentQuestion = 0
                        _score = 0
                    elif right == 2:
                        _running = False
                    logic.resetProgress()

            # mouse Part
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _running = False
                if play_again_btn.is_clicked(event=event):
                    print("Play Again...")
                    _GAME_STATE = "quiz"
                    _currentQuestion = 0
                    _score = 0
                
                if quit_result_btn.is_clicked(event):
                    _running = False

        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    logic.stop()

# ========================================================
# MAIN LOOP - END
# ========================================================


if __name__ == "__main__":
    try:
        if not pygame.get_init():
            pygame.init()


        StartCV2()
        time.sleep(0.5)
        MainLoop()

    except Exception as e:
        print("Exception: ", e)
    finally:
        logic.stop()
        pygame.quit()