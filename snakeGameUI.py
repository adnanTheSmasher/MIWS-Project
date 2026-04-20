import pygame
import HandTrackingModule as htm
import snakeGameLogic as logic
import threading
import random
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
# Snake Game Class
# ========================================================
CELL_SIZE = 20

class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [(WIDTH//2, HEIGHT//2)]
        self.direction = (CELL_SIZE, 0)
        self.food = self.spawnFood()
        self.score = 0

    def spawnFood(self):
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        return (x, y)
    
    def update_directions(self, gesture_dir):
        # gesture_dir: 1=up,2=right,3=down,4=left
        if gesture_dir == 1 and self.direction != (0, CELL_SIZE):
            self.direction = (0, -CELL_SIZE)
        elif gesture_dir == 2 and self.direction != (-CELL_SIZE, 0):
            self.direction = (CELL_SIZE, 0)
        elif gesture_dir == 3 and self.direction != (0, -CELL_SIZE):
            self.direction = (0, CELL_SIZE)
        elif gesture_dir == 4 and self.direction != (CELL_SIZE, 0):
            self.direction = (-CELL_SIZE, 0)

    def move(self):
        head_x, head_Y = self.snake[0]
        dx, dy = self.direction

        new_head = ((head_x+dx)%WIDTH, (head_Y+dy)%HEIGHT)

        if new_head in self.snake: # apne app k sath takkar hogai to out
            self.reset()        
            return
        
        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.spawnFood()
        else:
            self.snake.pop()
    
    def draw(self, screen):
        for bodyPart in self.snake:
            pygame.draw.rect(screen, WHITE, (*bodyPart, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, (255, 0, 0), (*self.food, CELL_SIZE, CELL_SIZE))

        score_text = font_button.render(f"SCORE: {self.score}", True, WHITE)
        rect = score_text.get_rect(center=(WIDTH//2, 30))
        screen.blit(score_text, rect)
    

# ========================================================
# Snake Game Class - END
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

snakeGame = SnakeGame()
move_delay = 0.12
last_move_time = time.time()
# ========================================================
# PYGAME VARIABLES - END
# ========================================================

def StartCV2():
    global _gesture_thread
    logic.setup()
    _gesture_thread = threading.Thread(target=logic.loopForGesture, daemon=True)
    _gesture_thread.start()

def MainLoop():
    global _running, _directions, _GAME_STATE, _currentQuestion, _score, last_move_time
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
                #print(_directions)
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
        
        elif _GAME_STATE == 'snake':
            if _directions:
                gesture_dir = _directions.get("direction", -1)
                snakeGame.update_directions(gesture_dir)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        print("W pressed...")
                        snakeGame.update_directions(1)
                    if event.key == pygame.K_LEFT:
                        print("A pressed...")
                        snakeGame.update_directions(4)
                    if event.key == pygame.K_DOWN:
                        print("S pressed...")
                        snakeGame.update_directions(3)
                    if event.key == pygame.K_RIGHT:
                        print("D pressed...")
                        snakeGame.update_directions(2)

            currentTime = time.time()
            if currentTime - last_move_time > move_delay:
                snakeGame.move()
                last_move_time = currentTime

            snakeGame.draw(screen)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    logic.stop()


if __name__ == "__main__":
    StartCV2()
    MainLoop()