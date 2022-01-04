import pygame
import random
import time
from pygame.font import Font

pygame.init()
size = 650, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Battle Tanks')
clock = pygame.time.Clock()
black = 0, 0, 0

back = pygame.image.load('images/back.jpg')
back = pygame.transform.scale(back, (650, 650))
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 18)
font3 = pygame.font.Font(None, 64)
go = True
running = True
new_game_button = font3.render('Новая игра', 1, (255, 255, 10))
new_game_button_pos = pygame.Rect(365, 40, 247, 45)
escape_button = font3.render('Выход', 1, (255, 255, 10))
escape_button_pos = pygame.Rect(450, 100, 154, 45)


def mmenu(go):
    global new_game_button, escape_button, new_game_button_pos, escape_button_pos, running
    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                go = False
            elif event.type == pygame.MOUSEMOTION:
                if escape_button_pos.collidepoint(event.pos):
                    escape_button = font3.render('Выход', 1, (255, 0, 0))
                    new_game_button = font3.render('Новая игра', 1, (255, 255, 10))
                    game = 2
                elif new_game_button_pos.collidepoint(event.pos):
                    new_game_button = font3.render('Новая игра', 1, (255, 0, 0))
                    escape_button = font3.render('Выход', 1, (255, 255, 10))
                    game = 1
                else:
                    new_game_button = font3.render('Новая игра', 1, (255, 255, 10))
                    escape_button = font3.render('Выход', 1, (255, 255, 10))
                    game = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game == 1:
                    go = False
                    running = True
                elif game == 2:
                    go = False
                    running = False
        screen.fill(black)
        screen.blit(back, (0, 0))
        screen.blit(new_game_button, new_game_button_pos)
        screen.blit(escape_button, escape_button_pos)
        pygame.display.flip()


mmenu(go)