import pygame
import HandTrackingModule as htm
import snakeGameLogic as logic
import threading
import time
import sys

pygame.init()

# ========================================================
# GLOBAL VARIABLE
# ========================================================

_running = True
_directions = None
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

# Colors (edit later for styling)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 255)
HOVER_BUTTON_COLOR = (0, 200, 255) 
GREEN = (0, 0, 255), 

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font_title = pygame.font.SysFont("Arial", 60)

# ========================================================
# PYGAME VARIABLES - END
# ========================================================

def StartCV2():
    global _gesture_thread
    logic.setup()
    _gesture_thread = threading.Thread(target=logic.loopForGesture, daemon=True)
    _gesture_thread.start()

def MainLoop():
    global _running, _directions, _GAME_STATE, _currentQuestion, _score
    clock = pygame.time.Clock()

    while _running:
        screen.fill(BLACK)
        _directions = logic.getDirections()

        if _GAME_STATE == 'menu':
            title_text = font_title.render("Are you Ready", True, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH//2, 200))
            screen.blit(title_text, title_rect)
            hover_start = False
            hover_quit = False
            
            if _directions:
                print(_directions)
                right = _directions.get("fingers_right", -1)
                progress = _directions.get("progress", 0)

                if progress >= 30:
                    if right == 1:
                        print("Start Game")
                        _GAME_STATE = 'snake'
                        _score = 0
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
                    pygame.quit()

                if start_btn.is_clicked(event):
                    print("Start Game")
                    _GAME_STATE = 'snake'
                    _score = 0
                if quit_btn.is_clicked(event):
                    _running = False

        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    logic.stop()


if __name__ == "__main__":
    StartCV2()
    MainLoop()