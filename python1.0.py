import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 800
WIN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
TEXTCOLOR = ('white')
BACKGROUNDCOLOR = (255, 255, 255)
MENUBACKGROUNDCOLOR = ('red')
# MenuGameBackground = pygame.image.load("snow.gif") #si vous voulez
FPS = 60
MINSIZE = 30  # ici le code a été modifié en suivant les conseils du livre (Ai Swegart) Ch. 20, Pg. 353-354
MEDSIZE = 45
MAXSIZE = 60  # la taille max d'un caractere
BADDIEMINSPEED = 1  # la vitesse minimale d'ennemi
BADDIEMAXSPEED = 4  # la vitesse maximale d'ennemi
ADDNEWBADDIERATE = 24  # le taux de reproduction de nouveaux ennemis
ADDNEWLUTINRATE=48 # le taux de reproduction de lutins
LUTINSPEED=1
PLAYERMOVERATE = 5  # la vitesse de déplacement de jouer


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
            baddies.remove(b)
            return True
    return False


def playerHasHitLutin(playerRect, lutin):    #code pour les lutins
   for l in lutin:
        if playerRect.colliderect(l['rect']):
            lutin.remove(l)
            return True

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('X-Mas Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48, bold=True)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('grinch_gameoversound.mp3')
BellsSound = pygame.mixer.Sound('Bells Sound effect.mp3')
PresentSound = pygame.mixer.Sound('Present_sound.mp3')
musicPlaying = True

# Set up images.
# LIVES = pygame.image.load('hp.png')
playerImage = pygame.image.load('santa-player.png')

playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('gremlin.png')
charbonImage = pygame.image.load('Charbon.png')
lutinImage = pygame.image.load('bonlutin.png')
cadeauImage = pygame.image.load('cadeau.png')
thundercloudImage = pygame.image.load('thundercloud.png')

gameBackground_lvl1 = pygame.image.load("winter_background.png")
gameBackground_lvl2 = pygame.image.load("lvl_2.png")
gameBackground_lvl3 = pygame.image.load("night_sky.png")
gameOverBackground = pygame.image.load("Grinch end game.png")

# Show the "Start" screen.
windowSurface.fill(MENUBACKGROUNDCOLOR)
drawText('X-Mas Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start', font, windowSurface, (WINDOWWIDTH / 3) - 40, (WINDOWHEIGHT / 3) + 50)
drawText('saving Christmas', font, windowSurface, (WINDOWWIDTH / 3) - 35, (WINDOWHEIGHT / 3) + 100)
pygame.display.update()
waitForPlayerToPressKey()

#todo set up pct score instead of absolute numbers
while True: #level 1
    # Set up the start of the game.
    baddies = []
    lutin = []
    scoreLutin = 0
    lives = 3  # The number of lives at the start of the game
    level = 1  # We start with the first level
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 80)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0  # ajouter de baddies horizontalement
    lutinAddCounter = 0  # ajouter des lutins horizontalement
    pygame.mixer.music.load('Jingle_Bells-Kevin_MacLeod.mp3')
    pygame.mixer.music.play(-1, 0.0)
    while True:  # The game loop runs while the game part is playing.
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
                    scoreLutin = 0
                if event.key == K_x:
                    slowCheat = False
                    scoreLutin = 0
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
            lutinAddCounter += 1
            baddieAddCounter += 1

        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(MINSIZE, MAXSIZE)
            newBaddie = {'rect': pygame.Rect(WINDOWWIDTH + 40 - baddieSize, random.randint(0, WINDOWWIDTH - baddieSize),
                                             baddieSize,
                                             baddieSize),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                         }

            baddies.append(newBaddie)

        if lutinAddCounter == ADDNEWLUTINRATE:
            lutinAddCounter = 0
            lutinSize = random.randint(MINSIZE, MEDSIZE)
            newLutin = {'rect': pygame.Rect(WINDOWWIDTH + 40 - lutinSize, random.randint(0, WINDOWWIDTH - lutinSize),
                                             lutinSize,
                                             lutinSize),
                         'speed': LUTINSPEED,
                         'surface': pygame.transform.scale(lutinImage, (lutinSize, lutinSize)),
                         }

            lutin.append(newLutin)

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
                b['rect'].move_ip(-b['speed'], 0)
            elif reverseCheat:
                b['rect'].move_ip(5, 0)
            elif slowCheat:
                b['rect'].move_ip(-1, 0)

        # Delete baddies that have come from the left.
        for b in baddies[:]:
            if b['rect'].left > WINDOWWIDTH:
                baddies.remove(b)

        # Move the lutins down.
        for l in lutin:
            if not reverseCheat and not slowCheat:
                l['rect'].move_ip(-l['speed'], 0)
            elif reverseCheat:
                l['rect'].move_ip(-1, 0)
            elif slowCheat:
                l['rect'].move_ip(5, 0)

        # Delete lutins that have come from the left.
        for l in lutin[:]:
            if l['rect'].left > WINDOWWIDTH:
                lutin.remove(l)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)
        # Set up the background
        windowSurface.blit(gameBackground_lvl1, (0, -100))
        # Draw the Lutin score and top score.
        drawText('Number of Elves Caught: %s' % (scoreLutin), font, windowSurface, 10, 0)
        drawText('Lives: %s' % (lives), font, windowSurface, 10, 40)
        drawText('Level: %s' % (level), font, windowSurface, WINDOWWIDTH - 150, 0)

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        # Draw each lutin.
        for l in lutin:
            windowSurface.blit(l['surface'], l['rect'])

        pygame.display.update()

        # Check if any of the lutins have been collected by the player.
        if playerHasHitLutin(playerRect, lutin) == True:
            scoreLutin += 1
            BellsSound.play()
            if scoreLutin >= 10:  # the player moves to the next level (for now the game stops)
                break
                #create method for levelling up
            else:
                continue


        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies) == True:
            lives -= 1
            for b in baddies:
                baddies.remove(b)
            if lives > 0:  # the player keeps playing if she/he has more than 0 lives
                pass
            else:  # when the player has 0 lives the game stops
                break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    if scoreLutin < 10:
        windowSurface.blit(gameOverBackground, (-850, 0))
        pygame.mixer.music.stop()
        gameOverSound.play()

        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('Press a key to retry', font, windowSurface, (WINDOWWIDTH / 3) - 45, (WINDOWHEIGHT / 3) + 50)
        drawText('to save Christmas', font, windowSurface, (WINDOWWIDTH / 3) - 45, (WINDOWHEIGHT / 3) + 100)
        pygame.display.update()
        waitForPlayerToPressKey()

        gameOverSound.stop()

 #-----------------------------------------------------------------------------------------------------------------------

    elif scoreLutin >= 10:                  #level-up code to lvl 2
        windowSurface.blit(gameBackground_lvl2, (-850, 0))
        pygame.mixer.music.stop()
        drawText("You WON!", font, windowSurface, (WINDOWWIDTH / 3)+50, (WINDOWHEIGHT / 3))
        pygame.display.update()
        waitForPlayerToPressKey()
        scoreLutin = 0
        while True: #lvl 2 of the game
            level += 1
            #Debug code
            if lives <= 0:  #this code helps to debug the previous problems
                break                  # when a player has less than 0 lives him/her back to the start of the game
            elif level >= 4:  #this code is useful when the player has completed the game, he can restart from lvl 1
                break
            # Set up the start of the game.
            baddies = []
            lutin = []
            scoreCadeau = 0
            playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 80)
            moveLeft = moveRight = moveUp = moveDown = False
            reverseCheat = slowCheat = False
            baddieAddCounter = 0  # ajouter de baddies horizontalement
            lutinAddCounter = 0  # ajouter des lutins horizontalement
            pygame.mixer.music.play(-1, 0.0)
            # level1 = GameLevel(1, "winter_background.png", 'gremlin_baddie.png')
            # level2=GameLevel(2, "night_sky.png", "bonlutin.png")
            while True:  # The game loop runs while the game part is playing.
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
                            scoreCadeau = 0
                        if event.key == K_x:
                            slowCheat = False
                            scoreCadeau = 0
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
                    lutinAddCounter += 1
                    baddieAddCounter += 1

                if baddieAddCounter == ADDNEWBADDIERATE:
                    baddieAddCounter = 0
                    baddieSize = random.randint(MEDSIZE, MAXSIZE)
                    newBaddie = {
                        'rect': pygame.Rect(WINDOWWIDTH + 40 - baddieSize, random.randint(0, WINDOWWIDTH - baddieSize),
                                            baddieSize,
                                            baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface': pygame.transform.scale(charbonImage, (baddieSize, baddieSize)),
                        }

                    baddies.append(newBaddie)

                if lutinAddCounter == ADDNEWLUTINRATE:
                    lutinAddCounter = 0
                    lutinSize = random.randint(MINSIZE, MEDSIZE)
                    newLutin = {
                        'rect': pygame.Rect(WINDOWWIDTH + 40 - lutinSize, random.randint(0, WINDOWWIDTH - lutinSize),
                                            lutinSize,
                                            lutinSize),
                        'speed': LUTINSPEED,
                        'surface': pygame.transform.scale(cadeauImage, (lutinSize, lutinSize)),
                        }

                    lutin.append(newLutin)

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
                        b['rect'].move_ip(-b['speed'], 0)
                    elif reverseCheat:
                        b['rect'].move_ip(5, 0)
                    elif slowCheat:
                        b['rect'].move_ip(-1, 0)

                # Delete baddies that have come from the left.
                for b in baddies[:]:
                    if b['rect'].left > WINDOWWIDTH:
                        baddies.remove(b)

                # Move the lutins down.
                for l in lutin:
                    if not reverseCheat and not slowCheat:
                        l['rect'].move_ip(-l['speed'], 0)
                    elif reverseCheat:
                        l['rect'].move_ip(-1, 0)
                    elif slowCheat:
                        l['rect'].move_ip(5, 0)

                # Delete lutins that have come from the left.
                for l in lutin[:]:
                    if l['rect'].left > WINDOWWIDTH:
                        lutin.remove(l)

                # Draw the game world on the window.
                windowSurface.fill(BACKGROUNDCOLOR)
                # Set up the background
                windowSurface.blit(gameBackground_lvl2, (0, -100))
                # Draw the Lutin score and top score.
                drawText('Number of Presents Caught: %s' % (scoreCadeau), font, windowSurface, 10, 0)
                drawText('Lives: %s' % (lives), font, windowSurface, 10, 40)
                drawText('Level: %s' % (level), font, windowSurface, WINDOWWIDTH - 150, 0)

                # Draw the player's rectangle.
                windowSurface.blit(playerImage, playerRect)

                # Draw each baddie.
                for b in baddies:
                    windowSurface.blit(b['surface'], b['rect'])

                # Draw each lutin.
                for l in lutin:
                    windowSurface.blit(l['surface'], l['rect'])

                pygame.display.update()

                # Check if any of the lutins have been collected by the player.
                if playerHasHitLutin(playerRect, lutin) == True:
                    scoreCadeau += 1
                    PresentSound.play()

                    if scoreCadeau >= 10:  # the player moves to the next level
                        break
                    else:
                        continue

                # Check if any of the baddies have hit the player.
                if playerHasHitBaddie(playerRect, baddies) == True:
                    lives -= 1
                    for b in baddies:
                        baddies.remove(b)
                    if lives > 0:  # the player keeps playing if she/he has more than 0 lives
                        pass
                    else:  # when the player has 0 lives the game stops
                        break
                        # Stop the game and show the "Game Over" screen.
                mainClock.tick(FPS)

            if scoreCadeau < 10:
                windowSurface.blit(gameOverBackground, (-850, 0))
                pygame.mixer.music.stop()
                gameOverSound.play()

                drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
                drawText('Press a key to retry', font, windowSurface, (WINDOWWIDTH / 3) - 45,
                         (WINDOWHEIGHT / 3) + 50)
                drawText('to save Christmas', font, windowSurface, (WINDOWWIDTH / 3) - 45, (WINDOWHEIGHT / 3) + 100)
                pygame.display.update()
                waitForPlayerToPressKey()

                gameOverSound.stop()

            # -----------------------------------------------------------------------------------------------------------------------
            elif scoreCadeau >= 10:  #level-up code to lvl 3
                windowSurface.blit(gameBackground_lvl3, (-850, 0))
                pygame.mixer.music.stop()
                drawText("You WON!", font, windowSurface, (WINDOWWIDTH / 3) + 50, (WINDOWHEIGHT / 3))
                drawText("Press key to play next level!", font, windowSurface, (WINDOWWIDTH / 3) -40, (WINDOWHEIGHT / 3) +50)
                pygame.display.update()
                waitForPlayerToPressKey()
                scoreCadeau=0
                while True:  # lvl 3 of the game
                    level += 1
                    # Debug code
                    if lives <= 0:    # this code helps to debug the previous problems
                        break         # when a player has less than 0 lives him/her back to the start of the game
                    elif level >= 4:  # this code is useful when the player has completed the game, he can restart from lvl 1
                        break         # this code in particular sends the player back to level 2
                    # Set up the start of the game.
                    baddies = []
                    lutin = []
                    scoreLutin = 0
                    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 80)
                    moveLeft = moveRight = moveUp = moveDown = False
                    reverseCheat = slowCheat = False
                    baddieAddCounter = 0  # ajouter de baddies horizontalement
                    lutinAddCounter = 0  # ajouter des lutins horizontalement
                    pygame.mixer.music.load('Katy Perry-CozyLittleChristmas.mp3')
                    pygame.mixer.music.play(-1, 0.0)
                    while True:  # The game loop runs while the game part is playing.
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
                                    scoreLutin = 0
                                if event.key == K_x:
                                    slowCheat = False
                                    scoreLutin = 0
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
                            lutinAddCounter += 1
                            baddieAddCounter += 1

                        if baddieAddCounter == ADDNEWBADDIERATE:
                            baddieAddCounter = 0
                            baddieSize = random.randint(MINSIZE, MAXSIZE)
                            newBaddie = {
                                'rect': pygame.Rect(WINDOWWIDTH + 40 - baddieSize,
                                                    random.randint(0, WINDOWWIDTH - baddieSize),
                                                    baddieSize,
                                                    baddieSize),
                                'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                                'surface': pygame.transform.scale(thundercloudImage, (baddieSize, baddieSize)),
                            }

                            baddies.append(newBaddie)

                        if lutinAddCounter == ADDNEWLUTINRATE:
                            lutinAddCounter = 0
                            lutinSize = random.randint(MINSIZE, MEDSIZE)
                            newLutin = {
                                'rect': pygame.Rect(WINDOWWIDTH + 40 - lutinSize,
                                                    random.randint(0, WINDOWWIDTH - lutinSize),
                                                    lutinSize,
                                                    lutinSize),
                                'speed': LUTINSPEED,
                                'surface': pygame.transform.scale(lutinImage, (lutinSize, lutinSize)),
                            }

                            lutin.append(newLutin)

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
                                b['rect'].move_ip(-b['speed'], 0)
                            elif reverseCheat:
                                b['rect'].move_ip(5, 0)
                            elif slowCheat:
                                b['rect'].move_ip(-1, 0)

                        # Delete baddies that have come from the left.
                        for b in baddies[:]:
                            if b['rect'].left > WINDOWWIDTH:
                                baddies.remove(b)

                        # Move the lutins down.
                        for l in lutin:
                            if not reverseCheat and not slowCheat:
                                l['rect'].move_ip(-l['speed'], 0)
                            elif reverseCheat:
                                l['rect'].move_ip(-1, 0)
                            elif slowCheat:
                                l['rect'].move_ip(5, 0)

                        # Delete lutins that have come from the left.
                        for l in lutin[:]:
                            if l['rect'].left > WINDOWWIDTH:
                                lutin.remove(l)

                        # Draw the game world on the window.
                        windowSurface.fill(BACKGROUNDCOLOR)
                        # Set up the background
                        windowSurface.blit(gameBackground_lvl3, (0, -100))
                        # Draw the Lutin score and top score.
                        drawText('Number of Elves Caught: %s' % (scoreLutin), font, windowSurface, 10, 0)
                        drawText('Lives: %s' % (lives), font, windowSurface, 10, 40)
                        drawText('Level: %s' % (level), font, windowSurface, WINDOWWIDTH - 150, 0)

                        # Draw the player's rectangle.
                        windowSurface.blit(playerImage, playerRect)

                        # Draw each baddie.
                        for b in baddies:
                            windowSurface.blit(b['surface'], b['rect'])

                        # Draw each lutin.
                        for l in lutin:
                            windowSurface.blit(l['surface'], l['rect'])

                        pygame.display.update()

                        # Check if any of the lutins have been collected by the player.
                        if playerHasHitLutin(playerRect, lutin) == True:
                            scoreLutin += 1
                            PresentSound.play()
                            # todo feedback sonore
                            if scoreLutin >= 10:  # the player moves to the next level
                                break
                            else:
                                continue

                        # Check if any of the baddies have hit the player.
                        if playerHasHitBaddie(playerRect, baddies) == True:
                            lives -= 1
                            for b in baddies:
                                baddies.remove(b)
                            if lives > 0:  # the player keeps playing if she/he has more than 0 lives
                                pass
                            else:  # when the player has 0 lives the game stops
                                break
                                # Stop the game and show the "Game Over" screen.
                        mainClock.tick(FPS)

                    if scoreLutin < 10:
                        windowSurface.blit(gameOverBackground, (-850, 0))
                        pygame.mixer.music.stop()
                        gameOverSound.play()

                        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
                        drawText('Press a key to retry', font, windowSurface, (WINDOWWIDTH / 3) - 45,
                                 (WINDOWHEIGHT / 3) + 50)
                        drawText('to save Christmas', font, windowSurface, (WINDOWWIDTH / 3) - 45,
                                 (WINDOWHEIGHT / 3) + 100)
                        pygame.display.update()

                        waitForPlayerToPressKey()
                        gameOverSound.stop()

                    # -----------------------------------------------------------------------------------------------------------------------
                    elif scoreLutin >= 10:  # End of the game
                        windowSurface.blit(gameBackground_lvl1, (-850, 0))
                        pygame.mixer.music.stop()
                        drawText("Well Done!", font, windowSurface, (WINDOWWIDTH / 3) + 50, (WINDOWHEIGHT / 3))
                        drawText("You Won!", font, windowSurface, (WINDOWWIDTH / 3) + 50,
                                 (WINDOWHEIGHT / 3) + 50)
                        pygame.display.update()
                        waitForPlayerToPressKey()

#todo lvl2 (present collection) + lvl3 (present distribution)