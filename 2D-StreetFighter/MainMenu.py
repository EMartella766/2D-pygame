import pygame

from buttons import Button


class MainLobby:

	def __init__(self):
		
		pygame.init()
		self.entered = True
		self.menu_state = "main_menu"
		self.char_select_entered = False
		self.how_to_play = False
		self.stats = False
		self.WIDTH, self.HEIGHT = 750, 750
		self.W_WIDTH, self.W_HEIGHT = 750, 750
		self.SURFACE = pygame.Surface((self.WIDTH, self.HEIGHT))
		self.lobby_window = pygame.display.set_mode((self.W_WIDTH, self.W_HEIGHT))
		self.lobby_title = pygame.display.set_caption("main lobby")
		self.WHITE = (255, 255, 255)
		self.BLACK = (0, 0, 0)
		self.RED = (255, 0, 0)
		self.font = pygame.font.Font("assets/fonts/menu.ttf", 20)
		self.main_title_font = pygame.font.Font("assets/fonts/font.ttf", 50)
		self.start_button = pygame.image.load("assets/icons/start_button.png").convert_alpha()
		self.instructions_button = pygame.image.load("assets/icons/how_to_play_button.png").convert_alpha()
		self.characters_button = pygame.image.load("assets/icons/characters_button.png").convert_alpha()
		self.exit_button = pygame.image.load("assets/icons/quit_button.png").convert_alpha()
		self.back_button = pygame.image.load("assets/icons/back_button.png").convert_alpha()
		self.xbox_button = pygame.image.load("assets/icons/xbox_button.png").convert_alpha()
		self.keyboard_button = pygame.image.load("assets/icons/keyboard_button.png").convert_alpha()
		self.toggle_button = pygame.image.load("assets/icons/toggle_button.png")
		self.running = True
		

		
    #draw main title
	def draw_text(self, text, x, y):
		
		image = self.main_title_font.render(text, True, self.RED)
		self.lobby_window.blit(image, (x, y))


    #draw background
	def blit_bg(self, x, y):

		bg = []

		for i in range(1, 9):
			img = pygame.image.load(f"assets/backgrounds/main_menu_bg/base_{i}.png").convert_alpha()
			scaled_bg = pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
			bg.append(scaled_bg)

		bg_width = bg[0].get_width()

		for image in bg:
			self.lobby_window.blit(image, (x, y))
			

    #main menu loop
	def main_lobby_loop(self):

		FPS = 120
		clock = pygame.time.Clock()
		while self.running and self.menu_state in ['main_menu', 'instructions', 'toggle', 'characters']:

			self.check_events()
			self.SURFACE.fill(self.WHITE)
			self.lobby_window.blit(self.SURFACE, (0,0))
			self.blit_bg(0, 0)

			self.draw_text("Z WARRIORS", 170, 20)
			
			if self.entered == True:
				
				#button instances
				start_button = Button(280, 350, self.start_button, 2)
				instructions_button = Button(280, 410, self.instructions_button, 2)
				stats_button = Button(280, 470, self.characters_button, 2)
				toggle_button = Button(280, 530, self.toggle_button, 2)
				quit_button = Button(280, 590, self.exit_button, 2)
				back_button = Button(10, 680, self.back_button, 1.5)
				xbox_button = Button(280, 400, self.xbox_button, 2)
				keyboard_button = Button(280, 500, self.keyboard_button, 2)
				
				if self.menu_state == "main_menu":
                    #start button
					if start_button.draw_button(self.lobby_window):
						print("Start Game Button Pressed!")
						self.menu_state = 'char_select'
						

					#how to play button
					if instructions_button.draw_button(self.lobby_window):
						print("How to Play Button Pressed!")
						self.menu_state = "instructions"

                    #character stats button
					if stats_button.draw_button(self.lobby_window):
						print("Stats Button Pressed!")
						self.menu_state = "characters"

					if toggle_button.draw_button(self.lobby_window):
						self.menu_state = "toggle"


					#quit button
					if quit_button.draw_button(self.lobby_window):
						self.running = False

				#back button if instructions button pressed
				if self.menu_state == "instructions":
					#back button
					if back_button.draw_button(self.lobby_window):
						print("Go back")
						self.menu_state = "main_menu"

				elif self.menu_state == "toggle":

					if xbox_button.draw_button(self.lobby_window):
						print("xbox")

					if keyboard_button.draw_button(self.lobby_window):
						print("keyboard")

					if back_button.draw_button(self.lobby_window):
						self.menu_state = "main_menu"

				elif self.menu_state == "characters":
					 #back button
					 if back_button.draw_button(self.lobby_window):
					 	self.menu_state = "main_menu"


			pygame.display.update()

			clock.tick(FPS)


		pygame.quit()
			

	#event handler
	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False



pygame.quit()
        
