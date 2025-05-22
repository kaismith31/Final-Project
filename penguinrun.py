import pygame
import sys
import os
import random

# Variables
width, height = 1000, 500
game_speed = 15
death_count = 0 
points = 0


pygame.init()
window = pygame.display.set_mode((width, height))
font = pygame.font.SysFont('Arial', 36)

SMALL_SPIKE = [
    pygame.transform.scale(pygame.image.load(os.path.join('Final Project', 'sprite', "small_rock1.png")), (75, 75))
    for i in range(3)
]

LARGE_SPIKE = [
    pygame.transform.scale(pygame.image.load(os.path.join('Final Project', 'sprite', "large_rock1.png")), (100, 100))
    for i in range(3)
]

# Classes
class Penguin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [
            pygame.transform.scale(pygame.image.load(os.path.join('Final Project', 'sprite', 'cute_penguin_run(1).png')), (90, 90)),
            pygame.transform.scale(pygame.image.load(os.path.join('Final Project', 'sprite', 'cute_penguin_run(2).png')), (90, 90))
        ]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.inflate_ip(-15, -15)
        self.animation_counter = 0
        self.onground = True
        self.jumping = False
        self.jump_velocity = 0
        self.max_jump_velocity = 10
        self.gravity = 1.2
        self.falling = False

    def jump(self):
        if self.onground:
            self.jumping = True
            self.onground = False
            self.jump_velocity = self.max_jump_velocity  

    def fall(self):
        self.jumping = False
        self.falling = True

    def stop_falling(self):
        self.falling = False
        self.onground = True
        self.jump_velocity = 0  

    def update(self):
        self.animation_counter += 1
        if self.animation_counter >= 15:
            self.animation_counter = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        if self.jumping:
            self.rect.y -= self.jump_velocity
            self.jump_velocity -= 0.5 
            if self.jump_velocity <= 0:
                self.fall()
        elif self.falling:
            self.rect.y += self.gravity * 3  
            if self.rect.y >= 250:  
                self.stop_falling()

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = width
        self.rect.inflate_ip(-10, -10)

    def update(self, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)  
            
    def draw(self, window):
        window.blit(self.image[self.type], self.rect)

class SmallSpike(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class LargeSpike(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 275

#main function
def main():
    run = True
    global game_speed, death_count
    clock = pygame.time.Clock()
    obstacles = []
    points = 0

    penguin = Penguin(100, 250)
    all_sprites = pygame.sprite.Group(penguin)

    while run:
        window.fill((192, 192, 192))
        pygame.draw.rect(window, (239, 239, 239), pygame.Rect(0, 350, 1000, 350))
        all_sprites.update()
        all_sprites.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                penguin.jump()

        if not obstacles:
            obstacles.append(SmallSpike(SMALL_SPIKE) if random.randint(0, 2) == 0 else LargeSpike(LARGE_SPIKE))

        for obstacle in obstacles[:]:  
            obstacle.draw(window)
            obstacle.update(obstacles)
            if obstacle.rect.colliderect(penguin.rect):
                death_count += 1
                menu(death_count)


        pygame.display.flip()
        clock.tick(60)

def menu(death_count):
    run = True
    while run:
        window.fill((192, 192, 192))
        font = pygame.font.Font(None, 36)
        
        if death_count == 0:
            text = font.render("Welcome to Penguin Run!: Press SPACE to Start/Jump", True, (0, 0, 0))
           
        else:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score_text = font.render(f"Your deaths: {death_count}", True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(width // 2, height // 2 + 50))
            window.blit(score_text, score_rect)
           

        text_rect = text.get_rect(center=(width // 2, height // 2))
        window.blit(text, text_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                
                    main()

if __name__ == "__main__":
    menu(death_count)
