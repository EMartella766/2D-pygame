import pygame
from pygame import mixer
from os.path import isfile, join
from os import listdir




mixer.init()

class Fighters:


	def __init__(self, player, x, y, h, w, fighter_1_steps, sfx_1):
		self.player = player
		self.rect = pygame.Rect((x, y, h, w))
		self.ult_x = 0
		self.ult_y = 0
		self.speed = 12
		self.velocity_y = 0
		self.jumping = False
		self.running = False
		self.attack = False 
		self.health = 400
		self.flip = False
		self.spritesheets_dict = {}
		self.animation_steps = fighter_1_steps
		self.current_move = 'idle'
		self.current_frame = 0
		self.current_time = pygame.time.get_ticks()
		self.hit = False
		self.count_hit = 0
		self.direction = "_left"
		self.current_image = self.spritesheets_dict
		self.alive = True
		self.win = False
		self.increase_bar = 0
		self.max_ultimate_bar = 300
		self.ultimate = False
		self.sfx_player_1 = sfx_1
		self.toggle = "keyboard"
		


	def sprite_flip(self, spritesheet_frames):
		return [pygame.transform.flip(sprite, True, False) for sprite in spritesheet_frames]

	def load_spritesheets(self, dir1):

		#create instance of CharSelect class since you only need to pass in the Button class.

		#try:
			#fighter_1_sprites = pygame.image.load("assets/sprites/ssj2_gohan/frame.png")
		#except FileNotFoundError:
			#print("Missing asset:", "frame.png")
    
		#loading the right files with right directories (file destinations)
		file_path = join("assets", "sprites", dir1)
		#list of all files with specified directory
		image_files = [f for f in listdir(file_path) if isfile(join(file_path, f))]

		
		x = 0
		while x != 19:
			for image in image_files:
				#print(image)
				#scale image with filename "ultimate"


				sprite_sheet = pygame.image.load(join(file_path, image)).convert_alpha()


				#work out width of frames
				frame_width = sprite_sheet.get_width() // self.animation_steps[x]
				#work out height for set of frames
				frame_height = sprite_sheet.get_height()

				x += 1

				#print(frame_width) Testing
				#print(x, "index position in list")
				#print(self.animation_steps[x - 1], "This is the amount of frames")

				spritesheet_frames = []

				for i in range(sprite_sheet.get_width() // frame_width):
					sprite_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA, 32)
					rect_frame = pygame.Rect(i * frame_width, 0, frame_width, frame_height) #going to move across frame_width every time an image is extracted from spritesheet, rect_frame = single frame
					
					sprite_surface.blit(sprite_sheet, (0,0), rect_frame) #draw spritesheet at coordinate 0,0 and it is only going to draw a portion of the sprite_sheet which is the single frame
					
					if "ultimate_2" in image:
						scaled_surface = pygame.transform.scale(sprite_surface, (1500, 600))
						spritesheet_frames.append(scaled_surface)

					else:
						spritesheet_frames.append(pygame.transform.scale2x(sprite_surface))
						

					

			
			    #add list of frames onto a dictionary
				self.spritesheets_dict[image.replace(".png", "") + "_right"] = spritesheet_frames
				self.spritesheets_dict[image.replace(".png", "") + "_left"] = self.sprite_flip(spritesheet_frames)
				#print(self.spritesheets_dict.keys())
				#print(self.sfx_player_1)
		        
    #character movement
	def fighter_move(self,width,height,surface, target, button, joystick, round_ended):
		self.speed = 12
		gravitational_field = 1
		change_x = 0
		change_y = 0
		self.attack_type = 0
		self.direction = "_left"


		if self.player == 1 and self.alive == True and round_ended == False and self.toggle == "keyboard":


			#movement
			if button[pygame.K_d]:
				change_x = self.speed
				self.running = True

			if button[pygame.K_a]:
				change_x = -self.speed
				self.running = True

			#jumping
			if button[pygame.K_w] and self.jumping == False:
				self.velocity_y = -24
				self.jumping = True


			#attacking inputs
			if self.attack == False:
				if button[pygame.K_e] or button[pygame.K_r] or button[pygame.K_t] or button[pygame.K_y] or button[pygame.K_z]:
					self.attack = True
					
            
			if self.current_move in {"move_back", "move_forward", "idle"}:
				
				if self.velocity_y == -24:
					self.switch_animation('jump')
				
				elif button[pygame.K_w] and self.jumping == True:
					self.switch_animation('jump')
				
				elif button[pygame.K_w] and button[pygame.K_a]:
					self.switch_animation('jump')
				
				elif button[pygame.K_w] and button[pygame.K_d]:
					self.switch_animation('jump')
				
				elif button[pygame.K_a] and self.running == True and self.jumping == False:
					self.switch_animation('move_back')

				elif button[pygame.K_d] and self.running == True and self.jumping == False:
					self.switch_animation('move_forward')

				elif self.hit == True:
					self.switch_animation('hit')
					self.hit = False
			

				else:
					self.switch_animation('idle')

		if self.player == 1 and self.alive == True and round_ended == False and self.toggle == "keyboard":


			for joystick in joystick:

				axis_x = joystick.get_axis(0)
				if abs(axis_x) > 0.05:
					change_x +=  axis_x * 10
					self.running == True

				if joystick.get_button(3) and self.jumping == False:
					self.velocity_y = -24
					self.jumping = True

				#attack inputs for controller
				if self.attack == False:
					if joystick.get_button(0) or joystick.get_button(1) or joystick.get_button(2) or joystick.get_button(4) or joystick.get_button(5):
						self.attack = True

				if self.current_move in {"move_back", "move_forward", "idle"}:

					if joystick.get_button(3) and self.jumping == True:
						self.switch_animation('jump')

					elif change_x > 0:
						self.switch_animation('move_forward')

					elif change_x < 0:
						self.switch_animation('move_back')

					elif self.hit == True:
						self.switch_animation('hit')
						self.hit = False

					else:
						self.switch_animation('idle')



		if self.player == 2 and self.alive == True and round_ended == False:

			#movement
			if button[pygame.K_RIGHT]:
				change_x = self.speed
				self.running = True

			if button[pygame.K_LEFT]:
				change_x = -self.speed
				self.running = True

			#jumping
			if button[pygame.K_UP] and self.jumping == False:
				self.velocity_y = -24
				self.jumping = True

			#attacking inputs
			if self.attack == False:

				if button[pygame.K_c] or button[pygame.K_v] or button[pygame.K_b] or button[pygame.K_n] or button[pygame.K_m]:
					self.attack = True
					
					
					

			if self.current_move in {"move_back", "move_forward", "idle"}:
				
				if self.velocity_y == -24:
					self.switch_animation('jump')
				
				elif button[pygame.K_UP] and self.jumping == True:
					self.switch_animation('jump')
				
				elif button[pygame.K_UP] and button[pygame.K_LEFT]:
					self.switch_animation('jump')
				
				elif button[pygame.K_UP] and button[pygame.K_RIGHT]:
					self.switch_animation('jump')
				
				elif button[pygame.K_LEFT] and self.running == True and self.jumping == False:
					self.switch_animation('move_forward')

				elif button[pygame.K_RIGHT] and self.running == True and self.jumping == False:
					self.switch_animation('move_back')

				elif self.hit == True:
					self.switch_animation('hit')
					self.hit = False

				else:
					self.switch_animation('idle')






	    #updating velocity and adding gravity
		change_y += self.velocity_y
		self.velocity_y += gravitational_field

			
		#making sure that player not going outside of screen left/right
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > width:
			self.rect.right = width

		#making sure that player does not go outside screen up/down
		if self.rect.bottom + change_y > height - 120:
			self.velocity_y = 0
			change_y = height - 120 - self.rect.bottom
			self.jumping = False
		

        #update x/y coordinates
		self.rect.x += change_x #coordinate x increased by change_x
		self.rect.y += change_y


	def moveset(self, button, joystick, event):

		if self.player == 1 and self.toggle == 'keyboard':

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					self.switch_animation('jump')
					
				elif event.key == pygame.K_e:
					self.switch_animation('punch')
					

				elif event.key == pygame.K_r:
					self.switch_animation('punch_2')
					
				elif event.key == pygame.K_t:
					self.switch_animation('kick_1')
					
				elif event.key == pygame.K_y:
					self.switch_animation('kick_2')
					
				elif event.key == pygame.K_z:
					if self.ultimate == True:
						self.switch_animation('ultimate_2')
						#pygame.mixer.Sound.play(self.sfx_player_1[0])

		if self.player == 1 and self.toggle == 'keyboard':
			
			for js in joystick:
				
				if joystick.get_button(0):
					self.switch_animation('punch')
				
				elif joystick.get_button(1):
					self.switch_animation('punch_2')
				
				elif joystick.get_button(2):
					self.switch_animation('kick_1')
				
				elif joystick.get_button(4):
					self.switch_animation('kick_2')
				
				elif joystick.get_button(5):
					if self.ultimate == True:
						self.switch_animation('ultimate_2')


		
		if self.player == 2:

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					self.switch_animation('jump')
				elif event.key == pygame.K_c:
					self.switch_animation('punch')
					
				elif event.key == pygame.K_v:
					self.switch_animation('punch_2')
					
				elif event.key == pygame.K_b:
					self.switch_animation('kick_1')
					
				elif event.key == pygame.K_n:
					self.switch_animation('kick_2')
					
				elif event.key == pygame.K_m:
					if self.ultimate == True:
						self.switch_animation('ultimate')
						#pygame.mixer.Sound.play(self.sfx_player_1[0])

				
	def animation(self, target, surface, button, joystick):

		if self.health <= 0:
			self.health = 0
			self.alive = False
			self.switch_animation('defeated')
			

		elif target.health <= 0:
			self.win = True
			self.switch_animation('winscreen')
			
		

		
		animation_cooldown = 100
		self.current_image = self.spritesheets_dict[self.current_move + self.direction][self.current_frame]
		

		#check if player has gone beyond opponent, if yes then flip sprites
		if target.rect.centerx < self.rect.centerx and self.alive == True:
				self.flip = True
				self.direction = "_left"
				self.current_image = self.spritesheets_dict[self.current_move + self.direction][self.current_frame]
		elif target.rect.centerx > self.rect.centerx:
				self.flip = False
				self.direction = "_right"
				self.current_image = self.spritesheets_dict[self.current_move + self.direction][self.current_frame]

		#if time passed during displaying of a single frame > animation_cooldown, then move onto next frame
		if pygame.time.get_ticks() - self.current_time > animation_cooldown:
			self.current_frame += 1
			#reset time since last frame update
			self.current_time = pygame.time.get_ticks()

		#check if animation has finished/ last frame played
		if self.current_frame >= len(self.spritesheets_dict[self.current_move + self.direction]):
			#if player hp < 0 then end animation
			if self.alive == False:
				self.current_frame = len(self.spritesheets_dict[self.current_move + self.direction]) - 1
			else:
				self.current_frame = 0
				self.current_move = 'idle'
				self.current_time = pygame.time.get_ticks()

				#check if an attack was performed --> keyboard
				if button[pygame.K_e] or button[pygame.K_r] or button[pygame.K_t] or button[pygame.K_y] or button[pygame.K_z] or button[pygame.K_v] or button[pygame.K_c] or button[pygame.K_b] or button[pygame.K_n] or button[pygame.K_m]:
					self.attack = False
					self.current_move = 'idle'

				#check if an attack was performed --> controller
				for joystick in joystick:
					if joystick.get_button(0) or joystick.get_button(1) or joystick.get_button(2) or joystick.get_button(4) or joystick.get_button(5):
						self.attack = False
						self.current_move = 'idle'

				#check if player took damage
				if self.current_move == 'hit':
					target.hit = False
					#if player was in the middle of an attack then both attack cancel out
					self.attack = False

		if self.current_move == 'ultimate_2':
			surface.blit(self.current_image, (0,0))
			


			#stop blitting opponent sprites until animation is finished!

		else:
			surface.blit(self.current_image, (self.rect.x, self.rect.y - 170))



	 # attacking + giving each attack different damage outputs
	def fighter_damage(self, surface, target, event, button, joystick):


			
			collision_rect = pygame.Rect(self.rect.centerx - ( 2 * self.rect.width * self.flip), self.rect.y - 100, 2 * self.rect.width, self.rect.height * 2)
			if collision_rect.colliderect(target.rect):

				
				if event.type == pygame.KEYDOWN and self.attack == True:

					#player 1 -- keyboard

					if event.key == pygame.K_e:
						pygame.mixer.Sound.play(self.sfx_player_1[2])
						target.health -= 20
						target.hit = True
						self.count_hit += 1
						#punch

					if event.key == pygame.K_r:
						pygame.mixer.Sound.play(self.sfx_player_1[3])
						target.health -= 20
						target.hit = True
						self.count_hit += 1
						#kick_1
					

					if event.key == pygame.K_t:
						pygame.mixer.Sound.play(self.sfx_player_1[2])
						target.health -= 20
						target.hit = True
						self.count_hit += 1
						#kick_2

					if event.key == pygame.K_y:
						pygame.mixer.Sound.play(self.sfx_player_1[3])
						target.hit = True
						target.health -= 20
						self.count_hit += 1


					#player 2

					if event.key == pygame.K_c:
						pygame.mixer.Sound.play(self.sfx_player_1[2])
						target.health -= 20
						target.hit = True
						self.count_hit += 1

					if event.key == pygame.K_v:
						pygame.mixer.Sound.play(self.sfx_player_1[3])
						target.health -= 20
						target.hit = True
						self.count_hit += 1

					if event.key == pygame.K_b:
						pygame.mixer.Sound.play(self.sfx_player_1[2])
						target.health -= 20
						target.hit = True
						self.count_hit += 1

					if event.key == pygame.K_n:
						pygame.mixer.Sound.play(self.sfx_player_1[3])
						target.health -= 20
						target.hit = True
						self.count_hit += 1

				#player 1 -- controller

				if event.type == pygame.JOYBUTTONDOWN and self.attack == True:
					for joystick in joystick:
						
						if joystick.get_button(0):
							pygame.mixer.Sound.play(self.sfx_player_1[2])
							target.health -= 20
							target.hit = True
							self.count_hit += 1

						if joystick.get_button(1):
							pygame.mixer.Sound.play(self.sfx_player_1[3])
							target.health -= 20
							target.hit = True
							self.count_hit += 1

						if joystick.get_button(2):
							pygame.mixer.Sound.play(self.sfx_player_1[2])
							target.health -= 20
							target.hit = True
							self.count_hit += 1

						if joystick.get_button(4):
							pygame.mixer.Sound.play(self.sfx_player_1[3])
							target.health -= 20
							target.hit = True
							self.count_hit += 1





				

                #handle ultimate bar mechanics
				if target.hit == True and self.ultimate == False:
					self.increase_bar += 10
					

				if self.increase_bar >= self.max_ultimate_bar:
					self.ultimate = True
					self.increase_bar = 0

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m and self.ultimate == True:
						target.health -= 35
						target.hit = True
						self.count_hit += 1
						self.ultimate = False

					if event.key == pygame.K_z and self.ultimate == True:
						target.health -= 35
						target.hit = True
						self.count_hit += 1
						self.ultimate = False





			#pygame.draw.rect(surface, (0, 255, 0), collision_rect)




	#function for switching between animations
	def switch_animation(self, updated_action):
		if updated_action != self.current_move:
			self.current_move = updated_action
			#reset index of animation
			self.current_frame = 0
			self.current_time = pygame.time.get_ticks()



