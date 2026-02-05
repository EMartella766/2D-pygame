import pygame

from buttons import Button

class CharSelect():

	def __init__(self):

		pygame.init()

		self.entered = True
		self.start_button = True
		self.choose_state = "kid_goku"
		self.choose_state_2 = "kid_goku_2"
		self.running = True
		self.WIDTH, self.HEIGHT = 1200, 900
		self.W_WIDTH, self.W_HEIGHT = 1200, 900
		self.SURFACE = pygame.Surface((self.WIDTH, self.HEIGHT))
		self.WINDOW = pygame.display.set_mode((self.W_WIDTH, self.W_HEIGHT))
		self.title = pygame.display.set_caption("Choose your character!")
		self.COLOUR = (255, 165, 0)
		self.BLACK = (0, 0, 0)
		self.WHITE = (255, 255, 255)
		self.button_font = pygame.font.Font("assets/fonts/menu.ttf", 20)
		self.text_font = pygame.font.Font("assets/fonts/font.ttf", 30)
		self.name_font = pygame.font.Font("assets/fonts/font.ttf", 25)
		self.bg = pygame.image.load("assets/backgrounds/bg_sc.jpg").convert_alpha()
		self.bg_scaled = pygame.transform.scale(self.bg, (1500, self.HEIGHT))
		self.symbol = pygame.image.load("assets/icons/Budokai.png")
		self.symbol_scaled = pygame.transform.scale( self.symbol, (500, 500))
		self.button = pygame.image.load("assets/icons/char_button.png").convert_alpha()
		self.char_1 = pygame.image.load("assets/imgs/goku_youth.png").convert_alpha() #img size 600x600
		self.vs = pygame.image.load("assets/icons/vs.png")
		self.vs_scaled = pygame.transform.scale( self.vs, (135, 135))
		self.char_1_selected = pygame.image.load("assets/imgs/goku_youth_selected.png").convert_alpha()
		self.char_2 = pygame.image.load("assets/imgs/gohan(Youth)/gohan_youth.png")
		self.char_2_selected = pygame.image.load("assets/imgs/gohan(Youth)/gohan_select.png")		
		self.start_button = pygame.image.load("assets/icons/start_button.png").convert_alpha()
		self.mouse_position = pygame.mouse.get_pos()


	def draw_text(self, text, x, y):

		image = self.text_font.render(text, True, self.WHITE)
		self.WINDOW.blit(image, (x, y))

	def draw_names(self, text, x, y):

		image = self.name_font.render(text, True, self.WHITE)		
		self.WINDOW.blit(image, (x, y))

	def draw_image(self, image, x, y):

		image = pygame.transform.scale(image, (100, 132))

		self.WINDOW.blit(image, (x, y))

	def draw_selected_char(self, image, x, y):

		#image = pygame.transform.scale(self.char_1_selected, (290, 350))
		self.WINDOW.blit(image, (x, y))



	def char_select_loop(self):

		FPS = 120
		clock = pygame.time.Clock()

		while self.running:

			self.check_events()
			self.SURFACE.fill(self.COLOUR)
			self.WINDOW.blit(self.SURFACE, (0,0))
			self.WINDOW.blit(self.bg_scaled, (0,0))
			self.WINDOW.blit(self.symbol_scaled, (340,100))
			self.WINDOW.blit(self.vs_scaled, (530, 200))
			self.draw_text("Select your character!", 340, 0)
			self.draw_text("P1: ", 50, 420)
			self.draw_text("P2: ",790, 420)
			self.draw_text("P1: ", 300, 50)
			self.draw_text(" :P2", 810, 50)

			
			start_button = Button(500, 380, self.start_button, 2)
			if start_button.draw_button(self.WINDOW):
				print("start button pressed")

			


			#player 1

			#kid goku:D

			kid_goku_button = Button(50, 470, self.button, 1.25)
			self.draw_image(self.char_1, 63, 478)
			print(kid_goku_button.position)
			

			if kid_goku_button.draw_button(self.WINDOW):

				print("pressed!")
				
				self.choose_state == "kid_goku"
				
				if self.choose_state == "kid_goku":
					self.draw_text("ready!", 355, 50)


			if kid_goku_button.rect.collidepoint(kid_goku_button.position):
				self.draw_selected_char(self.char_1_selected, 50, 35)
				self.draw_names("Goku (Youth)", 100, 424)

			#gohan SSJ2

			gohan_button = Button(176, 470, self.button, 1.25)
			self.draw_image(self.char_2, 189, 478)

			if gohan_button.draw_button(self.WINDOW):

				print("pressed")

				self.choose_state = "gohan"

				if self.choose_state == "gohan":
					self.draw_text("ready!", 355, 50)

			if gohan_button.rect.collidepoint(gohan_button.position):
				self.draw_selected_char(self.char_2_selected, 10, 50)
				self.draw_names(" SSJ2 Gohan (Youth)", 100, 424)


			#player 2

			#kid goku:D

			kid_goku_button_2 = Button(1020, 470, self.button, 1.25)			
			self.draw_image(self.char_1, 1033, 478)

			if kid_goku_button_2.draw_button(self.WINDOW):

				print("pressed!")

				self.choose_state_2 == "kid_goku_2"

				if self.choose_state_2 == "kid_goku_2":
					self.draw_text("ready!", 670, 50)

			if kid_goku_button_2.rect.collidepoint(kid_goku_button_2.position):
				self.draw_selected_char(self.char_1_selected, 900, 35)
				self.draw_names("Goku (Youth)", 845, 424)

			#gohan
			gohan_button_2 = Button(893, 470, self.button, 1.25)
			self.draw_image(self.char_2, 906, 478)

			if gohan_button_2.draw_button(self.WINDOW):

				print("pressed!")

				self.choose_state_2 = "gohan_2"

				if self.choose_state_2 == "gohan_2":
					self.draw_text("ready!", 670, 50)

			if gohan_button_2.rect.collidepoint(gohan_button_2.position):
				self.draw_selected_char(self.char_2_selected, 850, 50)
				self.draw_names("SSJ2 Gohan (Youth)", 855, 424)




			pygame.display.update()
			clock.tick(FPS)

		pygame.quit()

	#event handler
	def check_events(self):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False


#char_select = CharSelect(Button)
#while char_select.entered == True:

	#char_select.char_select_loop()

pygame.quit()
