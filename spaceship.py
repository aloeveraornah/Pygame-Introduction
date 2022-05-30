import pygame
import os
 
width, height = 900, 500
win = pygame.display.set_mode((width, height))  
pygame.display.set_caption("First game!")   

white = (255, 255, 255)
 
fps = 60
spaceship_width, spaceship_height = 55, 40
 
yellow_spaceship_image = pygame.image.load(
    os.path.join("assets", "spaceship_yellow.png"))
yellow_spaceship = pygame.transform.scale(yellow_spaceship_image, (spaceship_width, spaceship_height))
red_spaceship_image = pygame.image.load(
    os.path.join("assets", "spaceship_red.png"))
red_spaceship = pygame.transform.scale(red_spaceship_image, (spaceship_width, spaceship_height))
 
def draw_window(red, yellow):
    win.fill(white)
    win.blit(yellow_spaceship, (yellow.x, yellow.y))
    win.blit(red_spaceship, (red.x, red.y))
    pygame.display.update()
 
def main():
    red = pygame.Rect(700, 300, spaceship_width, spaceship_height)
    yellow = pygame.Rect(100, 300, spaceship_width, spaceship_height)  

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        red.x += 1
        draw_window(red, yellow)    
 
    pygame.quit()   
 
if __name__ == "__main__":
    main()
