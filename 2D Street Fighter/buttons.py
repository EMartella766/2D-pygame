import pygame

class Button():

	def __init__(self, x, y, image, scale):
		pygame.init()
		width = image.get_width()
		height = image.get_height()
		self.button_image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))  #get image and scale it
		self.rect = self.button_image.get_rect() #get rectangle of image
		self.rect.topleft = (x, y)
		self.clicked = False
		self.position = pygame.mouse.get_pos()
		

	def draw_button(self, window):

		action = False

		#get mouse position
		self.position = pygame.mouse.get_pos()#[0] left click, [2] right click

		#print("Mouse pos", position)
		#print("Button Rect", self.rect)

		#check if mouse over button
		if self.rect.collidepoint(self.position):
			#check for mouse clicks over button
			if pygame.mouse.get_pressed()[0] == 1 and  not self.clicked:
				self.clicked = True
				#print("button clicked!")
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw buttons
		window.blit(self.button_image, (self.rect.x, self.rect.y))

		return action


#create button instances button = Button(pass in arguments)
#call method
#Button(x, y, button image asset, scale )
