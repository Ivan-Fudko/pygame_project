import pygame
import random
import time
from pygame.font import Font
import levels



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


level = 0
dbase = pygame.image.load('images/dbase.png')
water = pygame.image.load('images/water.png')
fs = pygame.image.load('images/fs.png')
kir = pygame.image.load('images/kir.png')
beton = pygame.image.load('images/beton.png')
forest = pygame.image.load('images/forest.png')
base = pygame.image.load('images/base.png')
ggu = pygame.image.load('images/ggu.png')
bullet_up = pygame.image.load('images/ammo.png')
e = pygame.image.load('images/e.png')
bb = pygame.image.load('images/bboom.png')
bl = pygame.image.load('images/blopatka.png')
bz = pygame.image.load('images/bzvezdochka.png')
e_rect = e.get_rect()
e_rect.width = e_rect.height
slide_rect = e.get_rect()
slide_rect.width = slide_rect.height
bullet_down = pygame.transform.rotate(bullet_up, 180)
bullet_right = pygame.transform.rotate(bullet_up, 90)
bullet_left = pygame.transform.rotate(bullet_up, 270)
booms = []
shoots = []
plshoot = 1
basehp = 2
initbase = True
lopatka = 0



lev = levels.lev[level]
matrix = lev

class Base:
    def __init__(self, basehp):
        self.basehp = basehp
        initbase = False

    def destroy(self):
        if self.basehp == 0:
            base = dbase

class Boom:
    def __init__(self, e_rectcenter):
        self.explosion = e
        self.e_rect = e_rect
        self.e_rect.center = e_rectcenter
        self.slide_rect = slide_rect
        self.ilolo = 0

    def render(self, screen):
        screen.blit(e, self.e_rect, self.slide_rect)

    def step(self):
        self.ilolo += 1
        self.slide_rect.x = (self.ilolo // 2) * 20

    def destroy(self):
        if self.ilolo > 7:
            return True
        return False


class Shoot:
    def __init__(self, pos1, pos2, orient, sight):
        self.x = pos1
        self.y = pos2
        self.orient = orient
        self.speed = 2
        self.damage = 15
        self.sight = sight
        self.rect = pygame.Rect(self.x * 2 + 5, self.y * 2 + 5, 10, 10)

    def step(self):
        if self.orient == 1:
            self.y -= self.speed
        elif self.orient == 2:
            self.y += self.speed
        elif self.orient == 3:
            self.x -= self.speed
        elif self.orient == 4:
            self.x += self.speed
        self.rect = pygame.Rect(self.x * 2 + 5, self.y * 2 + 5, 10, 10)

    def destroy(self, matrix):
        if self.orient == 1:
            up = matrix[self.y // 10 + 1][self.x // 10]
            if up == 1:
                booms.append(Boom((self.x * 2 + 10, self.y * 2 + 20)))
                return True
            elif up == 6:
                booms.append(Boom((self.x * 2 + 10, self.y * 2 + 10)))
                bbase.basehp -= 1
                return True
            elif up == 2:
                matrix[self.y // 10 + 1][self.x // 10] = 0
                play.wall = 0
                booms.append(Boom((self.x * 2 + 10, self.y * 2 + 10)))
                return True
            else:
                return False
        elif self.orient == 2:
            down = matrix[self.y // 10][self.x // 10]
            if down == 1:
                booms.append(Boom((self.x * 2 + 10, self.y * 2)))
                return True
            elif down == 6:
                booms.append(Boom((self.x * 2 + 10, self.y * 2 + 10)))
                bbase.basehp -= 1
                return True
            elif down == 2:
                matrix[self.y // 10][self.x // 10] = 0
                play.wall = 0
                booms.append(Boom((self.x * 2 + 10, self.y * 2 + 10)))
                return True
            else:
                return False
        elif self.orient == 3:
            left = matrix[self.y // 10][self.x // 10 + 1]
            if left == 1:
                booms.append(Boom((self.x * 2 + 20, self.y * 2 + 10)))
                return True
            elif left == 6:
                booms.append(Boom((self.x * 2 + 14, self.y * 2 + 10)))
                bbase.basehp -= 1
                return True
            elif left == 2:
                matrix[self.y // 10][self.x // 10 + 1] = 0
                play.wall = 0
                booms.append(Boom((self.x * 2 + 14, self.y * 2 + 10)))
                return True
            else:
                return False
        elif self.orient == 4:
            right = matrix[self.y // 10][self.x // 10]
            if right == 1:
                booms.append(Boom((self.x * 2, self.y * 2 + 10)))
                return True
            elif right == 6:
                booms.append(Boom((self.x * 2 + 10, self.y * 2 + 10)))
                bbase.basehp -= 1
                return True
            elif right == 2:
                matrix[self.y // 10][self.x // 10] = 0
                play.wall = 0
                booms.append(Boom((self.x * 2 + 10, self.y * 2 + 10)))
                return True
            else:
                return False

    def render(self, screen):
        if self.orient == 1:
            screen.blit(bullet_up, (self.x * 2, self.y * 2))
        elif self.orient == 2:
            screen.blit(bullet_down, (self.x * 2, self.y * 2))
        elif self.orient == 3:
            screen.blit(bullet_right, (self.x * 2, self.y * 2))
        elif self.orient == 4:
            screen.blit(bullet_left, (self.x * 2, self.y * 2))

class Bonus:
    def __init__(self, matrix):
        global bb, bl, bz
        self.type = random.randint(1, 3)
        if self.type == 1:
            self.image = bb
        elif self.type == 2:
            self.image = bl
        elif self.type == 3:
            self.image = bz
        self.x = 0
        self.y = 0
        while matrix[self.y][self.x] != 0:
            self.x = random.randint(1, 23)
            self.y = random.randint(1, 23)
        self.rect = pygame.Rect((self.x * 20, self.y * 20), (20, 20))

    def render(self, screen):
        screen.blit(self.image, (self.x * 20, self.y * 20))


def pole(a):
    x = 0
    y = 0
    i = 0
    while i < 625:
        if a[y][x] == 0:
            screen.blit(fs, (x * 20, y * 20))
        elif a[y][x] == 1:
            screen.blit(beton, (x * 20, y * 20))
        elif a[y][x] == 2:
            screen.blit(kir, (x * 20, y * 20))
        elif a[y][x] == 4:
            screen.blit(water, (x * 20, y * 20))
        elif a[y][x] == 6:
            screen.blit(base, (x * 20, y * 20))

        elif a[y][x] == 7:
            screen.blit(fs, (x * 20, y * 20))
        x += 1
        if x > 24:
            x = 0
            y += 1
        i += 1


class Player:
    def __init__(self, pos1, pos2):
        self.ggx = pos1 * 10
        self.ggy = pos2 * 10
        self.orient = 1
        self.hp = 25
        self.lives = 3
        self.move = 0
        self.ggu = ggu
        self.ggd = pygame.transform.rotate(self.ggu, 180)
        self.ggl = pygame.transform.rotate(self.ggu, 90)
        self.ggr = pygame.transform.rotate(self.ggu, 270)
        self.gg = self.ggu
        self.wall = 0
        self.rect = pygame.Rect(self.ggx * 2, self.ggy * 2, 20, 20)
        self.power = 2

    def moveP(self, key):
        if self.orient == 1 and self.wall != 1:
            if key == 1:
                self.ggy -= 1
                self.wall = 0
            elif key != 0:
                self.orient = key
                self.move = 0
            if (self.ggy % 10) == 0:
                    key = 0
                    self.move = 0
            elif key == 0:
                    self.ggy -= 1
                    self.move = 1

        elif self.orient == 2 and self.wall != 2:
            if key == 2:
                self.ggy += 1
                self.wall = 0
            elif key != 0:
                self.orient = key
                self.move = 0
            if (self.ggy % 10) == 0:
                key = 0
                self.move = 0

            elif key == 0:
                self.ggy += 1
                self.move = 1

        elif self.orient == 3 and self.wall != 3:
            if key == 3:
                self.ggx -= 1
                self.wall = 0
            elif key != 0:
                self.orient = key
                self.move = 0
            if (self.ggx % 10) == 0:
                key = 0
                self.move = 0

            elif key == 0:
                self.ggx -= 1
                self.move = 1

        elif self.orient == 4 and self.wall != 4:
            if key == 4:
                self.ggx += 1
                self.wall = 0
            elif key != 0:
                self.orient = key
                self.move = 0
            if (self.ggx % 10) == 0:
                key = 0
                self.move = 0

            elif key == 0:
                self.ggx += 1
                self.move = 1
        else:
            self.move = 0
        self.rect = pygame.Rect(self.ggx * 2, self.ggy * 2, 20, 20)

    def walls(self, matrix):
        if (self.ggy % 10) == 0 and (self.ggx % 10) == 0:
            Y_axisd = matrix[self.ggy // 10 + 1][self.ggx // 10]
            Y_axisu = matrix[self.ggy // 10 - 1][self.ggx // 10]
            X_axisr = matrix[self.ggy // 10][self.ggx // 10 + 1]
            X_axisl = matrix[self.ggy // 10][self.ggx // 10 - 1]
            if (Y_axisd == 1 or Y_axisd == 2 or Y_axisd == 4 or Y_axisd == 6) and self.orient == 2:
                self.wall = 2
            elif (Y_axisu == 1 or Y_axisu == 2 or Y_axisu == 4 or Y_axisu == 6) and self.orient == 1:
                self.wall = 1
            elif (X_axisr == 1 or X_axisr == 2 or X_axisr == 4 or X_axisr == 6) and self.orient == 4:
                self.wall = 4
            elif (X_axisl == 1 or X_axisl == 2 or X_axisl == 4 or X_axisl == 6) and self.orient == 3:
                self.wall = 3

    def render(self, screen):
        screen.blit(self.gg, (self.ggx * 2, self.ggy * 2))


ggx = 9
ggy = 22
i = 0
shet = 0
plives = 3
zet = 0
player = 1
orient = 1
move = 0
enemyes = []
player = 1
player2 = 20
fight = 0
p2count = 20
kleo = 100
key = 0
enable = 0
reloads = 60
bonuses = []
shbonus = random.randint(300, 700)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and play.orient == 3 and play.wall != 3:
                key = 3
                enable = 1
            elif event.key == pygame.K_RIGHT and play.orient == 4 and play.wall != 4:
                key = 4
                enable = 1
            elif event.key == pygame.K_UP and play.orient == 1 and play.wall != 1:
                key = 1
                enable = 1
            elif event.key == pygame.K_DOWN and play.orient == 2 and play.wall != 2:
                key = 2
                enable = 1
            elif event.key == pygame.K_LEFT and play.orient != 3 and enable == 0 and play.move == 0:
                play.orient = 3
                play.gg = play.ggl
            elif event.key == pygame.K_RIGHT and play.orient != 4 and enable == 0 and play.move == 0:
                play.orient = 4
                play.gg = play.ggr
            elif event.key == pygame.K_UP and play.orient != 1 and enable == 0 and play.move == 0:
                play.orient = 1
                play.gg = play.ggu
            elif event.key == pygame.K_DOWN and play.orient != 2 and enable == 0 and play.move == 0:
                play.orient = 2
                play.gg = play.ggd
            elif event.key == pygame.K_SPACE:
                if fight <= 0:
                    shoots.append(Shoot(play.ggx, play.ggy, play.orient, 1))
                    if play.power == 3:
                        plshoot = 9
                    elif play.power == 4:
                        plshoot = 19
                    fight = 20
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and play.orient == 3:
                key = 0
                enable = 0
            elif event.key == pygame.K_RIGHT and play.orient == 4:
                key = 0
                enable = 0
            elif event.key == pygame.K_UP and play.orient == 1:
                key = 0
                enable = 0
            elif event.key == pygame.K_DOWN and play.orient == 2:
                key = 0
                enable = 0

    fight -= 1
    if initbase == True:
        bbase = Base(basehp)
        initbase = False
    if plshoot == 5:
        shoots.append(Shoot(play.ggx, play.ggy, play.orient, 1))
        plshoot = 1
    elif plshoot == 10:
        shoots.append(Shoot(play.ggx, play.ggy, play.orient, 1))
        plshoot -= 1
    elif plshoot == 1:
        pass
    else:
        plshoot -= 1

    if player == 1:
        player -= 1
        play = Player(ggx, ggy)

    play.moveP(key)
    play.walls(matrix)

    if shbonus == 0:
        bonuses.append(Bonus(matrix))
        shbonus = random.randint(300, 700)
    else:
        shbonus -= 1

    m1m = 0
    while m1m < len(shoots):
        m2m = 0
        while m2m < len(shoots):
            dx = shoots[m2m].x - shoots[m1m].x
            dy = shoots[m2m].y - shoots[m1m].y
            if dx < 0:
                dx = -dx
            if dy < 0:
                dy = -dy
            if shoots[m2m].sight == shoots[m1m].sight:
                pass
            elif (shoots[m2m].x == shoots[m1m].x and shoots[m2m].y == shoots[m1m].y) or (dx < 3 and dy < 3):
                booms.append(Boom((shoots[m1m].x * 2 + 10, shoots[m1m].y * 2 + 10)))
                shoots.pop(m2m)
                shoots.pop(m1m)

            m2m += 1
        m1m += 1
    fps = (str((float(int(clock.get_fps() * 10)) // 10)))
    fps2 = 'fps: ' + fps

    text = font.render(fps2, 1, (255, 255, 10))
    textpos = text.get_rect()
    textpos = (510, 30)

    text2 = font2.render(u'Осталось врагов: ' + str(p2count), 1, (255, 255, 10))
    textpos2 = text2.get_rect()
    textpos2 = (510, 60)

    text3 = font3.render(u'Вы победили!', 1, (255, 10, 10))
    textpos3 = text3.get_rect(centerx=(screen.get_width() - 140) // 2, centery=screen.get_height() // 2)
    text4 = font.render(u'Уровень: ' + str(level + 1), 1, (255, 255, 10))
    textpos4 = text4.get_rect()
    textpos4 = (510, 5)
    text5 = font3.render(u'Вы проиграли!', 1, (255, 10, 10))
    textpos5 = text5.get_rect(centerx=(screen.get_width() - 140) // 2, centery=screen.get_height() // 2)

    text9 = font3.render(u'Вы прошли игру!', 1, (255, 10, 10))
    textpos9 = text5.get_rect(centerx=(screen.get_width()) // 2, centery=screen.get_height() // 2)

    text6 = font2.render(u'Уровень игрока: ' + str(play.power - 1), 1, (255, 255, 10))
    textpos6 = text2.get_rect()
    textpos6 = (510, 80)

    text7 = font2.render(u'Здоровье игрока: ' + str(play.hp), 1, (255, 255, 10))
    textpos7 = text2.get_rect()
    textpos7 = (510, 100)

    text8 = font2.render(u'Жизни игрока: ' + str(plives), 1, (255, 255, 10))
    textpos8 = text2.get_rect()
    textpos8 = (510, 120)
    pygame.display.flip()

    for k in reversed(range(0, len(bonuses))):
        if play.rect.colliderect(bonuses[k].rect):
            if bonuses[k].type == 1:
                for i in reversed(range(0, len(enemyes))):
                    booms.append(Boom((enemyes[i].rect.center)))
                    enemyes.pop(i)
                    counten += 1
                p2count -= counten
                counten = 0
                bonuses.pop(k)
            elif bonuses[k].type == 2:
                matrix[23][11] = 1
                matrix[23][13] = 1
                matrix[22][11] = 1
                matrix[22][13] = 1
                matrix[22][12] = 1
                bonuses.pop(k)
                lopatka = 1
                lopatka_s = 300
            elif bonuses[k].type == 3:
                bonuses.pop(k)
                play.power += 1
                if play.power > 4:
                    play.power = 4
                play.hp += 5
    if lopatka == 1:
        if lopatka_s == 0:
            matrix[23][11] = 2
            matrix[23][13] = 2
            matrix[22][11] = 2
            matrix[22][13] = 2
            matrix[22][12] = 2
            lopatka = 0
        else:
            lopatka_s -= 1
    for i in reversed(range(0, len(booms))):
        booms[i].step()
        if booms[i].destroy():
            booms.pop(i)

    if zet == 0:
        play.render(screen)
    for shoot in shoots:
        shoot.render(screen)
    for i in reversed(range(0, len(shoots))):
        shoots[i].step()
        if shoots[i].destroy(matrix):
            shoots.pop(i)
    for i in reversed(range(0, len(booms))):
        booms[i].step()
        if booms[i].destroy():
            booms.pop(i)

    if zet != 0 and plives > 0:
        if zet == 20:
            play = Player(ggx, ggy)
            zet = 0
        else:
            zet += 1

    if bbase.basehp == 0:
        base = dbase

    screen.fill(black)
    pygame.draw.rect(screen, black, (0, 0, 500, 500), 5)
    pole(matrix)
    if zet == 0:
        play.render(screen)
    for shoot in shoots:
        shoot.render(screen)
    for boom in booms:
        boom.render(screen)
    for bonus in bonuses:
        bonus.render(screen)
    screen.blit(text, textpos)
    screen.blit(text2, textpos2)
    screen.blit(text4, textpos4)
    screen.blit(text6, textpos6)
    screen.blit(text7, textpos7)
    screen.blit(text8, textpos8)

    if bbase.basehp < 1 or plives < 1:
        screen.blit(text5, textpos5)
        if reloads != 0:
            reloads -= 1
        else:
            time.sleep(1)
            reloads = 60
            running = False
            go = True
    pygame.display.flip()
    clock.tick(30)