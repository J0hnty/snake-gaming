import json

import pygame
import random

high_scoreJson = {
    "name": "Jaap",
    "highscore": 100
}
try:
    with open('high_scores.json') as highScore_file:
        high_scoreJson = json.load(highScore_file)
except:
    print('no file')

leaderboard = high_scoreJson["leaderboard"]
print("this is the highscore inside the .json file", leaderboard)

array = []

pygame.init()

# colors used in game
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (71, 21, 69)
darkGreen = (25, 54, 25)
midGreen = (15, 115, 35)

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
snakeSpeed = 10

# fonts
loseFont = pygame.font.SysFont(None, 50)
scoreFont = pygame.font.SysFont(None, 30)

# position for the loss message
lossPosX = screenWidth // 2
lossPosY = screenHeight // 2

# position for the score message
scorePosX = 30
scorePosY = 30

high_score = 0


def scoreDisplay():
    temp = []
    for score in leaderboard:
        temp.append(score["score"])

    temp.sort(reverse=True)
    print(temp)
    return temp


def snake(snakeBlock, snakeList):
    for x in snakeList:
        # print("snake")
        pygame.draw.rect(screen, "green", [x[0], x[1], snakeBlock, snakeBlock])


def message(msg, color, typeMsg):
    """
    https://www.reddit.com/r/pygame/comments/ezohr9/how_do_i_add_multiline_text_in_pygame/
    gebruiken voor het reworkden van het printen van tekst op het scherm

    """
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
        text = scoreFont.render("score: " + msg, True, color)
        textRect = text.get_rect()
        textRect.topleft = posX, posY
        screen.blit(text, textRect)
    elif typeMsg == "highScore":
        posX = scorePosX
        posY = scorePosY + 30
        text = scoreFont.render("high score: " + msg, True, color)
        textRect = text.get_rect()
        textRect.topleft = posX, posY
        screen.blit(text, textRect)

    # instead of the line code under the text
    # I had to use the Rect that made the rectangle center first then put the variable textRect in the screen.blit()
    # what it did now was center the starting point of the text instead of the entire string
    # screen.blit(text, [screenWidth // 2, screenHeight // 2])
    # opgelost met behulp van deze pagina: https://stackoverflow.com/questions/23982907/how-to-center-text-in-pygame


def spawnFood():
    foodx = round(random.randrange(0, screenWidth - 50) / 10.0) * 10
    foody = round(random.randrange(0, screenHeight - 50) / 10.0) * 10
    pygame.draw.rect(screen, red, [foodx, foody, snakeBlock, snakeBlock])


# def highScore(points, highscore):
#     if points >= highscore:
#         highscore = points
#         print(f"points: {points}")
#         print(f"high score: {highscore}")


def gameLoop():
    global high_score, snakeSpeed

    firstTimeScoreCheck = True

    game_over = False
    game_end = False

    x1 = screenWidth / 2
    y1 = screenHeight / 2

    x1_change = 0
    y1_change = 0

    cheat_counter = 0

    snakeList = []

    foodx = round(random.randrange(0, screenWidth - snakeBlock) / 10.0) * 10
    foody = round(random.randrange(0, screenHeight - snakeBlock) / 10.0) * 10

    lenghtofSnake = 2
    lastInput = None

    score = (lenghtofSnake - 2) * 100
    message(str(score), white, "score")

    while not game_over:
        screen.fill(darkGreen)
        score = (lenghtofSnake - 2) * 100
        message(str(score), white, "score")

        while game_end:
            screen.fill(purple)
            if firstTimeScoreCheck:
                print("W")
                array = scoreDisplay()
                firstTimeScoreCheck = False
            message(str(score), white, "score")
            message(str(array[0]) + ", " +
                    str(array[1]) + ", " +
                    str(array[2]) + ", " +
                    str(array[3]) + ", " +
                    str(array[4]), midGreen, "highScore")
            message("You lost! press Q to quit or T to try again", red, "loss")
            if score > high_score:
                # highScore(score, high_score)
                high_score = score
                newhighscore = {'score': high_score}
                print("ingame highscore:", high_score, "in json string highscore:", newhighscore)
                high_scoreJson["leaderboard"].append(newhighscore)
                print(high_scoreJson)
                with open('high_scores.json', 'w') as highScore_file:
                    json.dump(high_scoreJson, highScore_file, indent=2)
                print(lenghtofSnake)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        lenghtofSnake = 2
                        game_over = True
                        game_end = False
                    if event.key == pygame.K_t:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if not lastInput == "RIGHT":
                        x1_change = -snakeBlock
                        y1_change = 0
                        lastInput = "LEFT"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if not lastInput == "LEFT":
                        x1_change = snakeBlock
                        y1_change = 0
                        lastInput = "RIGHT"
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if not lastInput == "DOWN":
                        y1_change = -snakeBlock
                        x1_change = 0
                        lastInput = "UP"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if not lastInput == "UP":
                        y1_change = snakeBlock
                        x1_change = 0
                        lastInput = "DOWN"
                elif event.key == pygame.K_p:
                    lenghtofSnake += 1
                    cheat_counter = cheat_counter + 1
                    print("you sneeky cheater. times cheated", cheat_counter)
                elif event.key == pygame.K_q:
                    snakeSpeed = 20
                    print("speed up")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    snakeSpeed = 10
                    print("speed down")
            if event.type == pygame.MOUSEBUTTONDOWN:
                lenghtofSnake += 1
                cheat_counter = cheat_counter + 1
                print("you sneeky cheater. times cheated", cheat_counter)
        if x1 >= screenWidth or x1 <= 0 or y1 >= screenHeight or y1 <= 0:
            game_end = True

        x1 += x1_change
        y1 += y1_change
        pygame.draw.rect(screen, red, [foodx, foody, snakeBlock, snakeBlock])
        pygame.draw.rect(screen, green, [x1, y1, snakeBlock, snakeBlock])
        snakeHead = [x1, y1]
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
            print(len(snakeList))
            lenghtofSnake += 1
            if lenghtofSnake:
                spawnFood()
                print("update")
                foodx = round(random.randrange(0, screenWidth - 50) / 10.0) * 10
                foody = round(random.randrange(0, screenHeight - 50) / 10.0) * 10
                screen.fill(darkGreen)
                message(str(score), white, "score")

        # set framerate
        clock.tick(snakeSpeed)

    pygame.quit()
    quit()


gameLoop()
