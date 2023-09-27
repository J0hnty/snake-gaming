import pygame
import random

pygame.init()

# colors used in game
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
purple = (71, 21, 69)
darkGreen = (25, 54, 25)

# screen size
screenWidth = 800
screenHeight = 600

# setting the size of the screen and the "gamename" in this case that I made the game
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('snake game by Johnty')

# for tracking time
clock = pygame.time.Clock()

# player probs
snakeBlock = 10
snakeSpeed = 20

# fonts
loseFont = pygame.font.SysFont(None, 50)
scoreFont = pygame.font.SysFont(None, 30)

# position for the loss message
lossPosX = screenWidth // 2
lossPosY = screenHeight // 2

# position for the score message
scorePosX = 30
scorePosY = 30


def snake(snakeBlock, snakeList):
    for x in snakeList:
        print("snake")
        pygame.draw.rect(screen, "green", [x[0], x[1], snakeBlock, snakeBlock])


def message(msg, color, typeMsg):
    posX = 0
    PosY = 0
    if typeMsg == "loss":
        posX = lossPosX
        posY = lossPosY
        text = loseFont.render(msg, True, color)
        textRect = text.get_rect()
        textRect.center = (posX, posY)
        screen.blit(text, textRect)
    elif typeMsg == "score":
        posX = scorePosX
        posY = scorePosY
        text = scoreFont.render(msg, True, color)
        textRect = text.get_rect()
        textRect.topleft = posX, posY
        screen.blit(text, textRect)
    # instead of the line code under the text
    # I had to use the Rect that made the rectangle center first then put the variable textRect in the screen.blit()
    # what it did now was center the starting point of the text instead of the entire string
    # screen.blit(text, [screenWidth // 2, screenHeight // 2])
    # opgelost met behulp van deze pagina: https://stackoverflow.com/questions/23982907/how-to-center-text-in-pygame


def spawnFood():
    foodx = round(random.randrange(0, screenWidth - snakeBlock) / 10.0) * 10
    foody = round(random.randrange(0, screenHeight - snakeBlock) / 10.0) * 10
    pygame.draw.rect(screen, red, [foodx, foody, snakeBlock, snakeBlock])


def gameLoop():
    game_over = False
    game_end = False

    x1 = screenWidth / 2
    y1 = screenHeight / 2

    x1_change = 0
    y1_change = 0

    snakeList = []

    foodx = round(random.randrange(0, screenWidth - snakeBlock) / 10.0) * 10
    foody = round(random.randrange(0, screenHeight - snakeBlock) / 10.0) * 10

    lenghtofSnake = 1
    highscore = 0
    screen.fill(darkGreen)
    message(f"score: {lenghtofSnake - 1}", white, "score")

    while not game_over:

        while game_end:
            screen.fill(purple)
            message("You lost! press Q to quit or T to try again", red, "loss")

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        if lenghtofSnake > highscore:
                            highscore = lenghtofSnake
                        lenghtofSnake = 1
                        game_over = True
                        game_end = False
                    if event.key == pygame.K_t:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x1_change = -snakeBlock
                    y1_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x1_change = snakeBlock
                    y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y1_change = -snakeBlock
                    x1_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y1_change = snakeBlock
                    x1_change = 0

        if x1 >= screenWidth or x1 <= 0 or y1 >= screenHeight or y1 <= 0:
            game_end = True

        x1 += x1_change
        y1 += y1_change
        pygame.draw.rect(screen, red, [foodx, foody, snakeBlock, snakeBlock])
        pygame.draw.rect(screen, green, [x1, y1, snakeBlock, snakeBlock])
        snakeHead = []
        snakeHead.append(x1)
        snakeHead.append(y1)
        snakeList.append(snakeHead)
        if len(snakeList) >= lenghtofSnake:
            del snakeList[0]

        for x in snakeList[:-1]:
            if x == snakeHead:
                game_end = True

        snake(snakeBlock, snakeList)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            print("Lekka!!")
            lenghtofSnake += 1
            if lenghtofSnake:
                spawnFood()
                print("update")
                foodx = round(random.randrange(0, screenWidth - snakeBlock) / 10.0) * 10
                foody = round(random.randrange(0, screenHeight - snakeBlock) / 10.0) * 10
                screen.fill(darkGreen)
                message(f"score: {lenghtofSnake - 1}", white, "score")

        # framerate set to 30fps
        clock.tick(snakeSpeed)  # limits FPS to 30

    pygame.quit()
    quit()


gameLoop()
