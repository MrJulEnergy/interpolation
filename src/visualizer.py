import pygame
import numpy as np
from .trig_interp import trigonometric_interpolation

class Visualize:
    def __init__(self):
        # Ganz viele Variablen zum Verändern vom Aussehen
        self.fps: int = 60 # Frames-Per-Second
        self.window_size = (1000, 700) # Fenstergröße in pixeln
        self.window_title = "Interactive Trigonometric Interpolation" # Fenster Titel

        self.background_color = (32, 32, 32) # (RGB) Hintergrundfarbe

        self.point_color = (200, 10, 10) # (RGB) Punktfarbe
        self.point_radius = 5 # Punktradius
        self.hitbox = 10

        self.line_color = (200, 200, 200) # Interpolationslinien Farbe
        self.line_width =2 # Dicke der Interpolationslinien
        
        self.setup_window() # Fenster Erstellen
        self.run() # Interaktives ermöglichen


    def setup_window(self):
        # Boilerplate um ein Fenster zu bekommen

        self.running = True # Variable, die in der run() funktion gebraucht wird
        self.points = [] # Leeres Array zum initalisieren
        self.drag = False
        self.dragged_point_index = None
        self.offset_x, self.offset_y = 0, 0
        self.fs = np.array([[],[]]) # Leeres Array zum initalisieren

        self.clock = pygame.time.Clock() # um die fps zu regulieren
        pygame.init() # startet pygame

        self.screen = pygame.display.set_mode(self.window_size) # startet fenster mit der vorgegeben größe
        pygame.display.set_caption(self.window_title) # ändert fenster titel

        self.screen.fill(self.background_color) # malt den Hintergrund an
        pygame.display.update() # aktualiert das fenster, sodass alles gezeichnet wird (also hier nur der Hintergrund)

    
    def ready_for_interp(self, points):
        # Formatiert die punkte von pygame so, dass sie von der 
        # interpolations funktion gelesen weren kännen 
        # [(px1,py1), (px2,py2), (...), ...]
        # wird zu:
        # [[px1, px2, ...],[py1, py2, ...]]
        x_coords = [point[0] for point in points] # List Comprehension um das zu ermöglichen
        y_coords = [point[1] for point in points]
        return np.array([x_coords, y_coords]) 
        
    def run(self):
        # Funktion für alles "interaktive"
        while self.running: 
            pos = self.check_events() # Schaut, ob userinput angekommen ist seit dem letzen frame
            if pos is not None: # falls was passiert:
                self.points.append(pos) # die position an der geklickt wurde wird gespeichert
                self.fs = trigonometric_interpolation(self.ready_for_interp(self.points)) # zwischen allen punken wird interpoliert
            if self.drag:
                self.fs = trigonometric_interpolation(self.ready_for_interp(self.points))
            # Dann wird alles auf das fenster gemalt. von hinten nach vorne:
            self.screen.fill(self.background_color) # Hintergrund
            self.draw_line(self.fs) # Interpolationslinie
            self.draw_particles() # Punkte
            pygame.display.update() # Fenster aktualisieren, sodass änderungen sichtbar sind
            dt = self.clock.tick(self.fps) / 1000 # für die fps
        pygame.quit() # Falls self.running==False wird das fenster geschlossen

    def check_events(self):
        ev = pygame.event.get() # frage alle user inputs ab
        for event in ev: # iteriere über alle inputs (falls z.b. linke maus und "W" gleichzeitig gedrückt werden)
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.button)
                if event.button == 1:  # Linke Mausetaste
                    return event.pos # gebe die position zurück, die angeklickt wurde
                if event.button == 3: # Rechte Maustaste
                    for i in range(len(self.points)):
                        mouse_pos = np.array(event.pos)
                        point_pos = np.array(self.points[i])
                        if np.linalg.norm(mouse_pos - point_pos) < self.hitbox:
                            self.drag = True
                            self.dragged_point_index = i
                            self.offset = point_pos - mouse_pos

            elif event.type == pygame.MOUSEMOTION:
                if self.drag and self.dragged_point_index is not None:
                    mouse_x, mouse_y = event.pos
                    self.points[self.dragged_point_index] = (mouse_x + self.offset[0], mouse_y + self.offset[1])

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.drag = False
        return None

    def draw_particles(self):
        # Malt da einen Punkt, wo hingeklicht wurde
        for point in self.points:
            pygame.draw.circle(self.screen, self.point_color, point, self.point_radius)
    
    def draw_line(self, line_points):
        if line_points.shape[1] <= 1: # Malt erst eine Linie, wenn es einen Punkt gibt
            return
        else:
            points_list = list(zip(line_points[0], line_points[1]))
            pygame.draw.lines(self.screen, self.line_color, False, points_list, self.line_width)