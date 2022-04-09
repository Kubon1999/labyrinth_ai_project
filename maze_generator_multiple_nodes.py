from numpy import iterable
import dfs
import bfs
import pygame
import sys
import random
import globals
import dijkstra_search, a_star
import copy
import time
import timeit
import gc
from globals import algorithm_data
import matplotlib.pyplot as plt

random.seed(None, 2)
globals.initialize()
# other
cells = []

global time_dfs, time_bfs, time_dijkstra, time_a_star
time_dfs = -1
time_bfs = -1
time_dijkstra = -1
time_a_star = -1
# generowanie dlugich sciezek
directions = []  # 0 -> top;  1 -> right;  2 -> bottom;  3 -> left
tabliczka = [-1, -1, -1, -1]
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

#args
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv.__contains__("-h") or sys.argv.__contains__("-help"):
            print()
            print("=============================================================================")
            print("Dostępne opcje: ")
            print("-long percent    // percent of repeating last direction while building maze")
            print("-rwalls percent  // percent of walls to be removed")
            print("-size integer    // n by n size of maze")
            print("-print t/f       // Print process of building maze")
            print("-default         // Print default values of options")
            print("-rand t/f        // Make last point in random place")
            print("=============================================================================")
            sys.exit()
        if sys.argv.__contains__("-long"):
            indexxx = sys.argv.index("-long")
            if int(sys.argv[indexxx + 1]):
                globals.change_dir_pos = int(sys.argv[indexxx + 1]) / 100
        if sys.argv.__contains__("-rwalls"):
            indexxx = sys.argv.index("-rwalls")
            if int(sys.argv[indexxx + 1]) >= 0:
                globals.rwalls_perc = int(sys.argv[indexxx + 1]) / 100
        if sys.argv.__contains__("-size"):
            indexxx = sys.argv.index("-size")
            if int(sys.argv[indexxx + 1]):
                globals.grid_w = int(sys.argv[indexxx + 1])
                globals.grid_h = int(sys.argv[indexxx + 1])
        if sys.argv.__contains__("-print"):
            indexxx = sys.argv.index("-print")
            if ['true', 'false', 't', 'f', 'True', 'False'].__contains__(sys.argv[indexxx + 1]):
                globals.show_creating_maze = True
        if sys.argv.__contains__("-rand"):
            globals.finish_random = True

        if sys.argv.__contains__("-default"):
            print("================")
            print("-long ", int(globals.change_dir_pos * 100), "%")
            print("-rwalls ", int(globals.rwalls_perc * 100), "%")
            print("-size ", int(globals.grid_w))
            print("-print ", globals.show_creating_maze)
            print("-finish_random ", globals.finish_random)
            print("================")
            sys.exit()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.top = True
        self.right = True
        self.bottom = True
        self.left = True
        self.visited = False
        self.searched = False
        self.path = False
        self.distance = float("inf")
        self.parent = 0
        self.distance_from_end = float("inf")
        self.waga_left = 0
        self.waga_right = 0
        self.waga_up = 0
        self.waga_down = 0

    def show(self, my_offset_x, my_offset_y):
        position_x = self.x * globals.cell_size + my_offset_x
        position_y = self.y * globals.cell_size + my_offset_y
        EMPTY_COLOR = globals.GRAY

        if self.visited:
            pygame.draw.rect(globals.screen, EMPTY_COLOR, pygame.Rect(
                position_x, position_y, globals.cell_size, globals.cell_size))

        if self.searched:
            pygame.draw.rect(globals.screen, globals.BLUE, pygame.Rect(
                position_x, position_y, globals.cell_size, globals.cell_size))
            EMPTY_COLOR = globals.BLUE

        if self.path:
            pygame.draw.rect(globals.screen, globals.PURPLE, pygame.Rect(
                position_x, position_y, globals.cell_size, globals.cell_size))
            EMPTY_COLOR = globals.PURPLE

        if self == current:
            pygame.draw.rect(globals.screen, globals.RED, pygame.Rect(
                position_x, position_y, globals.cell_size, globals.cell_size))

        if self.x == globals.finish_x and self.y == globals.finish_y:
            pygame.draw.rect(globals.screen, globals.GREEN, pygame.Rect(
                position_x, position_y, globals.cell_size, globals.cell_size))

        if not(self.top):
            pygame.draw.line(globals.screen, EMPTY_COLOR, (position_x,           position_y),
                             (position_x+globals.cell_size, position_y),           globals.line_width)
        if not(self.right):
            pygame.draw.line(globals.screen, EMPTY_COLOR, (position_x+globals.cell_size, position_y +
                                                           globals.cell_size), (position_x, position_y+globals.cell_size),           globals.line_width)
        if not(self.bottom):
            pygame.draw.line(globals.screen, EMPTY_COLOR, (position_x+globals.cell_size, position_y +
                                                           globals.cell_size), (position_x, position_y+globals.cell_size),           globals.line_width)
        if not(self.left):
            pygame.draw.line(globals.screen, EMPTY_COLOR, (position_x,           position_y+globals.cell_size),
                             (position_x, position_y),                             globals.line_width)

        if self.top:
            pygame.draw.line(globals.screen, globals.BLACK, (position_x,                   position_y),
                             (position_x+globals.cell_size, position_y),                   globals.line_width)

        if self.right:
            pygame.draw.line(globals.screen, globals.BLACK, (position_x+globals.cell_size, position_y),
                             (position_x+globals.cell_size, position_y+globals.cell_size), globals.line_width)

        if self.bottom:
            pygame.draw.line(globals.screen, globals.BLACK, (position_x+globals.cell_size, position_y+globals.cell_size),
                             (position_x, position_y+globals.cell_size),                   globals.line_width)

        if self.left:
            pygame.draw.line(globals.screen, globals.BLACK, (position_x,                   position_y+globals.cell_size),
                             (position_x, position_y),                                     globals.line_width)

    def checkNeighbors(self):
        neighbors = []
        iterator = 0
        if Index(self.x, self.y - 1) != -1:
            top = cells[Index(self.x, self.y - 1)]
            if not (top.visited):
                neighbors.append(top)
                directions.append(0)
                tabliczka[0] = iterator
                iterator += 1

        if Index(self.x + 1, self.y) != -1:
            right = cells[Index(self.x + 1, self.y)]
            if not (right.visited):
                neighbors.append(right)
                directions.append(1)
                tabliczka[1] = iterator
                iterator += 1

        if Index(self.x, self.y + 1) != -1:
            bottom = cells[Index(self.x, self.y + 1)]
            if not (bottom.visited):
                neighbors.append(bottom)
                directions.append(2)
                tabliczka[2] = iterator
                iterator += 1

        if Index(self.x - 1, self.y) != -1:
            left = cells[Index(self.x - 1, self.y)]
            if not (left.visited):
                neighbors.append(left)
                directions.append(3)
                tabliczka[3] = iterator
                iterator += 1

        proc = random.random()
        if globals.change_dir_pos > proc and directions.__contains__(globals.last_direction):
            directions.clear()
            # print(globals.last_direction)
            return neighbors[tabliczka[globals.last_direction]]

        if (len(neighbors) > 0):
            r = random.randint(0, len(neighbors) - 1)
            globals.last_direction = r
            directions.clear()
            return neighbors[r]
        else:
            return None

# main function


def Setup():
    if globals.finish_random:
        globals.finish_x = random.randrange(1, globals.grid_w)
        globals.finish_y = random.randrange(1, globals.grid_h)
    global current, stack
    InitGrid()
    current = cells[0]
    stack = []
    obieg = 0
    while True:

        # background
        # if the end of generation - create nodes
        if current == cells[0] and cells[1].visited == True:
            # generate_tree.drawTree(cells)
            if obieg == 1:
                start_dfs = time.time()
                dfs_res = dfs.dfs(cells, cells[0])
                end_dfs = time.time()
                time_dfs = end_dfs - start_dfs
                saveMap(cells, globals.map_dfs, globals.stats_dfs)
                if dfs_res:
                    start_bfs = time.time()
                    bfs.bfs(cells, cells[0])
                    end_bfs = time.time()
                    time_bfs = end_bfs - start_bfs
                    saveMap(cells, globals.map_bfs, globals.stats_bfs)
                    # time.sleep(1000)
                    if globals.bfs_found_path:
                        start_dijkstra = time.time()
                        dijkstra_search.dijkstra(cells, cells[0])
                        end_dijkstra = time.time()
                        time_dijkstra = end_dijkstra - start_dijkstra
                        saveMap(cells, globals.map_dijkstra, globals.stats_dijkstra)
                        if globals.dijkstra_found_path:
                            start_a_star = time.time()
                            a_star.a_star(cells, cells[0])
                            end_a_star = time.time()
                            time_a_star = end_a_star - start_a_star
                            saveMap(cells, globals.map_a_star, globals.stats_a_star)                       
                            break

            if obieg == 0:
                # for cell in cells:
                #     cell.visited = False
                # usun 5 randomowych scian
                iterator = 0
                for cell in cells:
                    if cell.top: iterator += 1
                    if cell.right: iterator += 1
                    if cell.bottom: iterator += 1
                    if cell.left: iterator += 1
                iterator -= (2 * globals.grid_w + 2 * globals.grid_h)
                iterator /= 2
                N_usuniec = int(iterator * globals.rwalls_perc)
                for i in range(N_usuniec):
                    temp = random.randrange(0, len(cells)-1)
                    for cell in cells:
                        cell.visited = False
                    neighbor = cells[temp].checkNeighbors()
                    for cell in cells:
                        cell.visited = True
                    if neighbor:
                        RemoveWalls(cells[temp], neighbor)
                obieg = obieg + 1
                pygame.display.flip()

            # print(found)
            #print(found.x, found.y)
        # jestesmy  na ostatnim zakoncz zadanko i lec dalej drugim
        # if current.x == globals.grid_w-1 and current.y == globals.grid_h-1:
        #     print("tak")
        #     current = cells[0]
        #     stack = []
        # update screen
        Draw()
    zrobione = False
    koncz = False
    while True:
        if koncz == False:
            for event in pygame.event.get():
                # wait for end
                if event.type == pygame.QUIT:
                    sys.exit(0)
            if not(zrobione):
                globals.screen.fill(globals.WHITE)
                showMap(globals.map_dijkstra, "Dijkstra", globals.offset_map1,
                        globals.stats_dijkstra, time_dijkstra)
                showMap(globals.map_dfs, "DFS", globals.offset_map2,
                        globals.stats_dfs, time_dfs)
                showMap(globals.map_bfs, "BFS", globals.offset_map3,
                        globals.stats_bfs, time_bfs)
                showMap(globals.map_a_star, "A*", globals.offset,
                        globals.stats_a_star, time_a_star)
                    

                # for cell in cells:
                #     cell.show(globals.offset, globals.offset)
                zrobione = True
                pygame.display.flip()
                globals.map_a_star = []
                globals.map_dijkstra = []
                globals.map_bfs = []
                globals.map_dfs = []
            koncz = True
        else:
            break
        # pygame.time.sleep(100000)


def InitGrid():
    for y in range(globals.grid_h):
        for x in range(globals.grid_w):
            cell = Cell(x, y)
            cells.append(cell)


def Draw():
    if globals.show_creating_maze:
        for cell in cells:
            cell.show(globals.offset, globals.offset)
    global current
    current.visited = True

    # find next cell and mark it as visited
    next_current = current.checkNeighbors()
    if next_current:
        next_current.visited = True

        stack.append(current)
        # remove cells betweeen current and neighbor
        RemoveWalls(current, next_current)
        current = next_current
    elif len(stack) > 0:
        current = stack.pop()


def Index(x, y):
    if(x < 0 or y < 0 or x > globals.grid_w-1 or y > globals.grid_h - 1):
        return -1
    return x + y * globals.grid_w


def RemoveWalls(current, neighbour):
    x_diff = current.x - neighbour.x
    #  |B|A| -- > |B A|
    waga = random.randrange(1,4)
    if x_diff == 1:
        current.left = False
        neighbour.right = False
        current.waga_left = waga
        neighbour.waga_right = waga
    #   |A|B| --> |A B| example a=46,b=47 a-b=-1
    elif x_diff == -1:
        current.right = False
        neighbour.left = False
        current.waga_right = waga
        neighbour.waga_left = waga

    y_diff = current.y - neighbour.y
    #  |A|        |A|
    #  |-|  --->  | |
    #  |B|        |B|
    if y_diff == 1:
        current.top = False
        neighbour.bottom = False
        current.waga_top = waga
        neighbour.waga_bottom = waga
    elif y_diff == -1:
        current.bottom = False
        neighbour.top = False
        current.waga_bottom = waga
        neighbour.waga_top = waga


def saveMap(cells, saveTo, stats):
    searched_cells = 0
    for cell in cells:
        temp = Cell(cell.x, cell.y)
        temp.top = cell.top
        temp.right = cell.right
        temp.bottom = cell.bottom
        temp.left = cell.left
        temp.visited = cell.visited
        temp.searched = cell.searched
        temp.path = cell.path
        #temp = copy.deepcopy(cell)
        saveTo.append(temp)
        # reset cell
        cell.searched = False
        cell.path = False
        cell.distance = float("inf")
        cell.parent = 0


def showMap(alg_map, title, offset, stats, time_spent):
    shortest_path = False
    searched_cells_count = 0
    cells_count = 0
    path_length = 0
    for cell in alg_map:
        cell.show(offset, globals.offset)
        # save stats
        if cell.searched:
            searched_cells_count += 1
        cells_count = 0
        if cell.path:
            path_length += 1

    if title == "Dijkstra":
        globals.shortest_path = path_length
        shortest_path = True
    elif path_length <= globals.shortest_path:
        shortest_path = True
    #print(title)
    if(title == "Dijkstra"):
        globals.stats_dijkstra.append(algorithm_data(shortest_path, searched_cells_count, len(cells), path_length, time_spent))
    if(title == "DFS"):
        globals.stats_dfs.append(algorithm_data(shortest_path, searched_cells_count, len(cells), path_length, time_spent))
    if(title == "BFS"):
        globals.stats_bfs.append(algorithm_data(shortest_path, searched_cells_count, len(cells), path_length, time_spent))
    if(title == "A*"):
        globals.stats_a_star.append(algorithm_data(shortest_path, searched_cells_count, len(cells), path_length, time_spent))
    #globals.stats[-1].print()
    algorithm_name = myfont.render(title, False, (0, 0, 0))
    globals.screen.blit(algorithm_name, (offset, globals.offset_map1))

    #clear
symulacje = 40
for i in range(symulacje):
    cells = []
    print(i, f"{symulacje}")
    globals.grid_w += 1
    globals.grid_h += 1
    globals.offset_map1 = globals.grid_w * globals.cell_size + 20
    globals.offset_map1 = globals.grid_w * globals.cell_size + 20
    globals.offset_map2 = 2*(globals.grid_w * globals.cell_size) + 30
    globals.offset_map2 = 2*(globals.grid_w * globals.cell_size) + 30
    globals.offset_map3 = 3*(globals.grid_w * globals.cell_size) + 40
    globals.offset_map3 = 3*(globals.grid_w * globals.cell_size) + 40
    globals.offset_map4 = 4*(globals.grid_w * globals.cell_size) + 50
    globals.offset_map4 = 4*(globals.grid_w * globals.cell_size) + 50
    globals.finish_x = globals.grid_w-1
    globals.finish_y = globals.grid_h-1
    Setup()
    # for xd in globals.stats_dijkstra:
    #     xd.print()
    # for xd in globals.stats_a_star:
    #     xd.print()
    # for xd in globals.stats_bfs:
    #     xd.print()
    # for xd in globals.stats_dfs:
    #     xd.print()
count = 0
time_spent_dijkstra =[] #czas spedzony na przeszukanie w danej iteracji
searched_dijkstra =[] #ile % przeszukalo planszy
searched_a_star =[]
searched_dfs =[]
searched_bfs =[] 
path_length_dijkstra = []
path_length_a_star = []
path_length_dfs = []
path_length_bfs = []
czas_przeszukane_komorki_dijkstra = []
czas_przeszukane_komorki_a_star = []
czas_przeszukane_komorki_dfs = []
czas_przeszukane_komorki_bfs = []
                    #dlugosc trasy od iteracji


for t in globals.stats_dijkstra:
    time_spent_dijkstra.append(t.time_spent)
    searched_dijkstra.append((t.searched_cells_count/t.cells_count)*100)
    path_length_dijkstra.append(t.path_length)
    czas_przeszukane_komorki_dijkstra.append((t.time_spent/t.searched_cells_count))

time_spent_a_star =[]
for t in globals.stats_a_star:
    time_spent_a_star.append(t.time_spent)
    searched_a_star.append((t.searched_cells_count/t.cells_count)*100)
    path_length_a_star.append(t.path_length)
    czas_przeszukane_komorki_a_star.append((t.time_spent/t.searched_cells_count))

time_spent_dfs =[]
for t in globals.stats_dfs:
    time_spent_dfs.append(t.time_spent)
    searched_dfs.append((t.searched_cells_count/t.cells_count)*100)
    path_length_dfs.append(t.path_length)
    czas_przeszukane_komorki_dfs.append((t.time_spent/t.searched_cells_count))


time_spent_bfs =[]
for t in globals.stats_bfs:
    time_spent_bfs.append(t.time_spent)
    searched_bfs.append((t.searched_cells_count/t.cells_count)*100)
    path_length_bfs.append(t.path_length)
    czas_przeszukane_komorki_bfs.append((t.time_spent/t.searched_cells_count))


fig, axs = plt.subplots(2, 2, figsize=(15,10))
axs[0, 0].plot(time_spent_dijkstra,'.',linewidth = random.randrange(1,4), label='dijkstra')
axs[0, 0].plot(time_spent_a_star,'--', label='a*')
axs[0, 0].plot(time_spent_bfs,'-.', label='bfs')
axs[0, 0].plot(time_spent_dfs,'-.', label='dfs')
axs[0, 0].set_title('Czas szukania rozwiazania do iteracji')
axs[0,0].set(xlabel='iteracja', ylabel='czas [s]')
axs[0,0].legend()

axs[0, 1].plot(searched_dijkstra,'.', label='dijkstra')
axs[0, 1].plot(searched_a_star,'--', label='a*')
axs[0, 1].plot(searched_bfs,'-.', label='bfs')
axs[0, 1].plot(searched_dfs,'-.', label='dfs')
axs[0, 1].set_title('procent przeszukanych pol od iteracji')
axs[0,1].set(xlabel='iteracja', ylabel='procent')
axs[0,1].legend()

axs[1, 0].plot(path_length_dijkstra,'.', label='dijkstra')
axs[1, 0].plot(path_length_a_star,'--', label='a*')
axs[1, 0].plot(path_length_bfs,'-.', label='bfs')
axs[1, 0].plot(path_length_dfs,'-.', label='dfs')
axs[1, 0].set_title('dlugosc sciezki od iteracji')
axs[1,0].set(xlabel='iteracja', ylabel='dlugosc sciezki')
axs[1,0].legend()

axs[1, 1].plot(czas_przeszukane_komorki_dijkstra, label='dijkstra')
axs[1, 1].plot(czas_przeszukane_komorki_a_star, label='a*')
axs[1, 1].plot(czas_przeszukane_komorki_bfs, label='bfs')
axs[1, 1].plot(czas_przeszukane_komorki_dfs, label='dfs')
axs[1, 1].set_title('srednia szybkosc przeszukiwania komorki')
axs[1,1].set(xlabel='iteracja', ylabel='czas [s]/ilosc przeszukanych komórek')
axs[1,1].legend()

plt.show()



