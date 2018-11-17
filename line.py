import numpy as np
from dcel import Vertex
class Line:
    def __init__(self, endpoint_1, endpoint_2):
        if (endpoint_1.coordinates[1] > endpoint_2.coordinates[1]):
            self.upper_endpoint = endpoint_1
            self.lower_endpoint = endpoint_2
        elif (endpoint_1.coordinates[1] < endpoint_2.coordinates[1]):
            self.upper_endpoint = endpoint_2
            self.lower_endpoint = endpoint_1
        elif (endpoint_1.coordinates[0] < endpoint_2.coordinates[0]):
            self.upper_endpoint = endpoint_1
            self.lower_endpoint = endpoint_2
        else:
            self.upper_endpoint = endpoint_2
            self.lower_endpoint = endpoint_1
    
    def intersect(self, line):
        x1, y1 = self.upper_endpoint.coordinates
        x2, y2 = self.lower_endpoint.coordinates
        x3, y3 = line.upper_endpoint.coordinates
        x4, y4 = line.lower_endpoint.coordinates
        if (x4-x3)*(y2-y1) == (x1-x2)*(y3-y4):
            return None
        xi = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4))/((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
        yi = ((x1*y2-y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4))/((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
        if xi < max(min(x1, x2), min(x3, x4)) or xi > min(max(x1, x2), max(x3, x4)):
            return None
        return Vertex((xi, yi))
    
    def point_location(self, point):
        '''
        +1 là bên phải
        -1 là bên trái
        '''
        x1, y1 = self.upper_endpoint.coordinates
        x2, y2 = self.lower_endpoint.coordinates
        x, y = point.coordinates
        if abs((x2 - x1)*(y - y1) - (y2 - y1)*(x - x1)) < 1e-4:
            return 0
        return np.sign((x2 - x1)*(y - y1) - (y2 - y1)*(x - x1))
    
    def get_lower_angle(self):
        x1, y1 = self.upper_endpoint.coordinates
        x2, y2 = self.lower_endpoint.coordinates
        angle = np.arctan2(y2-y1, x2-x1)*180/np.pi
        if angle <= 0:
            angle += 360
        return angle
    
    def get_upper_angle(self):
        x1, y1 = self.lower_endpoint.coordinates
        x2, y2 = self.upper_endpoint.coordinates
        
        angle = np.arctan2(y2-y1, x2-x1)*180/np.pi
        if angle < 0:
            angle += 360
        return angle
    
    def get_x(self, y):
        x1, y1 = self.lower_endpoint.coordinates
        x2, y2 = self.upper_endpoint.coordinates
        # Is Vertical Line
        if (y1 == y2):
            return x1
        x = (y - y1)/(y2 - y1)*(x2 - x1) + x1
        return x
    
    def is_vertical(self):
        _, y1 = self.lower_endpoint.coordinates
        _, y2 = self.upper_endpoint.coordinates
        return y1 == y2
    
        
    def compare_lower(self, point, line):
        point_loc = self.point_location(point)
        if point_loc != 0:
            return -point_loc
        a1 = self.get_lower_angle()
        a2 = line.get_lower_angle()
        return a1 - a2
    
    def compare_upper(self, point, line):
        point_y = point.coordinates[1]
        if line.is_vertical():
            intersect_point = point
        else:
            intersect_point = Vertex((line.get_x(point_y), point_y))
        point_loc = self.point_location(intersect_point)
        if point_loc != 0:
            return -point_loc
        a1 = self.get_upper_angle()
        a2 = line.get_upper_angle()
        return a2 - a1
    
    def __eq__(self, other):
        if isinstance(other, Line):
            return self.upper_endpoint.coordinates == other.upper_endpoint.coordinates and self.lower_endpoint.coordinates == other.lower_endpoint.coordinates
        return False