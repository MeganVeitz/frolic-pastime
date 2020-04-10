
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# score
#score_value = 0
#font = pygame.font.Font('Freesansbold.ttf', 32)

#textX = 10#
#textY = 10

class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        # i stands for row
        i = self.pos[0]
        # j stands for column
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis+8)
            circleMiddle2 = (i * dis + dis - radius * 2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


# snake body contain cube objects
class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            # print("Keys: {}".format(keys))
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    # now we need to remember where we turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    # now we need to remember where we turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    # now we need to remember where we turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    # now we need to remember where we turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # getting the index (i) and cube objects (c) in our self.body~made up of cube ojects
        for i, c in enumerate(self.body):
            # each cube obj has a position
            p = c.pos[:]
            # so we are grabbing those turns
            if p in self.turns:
                turn = self.turns[p]
                # giving direction it needs to move
                c.move(turn[0], turn[1])
                # if we are at the last cube, then we are removing it from the list
                if i == len(self.body)-1:
                    self.turns.pop(p)

            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


class Runner:
    def __init__(self, width=500, rows=20):
        self.width = width
        self.rows = rows
        self.s = Snake((255, 0, 0), (10, 10))
        self.snack = Cube(self.randomSnack(self.rows, self.s), color=(0, 255, 0))

    # Score Function
    #def show_score(x, y):
        #score = font.render("Score: " + str(score_value, True, (255,255,255)))
        #screen.blit(score,(x, y))
        #print("score_code")

    def drawGrid(self, w, rows, surface):
        sizeBtwn = w // rows

        x = 0
        y = 0
        for l in range(rows):
            x = x + sizeBtwn
            y = y + sizeBtwn
            # x is drawing vertical lines, y is drawing horizontal lines across the screen
            pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
            pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

    def redrawWindow(self, surface):
        surface.fill((0, 0, 0))
        self.s.draw(surface)
        self.snack.draw(surface)
        self.drawGrid(self.width, self.rows, surface)
        pygame.display.update()

    def randomSnack(self, rows, item):

        positions = item.body

        while True:
            x = random.randrange(rows)
            y = random.randrange(rows)
            # makes sure the snake doesn't land on the snake
            if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
                continue
            else:
                break

        return (x, y)

    def message_box(self, subject, content):
        try:
            print("in message box")
            root = tk.Tk()
            print("set up root")
            root.attributes("-topmost", True)
            print("Made attributes")
            root.withdraw()
            print("withdrawn")
            messagebox.showinfo(subject, content)
            root.destroy()
        except Exception as e:
            print(e)

    def main(self):
        """
        The main function!
        :return:
        """
        win = pygame.display.set_mode((self.width, self.width))
        flag = True

        clock = pygame.time.Clock()

        while flag:
            # How you change speed of snake
            pygame.time.delay(50)
            clock.tick(10)
            self.s.move()
            if self.s.body[0].pos == self.snack.pos:
                self.s.addCube()
                self.snack = Cube(self.randomSnack(self.rows, self.s), color=(0, 255, 0))

            for x in range(len(self.s.body)):
                if self.s.body[x].pos in list(map(lambda z: z.pos, self.s.body[x+1:])):
                    print("Score: ", len(self.s.body))
                    self.message_box("You Lost!", "Play Again...")
                    print("After message box")
                    self.message_box()
                    self.s.reset((10, 10))
                    break

            self.redrawWindow(win)

            # show_score(textX, textY)


run = Runner()
run.main()
