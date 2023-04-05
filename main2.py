#!/usr/bin/env python

#from __future__ import print_function, division
import pygame, os, random, socket
from pygame.locals import*

# udp listening stuff
UDP_IP="192.168.0.249"
UDP_PORT=58618
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(0)

# where to start and end the items
STARTROW=-50
ENDROW=825
# the rows (the Y coordinate)
ROW1=152
ROW2=315
ROW3=490
x_click=0	# x mouse click (current)
y_click=0	# y mouse click (current)
x_last=0	# last x mouse click (for drawing)
y_last=0	# last y mouse click (for drawing)
# no points starting off
player_points=0
# hit counter for displaying the circle where shot (dont change this)
hit=0
miss=0
# color definitions
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
BROWN    = (  99,  66,   0)
# game screen size
SCREEN_WIDTH=800
SCREEN_HEIGHT=600
# our timer
time = 30		# seconds on the clock
gameover=0              # is the game over?
# for particle explosions
FORCE_OF_GRAVITY = 19.81 # in pixel per second
fragmentgroup = pygame.sprite.Group()
allgroup = pygame.sprite.LayeredUpdates() # more sophisticated than simple group

class Fragment(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = [0.0,0.0]
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.image = pygame.Surface((10,10))
        self.image.set_colorkey(BLACK) # black transparent
        pygame.draw.circle(self.image, BROWN, (5,5), random.randint(2,5))
#        pygame.draw.circle(self.image, (random.randint(1,64),0,0), (5,5), random.randint(2,5))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos #if you forget this line the sprite sit in the topleft corner
        self.lifetime = 1 + random.random()*5 # max 6 seconds
        self.time = 0.0
        self.fragmentmaxspeed = 20 # try out other factors !
        self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
        self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)

    def update(self, seconds):
        self.time += seconds
#	print(self.time)
        if self.time > self.lifetime:
            self.kill()
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds
        #self.dy += FORCE_OF_GRAVITY # gravity suck fragments down
        self.rect.centerx = round(self.pos[0],0)
        self.rect.centery = round(self.pos[1],0)

class duck(pygame.sprite.Sprite):
    image = None
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        if duck.image is None:
            # this is the first time to load the image
            duck.image = pygame.image.load("GameDuck_Normal_Black.png")
	    duck.image.set_colorkey(WHITE)
            duck.flip_img = pygame.transform.flip(self.image, True, False)   # the flipped image too
        self.image = duck.image
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.name = "Duck"               # say my name!  (heisenberg)  You're god damn right!
        self.direction = "r"            # this is either r or l (right or left)
        self.speed = 5                  # this will vary depending on what your FPS is set to
        self.img_x = self.image.get_rect().size[0]      # get the width of our image
        self.img_y = self.image.get_rect().size[1]      # get the height of our image
        self.points = 10
    def update(self):
        if self.direction == "r":       # do the calculations if headed right
            screen.blit((self.flip_img),(self.rect.x,self.rect.y))   # place it on the screen
            self.rect.x += self.speed        # move the x at whatever speed to the right
            if self.rect.x > ENDROW:         # if we get to the end of the line, start over
                self.rect.x = STARTROW
        if self.direction == "l":       # do the calculations if headed left
            screen.blit((self.image),(self.rect.x,self.rect.y))
            self.rect.x -= self.speed        # move the x at whatever speed to the right
            if self.rect.x < STARTROW:
                self.rect.x = ENDROW
        self.check_hit()                # call the check_hit function evertime we update
    def check_hit(self):                # function to check the hit
        global hit_target, x_click, y_click, broken_glass, player_points   # use global to pull in main variables into the class
        if x_click > self.rect.x and x_click < (self.rect.x + self.img_x):        # if we're within the x range
                if y_click > self.rect.y and y_click < (self.rect.y + self.img_y):        # if we're withing the y range
                    #print "Bang! - ", self.name
                    quack_wav.play()         # play a sound
                    player_points += self.points
                    hit_target=True

class bottle(pygame.sprite.Sprite):
    image = None
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        if bottle.image is None:
            # this is the first time to load the image
            bottle.image = pygame.image.load("bottle.png")
	    bottle.image.set_colorkey(WHITE)
            bottle.flip_img = pygame.transform.flip(self.image, True, False)   # the flipped image too
        self.pos = [0,0] # dummy value to create a blank list
        self.image = bottle.image
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.pos[0] = self.rect.x
        self.pos[1] = self.rect.y
        self.name = "Bottle"               # say my name!  (heisenberg)  You're god damn right!
        self.direction = "r"            # this is either r or l (right or left)
        self.speed = 5                  # this will vary depending on what your FPS is set to
        self.img_x = self.image.get_rect().size[0]      # get the width of our image
        self.img_y = self.image.get_rect().size[1]      # get the height of our image
        self.points = 25                                # 25 points!
    def update(self):
        if self.direction == "r":       # do the calculations if headed right
            screen.blit((self.image),(self.rect.x,self.rect.y))   # place it on the screen
            self.rect.x += self.speed        # move the x at whatever speed to the right
            if self.rect.x > ENDROW:         # if we get to the end of the line, start over
                self.rect.x = STARTROW
        if self.direction == "l":       # do the calculations if headed left
            screen.blit((self.flip_img),(self.rect.x,self.rect.y))
            self.rect.x -= self.speed        # move the x at whatever speed to the right
            if self.rect.x < STARTROW:
                self.rect.x = ENDROW
        self.check_hit()                # call the check_hit function evertime we update
    def check_hit(self):                # function to check the hit
        global hit_target, player_points, x_click, y_click, broken_glass   # use global to pull in main variables into the class
        if x_click > self.rect.x and x_click < (self.rect.x + self.img_x):        # if we're within the x range
                if y_click > self.rect.y and y_click < (self.rect.y + self.img_y):        # if we're withing the y range
                    #print "Bang! - ", self.name
                    if self.direction=="r":
                        self.direction="l"
                    elif self.direction=="l":
                        self.direction="r"
                    broken_glass.play()         # play a sound
                    #increment points
                    player_points += self.points
                    hit_target=True
                    add_a_bottle()
                    for _ in range(random.randint(10,25)):
                        Fragment((self.rect.x+(self.img_x/2),self.rect.y+(self.img_y/2)))
                    self.kill()  	# bye bye bottle

def flip_coin():  #returns a true or false
    i = random.randrange(2)
    if i == 0:
        return True
    else:
        return False

def random_row():
    i = random.randrange(3) + 1
    if i == 1:
        row=ROW1
    if i == 2:
        row=ROW2
    if i == 3:
        row=ROW3
    return row

def write_text(txt):
    text = basicFont.render(txt, True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.topleft = [SCREEN_WIDTH-textRect.width, SCREEN_HEIGHT-textRect.height]
    screen.blit(text, textRect)

def add_a_duck():
    # "adding a duck"
    quack = duck([0,0])
    quack.rect.x = random.randrange(SCREEN_WIDTH)
    quack.rect.y = random_row() - quack.img_y
    quack.direction = "l"
    quack.speed = random.randrange(3,8)
    block_list.add(quack)
    all_sprites_list.add(quack)

def add_a_bottle():
    # "adding a bottle"
    da_bottle = bottle([90, 95])
    da_bottle.rect.x = random.randrange(800)
    da_bottle.rect.y = random_row() - da_bottle.img_y
    da_bottle.speed = random.randrange(3,8)
    da_bottle.direction = "l"
    block_list.add(da_bottle)
    all_sprites_list.add(da_bottle)

os.environ['SDL_VIDEO_CENTERED'] = '1'	# start centered
pygame.init()	# game init

flags = DOUBLEBUF	# i read DOUBLEBUF helps speed, use DOUBLEBUF | FULLSCREEN if needed
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, 32)		# 800x600
pygame.display.set_caption("Carnival")

screen.fill(BLACK)	# black bg color
#pygame.image.load("bg.png"), (0,0)	# load bg

#setup the font
basicFont = pygame.font.SysFont(None, 35)

# setup mixer and cfg volume
pygame.mixer.init(44100, -16, 2, 1024)
pygame.mixer.music.set_volume(0.8)
# setup our sounds
broken_glass=pygame.mixer.Sound("glass_break.wav")
quack_wav=pygame.mixer.Sound("quack.wav")

clock = pygame.time.Clock()  # start the game clock

# setup our groups for controlling and updating
block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
fragmentgroup = pygame.sprite.Group()

# setup our game timer
clock_time = time
pygame.time.set_timer(USEREVENT+1, 1000)

# timer holder (press T to toggle it)
holdtime=False

Fragment.groups = fragmentgroup, allgroup

for i in range(5):
    add_a_bottle()
for _ in range(15):
    add_a_duck()

FPS = 60
millimax = 0

while True:	# main loop
    hit_target=False
    check_target=False
    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    if milliseconds > millimax:
        millimax = milliseconds
    seconds = milliseconds / 200.0 # seconds passed since last frame

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            x_click, y_click = pygame.mouse.get_pos()	# get our mouse position
            x_last, y_last = x_click, y_click
            hit=50	# change this to leave the shot dot on the screen longer
            check_target = True
	elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_q: 	# press q or ESC to exit
                pygame.quit()
                exit()
            elif event.key == K_t:  # toggle timer hold
                if holdtime: 
                    print("Timer resumed")
                    holdtime = False
                elif not holdtime: 
                    print("Timer on hold")
                    holdtime = True
        if event.type == USEREVENT+1:
            if gameover != 1:
                if not holdtime: clock_time -= 1

    # serial shooting
    try:
        data, addr = sock.recvfrom(1024)
        print "data: ", data
        our_x=int(data.split('-')[3].split('.')[0])
        our_y=int(data.split('-')[4].split('.')[0])
        x_click, y_click = our_x, our_y  # get shooters position
        x_last, y_last = x_click, y_click
        hit=50	# change this to leave the shot dot on the screen longer
        check_target = True
        print our_x
        print our_y
        HIT=50
    except:
        ''' nothing here '''


    # number of times to process this loop a second, also frames per seconds
    clock.tick(FPS)

    # start of drawing
    screen.fill(BLACK)
    #the lines
    pygame.draw.rect(screen, BLUE, (0,ROW1,SCREEN_WIDTH,10), 0)  # first row
    pygame.draw.rect(screen, BLUE, (0,ROW2,SCREEN_WIDTH,10), 0)
    pygame.draw.rect(screen, BLUE, (0,ROW3,SCREEN_WIDTH,10), 0) 
    #print clock.get_fps()
    if gameover == 0: 
        block_list.update()
        allgroup.update(seconds)
        allgroup.draw(screen)
    #all_sprites_list.draw(screen)
    #screen.blit(pygame.image.load("bg.png"), (0,0))  # draw the bg
    if hit > 0:  # loop for drawing the red hit circle
        pygame.draw.circle(screen, RED, (x_last, y_last), 10)
        hit -= 2  # change this too for duration of red dot on screen

    # check for ending time
    if clock_time == 0 and gameover != 1:
        print("GAME OVER")
        gameover=1
	all_sprites_list.remove()

    if gameover == 1:
        text = basicFont.render("Click here to retry", True, WHITE, BLUE)
        textRect = text.get_rect()
        textRect.topleft = [(SCREEN_WIDTH/2)-(textRect.width/2),(SCREEN_HEIGHT/2)-(textRect.height/2)]
        screen.blit(text, textRect)
        if x_click > textRect.left and x_click < textRect.right:
            if y_click > textRect.top and y_click < textRect.bottom:
                print("Game on!")
                # reset all of our variables and re-init our sprites
                clock_time = time
                player_points = 0
                gameover = 0
                miss=0

    # clear out clicks!  This prevents a bottle/duck/whatever from getting more hits from scrolling
    x_click=None
    y_click=None

    if gameover == 0:    # not in game over mode
        if check_target:    # do we need to check for a miss?
            if not hit_target:   # did we really miss?
                miss += 1       # yep, we did
    # put the score on top of everything
    write_text('Points:' + str(player_points) + "   Missed:" + str(miss) + "   Timer:" + str(clock_time))
    pygame.display.update() # throw it all on screen

