import math
import sys
from typing import Tuple, List, Dict, Optional

import pygame

from intersection import Intersection
from car import Car
from rail import Rail


class IntersectionView:
    BACK_COLOUR = 0x2e, 0x7d, 0x32
    BORDER_COLOUR = 0, 0, 0
    ASPHALT_COLOUR = 0xcc, 0xcc, 0xcc
    LANE_WIDTH = 50
    BORDER_WIDTH = 5

    def __init__(self, *,
                 intersection: Intersection,
                 window_size: Tuple[int, int],
                 x_lanes: int,
                 y_lanes: int) -> None:
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
        #self.clock.tick(10)

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

        self.car_last_positions: Dict[Car, Tuple[int, int]] = {}

    def draw_cars(self, cars: List[Car], time: int):
        for car in cars:
            rail = car.rail
            scalar = car.get_pos(time)
            x, y = rail.get(scalar)
            y = -y

            # rotation
            rise = x - self.car_last_positions.get(car, (x, y))[0]
            run = y - self.car_last_positions.get(car, (x, y))[1]
            print(rise, run)
            if run:
                # no chance of a divide-by-0 error, so just calculate the angle
                angle = math.degrees(math.atan(rise / run))
                new_img = pygame.transform.rotate(self.car_img, angle-90)
            elif rise:
                # no change at all - don't transform i guess
                new_img = self.car_img
            else:
                # no x change so we're going vertically
                new_img = pygame.transform.rotate(self.car_img, -90)

            # new transformed rect
            new_rect = new_img.get_rect().copy()
            new_rect.center = (x + self.width/2, y + self.height/2)

            # draw onto screen
            self.screen.blit(new_img, new_rect)
            self.car_last_positions[car] = x, y

    def do_updates(self):
        super().do_updates()
        self.draw_cars(self.intersection.cars, self.time)


class SetupView(IntersectionView):
    CAR_HINT_MARGIN = 50

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pygame.display.set_caption("Setup")

        self.car_img = pygame.image.load("assets/car.png")
        self.car_img2 = pygame.image.load("assets/car2.png")
        # self.car_img_translucent = self.car_img.copy()
        # self.car_img_translucent.set_alpha(128)
        self.car_rect = self.car_img.get_rect()
        self.start_img = pygame.image.load("assets/start.png")

        # mode
        # 0 - place initial car position
        # 1 - place car end position
        self.mode = 0

        self.cars: List[Car] = []
        self.car_hint_showing = False
        self.rail_hint_showing = False

        # the "permanent hint" is the thing that stays on the screen
        # after you click a lane
        self.car_permanent_hint = self.car_img.get_rect()
        self.car_permanent_hint_rotated = False

        self.current_lane_bound_upper = 0
        self.current_lane_bound_lower = 0
        self.current_lane_area = 0

        centre_rect_width = self.y_lanes * self.LANE_WIDTH
        centre_rect_height = self.x_lanes * self.LANE_WIDTH
        self.centre_x = self.width / 2
        self.centre_y = self.height / 2
        self.centre_left_bound = self.centre_x - centre_rect_width / 2
        self.centre_right_bound = self.centre_x + centre_rect_width / 2
        self.centre_top_bound = self.centre_y - centre_rect_height / 2
        self.centre_bottom_bound = self.centre_y + centre_rect_height / 2

        self.current_rail: Optional[Rail] = None

        self.done = False  # program will exit when set to True

    def show_car_hint(self, mousex: int, mousey: int):
        self.car_hint_showing = False
        self.rail_hint_showing = False

        if mousex <= self.centre_left_bound:
            # left side of lines
            if self.x_lanes % 2 == 0:
                # even number of lanes
                # only check bottom
                for lane in range(self.x_lanes // 2):
                    lane_bound_upper = self.centre_y + self.LANE_WIDTH * lane
                    lane_bound_lower = self.centre_y + self.LANE_WIDTH * (lane + 1)
                    if lane_bound_upper <= mousey < lane_bound_lower:
                        self.car_hint_showing = True
                        new_rect = self.car_img2.get_rect().copy()
                        self.car_permanent_hint.center = new_rect.center = \
                            (self.centre_left_bound - self.CAR_HINT_MARGIN,
                             (lane_bound_lower + lane_bound_upper) / 2)
                        self.car_permanent_hint_rotated = False
                        self.screen.blit(self.car_img2, new_rect)
                        self.current_lane_bound_upper = lane_bound_upper
                        self.current_lane_bound_lower = lane_bound_lower
                        self.current_lane_area = self.centre_left_bound
        elif mousex >= self.centre_right_bound:
            # right side of lines
            if self.x_lanes % 2 == 0:
                # even number of lanes
                # only check top
                for lane in range(self.x_lanes // 2):
                    lane_bound_upper = self.centre_y - self.LANE_WIDTH * lane
                    lane_bound_lower = self.centre_y - self.LANE_WIDTH * (lane + 1)
                    if lane_bound_upper > mousey >= lane_bound_lower:
                        self.car_hint_showing = True
                        new_rect = self.car_img2.get_rect().copy()
                        self.car_permanent_hint.center = new_rect.center = \
                            (self.centre_right_bound + self.CAR_HINT_MARGIN,
                             (lane_bound_lower + lane_bound_upper) / 2)
                        self.car_permanent_hint_rotated = False
                        self.screen.blit(self.car_img2, new_rect)
                        self.current_lane_bound_upper = lane_bound_upper
                        self.current_lane_bound_lower = lane_bound_lower
                        self.current_lane_area = self.centre_right_bound
        elif mousey <= self.centre_top_bound:
            # top side of lines
            if self.y_lanes % 2 == 0:
                # even number of lanes
                # only check left
                for lane in range(self.y_lanes // 2):
                    lane_bound_left = self.centre_x - self.LANE_WIDTH * lane
                    lane_bound_right = self.centre_x - self.LANE_WIDTH * (lane + 1)
                    if lane_bound_left > mousex >= lane_bound_right:
                        self.car_hint_showing = True
                        new_img = pygame.transform.rotate(self.car_img2, -90)
                        new_rect = new_img.get_rect()
                        self.car_permanent_hint.center = new_rect.center = \
                            ((lane_bound_left + lane_bound_right) / 2,
                             self.centre_top_bound - self.CAR_HINT_MARGIN)
                        self.car_permanent_hint_rotated = True
                        self.screen.blit(new_img, new_rect)
                        self.current_lane_bound_upper = lane_bound_left
                        self.current_lane_bound_lower = lane_bound_right
                        self.current_lane_area = self.centre_top_bound
        elif mousey >= self.centre_bottom_bound:
            # right side of lines
            if self.y_lanes % 2 == 0:
                # even number of lanes
                # only check right
                for lane in range(self.x_lanes // 2):
                    lane_bound_left = self.centre_x + self.LANE_WIDTH * lane
                    lane_bound_right = self.centre_x + self.LANE_WIDTH * (lane + 1)
                    if lane_bound_left <= mousex < lane_bound_right:
                        self.car_hint_showing = True
                        new_img = pygame.transform.rotate(self.car_img2, 90)
                        new_rect = new_img.get_rect()
                        self.car_permanent_hint.center = new_rect.center = \
                            ((lane_bound_left + lane_bound_right) / 2,
                             self.centre_bottom_bound + self.CAR_HINT_MARGIN)
                        self.car_permanent_hint_rotated = True
                        self.screen.blit(new_img, new_rect)
                        self.current_lane_bound_upper = lane_bound_left
                        self.current_lane_bound_lower = lane_bound_right
                        self.current_lane_area = self.centre_bottom_bound

    def show_rail_hint(self, mousex: int, mousey: int):
        self.rail_hint_showing = False
        self.car_hint_showing = False

        if mousex <= self.centre_left_bound:
            # left side of lines
            if self.x_lanes % 2 == 0:
                # even number of lanes
                # only check top
                for lane in range(self.x_lanes // 2):
                    lane_bound_upper = self.centre_y - self.LANE_WIDTH * lane
                    lane_bound_lower = self.centre_y - self.LANE_WIDTH * (lane + 1)
                    if lane_bound_upper > mousey >= lane_bound_lower:
                        # update stuff
                        self.rail_hint_showing = True
                        self.current_rail_lane_bound_upper = lane_bound_upper
                        self.current_rail_lane_bound_lower = lane_bound_lower
                        self.current_rail_lane_area = self.centre_left_bound

                        # show coloured rail
                        for rail in self.intersection.rails:
                            if self._check_rail(rail):
                                endx, endy = rail.get(1000)
                                endy = -endy
                                #print(endy + self.height/2, lane_bound_upper, lane_bound_lower)
                                if lane_bound_upper > (endy + self.height/2) >= lane_bound_lower:
                                    pointlist = []
                                    for i in range(75, 1000):
                                        x, y = rail.get(i)
                                        y = -y
                                        pointlist.append((x + self.width/2, y + self.height/2))
                                    pygame.draw.lines(self.screen, (0xe6, 0x4a, 0x19), False, pointlist, 5)
                                    self.current_rail = rail
        elif mousex >= self.centre_right_bound:
            # right side of lines
            if self.x_lanes % 2 == 0:
                # even number of lanes
                # only check bottom
                for lane in range(self.x_lanes // 2):
                    lane_bound_upper = self.centre_y + self.LANE_WIDTH * lane
                    lane_bound_lower = self.centre_y + self.LANE_WIDTH * (lane + 1)
                    if lane_bound_upper <= mousey < lane_bound_lower:
                        # update stuff
                        self.rail_hint_showing = True
                        self.current_rail_lane_bound_upper = lane_bound_upper
                        self.current_rail_lane_bound_lower = lane_bound_lower
                        self.current_rail_lane_area = self.centre_right_bound

                        # show coloured rail
                        for rail in self.intersection.rails:
                            if self._check_rail(rail):
                                endx, endy = rail.get(1000)
                                endy = -endy
                                if lane_bound_upper <= (endy + self.height/2) < lane_bound_lower:
                                    pointlist = []
                                    for i in range(75, 1000):
                                        x, y = rail.get(i)
                                        y = -y
                                        pointlist.append((x + self.width/2, y + self.height/2))
                                    pygame.draw.lines(self.screen, (0xe6, 0x4a, 0x19), False, pointlist, 5)
                                    self.current_rail = rail
        elif mousey <= self.centre_top_bound:
            # top side of lines
            if self.y_lanes % 2 == 0:
                # even number of lanes
                # only check right
                for lane in range(self.y_lanes // 2):
                    lane_bound_left = self.centre_x + self.LANE_WIDTH * lane
                    lane_bound_right = self.centre_x + self.LANE_WIDTH * (lane + 1)
                    if lane_bound_left <= mousex < lane_bound_right:
                        # update stuff
                        self.rail_hint_showing = True
                        self.current_rail_lane_bound_upper = lane_bound_left
                        self.current_rail_lane_bound_lower = lane_bound_right
                        self.current_rail_lane_area = self.centre_top_bound

                        # show coloured rail
                        for rail in self.intersection.rails:
                            if self._check_rail(rail):
                                endx, endy = rail.get(1000)
                                endy = -endy
                                if lane_bound_left <= (endx + self.width/2) < lane_bound_right:
                                    pointlist = []
                                    for i in range(75, 1000):
                                        x, y = rail.get(i)
                                        y = -y
                                        pointlist.append((x + self.width/2, y + self.height/2))
                                    pygame.draw.lines(self.screen, (0xe6, 0x4a, 0x19), False, pointlist, 5)
                                    self.current_rail = rail
        elif mousey >= self.centre_bottom_bound:
            # right side of lines
            if self.y_lanes % 2 == 0:
                # even number of lanes
                # only check left
                for lane in range(self.x_lanes // 2):
                    lane_bound_left = self.centre_x - self.LANE_WIDTH * lane
                    lane_bound_right = self.centre_x - self.LANE_WIDTH * (lane + 1)
                    if lane_bound_left > mousex >= lane_bound_right:
                        # update stuff
                        self.rail_hint_showing = True
                        self.current_rail_lane_bound_upper = lane_bound_left
                        self.current_rail_lane_bound_lower = lane_bound_right
                        self.current_rail_lane_area = self.centre_right_bound

                        # show coloured rail
                        for rail in self.intersection.rails:
                            if self._check_rail(rail):
                                endx, endy = rail.get(1000)
                                endy = -endy
                                if lane_bound_left > (endx + self.width/2) >= lane_bound_right:
                                    pointlist = []
                                    for i in range(75, 1000):
                                        x, y = rail.get(i)
                                        y = -y
                                        pointlist.append((x + self.width/2, y + self.height/2))
                                    pygame.draw.lines(self.screen, (0xe6, 0x4a, 0x19), False, pointlist, 5)
                                    self.current_rail = rail

    def handle_start_button(self, event):
        if event.pos[0] > self.width - 100 and event.pos[1] > self.height - 100:
            self.done = True
            #pygame.quit()
            #sys.exit()

    def handle_event(self, event):
        super().handle_event(event)
        #if event.type == pygame.MOUSEMOTION:
        #    self.show_car_hint(*event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.car_hint_showing:
                self.mode = 1
            if self.rail_hint_showing:
                self.mode = 0
                self.cars.append(Car(1.0, self.current_rail, 0))
            self.handle_start_button(event)

    def _check_rail(self, rail: Rail) -> bool:
        x, y = rail.get(0)
        y = -y
        return ((self.current_lane_area == self.centre_left_bound
                    and self.current_lane_bound_upper <= (y + self.height/2) < self.current_lane_bound_lower)
                or (self.current_lane_area == self.centre_right_bound
                    and self.current_lane_bound_upper > (y + self.height/2) >= self.current_lane_bound_lower)
                or (self.current_lane_area == self.centre_top_bound
                    and self.current_lane_bound_upper > (x + self.width/2) >= self.current_lane_bound_lower)
                or (self.current_lane_area == self.centre_bottom_bound
                    and self.current_lane_bound_upper <= (x + self.width/2) < self.current_lane_bound_lower))

    def do_updates(self):
        super().do_updates()

        # show start button
        btn_rect = pygame.rect.Rect(self.width-100, self.height-100, 64, 64)
        self.screen.blit(self.start_img, btn_rect)

        mousex, mousey = pygame.mouse.get_pos()
        if self.mode == 0:
            self.show_car_hint(mousex, mousey)
        elif self.mode == 1:
            # make the car image stay on screen
            new_img = self.car_img
            new_rect = self.car_permanent_hint
            if self.car_permanent_hint_rotated:
                new_img = pygame.transform.rotate(new_img, 90)
                new_rect = new_img.get_rect()
                new_rect.center = self.car_permanent_hint.center
            self.screen.blit(new_img, new_rect)

            # draw rails
            for rail in self.intersection.rails:
                if self._check_rail(rail):
                    pointlist = []
                    for i in range(75, 1000):
                        x, y = rail.get(i)
                        y = -y
                        pointlist.append((x + self.width/2, y + self.height/2))
                    pygame.draw.lines(self.screen, (0xbb, 0xbb, 0xbb), False, pointlist, 5)

            # place end position
            self.show_rail_hint(mousex, mousey)
