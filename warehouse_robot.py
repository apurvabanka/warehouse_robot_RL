from enum import Enum
import pygame
import sys
import os
from os import path

class RobotAction(Enum):
    LEFT=0
    DOWN=1
    RIGHT=2
    UP=3
    PICKUP=4
    DROPOFF=5

class GridTile(Enum):
    _FLOOR=0
    ROBOT=1
    SOURCE=2
    TARGET=3
    OBSTACLE=4

    def __str__(self):
        return self.name[:1]


current_dir = os.getcwd()


class WarehouseRobot:
    
    def __init__(self, grid_rows=6, grid_cols=6, fps=4):
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.reset()

        self.fps = fps
        self.last_action=''
        self._init_pygame()

    def _init_pygame(self):
        pygame.init()
        pygame.display.init()

        self.clock = pygame.time.Clock()

        self.action_font = pygame.font.SysFont("Calibre",30)
        self.action_info_height = self.action_font.get_height()

        self.cell_height = 64
        self.cell_width = 64
        self.cell_size = (self.cell_width, self.cell_height)

        self.window_size = (self.cell_width * self.grid_cols, self.cell_height * self.grid_rows + self.action_info_height)

        self.window_surface = pygame.display.set_mode(self.window_size)

        file_name = path.join(current_dir, "img/bot_blue.png")
        img = pygame.image.load(file_name)
        self.robot_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(current_dir, "img/bot_with_package.png")
        img = pygame.image.load(file_name)
        self.robot_package_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(current_dir, "img/floor.png")
        img = pygame.image.load(file_name)
        self.floor_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(current_dir, "img/package.png")
        img = pygame.image.load(file_name)
        self.source_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(current_dir, "img/target.png")
        img = pygame.image.load(file_name)
        self.goal_img = pygame.transform.scale(img, self.cell_size)

        file_name = path.join(current_dir, "img/obstacle.png")
        img = pygame.image.load(file_name)
        self.obstacle_img = pygame.transform.scale(img, self.cell_size)
    
    def reset(self, seed=None):
        self.robot_pos = [0,0]
        self.source_pos = [1,1]
        self.obstacle_pos = [2,3]
        self.has_object = False
        self.done = False

        self.target_pos = [3,4]
    
    def perform_action(self, robot_action:RobotAction) -> bool:
        
        self.last_action = robot_action
        reward = -1

        if robot_action == RobotAction.LEFT:
            if self.robot_pos[1]>0:
                if self.robot_pos[1]-1 != self.obstacle_pos[1]:
                    self.robot_pos[1]-=1
                else:
                    reward = -20
        elif robot_action == RobotAction.RIGHT:
            if self.robot_pos[1]<self.grid_cols-1:
                if self.robot_pos[1]+1 != self.obstacle_pos[1]:
                    self.robot_pos[1]+=1
                else:
                    reward = -20
        elif robot_action == RobotAction.UP:
            if self.robot_pos[0]>0:
                if self.robot_pos[0]-1 != self.obstacle_pos[0]:
                    self.robot_pos[0]-=1
                else:
                    reward = -20
        elif robot_action == RobotAction.DOWN:
            if self.robot_pos[0]<self.grid_rows-1:
                if self.robot_pos[0]+1 != self.obstacle_pos[0]:
                    self.robot_pos[0]+=1
                else:
                    reward = -20
        elif robot_action == RobotAction.PICKUP and self.robot_pos == self.source_pos:
            self.has_object = True
            self.source_pos = self.robot_pos
            reward = 25
        elif robot_action == RobotAction.DROPOFF:
            if self.has_object:
                if self.robot_pos == self.target_pos:
                    self.done = True
                    reward = 100
                else:
                    self.has_object = False
                    self.done = True
                    # self.source_pos = self.source_pos
                    reward = -25
        
        return self.done, reward
    
    def render(self):
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):

                if([r,c] == self.robot_pos):
                    print(GridTile.ROBOT, end=' ')
                elif([r,c] == self.target_pos):
                    print(GridTile.TARGET, end=' ')
                elif([r,c] == self.source_pos):
                    print(GridTile.SOURCE, end=' ')
                elif([r,c] == self.obstacle_pos):
                    print(GridTile.OBSTACLE, end=' ')
                else:
                    print(GridTile._FLOOR, end=' ')

            print()
        print()

        self._process_events()

        self.window_surface.fill((255,255,255))

        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                
                pos = (c * self.cell_width, r * self.cell_height)
                self.window_surface.blit(self.floor_img, pos)

                if([r,c] == self.target_pos):
                    self.window_surface.blit(self.goal_img, pos)

                if([r,c] == self.robot_pos):
                    self.window_surface.blit(self.robot_img, pos)
                if([r,c] == self.obstacle_pos):
                    self.window_surface.blit(self.obstacle_img, pos)
                
                if([r,c] == self.source_pos):
                    self.window_surface.blit(self.source_img, pos)
                
        text_img = self.action_font.render(f'Action: {self.last_action}', True, (0,0,0), (255,255,255))
        text_pos = (0, self.window_size[1] - self.action_info_height)
        self.window_surface.blit(text_img, text_pos)       

        pygame.display.update()

        self.clock.tick(self.fps)  

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
