import math
import sys
from typing import Tuple, List

import pygame

from intersection import Intersection
from car import Car


class IntersectionView:
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

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            # User clicked the close button
            sys.exit()

    def do_updates(self):
        # Background colour
        self.screen.fill(self.BACK_COLOUR)

        # draw stuff
        self.draw_intersection(self.x_lanes, self.y_lanes)

        # Respond to events
        for event in pygame.event.get():
            self.handle_event(event)

    def tick(self):
        # delay
        self.clock.tick(4)

        self.do_updates()

        # Update display
        pygame.display.flip()

        # Increment timer
        self.time += 1


class ZipperView(IntersectionView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pygame.display.set_caption("Traffic Zipper")

        self.car_img = pygame.image.load("assets/car.png")
        self.car_rect = self.car_img.get_rect()
        pygame.display.set_icon(self.car_img)

    def draw_cars(self, cars: List[Car], time: int):
        for car in cars:
            rail = car.rail
            scalar = car.get_pos(time)
            x, y = rail.fun(scalar)

            # rotation
            rise = x - self.lastx
            run = y - self.lasty
            print(rise, run)
            if run:
                # no chance of a divide-by-0 error, so just calculate the angle
                angle = math.degrees(math.atan(rise / run))
                new_img = pygame.transform.rotate(self.car_img, angle-90)
            elif rise:
                # no x change so we're going vertically
                new_img = pygame.transform.rotate(self.car_img, -90)
            else:
                # no change at all - don't transform i guess
                new_img = self.car_img

            # new transformed rect
            new_rect = new_img.get_rect().copy()
            new_rect.center = (x + self.width/2, y + self.height/2)

            # draw onto screen
            self.screen.blit(new_img, new_rect)
            self.lastx, self.lasty = x, y

    def do_updates(self):
        super().do_updates()
        self.draw_cars(self.intersection.cars, self.time)


class SetupView(IntersectionView):
    CAR_HINT_MARGIN = 50

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pygame.display.set_caption("Setup")

        self.car_img = pygame.image.load("assets/car.png")
        self.car_img_translucent = self.car_img.copy()
        self.car_img_translucent.set_alpha(0.5)
        self.car_rect = self.car_img.get_rect()

    def show_car_hint(self, mousex: int, mousey: int):
        x_lines = self.x_lanes + 1
        y_lines = self.y_lanes + 1
        centre_rect_width = self.y_lanes * self.LANE_WIDTH
        centre_rect_height = self.x_lanes * self.LANE_WIDTH
        centre_x = self.width / 2
        centre_y = self.height / 2
        centre_left_bound = centre_x - centre_rect_width / 2
        centre_right_bound = centre_x + centre_rect_width / 2
        centre_top_bound = centre_y - centre_rect_height / 2
        centre_bottom_bound = centre_y + centre_rect_height / 2

        if mousex <= centre_left_bound:
            # left side of lines
            if self.x_lanes % 2 == 0:
                # even number of lanes
                # only check bottom
                for lane in range(self.x_lanes // 2):
                    lane_bound_upper = centre_y + self.LANE_WIDTH * lane
                    lane_bound_lower = centre_y + self.LANE_WIDTH * (lane + 1)
                    if lane_bound_upper <= mousey < lane_bound_lower:
                        new_rect = self.car_img_translucent.get_rect().copy()
                        new_rect.center = (centre_left_bound - self.CAR_HINT_MARGIN,
                                           (lane_bound_lower + lane_bound_upper) / 2)
                        self.screen.blit(self.car_img_translucent, new_rect)
        elif mousex >= centre_right_bound:
            # right side of lines
            if self.x_lanes % 2 == 0:
                # even number of lanes
                # only check top
                for lane in range(self.x_lanes // 2):
                    lane_bound_upper = centre_y - self.LANE_WIDTH * lane
                    lane_bound_lower = centre_y - self.LANE_WIDTH * (lane + 1)
                    if lane_bound_upper > mousey >= lane_bound_lower:
                        new_rect = self.car_img_translucent.get_rect().copy()
                        new_rect.center = (centre_right_bound + self.CAR_HINT_MARGIN,
                                           (lane_bound_lower + lane_bound_upper) / 2)
                        self.screen.blit(self.car_img_translucent, new_rect)
        elif mousey <= centre_top_bound:
            # top side of lines
            if self.y_lanes % 2 == 0:
                # even number of lanes
                # only check left
                for lane in range(self.y_lanes // 2):
                    lane_bound_left = centre_x - self.LANE_WIDTH * lane
                    lane_bound_right = centre_x - self.LANE_WIDTH * (lane + 1)
                    if lane_bound_left > mousex >= lane_bound_right:
                        new_img = pygame.transform.rotate(self.car_img_translucent, -90)
                        new_rect = new_img.get_rect()
                        new_rect.center = ((lane_bound_left + lane_bound_right) / 2,
                                           centre_top_bound - self.CAR_HINT_MARGIN)
                        self.screen.blit(new_img, new_rect)
        elif mousey >= centre_bottom_bound:
            # right side of lines
            if self.y_lanes % 2 == 0:
                # even number of lanes
                # only check right
                for lane in range(self.x_lanes // 2):
                    lane_bound_left = centre_x + self.LANE_WIDTH * lane
                    lane_bound_right = centre_x + self.LANE_WIDTH * (lane + 1)
                    if lane_bound_left <= mousex < lane_bound_right:
                        new_img = pygame.transform.rotate(self.car_img_translucent, 90)
                        new_rect = new_img.get_rect()
                        new_rect.center = ((lane_bound_left + lane_bound_right) / 2,
                                           centre_bottom_bound + self.CAR_HINT_MARGIN)
                        self.screen.blit(new_img, new_rect)

    def handle_event(self, event):
        super().handle_event(event)
        #if event.type == pygame.MOUSEMOTION:
        #    self.show_car_hint(*event.pos)

    def do_updates(self):
        super().do_updates()
        mousex, mousey = pygame.mouse.get_pos()
        self.show_car_hint(mousex, mousey)
