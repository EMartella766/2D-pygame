import pygame

from pygame import mixer
from moveset import Fighters

class Stage():

    def __init__(self, Fighters):
        pygame.init()
        mixer.init()

        self.Fighters = Fighters
        
        self.running = True
        self.WIDTH, self.HEIGHT = 2000, 700
        self.FPS = 120
        self.clock = pygame.time.Clock()

        #self.SURFACE = pygame.display
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.title = pygame.display.set_caption("Fighting stage")
        #fonts
        self.countdown_font = pygame.font.Font("assets/fonts/font.ttf", 100)
        self.score_font = pygame.font.Font("assets/fonts/font.ttf", 30)
        self.hit_counter_font = pygame.font.Font("assets/fonts/font.ttf", 30)
        self.first_count = 3
        self.previous_count = pygame.time.get_ticks()
        self.fight_text_count = 30
        #colours
        self.RED = (255, 0, 0)
        self.GREY = (128, 128, 128)
        self.BLUE = (0, 0, 255)
        self.WHITE = (0, 0, 0)
        #background
        self.scroll = 0
        #round over variables
        self.score = [0, 0] #P1, P2
        self.round_ended = False
        self.round_ended_cooldown = 3000
        self.ulf_image = pygame.image.load("assets/icons/ULF_roundover.png").convert_alpha()
        #sound sfx
        self.player_1_sfx = []
        self.player_2_sfx = []
        #fighter number of frames for each action
        self.fighter_1_num_frames = [12, 9, 24, 15, 15, 10, 9, 7, 12, 14, 10]
        self.fighter_2_num_frames = [12, 9, 24, 15, 15, 10, 9, 7, 12, 14, 10]
        #button
        self.button = pygame.key.get_pressed()



    def load_music(self):

        pygame.mixer.music.load("assets/audio/music/music_2.mp3")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1, 0.0, 5000)

    def load_sfx(self):

        footsteps = pygame.mixer.Sound("assets/audio/sfx/footsteps.mp3")
        footsteps.set_volume(0.1)
        self.player_1_sfx.append(footsteps)
        self.player_2_sfx.append(footsteps)

        heavy_punch = pygame.mixer.Sound("assets/audio/sfx/heavy_punch.mp3")
        heavy_punch.set_volume(0.1)
        self.player_1_sfx.append(heavy_punch)
        self.player_2_sfx.append(heavy_punch)

        kick = pygame.mixer.Sound("assets/audio/sfx/kick_roundhouse.mp3")
        kick.set_volume(0.1)
        self.player_1_sfx.append(kick)
        self.player_2_sfx.append(kick)

        defeated = pygame.mixer.Sound("assets/audio/sfx/defeated.mp3")
        defeated.set_volume(0.1)
        self.player_1_sfx.append(defeated)
        self.player_2_sfx.append(defeated)

    def text(self, text, font, colour, x, y):

     	image = font.render(text, True, colour)
     	self.window.blit(image, (x, y))

    def parallax_bg(self):

     	BG_IMGS = []

     	for i in range (1, 11):
     		IMG = pygame.image.load(f"assets/bg_glacier/parallax-{i}.png").convert_alpha()
     		scaled_bg = pygame.transform.scale(IMG, (1300, self.HEIGHT))
     		BG_IMGS.append(scaled_bg)

     	#get width of first image
     	BG_WIDTH = BG_IMGS[0].get_width()

     	for x in range(3):
     		speed = 0.5
     		for i in BG_IMGS:
     			self.window.blit(i, ((x * BG_WIDTH) - self.scroll * speed, 0))
     			speed += 0.2


    def healthbars(self, health, x, y):
     	health_ratio = health / 400
     	pygame.draw.rect(self.window, (0, 0, 0), (x - 2, y - 2, 404, 34))
     	pygame.draw.rect(self.window, (255, 0, 0), (x, y, 400, 30))
     	pygame.draw.rect(self.window, (255, 215, 0), (x, y, 400 * health_ratio, 30))


    def draw_ultimate_bar(self, increment_bar, x, y):

     	pygame.draw.rect(self.window, self.WHITE, (x - 2, y - 2, 304, 24))
     	pygame.draw.rect(self.window, self.GREY, (x, y, 300, 20))

     	if increment_bar > 0:
     		pygame.draw.rect(self.window, self.BLUE, (x, y, 0 + increment_bar, 20))


    def draw_counter(self, hits, font, colour, x, y):

     	counter_img = font.render(hits, True, colour)
     	self.window.blit(counter_img, (x, y))



    def game_loop(self):

    	clock = pygame.time.Clock()


    	while self.running:


            fighter_1 = Fighters(1, 420, 500, 70, 95, self.fighter_1_num_frames, self.player_1_sfx)
            fighter_2 = Fighters(2, 1500, 500, 80, 95, self.fighter_2_num_frames, self.player_2_sfx)
            fighter_1.load_spritesheets("kid_goku")
            fighter_2.load_spritesheets("kid_goku")

            self.check_events()
            self.parallax_bg()
            self.load_music()
            self.load_sfx()

            #countdown timer
            if self.first_count <= 0:
            	#movement
            	fighter_1.fighter_move(self.WIDTH, self.HEIGHT, self.window, fighter_2, self.button, self.round_ended)
            	fighter_2.fighter_move(self.WIDTH, self.HEIGHT, self.window, fighter_1, self.button, self.round_ended)

            else:
            	#display countdown timer
            	self.text( str(self.first_count), self.countdown_font, self.RED, self.WIDTH/2, self.HEIGHT/3)

            	#update countdown timer
            	if (pygame.time.get_ticks() - self.previous_count) > 1000:
            		self.first_count -= 1
            		self.previous_count = pygame.time.get_ticks()
            
            if self.first_count == 0:
            	
            	if self.fight_text_count > 0:
            		self.text("FIGHT!", self.countdown_font, self.RED, 800, self.HEIGHT/3)
            		self.fight_text_count -= 10

            #check for player defeat
            if self.round_ended == False:
            	if fighter_1.alive == False:
            		self.score[0] += 1
            		self.round_ended == True
            		round_over_time = pygame.time.get_ticks()

            	elif fighter_2.alive == False:
            		self.score[1] += 1
            		self.round_ended = True
            		round_over_time = pygame.time.get_ticks()

            else:
            	#display victory image
            	self.window.blit(self.ulf_image, (650, 150))
            	if pygame.time.get_ticks() - round_over_time > self.round_ended_cooldown:
            		self.round_ended = False
            		self.first_count = 3
            		fighter_1 = Fighters( 1, 420, 500, 70, 95, self.fighter_1_num_frames, self.player_1_sfx)
            		fighter_2 = Fighters( 1, 420, 500, 70, 95, self.fighter_1_num_frames, self.player_2_sfx)

            #draw player round score
            #text("Fighter 1: " + str(score[0], self.score_font, self.RED, 20 , 120))

            self.text("Son Goku (Youth)" , self.score_font, self.RED, 20, 120)
            self.text("Son Goku (Youth)", self.score_font, self.RED, 1650, 120)

            #draw healthbars           
            self.healthbars(fighter_1.health, 200, 30)
            self.healthbars(fighter_2.health, 1400, 30)

            #draw ultimate bar
            self.draw_ultimate_bar(fighter_1.increase_bar, 200, 65)
            self.draw_ultimate_bar(fighter_2.increase_bar, 1500, 65)

            #draw hit counter
            self.draw_counter(str(fighter_1.count_hit) + " hits!", self.hit_counter_font, self.RED, 20, self.HEIGHT/3)
            self.draw_counter(str(fighter_2.count_hit) + " hits!", self.hit_counter_font, self.RED, 1820, self.HEIGHT/3)

            #giving player boundaries
            key = pygame.key.get_pressed()

            if fighter_1.alive == False or fighter_2.alive == False:

            	self.scroll = 0
            else:

            	if key[pygame.K_a] and self.scroll > 0:

            		self.scroll -= 6

            	if key[pygame.K_d] and self.scroll < 800:

            		self.scroll += 6


            #animation
            fighter_1.animation(fighter_2, self.window, self.button)
            fighter_2.animation(fighter_1, self.window, self.button)

            pygame.display.update()

            clock.tick(120)
            

    #exit pygame
    pygame.quit()

    def check_events(self):

    	fighter_1 = Fighters(1, 420, 500, 70, 95, self.fighter_1_num_frames, self.player_1_sfx)
    	fighter_2 = Fighters(1, 420, 500, 70, 95, self.fighter_1_num_frames, self.player_2_sfx)

    	#event handler
    	for event in pygame.event.get():
    		#attack animations
    		fighter_1.moveset(self.button, event)
    		fighter_2.moveset(self.button, event)

    		if event.type == pygame.QUIT:
    			self.running = False

 



fighting_stage = Stage(Fighters)
while fighting_stage.running:

    fighting_stage.game_loop()


#exit loop
pygame.quit()


