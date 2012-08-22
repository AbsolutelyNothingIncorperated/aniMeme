import pygame
from random import randint, choice
import matplotlib.pyplot as plt


MUTATION_COEF = 1
SHARING_COEF = .1
SEEING_VALUE = 10
ANTI_SEEING_VALUE = 10
BOARD_SIDE_LENGTH = 400


class gui():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_SIDE_LENGTH,BOARD_SIDE_LENGTH))
        self.black = 0,0,0
        pygame.display.flip()
    def draw (self,actors):
        self.screen.fill(self.black)
        for actor in actors:
            x = (2*actor.x)
            y = (2*actor.y)
            red,green,blue = 0,0,0
            if actor.color == 'red':
                red = actor.colors['red']
            elif actor.color == 'green':
                green = actor.colors['green']
            elif actor.color == 'blue':
                blue = actor.colors['blue']
            pygame.draw.rect(self.screen, (red,green,blue), (x, y, 2, 2))
        pygame.display.flip()
    def flash (self,x,y):
        pygame.draw.rect(self.screen, (255,255,255), (x*2, y*2, 2, 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        
class sim():
    def __init__(self):
        self.iteration = 0
        self.actors = {}
        for i in range(0,600):
            self.actors[i] = actor(i, randint(1,BOARD_SIDE_LENGTH/2), randint(1,BOARD_SIDE_LENGTH/2),self)
        self.gui = gui()
        self.draw()
    def iterate(self):
        self.iteration += 1
        print "Iteration",self.iteration
        for actor in self.actors.values():
            actor.act()
    def draw(self):
        self.gui.draw(self.actors.values())
    def run(self,x):
        for i in range(0,x):
            self.iterate()
            self.draw()
    def infrun(self):
        while True:
            self.iterate()
            self.draw()
    def getinfo(self, name):
        print "name\t",self.actors[name].name
        print "red\t",self.actors[name].colors['red']
        print "green\t",self.actors[name].colors['green']
        print "blue\t",self.actors[name].colors['blue']
        print "color\t",self.actors[name].color
        self.gui.flash(self.actors[name].x,self.actors[name].y)
        self.draw()
    def datarun(self):
        self.data = []
        self.data.append(self.getcolordata())
        for i in range(0,500):
            self.run(100)
            newdata = self.getcolordata()
            self.data.append(newdata)
            if [bool(newdata[0]), bool(newdata[1]), bool(newdata[2])].sort() == [False, False, True]:
                print "Ended a run" #if only one of the three colors is present
                break
            
        
    def getcolordata(self):
        red = 0
        green = 0
        blue = 0
        for actor in self.actors.values():
            if actor.color == 'red':
                red += 1
            elif actor.color == 'green':
                green += 1
            elif actor.color == 'blue':
                blue += 1
        return (red,green,blue)
            
class actor():
    def __init__(self,name,x,y,parent):
        self.name = name
        self.x = x
        self.y = y
        self.parent = parent
        self.colors = {}
        self.colors['blue'] = randint(1,100)
        self.colors['green'] = randint(1,100)
        self.colors['red'] = randint(1,100)
        self.color = ''
        print "added actor at",x,",",y
        self.sanitize()
        
    def act(self):
        self.x += self.getxmove()
        self.y += self.getymove()
        o_r = self.colors['red']
        o_g = self.colors['green']
        o_b = self.colors['blue']
        count = 0
        for actor in self.parent.actors.values():
            if abs(actor.x-self.x) < 6 and abs(actor.y-self.y) < 6:
                if not actor is self:
                    self.see(actor)
                    count += 1
        for color in self.colors:
            self.colors[color] -= 1
        #print self.name,"|",count,"|",self.colors['red']-o_r,"|",self.colors['green']-o_g,"|",self.colors['blue']-o_b
        #self.mutate()
        self.sanitize()
                
    def getxmove(self):
        choices = [-1,0,1]
        return choice(choices) # the rest of these functions was a silly idea
        direction = 0
        if self.x > 100:
            direction = -1
        elif self.x < 100:
            direction = 1
        if self.colors[self.color] > 150:
            choices.append(direction)
        if self.colors[self.color] > 200:
            choices.append(direction)
        if self.colors[self.color] < 100:
            choices.append(-direction)
        if self.colors[self.color] < 50:
            choices.append(-direction)
        return choice(choices)      
    
    def getymove(self):
        choices = [-1,0,1]
        return choice(choices)
        direction = 0
        if self.y > 100:
            direction = -1
        elif self.y < 100:
            direction = 1
        if self.colors[self.color] > 150:
            choices.append(direction)
        if self.colors[self.color] > 200:
            choices.append(direction)
        if self.colors[self.color] < 100:
            choices.append(-direction)
        if self.colors[self.color] < 50:
            choices.append(-direction)
        return choice(choices)      
    
    def see(self,actor):
        self.colors[actor.color] += 2
        self.sanitize()
        
    def sanitize(self):
        if self.x > BOARD_SIDE_LENGTH/2:
            self.x = BOARD_SIDE_LENGTH/2
        elif self.x < 0:
            self.x = 0
        if self.y > BOARD_SIDE_LENGTH/2:
            self.y = BOARD_SIDE_LENGTH/2
        elif self.y < 0:
            self.y = 0
        
        for color in self.colors:
            if self.colors[color] > 255:
                self.colors[color] = 255
            elif self.colors[color] < 0:
                self.colors[color] = 0
        self.top = max(self.colors.values())
        favorites = []
        for color in self.colors:
            if self.colors[color] == self.top:
                favorites.append(color)
        if len(favorites) > 1:
            remove = choice(favorites)
            if self.colors[remove] < 5:
                self.colors[remove] += 1
            else:
                self.colors[remove] -= 1
            self.sanitize()
        else:
            self.color = favorites[0]
        
    def mutate(self):
        for color in self.colors:
            self.colors[color] += choice([-1,0,0,0,0,0,0,0,0,0,0,1])
        self.sanitize()
        

def ten_data_run():
    for i in range(0,10):
        s = sim()
        s.datarun()
        plt.figure()
        x_s = [i*100 for i in range(0,len(s.data))]
        y_r = [d[0] for d in s.data]
        y_g = [d[1] for d in s.data]
        y_b = [d[2] for d in s.data]
        plt.plot(x_s,y_b)
        plt.plot(x_s,y_g)
        plt.plot(x_s,y_r)
        plt.savefig("data"+str(i)+".png")
        
if __name__ == '__main__':
    s = sim()
    s.draw()
    s.run(5000)
        
