import math
import sys
from typing import Tuple, List

import pygame

from intersection import Intersection
from car import Car


class ZipperView:
    BACK_COLOUR = 0x2e, 0x7d, 0x32
    BORDER_COLOUR = 0, 0, 0
    ASPHALT_COLOUR = 0xcc, 0xcc, 0xcc
    LANE_WIDTH = 60
    BORDER_WIDTH = 5

    def __init__(self, *,
                 intersection: Intersection,
                 window_size: Tuple[int, int],
                 x_lanes: int,
                 y_lanes: int):
        self.intersection = intersection
        self.width, self.height = window_size
        self.x_lanes = x_lanes
        self.y_lanes = y_lanes
        self.time = 0
        self.lastx = self.lasty = 0

        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Traffic Zipper")

        self.car_img = pygame.image.load("assets/car.png")
        self.car_rect = self.car_img.get_rect()
        pygame.display.set_icon(self.car_img)

        self.clock = pygame.time.Clock()

    def draw_intersection(self, x_lanes: int, y_lanes: int):
        x_lines = x_lanes + 1
        y_lines = y_lanes + 1
        centre_rect_width = y_lanes * self.LANE_WIDTH
        centre_rect_height = x_lanes * self.LANE_WIDTH
        centre_x = self.width / 2
        centre_y = self.height / 2
        centre_left_bound = centre_x - centre_rect_width / 2
        centre_right_bound = centre_x + centre_rect_width / 2
        centre_top_bound = centre_y - centre_rect_height / 2
        centre_bottom_bound = centre_y + centre_rect_height / 2

        # asphalt
        # horizontal
        pygame.draw.line(self.screen,                       # display
                         self.ASPHALT_COLOUR,               # colour
                         (0, centre_y),                     # startpos
                         (self.width, centre_y),            # endpos
                         centre_rect_height)                # width
        # vertical
        pygame.draw.line(self.screen,                       # display
                         self.ASPHALT_COLOUR,               # colour
                         (centre_x, 0),                     # startpos
                         (centre_x, self.height),           # endpos
                         centre_rect_width)                 # width

        # lines
        # horizontal
        if x_lines % 2 != 0:
            # left side
            # centre line
            pygame.draw.line(self.screen,                    # display
                             self.BORDER_COLOUR,             # colour
                             (0, centre_y),                  # startpos
                             (centre_left_bound, centre_y),  # endpos
                             self.BORDER_WIDTH)              # width
            # lines above
            for above_index in range(1, x_lines // 2 + 1):
                y = centre_y + above_index * self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (0, y),                      # startpos
                                 (centre_left_bound, y),      # endpos
                                 self.BORDER_WIDTH)           # width
            # lines below
            for below_index in range(1, x_lines // 2 + 1):
                y = centre_y - below_index * self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (0, y),                      # startpos
                                 (centre_left_bound, y),      # endpos
                                 self.BORDER_WIDTH)           # width
            # right side
            # centre line
            pygame.draw.line(self.screen,                     # display
                             self.BORDER_COLOUR,              # colour
                             (self.width, centre_y),          # startpos
                             (centre_right_bound, centre_y),  # endpos
                             self.BORDER_WIDTH)               # width
            # lines above
            for above_index in range(1, x_lines // 2 + 1):
                y = centre_y + above_index * self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (self.width, y),             # startpos
                                 (centre_right_bound, y),     # endpos
                                 self.BORDER_WIDTH)           # width
            # lines below
            for below_index in range(1, x_lines // 2 + 1):
                y = centre_y - below_index * self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (self.width, y),             # startpos
                                 (centre_right_bound, y),     # endpos
                                 self.BORDER_WIDTH)           # width
        else:
            # left side
            # lines above
            for above_index in range(x_lines // 2):
                y = centre_y + self.LANE_WIDTH/2 + above_index*self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (0, y),                      # startpos
                                 (centre_left_bound, y),      # endpos
                                 self.BORDER_WIDTH)           # width
            # lines below
            for below_index in range(x_lines // 2):
                y = centre_y - self.LANE_WIDTH/2 - below_index*self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (0, y),                      # startpos
                                 (centre_left_bound, y),      # endpos
                                 self.BORDER_WIDTH)           # width
            # right side
            # lines above
            for above_index in range(x_lines // 2):
                y = centre_y + self.LANE_WIDTH/2 + above_index*self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (self.width, y),             # startpos
                                 (centre_right_bound, y),     # endpos
                                 self.BORDER_WIDTH)           # width
            # lines below
            for below_index in range(x_lines // 2):
                y = centre_y - self.LANE_WIDTH/2 - below_index*self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (self.width, y),             # startpos
                                 (centre_right_bound, y),     # endpos
                                 self.BORDER_WIDTH)           # width

        # vertical
        if y_lines % 2 != 0:
            # top side
            # centre line
            pygame.draw.line(self.screen,                    # display
                             self.BORDER_COLOUR,             # colour
                             (centre_x, 0),                  # startpos
                             (centre_x, centre_top_bound),   # endpos
                             self.BORDER_WIDTH)              # width
            # lines above
            for above_index in range(1, y_lines // 2 + 1):
                x = centre_x + above_index * self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (x, 0),                      # startpos
                                 (x, centre_top_bound),       # endpos
                                 self.BORDER_WIDTH)           # width
            # lines below
            for below_index in range(1, y_lines // 2 + 1):
                x = centre_x - below_index * self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (x, 0),                      # startpos
                                 (x, centre_top_bound),       # endpos
                                 self.BORDER_WIDTH)           # width
            # right side
            # centre line
            pygame.draw.line(self.screen,                     # display
                             self.BORDER_COLOUR,              # colour
                             (centre_x, self.height),         # startpos
                             (centre_x, centre_bottom_bound),  # endpos
                             self.BORDER_WIDTH)               # width
            # lines above
            for above_index in range(1, y_lines // 2 + 1):
                x = centre_x + above_index * self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (x, self.height),            # startpos
                                 (x, centre_bottom_bound),    # endpos
                                 self.BORDER_WIDTH)           # width
            # lines below
            for below_index in range(1, y_lines // 2 + 1):
                x = centre_x - below_index * self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (x, self.height),            # startpos
                                 (x, centre_bottom_bound),    # endpos
                                 self.BORDER_WIDTH)           # width
        else:
            # left side
            # lines above
            for above_index in range(y_lines // 2):
                x = centre_x + self.LANE_WIDTH/2 + above_index*self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (x, 0),                      # startpos
                                 (x, centre_top_bound),       # endpos
                                 self.BORDER_WIDTH)           # width
            # lines below
            for below_index in range(y_lines // 2):
                x = centre_x - self.LANE_WIDTH/2 - below_index*self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (x, 0),                      # startpos
                                 (x, centre_top_bound),       # endpos
                                 self.BORDER_WIDTH)           # width
            # right side
            # lines above
            for above_index in range(y_lines // 2):
                x = centre_x + self.LANE_WIDTH/2 + above_index*self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (x, self.height),            # startpos
                                 (x, centre_bottom_bound),    # endpos
                                 self.BORDER_WIDTH)           # width
            # lines below
            for below_index in range(y_lines // 2):
                x = centre_x - self.LANE_WIDTH/2 - below_index*self.LANE_WIDTH
                pygame.draw.line(self.screen,                 # display
                                 self.BORDER_COLOUR,          # colour
                                 (x, self.height),            # startpos
                                 (x, centre_bottom_bound),    # endpos
                                 self.BORDER_WIDTH)           # width

        # corners
        # top left
        top_left_corner = pygame.rect.Rect(centre_left_bound-self.BORDER_WIDTH//2,
                                           centre_top_bound-self.BORDER_WIDTH//2,
                                           self.BORDER_WIDTH,
                                           self.BORDER_WIDTH)
        self.screen.fill(self.BORDER_COLOUR, top_left_corner)
        # top right
        top_right_corner = pygame.rect.Rect(centre_right_bound-self.BORDER_WIDTH//2,
                                            centre_top_bound-self.BORDER_WIDTH//2,
                                            self.BORDER_WIDTH,
                                            self.BORDER_WIDTH)
        self.screen.fill(self.BORDER_COLOUR, top_right_corner)
        # bottom left
        bottom_left_corner = pygame.rect.Rect(centre_left_bound-self.BORDER_WIDTH//2,
                                              centre_bottom_bound-self.BORDER_WIDTH//2,
                                              self.BORDER_WIDTH,
                                              self.BORDER_WIDTH)
        self.screen.fill(self.BORDER_COLOUR, bottom_left_corner)
        # bottom right
        bottom_right_corner = pygame.rect.Rect(centre_right_bound-self.BORDER_WIDTH//2,
                                               centre_bottom_bound-self.BORDER_WIDTH//2,
                                               self.BORDER_WIDTH,
                                               self.BORDER_WIDTH)
        self.screen.fill(self.BORDER_COLOUR, bottom_right_corner)

    def draw_cars(self, cars: List[Car], time: int):
        for car in cars:
            rail = car.rail
            scalar = car.get_pos(time)
            x, y = rail.fun(scalar)

            # rotation
            rise = x - self.lastx
            run = y - self.lasty
            if run:
                angle = math.degrees(math.atan(rise / run))
                new_img = pygame.transform.rotate(self.car_img, angle-90)
            else:
                new_img = self.car_img

            # new transformed rect
            new_rect = new_img.get_rect().copy()
            new_rect.center = (x + self.width/2, y + self.height/2)

            # draw onto screen
            self.screen.blit(new_img, new_rect)
            self.lastx, self.lasty = x, y

    def tick(self):
        # delay
        self.clock.tick(4)

        # Respond to events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # User clicked the close button
                sys.exit()

        # Background colour
        self.screen.fill(self.BACK_COLOUR)

        # draw stuff
        self.draw_intersection(self.x_lanes, self.y_lanes)
        self.draw_cars(self.intersection.cars, self.time)

        # Update display
        pygame.display.flip()

        # Increment timer
        self.time += 1
