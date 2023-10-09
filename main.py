import json
import random
import os
import pygame
from pygame.sprite import Sprite, Group
from itertools import count as iter_count

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


class Text(Sprite):
    # @anchor uses rect position
    def __init__(self, text, font, color, position, anchor="topleft"):
        Sprite.__init__(self)
        self._text = text
        self._font = font
        self._color = color
        self._position = position
        self._anchor = anchor
        self.render()

    def render(self):
        self.image = self._font.render(self._text, 1, self._color)
        self.rect = self.image.get_rect(**{self._anchor: self._position})


class MultiText(Sprite):
    # @anchor uses rect position
    def __init__(self, texts, font, color, position, anchor="topleft"):
        Sprite.__init__(self)
        self._texts = texts
        self._font = font
        self._color = color
        self._position = position
        self._anchor = anchor
        self.render()

    def render(self):
        width, height = 0, 0
        for text in self._texts:
            height += self._font.get_linesize()
            w, _ = self._font.size(text)
            if w > width:
                width = w

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(**{self._anchor: self._position})
        line = iter_count(0, self._font.get_linesize())
        for text in self._texts:
            image = self._font.render(text, 1, self._color)
            self.image.blit(image, (0, next(line)))


# Interface
class Scene:
    def __init__(self, manager):
        self.manager = manager

    def on_draw(self, surface): pass

    def on_event(self, event): pass

    def on_update(self, delta): pass

    def on_quit(self):
        self.manager.quit()


# Handles what scene is active
class Manager:
    def __init__(self, center=True, flags=0):
        if center:
            os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Basic pygame setup
        self.surface = pygame.display.set_mode((screenWidth, screenHeight), flags)
        self.rect = self.surface.get_rect()
        self.running = False

        self.scene = Scene(self)

    def mainloop(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.scene.on_quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        lenghtofSnake = 2
                        print("quit")
                        game_over = True
                        game_end = False
                        pygame.quit()
                    if event.key == pygame.K_t:
                        gameLoop()
                else:
                    self.scene.on_event(event)

            self.scene.on_update(clock)
            self.scene.on_draw(self.surface)
            pygame.display.flip()

    def quit(self):
        self.running = False


class MainScene(Scene):
    def __init__(self, manager, typeMsg, game_end, score):
        Scene.__init__(self, manager)
        self.sprites = Group()
        self.loseFont = pygame.font.SysFont(None, 50)
        self.font_48 = pygame.font.Font(None, 48)
        self.font_40 = pygame.font.Font(None, 40)
        self.font_36 = pygame.font.Font(None, 36)
        self.scoreFont = pygame.font.SysFont(None, 30)
        self.font_28 = pygame.font.Font(None, 28)
        self.font_18 = pygame.font.Font(None, 18)
        self.font_14 = pygame.font.Font(None, 14)
        self.create_texts(typeMsg, game_end, score)

    def create_texts(self, typeMsg, game_end, score):
        # tempText = "has to go in the method"
        lossText = ["You lost!", "press Q to quit or", "T to try again"]
        scoreText = ["score: " + str(score)]
        highScoreIntList = scoreDisplay()
        highScoresText = [str(x) for x in highScoreIntList[0:9]]
        highScoreText = ["high score:"]
        print("strings in list", highScoresText)
        lossOffset = (0, 50)
        scoreOffset = (30, 30)
        highScoresOffset = (0, 50)
        lossPosition = pygame.Vector2(self.manager.rect.center) + pygame.Vector2(lossOffset)
        scorePosition = pygame.Vector2(self.manager.rect.topleft) + pygame.Vector2(scoreOffset)
        highScoresPosition = pygame.Vector2(self.manager.rect.centerx) + pygame.Vector2(highScoresOffset)
        if game_end:
            self.sprites.add(
                MultiText(lossText,
                          self.loseFont, pygame.Color(red),
                          lossPosition, "center"))
            self.sprites.add(
                MultiText(scoreText,
                          self.scoreFont, pygame.Color(white),
                          scorePosition, "topleft"))
            self.sprites.add(
                MultiText(highScoreText + highScoresText,
                          self.font_36, pygame.Color(darkGreen),
                          self.manager.rect.centerx, "centerx"))
            # self.sprites.add(
            #     MultiText(highScoresText,
            #               self.font_28, pygame.Color(darkGreen),
            #               highScoresPosition, "centerx"))

        else:
            pass

        # if typeMsg == "loss":
        #     pass
        # elif typeMsg == "score\n s":
        #     for item in text:
        #         self.sprites.add(Text(item, self.font_14, pygame.Color(color), (0, next(line))))
        # elif typeMsg == "highScore\n h":
        #     pass

        # text = ["Hello World !", "This is an example.", "Of a mulittext line"]
        #
        # text = "Hello World !\nThis is an example.\nOf a mulittext line"
        # text = text.split('\n')

        # Or you can do it with single lines of text
        # line = iter_count(0, self.font_14.get_linesize())
        # for item in text:
        #     self.sprites.add(Text(item, self.font_40, pygame.Color(color), (0, next(line))))

    def on_draw(self, surface):
        surface.fill(pygame.Color(85, 39, 105))
        self.sprites.draw(surface)


def main(typeMsg, game_end, score):
    manager = Manager()
    manager.scene = MainScene(manager, typeMsg, game_end, score)
    manager.mainloop()


def scoreDisplay():
    temp = []
    for score in leaderboard:
        temp.append(score["score"])

    temp.sort(reverse=True)
    print("ints", temp)
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

    if typeMsg == "score":
        posX = scorePosX
        posY = scorePosY
        text = scoreFont.render("score: " + msg, True, color)
        textRect = text.get_rect()
        textRect.topleft = posX, posY
        screen.blit(text, textRect)


    # instead of the line code under the text
    # I had to use the Rect that made the rectangle center first then put the variable textRect in the screen.blit()
    # what it did now was center the starting point of the text instead of the entire string
    # screen.blit(text, [screenWidth // 2, screenHeight // 2])
    # fixed with this page: https://stackoverflow.com/questions/23982907/how-to-center-text-in-pygame


def spawnFood():
    foodx = round(random.randrange(0, screenWidth - 50) / 10.0) * 10
    foody = round(random.randrange(0, screenHeight - 50) / 10.0) * 10
    pygame.draw.rect(screen, red, [foodx, foody, snakeBlock, snakeBlock])


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
            if firstTimeScoreCheck:
                print("W")
                array = scoreDisplay()
                firstTimeScoreCheck = False
            # message(str(score), white, "score")
            # message(str(array[0]) + ", " +
            #         str(array[1]) + ", " +
            #         str(array[2]) + ", " +
            #         str(array[3]) + ", " +
            #         str(array[4]), midGreen, "highScore")
            # message("You lost! press Q to quit or T to try again", red, "loss")

            if score >= high_score or score <= high_score:
                # highScore(score, high_score)
                high_score = score
                newhighscore = {'score': high_score}
                print("ingame highscore:", high_score, "in json string highscore:", newhighscore)
                high_scoreJson["leaderboard"].append(newhighscore)
                print(high_scoreJson)
                with open('high_scores.json', 'w') as highScore_file:
                    json.dump(high_scoreJson, highScore_file, indent=2)
                print(lenghtofSnake)
            main("highScore", game_end, score)
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
