from instabot import Bot
bot = Bot()
bot.login(username="maze_account", password="QAWsed987123_20")

import pygame, sys, random
random.seed(None, 2)
#global

grid_w = 30
grid_h = 30
#screen_w = 1280
#screen_h = 720
screen_w = 450
screen_h = 450
offset = 10
cell_size = 15
line_width = 2
#colors
GREEN = (0, 222, 0)
BLUE = (0, 0, 222)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (222, 0, 0)
PURPLE = (190, 120 ,219)
GRAY = (220,220,220)
#other
cells = []
screen = pygame.display.set_mode((screen_w,screen_h))
pygame.init()
class Cell:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.top = True
    self.right = True
    self.bottom = True
    self.left = True
    self.visited = False

  def show(self):
    position_x = self.x * cell_size +offset
    position_y = self.y * cell_size +offset
    EMPTY_COLOR = WHITE
    if self.visited:
        pygame.draw.rect(screen, EMPTY_COLOR, pygame.Rect(position_x, position_y, cell_size, cell_size))

    if self == current:
        pygame.draw.rect(screen, RED, pygame.Rect(position_x, position_y, cell_size, cell_size))
    
    if self.x == grid_w-1 and self.y == grid_h-1:
        pygame.draw.rect(screen, GREEN, pygame.Rect(position_x, position_y, cell_size, cell_size))

    if not(self.top):
        pygame.draw.line(screen, EMPTY_COLOR, (position_x,           position_y),           (position_x+cell_size, position_y),           line_width) 
    if not(self.right):
        pygame.draw.line(screen, EMPTY_COLOR, (position_x+cell_size, position_y+cell_size), (position_x, position_y+cell_size),           line_width)
    if not(self.bottom):
        pygame.draw.line(screen, EMPTY_COLOR, (position_x+cell_size, position_y+cell_size), (position_x, position_y+cell_size),           line_width)
    if not(self.left):
        pygame.draw.line(screen, EMPTY_COLOR, (position_x,           position_y+cell_size), (position_x, position_y),                     line_width)


    if self.top:
        pygame.draw.line(screen, GRAY, (position_x,           position_y),           (position_x+cell_size, position_y),           line_width)

    if self.right:
        pygame.draw.line(screen, GRAY, (position_x+cell_size, position_y),           (position_x+cell_size, position_y+cell_size), line_width)            

    if self.bottom:
        pygame.draw.line(screen, GRAY, (position_x+cell_size, position_y+cell_size), (position_x, position_y+cell_size),           line_width)

    if self.left:
        pygame.draw.line(screen, GRAY, (position_x,           position_y+cell_size), (position_x, position_y),                     line_width)
    
  def checkNeighbors(self):
    neighbors = []
    if Index(self.x, self.y-1) != -1:
        top = cells[Index(self.x, self.y-1)]
        if not(top.visited):
            neighbors.append(top)

    if Index(self.x+1, self.y) != -1:     
        right = cells[Index(self.x+1, self.y)]
        if not(right.visited):
            neighbors.append(right)

    if Index(self.x, self.y+1) != -1:
        bottom = cells[Index(self.x, self.y+1)]
        if not(bottom.visited):
            neighbors.append(bottom)
    
    if Index(self.x-1, self.y) != -1:
        left = cells[Index(self.x-1, self.y)]
        if not(left.visited):
            neighbors.append(left)
    
    if (len(neighbors) > 0):
        r = random.randint(0,len(neighbors)-1)
        return neighbors[r]
    else:
        return None 

#main function
def Setup():
    global current, stack
    InitGrid()
    current = cells[0]
    stack = []
    while True:
        for event in pygame.event.get():
            #wait for end 
            if event.type == pygame.QUIT:
                sys.exit(0)
        #background
        screen.fill(WHITE)
        Draw()
        #update screen
        pygame.display.flip()
        #pygame.time.wait(1)
        if current == cells[0]:
            pygame.image.save(screen, "./maze.png")
            break
    bot.upload_photo("./maze.png", Caption="Solve maze :), red - start, green - end")

def InitGrid():
    for y in range(grid_h):
        for x in range(grid_w):
            cell = Cell(x,y)
            cells.append(cell)

def Draw():
    for cell in cells:
        cell.show()
    global current
    current.visited = True  
    #find next cell and mark it as visited
    next_current = current.checkNeighbors()
    if next_current:
        next_current.visited = True

        stack.append(current)
        #remove cells betweeen current and neighbor
        RemoveWalls(current, next_current)
        current = next_current
    elif len(stack) > 0:
        current = stack.pop()

def Index(x,y):
    if(x < 0 or y < 0 or x > grid_w-1 or y > grid_h -1):
        return -1
    return x + y * grid_w

def RemoveWalls(current, neighbour):
    x_diff = current.x - neighbour.x
    #  |B|A| -- > |B A|
    if x_diff == 1:
        current.left = False
        neighbour.right = False
    #   |A|B| --> |A B| example a=46,b=47 a-b=-1
    elif x_diff == -1:
        current.right = False
        neighbour.left = False

    y_diff = current.y - neighbour.y   
    #  |A|        |A|
    #  |-|  --->  | |
    #  |B|        |B|
    if y_diff == 1:
        current.top = False
        neighbour.bottom = False
    elif y_diff == -1:
        current.bottom = False
        neighbour.top = False      


    

Setup()
