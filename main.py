import pygame, os, random, socket
from pygame.locals import*
# shouldn't need to specify an ip since we're listening anyway
UDP_IP="192.168.0.125"
UDP_PORT=58618
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(0)

# where to start and end the items
STARTROW=-25
ENDROW=825
# the rows (the Y coordinate)
#ROW1=152
#ROW2=315
#ROW3=490
x_click=0	# x mouse click (current)
y_click=0	# y mouse click (current)
x_last=0	# last x mouse click (for drawing)
y_last=0	# last y mouse click (for drawing)
# no points starting off
player_points=0
# hit counter for displaying the circle where shot (dont change this)
hit=0
# color definitions
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
# game screen size
SCREEN_WIDTH=800
SCREEN_HEIGHT=600
# our timer
time = 30		# seconds on the clock
gameover=0              # is the game over?
# for particle explosions
FORCE_OF_GRAVITY = 9.81 # in pixel per second

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
            self.rect.y += self.speed
            if self.rect.y > SCREEN_HEIGHT:
                self.rect.y = -25
        if self.direction == "l":       # do the calculations if headed left
            screen.blit((self.image),(self.rect.x,self.rect.y))
            self.rect.x -= self.speed        # move the x at whatever speed to the right
            if self.rect.x < STARTROW:
                self.rect.x = ENDROW
            self.rect.y -= self.speed
            if self.rect.y < -25:
                self.rect.y = SCREEN_HEIGHT
        self.check_hit()                # call the check_hit function evertime we update
    def check_hit(self):                # function to check the hit
        global x_click, y_click, broken_glass, player_points   # use global to pull in main variables into the class
        if x_click > self.rect.x and x_click < (self.rect.x + self.img_x):        # if we're within the x range
                if y_click > self.rect.y and y_click < (self.rect.y + self.img_y):        # if we're withing the y range
                    #print "Bang! - ", self.name
                    if self.direction=="r":
                        self.direction="l"
                    elif self.direction=="l":
                        self.direction="r"
                    quack_wav.play()         # play a sound
                    player_points += self.points

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
            self.rect.y -= self.speed
            if self.rect.y < -25:
                self.rect.y = SCREEN_HEIGHT
        if self.direction == "l":       # do the calculations if headed left
            screen.blit((self.flip_img),(self.rect.x,self.rect.y))
            self.rect.x -= self.speed        # move the x at whatever speed to the right
            if self.rect.x < STARTROW:
                self.rect.x = ENDROW
            self.rect.y += self.speed
            if self.rect.y > SCREEN_HEIGHT:
                self.rect.y = -25
        self.check_hit()                # call the check_hit function evertime we update
    def check_hit(self):                # function to check the hit
        global player_points, x_click, y_click, broken_glass   # use global to pull in main variables into the class
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
                    add_a_bottle()
                    #for _ in range(random.randint(3,15)):
                    #    Fragment(self.pos)
                    self.kill()  	# bye bye bottle


def add_a_duck():
    print "adding a duck"
    quack = duck([0,0])
    quack.rect.x = random.randrange(SCREEN_WIDTH)
    quack.rect.y = random.randrange(SCREEN_HEIGHT-70)
    quack.speed = random.randrange(3,8)
    quack.direction = "l"
    block_list.add(quack)
    all_sprites_list.add(quack)

def add_a_bottle():
    print "adding a bottle"
    da_bottle = bottle([90, 95])
    da_bottle.rect.x = random.randrange(800)
    da_bottle.rect.y = random.randrange(600)
    da_bottle.speed = random.randrange(3,8)
    da_bottle.direction = "r"
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

for i in range(10):
    add_a_duck()
    add_a_bottle()

while True:	# main loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            x_click, y_click = pygame.mouse.get_pos()	# get our mouse position
            x_last, y_last = x_click, y_click
            hit=50	# change this to leave the shot dot on the screen longer
	elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_q: 	# press q or ESC to exit
                pygame.quit()
                exit()
        if event.type == USEREVENT+1:
            if gameover != 1:
                clock_time -= 1

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
    clock.tick(30)

    # start of drawing
    screen.fill(BLACK)

    #print clock.get_fps()
    if gameover == 0: block_list.update()
    #all_sprites_list.draw(screen)
    #screen.blit(pygame.image.load("bg.png"), (0,0))  # draw the bg
    if hit > 0:  # loop for drawing the red hit circle
        pygame.draw.circle(screen, RED, (x_last, y_last), 10)
        hit -= 2  # change this too for duration of red dot on screen

    # check for ending time
    if clock_time == 0 and gameover != 1:
        print "GAME OVER"
        gameover=1
	all_sprites_list.remove()

    if gameover == 1:
        text = basicFont.render("Click here to retry", True, WHITE, BLUE)
        textRect = text.get_rect()
        textRect.topleft = [(SCREEN_WIDTH/2)-(textRect.width/2),(SCREEN_HEIGHT/2)-(textRect.height/2)]
        screen.blit(text, textRect)
        if x_click > textRect.left and x_click < textRect.right:
            if y_click > textRect.top and y_click < textRect.bottom:
                print "Game on!"
                # reset all of our variables and re-init our sprites
                clock_time = time
                player_points = 0
                gameover = 0

    # clear out clicks!  This prevents a bottle/duck/whatever from getting more hits from scrolling
    x_click=None
    y_click=None

    # put the score on top of everything
    text = basicFont.render('Points:' + str(player_points) + "   Timer:" + str(clock_time), True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.topleft = [SCREEN_WIDTH-textRect.width, SCREEN_HEIGHT-textRect.height]
    screen.blit(text, textRect)
    pygame.display.update() # throw it all on screen

