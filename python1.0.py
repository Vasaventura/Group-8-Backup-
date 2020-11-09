import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 800
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
MENUBACKGROUNDCOLOR = ('lavenderblush')
FPS = 60
BADDIEMINSIZE = 25 #ici le code a été modifié en suivant les conseils du livre (Ai Swegart) Ch. 20, Pg. 353-354
BADDIEMAXSIZE = 60
BADDIEMINSPEED = 1  # la vitesse minimale d'ennemi
BADDIEMAXSPEED = 4  # la vitesse maximale d'ennemi
ADDNEWBADDIERATE = 12  # le taux de reproduction de nouveaux ennemis
PLAYERMOVERATE = 5


def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                return


def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48, bold=True)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('grinch_gameoversound.mp3')
pygame.mixer.music.load('KatyPerry-CozyLittleChristmas.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.load('KatyPerry-CozyLittleChristmas.mp3')
musicPlaying = True

# Set up images.
playerImage = pygame.image.load('santa-player.png')
playerRect = playerImage.get_rect()
playerStretchedImage = pygame.transform.scale(playerImage, (10, 10))
baddieImage = pygame.image.load('gremlin_baddie.png')


gameBackground = pygame.image.load("winter_background.png")
gameOverBackground = pygame.image.load("Grinch end game.png")

# Show the "Start" screen.
windowSurface.fill(MENUBACKGROUNDCOLOR)
drawText('X-Mas Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start', font, windowSurface, (WINDOWWIDTH / 3)-40, (WINDOWHEIGHT / 3) + 50)
drawText('saving Christmas', font, windowSurface, (WINDOWWIDTH / 3)-35, (WINDOWHEIGHT / 3) + 100)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)
    #class GameLevel():
      #  def __init__(self, level, background, baddie):
       #     self.level = level
       #     self.background = pygame.image.load(background)
       #     self.gameBackground=windowSurface.blit(background, (0, 0))
        #    self.baddie = pygame.image.load(baddie)




    #level1 = GameLevel(1, "Grinch end game.png", 'gremlin_baddie.png')
    #level2=GameLevel(2, "night_sky.png", "bonlutin.png")
    while True:  # The game loop runs while the game part is playing.



        score += 1  # Increase score.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True
                # option mute pour enlever le son du jeu. Par contre le son du Game Over reste toujours
                if event.key == K_m:
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                musicPlaying = not musicPlaying  # le code a ete adapte depuis le livre de cours (Ai Swegart) Ch. 19 Page 325-326

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where to the cursor.
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize,
                                             baddieSize),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                         }

            baddies.append(newBaddie)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the baddies to the left.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(5, 0)
            elif slowCheat:
                b['rect'].move_ip(-1, 0)

        # Delete baddies that have come from the right.
        for b in baddies[:]:
            if b['rect'].left > WINDOWWIDTH:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)
        #Set up the background
        windowSurface.blit(gameBackground, (0, -100))
        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score  # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    windowSurface.blit(gameOverBackground, (-850, 0))
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to retry', font, windowSurface, (WINDOWWIDTH / 3) - 45, (WINDOWHEIGHT / 3) + 50)
    drawText('to save Christmas', font, windowSurface, (WINDOWWIDTH / 3) - 45,(WINDOWHEIGHT / 3) + 100)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
