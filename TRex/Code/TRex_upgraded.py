import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        trex_walk_1 = pygame.image.load('Images/TRex_Stand1.png').convert_alpha()
        trex_walk_2 = pygame.image.load('Images/TRex_Walk1.png').convert_alpha()
        trex_walk_3 = pygame.image.load('Images/TRex_Stand2.png').convert_alpha()
        trex_walk_4 = pygame.image.load('Images/TRex_Walk2.png').convert_alpha()
        self.trex_walk = [trex_walk_1, trex_walk_2, trex_walk_3, trex_walk_4]
        self.trex_index = 0
        self.trex_jump = pygame.image.load('Images/TRex_Jump2.png').convert_alpha()
                
        self.image = self.trex_walk[self.trex_index]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0
    
    def trex_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -23
        
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300
    
    def animation_state(self):
        if self.rect.bottom <300:
            self.image = self.trex_jump
        else:
            self.trex_index += 0.1
            if self.trex_index >= len(self.trex_walk): self.trex_index = 0
            self.image = self.trex_walk[int(self.trex_index)]
    
    def update(self):
        self.trex_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'pterodactyl':
           pterodactyl_1 = pygame.image.load('Images/Pterodactyl_1.png').convert_alpha()
           pterodactyl_2 = pygame.image.load('Images/Pterodactyl_2.png').convert_alpha()
           pterodactyl_3 = pygame.image.load('Images/Pterodactyl_3.png').convert_alpha()
           pterodactyl_4 = pygame.image.load('Images/Pterodactyl_4.png').convert_alpha()
           self.frames = [pterodactyl_1, pterodactyl_2, pterodactyl_3, pterodactyl_4]
           y_pos = 210
        else:
           raptor_1 = pygame.image.load('Images/Raptor_N1.png').convert_alpha()
           raptor_2 = pygame.image.load('Images/Raptor_N2.png').convert_alpha()
           raptor_3 = pygame.image.load('Images/Raptor_N3.png').convert_alpha()
           raptor_4 = pygame.image.load('Images/Raptor_N4.png').convert_alpha()
           self.frames = [raptor_1, raptor_2, raptor_3, raptor_4]
           y_pos = 300
        
        self.animation_index = 0        
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 11
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time
    
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
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

def collision_sprite():
    if pygame.sprite.spritecollide(trex.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

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
test_font = pygame.font.Font('Images/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

# groups
trex = pygame.sprite.GroupSingle()
trex.add(Player())
obstacle_group = pygame.sprite.Group()

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
pterodactyl_surf = pterodactyl_frames[raptor_frame_index]

obstacle_rect_list = []

trex_walk_1 = pygame.image.load('Images/TRex_Stand1.png').convert_alpha()
trex_walk_2 = pygame.image.load('Images/TRex_Walk1.png').convert_alpha()
trex_walk_3 = pygame.image.load('Images/TRex_Stand2.png').convert_alpha()
trex_walk_4 = pygame.image.load('Images/TRex_Walk2.png').convert_alpha()
trex_walk = [trex_walk_1, trex_walk_2, trex_walk_3, trex_walk_4]
trex_index = 0
trex_jump = pygame.image.load('Images/TRex_Jump2.png').convert_alpha()

trex_surf = trex_walk[trex_index]
trex_rect = trex_surf.get_rect(midbottom = (80,300))
trex_gravity = 0

#intro screen
trex_stand = pygame.image.load('Images/TRex_Stand.png').convert_alpha()
trex_stand = pygame.transform.rotozoom(trex_stand,0,2)
trex_stand_rect = trex_stand.get_rect(center = (400,200))

game_name = test_font.render('T Rex Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run', False, (111,196,169))
game_message_rect = game_name.get_rect(center = (340,340))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

raptor_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(raptor_animation_timer, 500)

pterodactyl_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(pterodactyl_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if trex_rect.collidepoint(event.pos) and trex_rect.bottom >= 300:
                    trex_gravity = -23
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and trex_rect.bottom >= 300:
                    trex_gravity = -23
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                
                start_time = int(pygame.time.get_ticks() / 1000)
                
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['pterodactyl', 'raptor', 'raptor', 'raptor'])))

            if event.type == raptor_animation_timer:
                if raptor_frame_index == 0: raptor_frame_index =1
                else: raptor_frame_index = 0
                raptor_surf = raptor_frames[raptor_frame_index]
            
            if event.type == pterodactyl_animation_timer:
                if pterodactyl_frame_index == 0: pterodactyl_frame_index =1
                else: pterodactyl_frame_index = 0
                pterodactyl_surf = pterodactyl_frames[pterodactyl_frame_index]
                   
    if game_active:   
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score = display_score()
        trex.draw(screen)
        trex.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
       
        #collision
        game_active = collision_sprite()
    else:
        screen.fill((94,129,162))
        screen.blit(trex_stand, trex_stand_rect)
        obstacle_rect_list.clear()
        trex_rect.midbottom = (80,300)
        trex_gravity = 0
        
        score_message = test_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name,game_name_rect)
        
        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message, score_message_rect)
    
    pygame.display.update()
    clock.tick(60)
    