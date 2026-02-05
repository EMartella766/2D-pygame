import pygame
from MainMenu import MainLobby
from CharSelect import CharSelect
from buttons import Button

pygame.init()

main_lobby = MainLobby()	

while main_lobby.menu_state == 'main_menu':

	main_lobby.main_lobby_loop()


char_select = CharSelect()

while main_lobby.menu_state == 'char_select':

	char_select.char_select_loop()

