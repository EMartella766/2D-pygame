import pygame
from pygame import mixer
from moveset import Fighters




mixer.init()
pygame.init()

#initialise joystick module
pygame.joystick.init()


joysticks = []
for i in range(0, pygame.joystick.get_count()):
	joysticks.append(pygame.joystick.Joystick(i))
	joysticks[-1].init()
	print("detected joystick", joysticks[-1].get_name())



#===========================================================================================================================
#GAME VARIABLES


#create window for fighting stage
WIDTH = 2000
HEIGHT = 700

window = pygame.display.set_mode ((WIDTH, HEIGHT))
pygame.display.set_caption ("Fighting stage")




#font for text
countdown_font = pygame.font.Font("assets/fonts/font.ttf", 100)
score_font = pygame.font.Font("assets/fonts/font.ttf", 25)
hit_counter_font = pygame.font.Font("assets/fonts/font.ttf", 30)



#countdown timer variables
first_count = 3
previous_count = pygame.time.get_ticks() 
fight_text_count = 30


#define colours
red = (255, 0, 0)
grey = (128, 128, 128)
blue = (0, 0, 255)
white = (0, 0, 0)
text_colour = (0, 0, 0)


#round over variables
score = [0, 0] #P1, P2
round_ended = False
round_ended_cooldown = 3000


#victory image (when round over)
ulf_image = pygame.image.load("assets/icons/ULF_roundover.png").convert_alpha()
window.blit(ulf_image, (1000, 500))


#sound effects variables
player_1_sfx = []
player_2_sfx = []

#load music
#pygame.mixer.music.load("assets/audio/music/music_2.mp3")
#pygame.mixer.music.set_volume(0.05)
#pygame.mixer.music.play(-1, 0.0, 5000)


#load sound effects
kamehameha = pygame.mixer.Sound("assets/audio/sfx/kamehameha.mp3")
kamehameha.set_volume(0.5)
player_1_sfx.append(kamehameha)
player_2_sfx.append(kamehameha)

footsteps = pygame.mixer.Sound("assets/audio/sfx/footsteps.mp3")
footsteps.set_volume(0.1)
player_1_sfx.append(footsteps)
player_2_sfx.append(footsteps)

heavy_punch = pygame.mixer.Sound("assets/audio/sfx/heavy_punch.mp3")
heavy_punch.set_volume(0.1)
player_1_sfx.append(heavy_punch)
player_2_sfx.append(heavy_punch)

kick = pygame.mixer.Sound("assets/audio/sfx/kick_roundhouse.mp3")
kick.set_volume(0.1)
player_1_sfx.append(kick)
player_2_sfx.append(kick)

defeated = pygame.mixer.Sound("assets/audio/sfx/defeated.mp3")
defeated.set_volume(0.1)
player_1_sfx.append(defeated)
player_2_sfx.append(defeated)


#fighter number of frames for each action
fighter_1_num_frames = [3, 3, 10, 8, 4, 4, 7, 7, 5, 5, 1, 1, 5, 5, 6, 6, 34, 6, 4]
fighter_2_num_frames = [3, 3, 10, 8, 4, 4, 7, 7, 5, 5, 1, 1, 5, 5, 6, 6, 34, 6, 4]

#==========================================================================================================================


#draw text
def text(text, font, colour, x, y):
	image = font.render(text, True, colour)
	window.blit(image, (x, y))


#parallax background
BG_IMGS = []
for i in range (1,11):
   IMG = pygame.image.load (f"assets/bg_glacier/parallax-{i}.png").convert_alpha()
   scaled_bg = pygame.transform.scale(IMG, (1300, HEIGHT)) 
   BG_IMGS.append(scaled_bg) 

#get width of first image
BG_WIDTH = BG_IMGS[0].get_width()  

scroll = 0

#function to draw background images
def draw():
	for x in range(3):
		speed = 0.5
		for i in BG_IMGS:
			window.blit( i,(( x * BG_WIDTH ) - scroll * speed, 0))
			speed += 0.2



#create two instances of fighter objects
fighter_1 = Fighters( 1, 420, 500, 70, 95, fighter_1_num_frames, player_1_sfx)   # x, y, width, height
fighter_2 = Fighters( 2, 1500, 500, 80, 95, fighter_2_num_frames, player_2_sfx)  # y-axis stays the same but x-axis different


#load spritesheets for character
fighter_1.load_spritesheets("ssj2_gohan")
fighter_2.load_spritesheets("ssj2_gohan")


#function to draw healthbars

def healthbars(health, x, y):
    health_ratio = health / 400
    pygame.draw.rect(window, (0, 0, 0), (x - 2, y - 2, 404, 34))
    pygame.draw.rect(window, (255, 0, 0), (x, y, 400, 30)) #surface, colour, x, y, w, h
    pygame.draw.rect(window, (255, 215, 0), (x, y, 400 * health_ratio, 30))

#function to draw ultimate

def draw_ultimate_bar(increment_bar, x, y):

	pygame.draw.rect(window, white, (x - 2, y - 2, 304, 24))
	pygame.draw.rect(window, grey, (x, y, 300, 20))

	if increment_bar > 0:
		pygame.draw.rect(window, blue, (x, y, 0 + increment_bar, 20)) #make bar longer every time hit landed

	
#hit counter - check if player hit opponent
def draw_counter(hits, font, colour, x, y):
	
	counter_img = font.render(hits, True, colour)
	window.blit(counter_img, (x, y))




#FPS limit
clock = pygame.time.Clock()


running = True


while running:

	#button
	

    # Drawing images/ parallax
	draw()

	#countdown timer
	if first_count <= 0:
		#movement
		fighter_1.fighter_move(WIDTH, HEIGHT, window, fighter_2, button, joysticks, round_ended)
		fighter_2.fighter_move(WIDTH, HEIGHT, window, fighter_1, button, joysticks, round_ended)
	else:
		#display countdown timer
		text( str(first_count), countdown_font, red, WIDTH/2, HEIGHT/3 )
		

		#update countdown timer
		if (pygame.time.get_ticks() - previous_count) > 1000:
			first_count -= 1
			previous_count = pygame.time.get_ticks()
	if first_count == 0:
		if fight_text_count > 0:
			text( "FIGHT!", countdown_font, red, 800, HEIGHT/3) #could insert an image instead
			fight_text_count -= 1

	#check for player defeat
	if round_ended == False:
		if fighter_1.alive == False:
			score[0] += 1
			round_ended = True
			round_over_time = pygame.time.get_ticks()
		elif fighter_2.alive == False:
			score[1] += 1
			round_ended = True
			round_over_time = pygame.time.get_ticks()
	else:
		#display victory image
		window.blit(ulf_image, (650, 150))
		#if pygame.time.get_ticks() - round_over_time > round_ended_cooldown:
			#round_ended = False
			#first_count = 3
			#fighter_1 = Fighters( 1, 420, 500, 70, 95, fighter_1_num_frames, player_1_sfx)
			#fighter_1.current_image = fighter_1.kid_goku_spritesheets = ['idle' + '_right'][0]
			#fighter_2 = Fighters( 2, 1500, 500, 80, 95, fighter_2_num_frames, player_2_sfx)
			#fighter_2.current_image = fighter_2.kid_goku_spritesheets = ['idle' + '_left'][0]


	#draw player round score
	#text("Fighter 1: " + str(score[0]), score_font, red, 20, 120)
	

	text("Fighter 1" , score_font, red, 20, 120)
	text("Fighter 2", score_font, red, 1650, 120)

	
    #draw healthbars
	healthbars(fighter_1.health, 200, 30)
	healthbars(fighter_2.health, 1400, 30)

	#draw ultimate bar
	draw_ultimate_bar(fighter_1.increase_bar, 200, 65) 
	draw_ultimate_bar(fighter_2.increase_bar, 1500, 65)

	#hit counter
	draw_counter(str(fighter_1.count_hit) + " hits!", hit_counter_font, red, 20, HEIGHT/3)
	draw_counter(str(fighter_2.count_hit) + " hits!", hit_counter_font, red, 1820, HEIGHT/3)
	
	


    
    #giving boundaries. if player doesnt hit boundaries then allowed to scroll left/right
	key = pygame.key.get_pressed()
	if fighter_1.alive == False or fighter_2.alive == False:
		scroll = 0
	else:
		if key[pygame.K_a] and scroll > 0 and first_count<=0:
			scroll -= 6
		if key[pygame.K_d] and scroll < 800 and first_count<0:
			scroll += 6

	
		
	
		


	#event handler
	for event in pygame.event.get():

		button = pygame.key.get_pressed()

		#attacks animations
		fighter_1.moveset(button, joysticks, event)
		fighter_2.moveset(button, joysticks, event)

		fighter_1.fighter_damage(window, fighter_2, event, button, joysticks)
		fighter_2.fighter_damage(window, fighter_1, event, button, joysticks)

		if event.type == pygame.QUIT:
			
			running = False


	#animation
	fighter_1.animation(fighter_2, window, button, joysticks)
	fighter_2.animation(fighter_1, window, button, joysticks)


    #update display
	pygame.display.update()		

	clock.tick(120)



#exit game
pygame.quit()
