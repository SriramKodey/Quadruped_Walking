import math
from controller import Robot, Motor
import numpy as np

robot = Robot()

TIME_STEP = 1

class Leg:
    def __init__(self , leg_name):
        self.sh = robot.getMotor("shoulder " + leg_name)
        self.el = robot.getMotor("elbow " + leg_name)

    def go_to(self, x, y):        
        l1 = 0.3
        l2 = 0.3
        self.current_x = x
        
        if y == 0: 
            y = 0.0001
             
        self.current_y = y

        theta_2 = math.acos((x**2 + y**2 - l1**2 - l2**2)/(2*l1*l2))

        theta_1 = math.atan(x/y) - math.atan((l2 * math.sin(theta_2)/(l1 + l2*math.cos(theta_2))))

        self.sh.setPosition(theta_1)
        self.el.setPosition(theta_2)
        
        print("theta_1 = ", theta_1)
        print("theta_2 = ", theta_2)

    def go_to_2(self, x, y):
        l1 = 0.3
        l2 = 0.3
        self.current_x = x
        self.current_y = y

        theta_2 = math.pi - math.acos((l1**2 + l2**2 - x**2 - y**2)/(2*l1*l2))

        theta_1 = math.atan(x/y) - math.atan((l2 * math.sin(theta_2)/(l1 + l2*math.cos(theta_2))))

        theta_1 = theta_1 - theta_2

        self.sh.setPosition(theta_1)
        self.el.setPosition(theta_2)
        
        print("theta_1 = ", theta_1)
        print("theta_2 = ", theta_2)
            
    def swing(self, i):
        #start = (-0.05, 0.4)
        #end = (0.05, 0.4)
        
        x = np.linspace(-0.1, 0.1, 25)
        y_1 = np.linspace(0.4, 0.37, 12)
        y_2 = np.linspace(0.37, 0.4, 13)
        y = np.append(y_1, y_2)
        
        self.go_to(x[i], y[i])
        
    def stance(self, i):
        #start = (0.05, 0.4)
        #end = (-0.05, 0.4)
        
        x = np.linspace(0.1, -0.1, 25)
        y = 0.4
        
        self.go_to(x[i], y)
        
 
class Quad:
    def __init__(self):
        self.lf = Leg("left front")
        self.rf = Leg("right front")
        self.rr = Leg("right rear")
        self.lr = Leg("left rear")

    def stand(self):
        self.lf.go_to(0, 0.4)
        self.rf.go_to(0, 0.4)
        self.lr.go_to(0, 0.4)
        self.rr.go_to(0, 0.4)
    
    def sit(self):
        self.lf.go_to(0, 0)
        self.rf.go_to(0, 0)
        self.lr.go_to(0, 0)
        self.rr.go_to(0, 0)

    def see_up(self):
        self.lf.go_to(0, 0.4)
        self.rf.go_to(0, 0.4)
        self.rr.go_to(0, 0.35)
        self.lr.go_to(0, 0.35)
        
    def set_height(self, y):
        self.lf.go_to(0, y)
        self.rf.go_to(0, y)
        self.rr.go_to(0, y)
        self.lr.go_to(0, y)
        
    def walk_position(self):
        self.lf.go_to(0.1, 0.4)
        self.rf.go_to(-0.1, 0.4)
        self.rr.go_to(0.1, 0.4)
        self.lr.go_to(-0.1, 0.4)
        
    def walk(self, i):
        step_length = 0.1
        
        if i<25:
            self.lf.stance(i)
            self.rf.swing(i)
            self.rr.stance(i)
            self.lr.swing(i)
            
        else:
            i = i - 25
            self.rf.stance(i)
            self.lf.swing(i)
            self.lr.stance(i)
            self.rr.swing(i)
        

i = 0

quad = Quad()

y = np.linspace(0.1, 0.5, 100)

while robot.step(TIME_STEP) != -1:
    quad.walk(i)
        
    i += 1
         
    if i == 50:
         i = 0
         