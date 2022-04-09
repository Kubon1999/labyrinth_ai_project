#global
import pygame 
def initialize():
    global grid_w, grid_h, screen_w, screen_h, offset,cell_size,line_width, GREEN, BLUE, WHITE, BLACK, RED, PURPLE, GRAY, screen, offset_map1, offset_map2, offset_map3
    global bfs_found_path, stats_dfs, stats_bfs, stats_dijkstra, last_direction, change_dir_pos, dijkstra_found_path, stats_a_star, offset_map4, stats
    global map_dfs, map_bfs, map_a_star, map_dijkstra, rwalls_perc, show_creating_maze, finish_x, finish_y, finish_random
    grid_w = 5
    grid_h = 5
    screen_w = 1850#1280
    screen_h = 500#720
    offset = 10
    cell_size = 7
    line_width = 1
    offset_map1 = grid_w * cell_size + 20
    offset_map1 = grid_w * cell_size + 20
    offset_map2 = 2*(grid_w * cell_size) + 30
    offset_map2 = 2*(grid_w * cell_size) + 30
    offset_map3 = 3*(grid_w * cell_size) + 40
    offset_map3 = 3*(grid_w * cell_size) + 40
    offset_map4 = 4*(grid_w * cell_size) + 50
    offset_map4 = 4*(grid_w * cell_size) + 50
    #colors
    GREEN = (0, 222, 0)
    BLUE = (0, 0, 222)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (222, 0, 0)
    PURPLE = (190, 120 ,219)
    GRAY = (220,220,220)
    screen = pygame.display.set_mode((screen_w,screen_h))
    bfs_found_path = False
    dijkstra_found_path = False
    stats_dfs = []
    stats_bfs = []
    stats_dijkstra = []
    stats_a_star = []
    last_direction = 0
    change_dir_pos = 0
    stats = []
    map_dfs = []
    map_bfs = []
    map_dijkstra = []
    map_a_star = []
    rwalls_perc = 0
    show_creating_maze = False
    finish_x = grid_w - 1
    finish_y = grid_h - 1
    finish_random = False

class algorithm_data:
    def __init__(self, shortest_path, searched_cells_count, cells_count, path_length, time_spent):
        self.shortest_path = shortest_path
        self.searched_cells_count = searched_cells_count
        self.cells_count = cells_count
        self.path_length = path_length
        self.time_spent = time_spent

    def print(self):
        print("shortest_path: " , self.shortest_path, "searched_cells_count: ", self.searched_cells_count, "cells_count: ", self.cells_count, "path_length: ",
        self.path_length, "time_spent: ", self.time_spent)




