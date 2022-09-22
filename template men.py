from PyQt5 import (QtWidgets,
                   QtCore,
                   QtGui,
                   uic,)
import sys
from sqlite3 import *
def connection():
    conn = connect('usersAndFilms.db')
    cur = conn.cursor()
    return conn, cur
def SearchForUser(username):
    conn, cur = connection()
    cur.execute('Select UserID, username, password FROM users WHERE username =?',(username,))
    returnData = cur.fetchall()
    conn.close()
    return returnData


class Login(QtWidgets.QMainWindow): 
    def __init__(self):
        super(Login, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('log in.ui',self) #Loads window design from the ui file
        self.show() #Window is shown when an instance of the class is made
        
        #Handles the event of buttons being clicked
        self.submitButton.clicked.connect(self.loginButtonMethod)
        self.clearButton.clicked.connect(self.clearButtonMethod)
    
        self.defaultUser = 'username'
        self.defaultUser = 'password'

    
    def loginButtonMethod(self):
        username = self.input1.text()
        password = self.input2.text()
        
        if username == "" or password == "":
            self.messageBox('Blank fields', 'Please enter both a username and password!','warning')
        else:
            userdata = SearchForUser(username)
            if len(userdata) > 0:
                if userdata[0][2] == password:
                    self.messageBox('Login Succesful ', 'You have logged in succesfully !', 'warning')
                    self.clearButtonMethod()
                    self.close()
                else:
                    self.messageBox('Log in Failed', 'Incorrect password entered','info')
                    self.clearButtonMethod()
            else:
                    self.messageBox('Log in Failed', 'Incorrect username entered','info')
                    self.clearButtonMethod()
                
                
                
    def clearButtonMethod(self):
        self.input1.setText('')
        self.input2.setText('')

    def messageBox(self, title, content, iconType="info"):
        #A message box object is created
        msgBox = QtWidgets.QMessageBox()
        #Sets the message box icon based on icon type passed as a parameter
        if iconType == "info":
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
        elif iconType == "question":
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
        elif iconType == "warning":
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        else:
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        #Sets text and title to arguments passed into the function
        msgBox.setText(content)
        msgBox.setWindowTitle(title)
        #Shows the message box to the user
        msgBox.exec()
     
def main():
    app = QtWidgets.QApplication(sys.argv)
    #Initialises various menus
    loginWindow = Login()
    #Starts menu execution
    app.exec()
    #Quits menu execution when all windows are closed
    QtWidgets.QApplication.quit()
        
main()

import pygame
import random

from os import path
img_dir = path.join(path.dirname(__file__),'img')

           
WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('space inavder')
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        self.image.fill(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        
        self.speedx = 0
 
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
            
        self.rect.x += self.speedx
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,8)
    def update(self):
        self.rect.y += self.speedy
        
        if self.rect.top > HEIGHT +10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):
        self.rect.y +=self.speedy
        if self.rect.bottom < 0:
            self.kill()
        


all_sprites = pygame.sprite.Group()

mobs = pygame.sprite.Group()

bullets = pygame.sprite.Group()

player = Player()

mob = Mob()

for i in range(20):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
all_sprites.add(player)



running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            
    all_sprites.update()
    
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)
    
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    
    hits = pygame.sprite.spritecollide(player,mobs,False)
    
    
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    
    if hits:
        running = False
        
    screen.fill(RED)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()  
