from pygame import *
from sys import *
from random import randint, choice
font.init()
# load functions for working with fonts separately
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (0, 128, 0))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)

#music
mixer.init()
fire_sound = mixer.Sound("fire.ogg")
pick_sound = mixer.Sound("click.ogg")

#pictures:
img_back = "galaxy.jpg" # game background
img_bullet = "bullet.png" # bullet
img_bullet1 = "bullet1.png"# enemy bullet
img_hero = "hero.png" # character
img_enemy = "enemy.png" # enemy
img_pw1 = "power_up1.png" # +1 life
life = 3 # life
score = 0 # ships hit
goal = 20 # how many ships need to be hit to win
min_life = 0
# Create the window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the fonts
font = font.Font(None, 36)

# Set up the buttons
button_width = 200
button_height = 50
button_padding = 20

play_button = Rect(
    win_width // 2 - button_width // 2,
    win_height // 2 - button_height - button_padding,
    button_width,
    button_height,
)
quit_button = Rect(
    win_width // 2 - button_width // 2,
    win_height // 2,
    button_width,
    button_height,
)



class GameSprite(sprite.Sprite):
  # class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # We call the class constructor (Sprite):
        sprite.Sprite.__init__(self)
        self.bullets = []
        # each sprite must store an image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # each sprite must store the rect property it is inscribed in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # method that draws the character in the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# main player class
class Player(GameSprite):
    # method for controlling the sprite with keyboard arrows
    def update(self):
        self.speed = 20
        keys = key.get_pressed()
        if keys[K_DOWN] and self.rect.y < 430:
            self.rect.y += self.speed
        if keys[K_UP]and self.rect.y > 150:
            self.rect.y -= self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # the "fire" method (use the player's place to create a bullet there)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) 
class Enemy(GameSprite):
    side = 'left'
    side1 = 'up'

    def update(self):
        self.speed = 5
        val = randint(1,2)
        if val == 1:
            if self.rect.x  <= 10:
                self.side = 'right'
            if self.rect.x >= 615:
                self.side = 'left'

            if self.side == 'left':
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
        else:
            if self.rect.y <= 0:
                self.side1 = 'down'

            if self.rect.y >=200:
                self.side1 = 'up'
            
            if self.side1 == 'up':
                self.rect.y -= self.speed

            else:
                self.rect.y += self.speed   
        # disappears if it reaches the edge of the screen
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
    def fire1(self):
        bullet1 = Bullet1(img_bullet1, self.rect.centerx, self.rect.bottom, 5, 10, -15)
        bullets2.add(bullet1)
    def fire2(self):
        powerup1 = move(img_pw1, self.rect.centerx, self.rect.bottom, 40, 40, -15)
        powers.add(powerup1)
# bullet sprite class   
class Bullet(GameSprite):
    # enemy movement
    def update(self):
        self.speed = 20
        self.rect.y -= self.speed
        # disappears if it reaches the edge of the screen
        if self.rect.y < 0:
            self.kill()
class Bullet1(GameSprite):
    def update(self):
        
        self.speed = 5
        self.rect.y += self.speed
        # disappears if it reaches the edge of the screen
        if self.rect.y > 500:
            self.kill()
class move(GameSprite):
    def update(self):
        
        self.speed = 3
        self.rect.y += self.speed
# disappears if it reaches the edge of the screen
        if self.rect.y > 500:
            self.kill()

# create sprites
ship = Player(img_hero, 50, win_height - 80, 60, 60, 60)
 
# creating a group of enemy sprites
monsters = sprite.Group()
for i in range(0, 3):
    monster = Enemy(img_enemy, randint(80, win_width - 80), 40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()
bullets2 = sprite.RenderPlain()
bullet = sprite.Group()
powers = sprite.RenderClear()
# the "game over" variable: as soon as it is True, the sprites stop working in the main loop
finish = False
# the flag is cleared with the close window button
firem = True
running = True
run = True
# starting screen and menu
def menu():
    global running, run
    
    window.fill(BLACK)
    while running:
        run = False
        for f in event.get():
            if f.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()

                if play_button.collidepoint(mouse_pos):
                    pick_sound.play()
                    run = True
                    running = False
                if quit_button.collidepoint(mouse_pos):
                    pick_sound.play()
                    quit()
                    exit()

        # Clear the screen
        window.fill(BLACK)
        # Draw the buttons
        draw.rect(window, WHITE, play_button)
        draw.rect(window, WHITE, quit_button)

        # Draw the button labels
        play_text = font.render("Play Game", True, BLACK)
        quit_text = font.render("Quit", True, BLACK)

        window.blit(play_text, (play_button.x + 10, play_button.y + 10))
        window.blit(quit_text, (quit_button.x + 10, quit_button.y + 10))
        display.update()


while run:
    menu()
    # the press the Close button event
    for e in event.get():
        if e.type == QUIT:
            run = False
        # press on the space bar event - the sprite fires
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

  # the game itself: sprite actions, checking the rules of the game, redrawing
    if not finish:
        # refresh background
        window.blit(background,(0,0))
        # writing text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("life: " + str(life), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # producing sprite movements
        ship.update()
        monsters.update()
        bullets.update()
        bullets2.update()
        for powerup in powers:
            powerup.update()

        # updating them at a new location on each iteration of the loop
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        bullets2.draw(window)
        powers.draw(window)
        # pausing the game
        d = key.get_pressed()
        if d[K_TAB]:
            run = False
            running = True
            menu()

        
 
        # bullet-monster collision check (both monster and bullet disappear upon touching)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            v = randint(1,5)
            if v == 3:
                monster.fire2()
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), 40, 80, 50, randint(1, 5))
            monsters.add(monster)
        # life and if bullet hits you you lose 
        if life == 0:
            finish = True # lost, set the background and no more sprite control.
            window.blit(lose, (200, 200))
        if sprite.spritecollide(ship, bullets2, True):
            # ship = Player(img_hero, 50, win_height - 80, 60, 60, 60)
            life = life - 1 
        # win check: how many points did you score?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        if sprite.spritecollide(ship, powers, True):
            life = life + 1


        g = randint(1,20)
        for monster in monsters:
            if g == 4:
                monster.fire1()
        display.update()
    # the loop runs every 0.05 seconds
    time.delay(50)
