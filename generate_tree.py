import pygame 
import globals
globals.initialize()

class Tree:
    def __init__(self):
        self.childs = []


def drawTree(cells):
    #create nodes
    for cell in cells:
        position_x = cell.x * globals.cell_size +globals.offset
        position_y = cell.y * globals.cell_size +globals.offset

        if not(cell.top and cell.bottom and not(cell.left) and not(cell.right)) and not(cell.left and cell.right and not(cell.top) and not(cell.bottom)):   
            pygame.draw.circle(globals.screen, globals.RED, (position_x+globals.cell_size/2, position_y+globals.cell_size/2),5)
        #_
        #_
        if cell.top and cell.bottom and not(cell.left) and not(cell.right):
            pygame.draw.line(globals.screen, globals.RED, (position_x,position_y+globals.cell_size/2),(position_x+globals.cell_size, position_y+globals.cell_size/2),globals.line_width)
        #| |
        if cell.left and cell.right and not(cell.top) and not(cell.bottom):
            pygame.draw.line(globals.screen, globals.RED, (position_x+globals.cell_size/2,position_y),(position_x+globals.cell_size/2, position_y+globals.cell_size),globals.line_width)

#def createTree(cells):
    #root = cells[0]
    #for cell in cells:
      #  if not(cell.top and cell.bottom and not(cell.left) and not(cell.right)) and not(cell.left and cell.right and not(cell.top) and not(cell.bottom)):
            #to jest node do dodania do drzewa
            #dodaj sasiednie node do tego