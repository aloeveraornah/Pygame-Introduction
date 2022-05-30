import pygame
import os
pygame.font.init()
pygame.mixer.init()
 
#dimensions set for the window created
width, height = 1200, 700
window = pygame.display.set_mode((width, height))  
pygame.display.set_caption("Saiyan Showdown")   

#colors and the horizontal line in the middle
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)   
orange = (255, 128, 0)
border = pygame.Rect(0, height/2-2, width, 5)

#this loads the mp3 sound files
explosian = pygame.mixer.Sound(os.path.join("dragonball", 'explosian.mp3'))
gokublast = pygame.mixer.Sound(os.path.join("dragonball", 'gokukiblast.mp3'))
vegetablast = pygame.mixer.Sound(os.path.join("dragonball", 'vegetakiblast.mp3'))

#this loads the font for the player's health bar and for when the player wins or loses
font_health =  pygame.font.SysFont("times", 60)
font_winner = pygame.font.SysFont("times", 80)

#frames per second of the window 
fps = 60
#speed of the ki blasts
kiblast_movement_speed = 10
#max number of ki blasts available to shoot when missed
ki_level_limit = 10
fighter_width, fighter_height = 100, 100

#this enables for hits and health to be assigned and updated by pygame
goku_damage = pygame.USEREVENT + 1
vegeta_damage = pygame.USEREVENT + 2 

#this loads the image of Goku
goku_image = pygame.image.load(os.path.join("dragonball", "goku.png"))
gokudisplay = pygame.transform.scale(goku_image, (fighter_width, fighter_height))

#this loads the image of Vegeta
vegeta_image = pygame.image.load(os.path.join("dragonball", "vegeta.png"))
vegetadisplay = pygame.transform.scale(vegeta_image, (fighter_width, fighter_height))

#this loads the image of the mountain range Goku and Vegeta fight in
mountain_range = pygame.transform.scale(pygame.image.load(os.path.join('dragonball', 'battle.png')), (width, height))
 
#this function manages how every image or render is displayed onto the window
def image_design(vegeta, goku, vegeta_kiblast, goku_kiblast, vegeta_life_force, goku_life_force):
    #where the mountain range is displayed
    window.blit(mountain_range, (0,0))

    #how the black bar in the middle is displayed
    pygame.draw.rect(window, black, border)

    #how the health bars are displayed
    vegeta_health_bar = font_health.render("Vegeta's life force: " +  str(vegeta_life_force), 1, white)
    goku_health_bar = font_health.render("Goku's life force: " +  str(goku_life_force), 1, white) 

    #where the health bars are displayed
    window.blit(vegeta_health_bar, (width - vegeta_health_bar.get_width() - 10, 10))
    window.blit(goku_health_bar, (15, height - goku_health_bar.get_height()-15))

    #where and how goku and vegeta are displayed
    window.blit(gokudisplay, (goku.x, goku.y))
    window.blit(vegetadisplay, (vegeta.x, vegeta.y))

    #Vegeta's ki blasts are drawn when user presses attack
    for kiblast in vegeta_kiblast:
        pygame.draw.rect(window, blue, kiblast)

    #Goku's ki blasts are drawn when user presses attack
    for kiblast in goku_kiblast:
        pygame.draw.rect(window, orange, kiblast)

    pygame.display.update()
 
#the controls and limits for Goku
def goku_controls(keys_pressed, goku):
    if keys_pressed[pygame.K_a] and goku.x - goku_movement_speed > 0: #left
        goku.x -= goku_movement_speed
    if keys_pressed[pygame.K_d] and goku.x + goku_movement_speed + goku.width < width: #right   
        goku.x += goku_movement_speed 
    if keys_pressed[pygame.K_w] and goku.y - goku_movement_speed > border.y + 15: #up
        goku.y -= goku_movement_speed
    if keys_pressed[pygame.K_s] and goku.y + goku_movement_speed + goku.height < height - 15: #down
        goku.y += goku_movement_speed

#the controls and limits for Vegeta
def vegeta_controls(keys_pressed, vegeta): 
    if keys_pressed[pygame.K_LEFT] and vegeta.x - vegeta_movement_speed > 0: #left
        vegeta.x -= vegeta_movement_speed 
    if keys_pressed[pygame.K_RIGHT] and vegeta.x + vegeta_movement_speed + vegeta.width < width: #right
        vegeta.x += vegeta_movement_speed 
    if keys_pressed[pygame.K_UP] and vegeta.y - vegeta_movement_speed > 0: #up
        vegeta.y -= vegeta_movement_speed
    if keys_pressed[pygame.K_DOWN] and vegeta.y + vegeta_movement_speed + vegeta.height < border.y - 15: #down
        vegeta.y += vegeta_movement_speed 

def kiblast_attack(goku_kiblast, vegeta_kiblast, goku, vegeta):
    #this makes sure to remove Goku's kiblast when it hits Vegeta
    for kiblast in goku_kiblast:
        kiblast.y -= kiblast_movement_speed
        if vegeta.colliderect(kiblast):
            pygame.event.post(pygame.event.Event(vegeta_damage))
            goku_kiblast.remove(kiblast)
        elif kiblast.y > height:
            goku_kiblast.remove(kiblast)
    
    #this makes sure to remove Vegeta's kiblast when it hits Goku
    for kiblast in vegeta_kiblast:
        kiblast.y += kiblast_movement_speed
        if goku.colliderect(kiblast): 
            pygame.event.post(pygame.event.Event(goku_damage))
            vegeta_kiblast.remove(kiblast)
        elif kiblast.y < 0:
            vegeta_kiblast.remove(kiblast)

#this displays the text that the player won for 4 seconds
def winner_display(text):
    insert_text = font_winner.render(text, 1, white)
    window.blit(insert_text, (width/2 - insert_text.get_width()/2, height/2 - insert_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)

def game_data():
    #these two lines below are the starting positions and dimensions of Goku and Vegeta
    vegeta = pygame.Rect(width/2 - fighter_width/2, height/4, fighter_width, fighter_height) 
    goku = pygame.Rect(width/2 - fighter_width/2, height - height/4, fighter_width, fighter_height) 

    #empty lists where ki blasts are appended to when player presses the attack keys
    vegeta_kiblast = []
    goku_kiblast = []

    """
    the two lines of speed variables below are my modifications of the game. The unique gameplay of my game
    is where every time a player is hit by an attack their movement speed decreases by 1 and becomes gradually 
    slower as the game progresses. This is to display a realistic point of view on how a fighter would sustain and 
    suffer from injuries after getting hit by an attack.
    """
    global goku_movement_speed, vegeta_movement_speed
    goku_movement_speed = 15
    vegeta_movement_speed = 15     

    vegeta_life_force = 15
    goku_life_force = 15

    clock = pygame.time.Clock() 
    run = True
    #this while loop keeps running for the game to keep playing per command and frame
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            #this if statement manages how the ki blasts are shot and the position they're shot from for both players
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(goku_kiblast) < ki_level_limit:
                    kiblast = pygame.Rect(goku.x + goku.width/2, goku.y, 30, 30)
                    goku_kiblast.append(kiblast)
                    vegetablast.play()

                if event.key == pygame.K_RSHIFT and len(vegeta_kiblast) < ki_level_limit:
                    kiblast = pygame.Rect(vegeta.x + vegeta.width/2, vegeta.y, 30, 30)
                    vegeta_kiblast.append(kiblast)
                    gokublast.play()

            if event.type == vegeta_damage:
                vegeta_life_force -= 1
                #gameplay of where the int value of the speed variable decreases by 1
                vegeta_movement_speed -=1
                explosian.play()

            if event.type == goku_damage:
                goku_life_force -=1
                #gameplay of where the int value of the speed variable decreases by 1
                goku_movement_speed -=1
                explosian.play()

        #these texts play depending on which player loses all their lives first
        winner_text = " "
        if vegeta_life_force <= 0:
            winner_text =  "Goku defeats Vegeta! Anger!"
        if goku_life_force <=0:
            winner_text = "Vegeta outwits Goku! No shot!"
        if winner_text != " ":
            winner_display(winner_text)
            break 

        #this enables for key pressing in pygame
        keys_pressed = pygame.key.get_pressed()
        goku_controls(keys_pressed, goku)
        vegeta_controls(keys_pressed, vegeta)

        #this manages the functionality of ki blasts 
        kiblast_attack(goku_kiblast, vegeta_kiblast, goku, vegeta)

        #this enables all the images to render and display
        image_design(vegeta, goku, vegeta_kiblast, goku_kiblast, vegeta_life_force, goku_life_force)    
    
    game_data() 
 
if __name__ == "__main__":
    game_data()
