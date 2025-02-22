import pygame
import sys
import math
import json 
import os 
pygame.init()
WIDTH,HEIGHT=800,600
BG_color=(0,0,0)
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Brick breaker game ")
# Color name with color code for easy reference
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
# Game configuration all the parameters are here 
class GameConfig:
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    PADDLE_WIDTH = 100
    PADDLE_HEIGHT = 20
    BALL_RADIUS = 20
    BRICK_WIDTH = 80
    BRICK_HEIGHT = 30
    BRICK_PADDING = 10
    BALL_SPEED = 5
    POINTS_PER_BRICK=10
# Paddle class for the player control
class Paddle:
    def __init__(self):
        self.height=GameConfig.PADDLE_HEIGHT
        self.width=GameConfig.PADDLE_WIDTH
        self.x=GameConfig.WIDTH//2 - GameConfig.PADDLE_WIDTH//2
        self.y=GameConfig.HEIGHT-40

        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)

    def update(self):
        #move paddle with the mouse
        mouse_x, _ = pygame.mouse.get_pos()  
        self.x=mouse_x-self.width//2
        self.x = max(0, min(self.x, WIDTH - self.width))
        self.rect.x=self.x
        
    def draw(self,screen):
        # draw paddle on the screen
        pygame.draw.rect(screen, Colors.WHITE, self.rect)

# Ball class for the movements and collision
class Ball:
    def __init__(self):
        self.radius=GameConfig.BALL_RADIUS
        self.x=GameConfig.WIDTH//2 
        self.y=GameConfig.HEIGHT-60
        self.speed_x=GameConfig.BALL_SPEED
        self.speed_y=-GameConfig.BALL_SPEED
        self.last_collison_time=0
        self.rect=pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)

    def reset_position(self):
        #Reset ball position after losing life
        self.x=GameConfig.WIDTH//2
        self.y=GameConfig.HEIGHT-60
        self.speed_x=GameConfig.BALL_SPEED
        self.speed_y=-GameConfig.BALL_SPEED
        self.rect=pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)

    def move(self):
        # move the ball and handle screen collision 
        self.x+=self.speed_x
        self.y+=self.speed_y

        if self.x<=self.radius or self.x>=GameConfig.WIDTH-self.radius:
            self.speed_x*=-1
        if self.y<=self.radius:
            self.speed_y*=-1
        self.rect.center=(self.x,self.y)

        
    def paddle_handle_collision(self,paddle):
        # handle collision with the paddle with angles based collision
        if self.rect.colliderect(paddle.rect):
            relative_intersect_x = (paddle.rect.x + paddle.rect.width/2) - self.x
            normalized_relative_intersect_x = relative_intersect_x / (paddle.rect.width/2)
            bounce_angle = normalized_relative_intersect_x * (math.pi/3)  # Up to 60 degrees
            self.speed_x = -5 * math.sin(bounce_angle)
            self.speed_y = -abs(-GameConfig.BALL_SPEED * math.cos(bounce_angle))
            self.y=paddle.rect.top-self.radius
    
    def draw(self,screen):
        # draw the ball on the screen
        pygame.draw.circle(screen, Colors.RED, (int(self.x), int(self.y)), self.radius)

#Brick class 
class Brick:
    def __init__(self,x,y ):
        self.rect = pygame.Rect(x, y, GameConfig.BRICK_WIDTH, GameConfig.BRICK_HEIGHT)

    
    def draw(self,screen):
        pygame.draw.rect(screen, Colors.RED, self.rect)

# Main game code
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameConfig.WIDTH, GameConfig.HEIGHT))
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.load_high_score()
        self.reset_game()
    def load_high_score(self):
        # Load high score 
        try:
            if os.path.exists("highscore.json"):
                with open("highscore.json", "r") as file:
                    data=json.load(file)
                    self.high_score=data.get("high_score",0)
            else:
                self.high_score=0
        except:
            self.high_score=0
    def save_high_score(self):
        # save high score in json file 
        with open("highscore.json", "w") as file:
            json.dump({'high_score': self.high_score},file)

    def reset_game(self):
        # Reset game state
        self.level = 1
        self.score=0
        self.lives=3
        self.paddle = Paddle()
        self.ball = Ball()
        self.create_brick()

    def handle_brick_collision(self):
        # Handle brick collision with the ball and update the score and lives
        for brick in self.bricks[:]:
            if self.ball.rect.colliderect(brick.rect):
                self.bricks.remove(brick)
                self.score+=GameConfig.POINTS_PER_BRICK * self.level
                if self.score>self.high_score:
                    self.high_score=self.score
                    self.save_high_score()

                overlap_x = min(self.ball.rect.right, brick.rect.right) - max(self.ball.rect.left, brick.rect.left)
                overlap_y = min(self.ball.rect.bottom, brick.rect.bottom) - max(self.ball.rect.top, brick.rect.top)
                
                if overlap_x > overlap_y:
                    self.ball.speed_y *= -1
                else:
                    self.ball.speed_x *= -1
                return True
        return False

    def create_brick(self,rows=5,coloumns=10):
        # Creating bricks 
        rows = min(5 + self.level - 1, 10)
        columns = 10
        start_x = (GameConfig.WIDTH - (columns * (GameConfig.BRICK_WIDTH + GameConfig.BRICK_PADDING))) // 2
        start_y = 50
        
        self.bricks = []
        for row in range(rows):
            for col in range(columns):
                x = start_x + col * (GameConfig.BRICK_WIDTH + GameConfig.BRICK_PADDING)
                y = start_y + row * (GameConfig.BRICK_HEIGHT + GameConfig.BRICK_PADDING)
                self.bricks.append(Brick(x, y))


    def show_message(self,message):
        # display message on the screen 
        screen.fill(BG_color)
        text = self.font.render(message, True, Colors.WHITE)
        screen.blit(text, (GameConfig.WIDTH // 2 - 100, GameConfig.HEIGHT // 2))
        score_text = self.font.render(f"Score: {self.score}", True, Colors.WHITE)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, Colors.WHITE)
        screen.blit(score_text, (GameConfig.WIDTH // 2 - 100, GameConfig.HEIGHT // 2 + 40))
        screen.blit(high_score_text, (GameConfig.WIDTH // 2 - 100, GameConfig.HEIGHT // 2 + 80))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False  # Start game


  # Restart game
    def run(self):
        while True:
            self.show_message("Press SPACE to Start")
            self.reset_game()

            running = True
            
            while running:
                    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.save_high_score()
                        pygame.quit()
                        sys.exit()
                self.paddle.update()
                self.ball.move()
                self.ball.paddle_handle_collision(self.paddle)
                self.handle_brick_collision()
                # Ball and paddle collision
                # Drawing
                self.screen.fill(Colors.BLACK)
                self.paddle.draw(self.screen)
                self.ball.draw(self.screen)
                for brick in self.bricks:
                    brick.draw(self.screen)
                
                level_text = self.font.render(f"Level: {self.level}", True, Colors.WHITE)
                score_text = self.font.render(f"Score: {self.score}", True, Colors.WHITE)
                lives_text = self.font.render(f"Lives: {self.lives}", True, Colors.WHITE)
                high_score_text = self.font.render(f"High Score: {self.high_score}", True, Colors.WHITE)
                
                self.screen.blit(level_text, (10, 10))
                self.screen.blit(score_text, (10, 40))
                self.screen.blit(lives_text, (10, 70))
                self.screen.blit(high_score_text, (GameConfig.WIDTH - 200, 10))

                if self.ball.y > GameConfig.HEIGHT:
                    self.lives -= 1
                    if self.lives>0:
                        self.ball.reset_position()
                    else:
                        self.show_message("Game Over")
                        running=False
                # Check win/lose conditions
                if len(self.bricks) == 0:
                    if self.level <=3  :
                        self.level += 1
                        self.ball.reset_position()
                        self.show_message(f"Level {self.level}! Press SPACE to continue")
                        break
                    else:
                        self.show_message("Congratulations! You've completed all levels! Press R to play again")
                        self.level = 1  # Reset to level 1
                        running = False

                pygame.display.flip()
                self.clock.tick(GameConfig.FPS)
                    

if __name__=="__main__":
    game=Game()
    game.run()