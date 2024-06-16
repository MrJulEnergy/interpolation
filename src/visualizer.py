import pygame
import numpy as np
from .trig_interp import trigonometric_interpolation

class Visualize:
    def __init__(self):
        self.points = []
        self.fs = np.array([[],[]])
        self.bounds = [-5, 5, -5, 5] # xmim,xmax,ymin,ymax
        self.fps: int = 60
        self.window_size = (700, 700)
        self.window_title = "Interactive Trigonometric Interpolation"
        self.background_color = (32, 32, 32) # Dunkel Grau
        self.point_color = (150, 150, 150)
        self.point_radius = 10
        self.line_color = (200, 200, 200)
        

        self.bounds_center = np.array([(self.bounds[1]+self.bounds[0])/2, (self.bounds[3]+self.bounds[2])/2])
        self.bounds_width = self.bounds[1]-self.bounds[0]
        self.bounds_height = self.bounds[3]-self.bounds[2]
        self.min_idx = np.argmin(self.window_size)
        
        self.setup_window()
        self.run()


    def setup_window(self):
        # Einfuch nur Boilerplate um ein Fenster zu bekommen
        self.running = True
        self.clock = pygame.time.Clock()    
        pygame.init()

        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.window_title)
        
        self.screen.fill(self.background_color)
        pygame.display.update()

    def transform_coords(self, point):
        x, y = point

        norm_x = (x - self.bounds[0]) / (self.bounds[1] - self.bounds[0])
        norm_y = (y - self.bounds[2]) / (self.bounds[3] - self.bounds[2])
    
        scaled_x = norm_x * self.window_size[1]
        scaled_y = norm_y * self.window_size[1]
        return scaled_x, self.window_size[1]-scaled_y
    
    def inverse_transform_coords(self, screen_point):
        scaled_x, scaled_y = screen_point

        norm_x = scaled_x / self.window_size[1]
        norm_y = (self.window_size[1] - scaled_y) / self.window_size[1]

        x = norm_x * (self.bounds[1] - self.bounds[0]) + self.bounds[0]
        y = norm_y * (self.bounds[3] - self.bounds[2]) + self.bounds[2]

        return np.array([x, y])
    
    def ready_for_interp(self, points):
        # [(px1,py1), (px2,py2), (...), ...]
        x_coords = [point[0] for point in points]
        y_coords = [point[1] for point in points]
        return np.array([x_coords, y_coords])
        
    def run(self):
        while self.running:
            pos = self.check_events()
            if pos is not None:
                trans_pos = self.inverse_transform_coords(pos) # pixel to xy
                print(trans_pos)
                self.points.append(pos)
                
                self.fs = trigonometric_interpolation(self.ready_for_interp(self.points))
            
            self.screen.fill(self.background_color)
            self.draw_line(self.fs)
            self.draw_particles()
            pygame.display.update()
            dt = self.clock.tick(self.fps) / 1000
        pygame.quit()

    def check_events(self):
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linke Mausetaste
                    return event.pos
        return None

    def draw_particles(self):
        for point in self.points:
            #transformed_pos = self.transform_coords(poinz)
            pygame.draw.circle(self.screen, self.point_color, point, self.point_radius)
    
    def draw_line(self, line_points):
        if line_points.shape[1] <= 3:
            pass
        else:
            points_list = list(zip(line_points[0], line_points[1]))
            pygame.draw.lines(self.screen, self.line_color, False, points_list, 2)