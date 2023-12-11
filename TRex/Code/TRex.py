import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = reserve_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 13

            if obstacle_rect.bottom == 300:  screen.blit(raptor_surf,obstacle_rect)
            else: screen.blit(pterodactyl_surf,obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x >-100]
        
        return obstacle_list
    else: return []

def collisions(trex, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if trex.colliderect(obstacle_rect): return False
    return True

def trex_animation():
    global trex_surf, trex_index

    if trex_rect.bottom <300:
        trex_surf = trex_jump
    else:
        trex_index += 0.1
        if trex_index >= len(trex_walk): trex_index =0
        trex_surf = trex_walk[int(trex_index)]
       
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('T-Rex')
clock = pygame.time.Clock()
reserve_font = pygame.font.Font('Images/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('Images/JurassicSky.png').convert()
ground_surface = pygame.image.load('Images/JurassicGround.png').convert()

# raptor
raptor_1 = pygame.image.load('Images/Raptor_N1.png').convert_alpha()
raptor_2 = pygame.image.load('Images/Raptor_N2.png').convert_alpha()
raptor_3 = pygame.image.load('Images/Raptor_N3.png').convert_alpha()
raptor_4 = pygame.image.load('Images/Raptor_N4.png').convert_alpha()
raptor_frames = [raptor_1, raptor_2, raptor_3, raptor_4]
raptor_frame_index = 0
raptor_surf = raptor_frames[raptor_frame_index]

# pterodactyl
pterodactyl_1 = pygame.image.load('Images/Pterodactyl_1.png').convert_alpha()
pterodactyl_2 = pygame.image.load('Images/Pterodactyl_2.png').convert_alpha()
pterodactyl_3 = pygame.image.load('Images/Pterodactyl_3.png').convert_alpha()
pterodactyl_4 = pygame.image.load('Images/Pterodactyl_4.png').convert_alpha()
pterodactyl_frames = [pterodactyl_1, pterodactyl_2, pterodactyl_3, pterodactyl_4]
pterodactyl_frame_index = 0
pterodactyl_surf = pterodactyl_frames[pterodactyl_frame_index]

obstacle_rect_list = []

trex_walk_1 = pygame.image.load('Images/TRex_Stand1.png').convert_alpha()
trex_walk_2 = pygame.image.load('Images/TRex_Walk1.png').convert_alpha()
trex_walk_3 = pygame.image.load('Images/TRex_Stand2.png').convert_alpha()
trex_walk_4 = pygame.image.load('Images/TRex_Walk2.png').convert_alpha()
trex_walk = [trex_walk_1, trex_walk_2, trex_walk_3, trex_walk_4]
trex_index = 0
trex_jump = pygame.image.load('Images/TRex_Jump2.png').convert_alpha()

trex_surf = trex_walk[trex_index]
trex_rect = trex_surf.get_rect(midbottom = (200,300))
trex_gravity = 0

#intro screen
trex_stand = pygame.image.load('Images/TRex_Stand.png').convert_alpha()
trex_stand = pygame.transform.rotozoom(trex_stand,0,2)
trex_stand_rect = trex_stand.get_rect(center = (400,200))

game_name = reserve_font.render('T Rex Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80)) 

game_message = reserve_font.render('Press space to run', False, (111,196,169))
game_message_rect = game_name.get_rect(center = (340,340))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

raptor_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(raptor_animation_timer, 10)

pterodactyl_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(pterodactyl_animation_timer, 10)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and trex_rect.bottom >= 300: 
                    trex_gravity = -21
                    
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
   
        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(raptor_surf.get_rect(
                                        bottomright = (randint(900,1100), 300)))
                else:
                    obstacle_rect_list.append(pterodactyl_surf.get_rect(
                                        bottomright = (randint(900,1100), 180))) 

            if event.type == raptor_animation_timer:
                raptor_frame_index += 0.1
                if raptor_frame_index >= len(raptor_frames): 
                    raptor_frame_index = 0
                raptor_surf = raptor_frames[int(raptor_frame_index)]
                            
            if event.type == pterodactyl_animation_timer:
                pterodactyl_frame_index += 0.1
                if pterodactyl_frame_index >= len(pterodactyl_frames): 
                    pterodactyl_frame_index = 0
                pterodactyl_surf = pterodactyl_frames[int(pterodactyl_frame_index)]            
  
    if game_active:        
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score = display_score()
        
        #T Rex
        trex_gravity += 1
        trex_rect.y += trex_gravity
        if trex_rect.bottom >= 300: trex_rect.bottom = 300
        trex_animation()
        screen.blit(trex_surf, trex_rect)
        
        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        #Collision
        game_active = collisions(trex_rect, obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(trex_stand, trex_stand_rect)
        obstacle_rect_list.clear()
        trex_rect.midbottom = (200,300)
        trex_gravity = 0
        
        score_message = reserve_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name,game_name_rect)
                
        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message, score_message_rect)
        
    pygame.display.update()
    clock.tick(60) 