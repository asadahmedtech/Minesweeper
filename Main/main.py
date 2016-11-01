"""
MADE BY ASAD AHMED
"""

from random import randint
import pygame
import pickle

class Tile_Create(object):

    def __init__(self,Row,Column,NOFM):
        self.row = Row
        self.column = Column
        self.no_of_mines = NOFM
        self.NewMapGenerator()

    def __NullColorRow(self):
        Temp_number = 0
        Empty_Row = [0 for i in range(self.column)]
        for rows in range(self.row):
            if self.NeighbourMap[rows] == Empty_Row:
                Temp_number+=1
        return Temp_number

    def __isMine(self,coordinates):
        x,y=coordinates
        try:
            return True if self.__TempArray[x][y] == '1' else False
        except IndexError:
            pass

    def __NeighbourMines(self,coordinates):
        x,y=coordinates
        No_of_mines = 0

        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                try:
                    if i<0 or j<0:
                        raise IndexError
                    desc = self.__isMine((i,j))
                    if desc:
                        No_of_mines+=1
                    if i==x and j==y and desc:
                        No_of_mines-=1
                        pass
                except IndexError:
                    pass
        return No_of_mines

    def __NeighbourMap(self):
        Temp_Map=[]
        Temp_MinesCoordinate = []
        for i in range(self.row):
            Temp = []
            for j in range(self.column):
                Temp.append('M' if self.__isMine((i,j)) else self.__NeighbourMines((i,j)))
                if self.__isMine((i,j)):
                    Temp_MinesCoordinate.append((i,j))
            Temp_Map.append(Temp)
        return Temp_Map,Temp_MinesCoordinate

    def __CreateArray(self):
        minesloaded = 0
        while minesloaded<self.no_of_mines:
            x,y=randint(0,self.row-1),randint(0,self.column-1)
            if not self.__isMine((x,y)):
                self.__TempArray[x][y]='1'
                minesloaded+=1
        return self.__TempArray

    def NewMapGenerator(self):
        self.__TempArray = [['0'for j in range(self.column)]for i in range(self.row)]
        self.Mine_Map = self.__CreateArray()
        self.NeighbourMap,self.MinesCoordinate = self.__NeighbourMap()
        if self.__NullColorRow()>3:
            self.Mine_Map = self.__CreateArray()
            self.NeighbourMap = self.__NeighbourMap()

class Tile_Actions(Tile_Create):
    def __init__(self,Row,Column,NOFM):
        super(Tile_Actions, self).__init__(Row,Column,NOFM)             #it will take the total mines and remove every mine that is flagged
        self.Armed = self.no_of_mines
        self.MineOpened = False
        self.FlaggedMap = [['0' for i in range(self.column)]for j in range(self.row)]
        self.OpenMap = [[''for i in range(self.column)]for j in range(self.row)]
        self.FlaggedTile = NOFM
        ##self.__PrintArray(self.NeighbourMap,self.row,self.column)
        self.Visited = 0
        self.VisitedMap = [['' for i in range(self.column)] for j in range(self.row)]
    def __PrintArray(self,Array,ROW,COL):
        for i in range(ROW):
            for j in range(COL):
                print Array[i][j],
            print

    def __toFlag(self,coordinates):
        x,y=coordinates
        try:
            self.FlaggedMap[x][y]='F'
            if self.__isMine(coordinates):
                self.MinesCoordinate.remove(coordinates)
        except IndexError:
            pass

    def __isMine(self,coordinates):
        x,y=coordinates
        try:
            return True if self.Mine_Map[x][y] == '1' else False
        except IndexError:
            pass

    def __toDisarm(self,coordinates):
        x,y=coordinates
        try:
            if self.__isMine(coordinates) and self.FlaggedMap[x][y]=='F':
                self.Armed-=1
                self.Mine_Map[x][y]='0'
        except IndexError:
            pass

    def OpenTile(self,coordinate):
        x,y=coordinate
        if self.FlaggedMap[x][y] == 'F':
            pass

        elif self.NeighbourMap[x][y] == 'M':
            self.OpenMap[x][y]='GO'

        elif self.OpenMap[x][y]=='':
            self.VisitedMap[x][y] = 'O'
            self.Visited+=1
            if self.NeighbourMap[x][y]==0:
                self.OpenMap[x][y]='O'
                self.__OpenSurroundingTile(coordinate)
            elif self.NeighbourMap[x][y]!='M':
                self.OpenMap[x][y]='O'

    def __OpenSurroundingTile(self,coordinates):
        x,y=coordinates
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                try:
                    if self.row>=i>=0 and self.column>=j>=0:
                        self.OpenTile((i,j))
                except IndexError:
                    pass

    def Flag(self,coordinates):                                                                     #It will flag the mine with coordinate given and remove the 'DISARM' from MineMAp is the flagged tile is a mine
        x,y=coordinates
        if self.FlaggedMap[x][y]=='F':
            self.FlaggedMap[x][y]='0'
            self.FlaggedTile+=1
            if self.NeighbourMap[x][y] == 'M':
                self.MinesCoordinate.append((x,y))
        else:
            self.FlaggedTile-=1
            self.__toFlag(coordinates)


class GameBoard:

    def __init__(self):
        pygame.init()
        self.home = True
        self.font = pygame.font.SysFont(None, 32)
        self.__getHighScore()
        self.Top_bar = 50
        self.blockSize = 30

        self.images={
        'covered':pygame.image.load('covered_tile.png'),
        'uncovered_0':pygame.transform.scale(pygame.image.load('uncovered_tile_0.png'),(self.blockSize,self.blockSize)),
        'uncovered_1':pygame.transform.scale(pygame.image.load('uncovered_tile_1.png'),(self.blockSize,self.blockSize)),
        'uncovered_2':pygame.transform.scale(pygame.image.load('uncovered_tile_2.png'),(self.blockSize,self.blockSize)),
        'uncovered_3':pygame.transform.scale(pygame.image.load('uncovered_tile_3.png'),(self.blockSize,self.blockSize)),
        'uncovered_4':pygame.transform.scale(pygame.image.load('uncovered_tile_4.png'),(self.blockSize,self.blockSize)),
        'uncovered_5':pygame.transform.scale(pygame.image.load('uncovered_tile_5.png'),(self.blockSize,self.blockSize)),
        'uncovered_6':pygame.transform.scale(pygame.image.load('uncovered_tile_6.png'),(self.blockSize,self.blockSize)),
        'uncovered_7':pygame.transform.scale(pygame.image.load('uncovered_tile_7.png'),(self.blockSize,self.blockSize)),
        'uncovered_8':pygame.transform.scale(pygame.image.load('uncovered_tile_8.png'),(self.blockSize,self.blockSize)),
        'covered_mine': pygame.transform.scale(pygame.image.load('covered_mine.png'),(self.blockSize, self.blockSize)),
        'flagged':pygame.transform.scale(pygame.image.load('flagged_tile.png'),(self.blockSize,self.blockSize)),
        'correct_mine':pygame.transform.scale(pygame.image.load('correct_tile.png'),(self.blockSize,self.blockSize)),
        'mined':pygame.transform.scale(pygame.image.load('mined_tile.png'),(self.blockSize,self.blockSize)),
        'openedmine':pygame.transform.scale(pygame.image.load('selected_mined_tile.png'),(self.blockSize,self.blockSize)),
        'home':pygame.transform.scale(pygame.image.load('home.png'),(self.blockSize,self.blockSize)),
        'restart':pygame.transform.scale(pygame.image.load('restart.png'),(self.blockSize,self.blockSize)),
        'game_over':pygame.transform.scale(pygame.image.load('game_over.jpg'),(self.blockSize,self.blockSize)),
        'game_won':pygame.transform.scale(pygame.image.load('game_won.jpg'),(self.blockSize,self.blockSize)),
        'mine-home':pygame.transform.scale(pygame.image.load('Mine_Homepage.png'),(200,200)),
        'icon':pygame.image.load('mine_icon.jpg')}
        self.homePage()

        self.CurrentScore = []

        self.clock = pygame.time.Clock()
        self.white = (247, 247, 247)

        self.gameDimens = self.__getDimens()
        self.gameDisplay=pygame.display.set_mode(self.gameDimens)
        pygame.display.set_caption('MINESWEEPER')
        pygame.display.set_icon(self.images['icon'])
        self.MineObject = Tile_Actions(self.row,self.column,self.no_of_mines)
        self.IdealOpen = self.__idealMap()

        self.gameOver = False
        self.gameQuit = False

        self.gamewon = False
        self.mineopened = False

        self.startTime = 0
        self.TimeDisplay = False
        self.gameStarted = False

        self.stringInput = ''
        self.cheatCode = '1729'
        self.cheatActivated = False
        self.cheatUsed = False

    def __getDimens(self):

        x = (self.blockSize*self.column)
        y = self.Top_bar+(self.blockSize*self.row)
        return (x,y)

    def __idealMap(self):

        Temp_ideal = []
        for i in range(self.row):
            Temp=[]
            for j in range(self.column):
                if self.MineObject.NeighbourMap[i][j]!='M':
                    Temp.append('O')
                else:
                    Temp.append('')
            Temp_ideal.append(Temp)
        return Temp_ideal

    def __getHighScore(self):

        File = open('HighScore.dat','rb')
        self.HighScore = pickle.load(File)
        File.close()

    def __storeHighScore(self):

        File = open('HighScore.dat','wb')
        pickle.dump(self.HighScore,File)
        File.close()

    def __getPos(self,coordinate):

        try:
            y,x=coordinate
            if x <= self.Top_bar:
                raise IndexError
            return ((x-self.Top_bar)/self.blockSize,(y)/self.blockSize)
        except IndexError:
            return None

    def __clickEvent(self,coordinate,status):

        if self.__getPos(coordinate) != None :
            x,y=self.__getPos(coordinate)
            if status == 0: #for left click
                if (x,y) in self.MineObject.MinesCoordinate:
                    self.__openAllMine((x,y))
                else:
                    self.MineObject.OpenTile((x,y))

            elif status == 2:#for right click
                if self.MineObject.OpenMap[x][y]!='O':
                    self.MineObject.Flag((x,y))

            elif status == 1:#for double click
                Neighboursatisfy, WrongFlag, Iter = True, False, 0
                while Iter < 2:
                    for i in range(x - 1, x + 2):
                        for j in range(y - 1, y + 2):
                            try:
                                if i >= 0 and j >= 0:
                                    if self.MineObject.NeighbourMap[i][j] == 'M' and self.MineObject.FlaggedMap[i][
                                        j] != 'F':
                                        Neighboursatisfy = False
                                    if (i, j) not in self.MineObject.MinesCoordinate and self.MineObject.FlaggedMap[i][
                                        j] == 'F':
                                        WrongFlag = True
                                    if WrongFlag:
                                        if (i, j) in self.MineObject.MinesCoordinate:
                                            Neighboursatisfy = False
                                            self.gameOver = True
                                            self.mineopened = True
                                            self.__openAllMine((i, j))
                            except IndexError:
                                pass
                    Iter += 1
                if Neighboursatisfy:
                    for i1 in range(x-1,x+2):
                        for j1 in range(y-1,y+2):
                            try:
                                if i1 >= 0 and j1 >= 0:
                                    if self.MineObject.NeighbourMap[i1][j1] != 'M':
                                        self.MineObject.OpenTile((i1, j1))
                            except IndexError:
                                pass

    def __openAllMine(self,coordinate):

        x,y=coordinate
        for i in range(self.row):
            for j in range(self.column):
                if i == x and j == y:
                    self.MineObject.OpenMap[i][j] = 'GO'
                elif self.MineObject.NeighbourMap[i][j] == 'M':
                    if self.MineObject.FlaggedMap[i][j] == 'F':
                        self.MineObject.OpenMap[i][j] = 'FM'
                    else:
                        self.MineObject.OpenMap[i][j]='M'

    def __GUIDisplay(self):

        for i in range(self.row):
            for j in range(self.column):
                if self.MineObject.OpenMap[i][j] == 'O':
                    Temp_Image = self.images['uncovered_'+str(self.MineObject.NeighbourMap[i][j])]
                elif self.MineObject.OpenMap[i][j] == 'M':
                    Temp_Image = self.images['mined']
                elif self.MineObject.OpenMap[i][j] == 'GO':
                    Temp_Image = self.images['openedmine']
                elif self.MineObject.FlaggedMap[i][j] == 'F' and self.MineObject.OpenMap[i][j] != 'FM':
                    Temp_Image = self.images['flagged']
                elif self.MineObject.OpenMap[i][j] == 'FM':
                    Temp_Image = self.images['correct_mine']
                elif self.MineObject.OpenMap[i][j] == '':
                    if self.cheatActivated and self.MineObject.NeighbourMap[i][j] == 'M':
                        Temp_Image = self.images['covered_mine']
                    else:
                        Temp_Image = self.images['covered']

                self.gameDisplay.blit(Temp_Image,(self.blockSize*j,self.Top_bar+self.blockSize*i))

    def __button(self,text, buttonx, buttony, width, height,buttoncolor,textcolor,ActiveColor = None,action=None,stat=None):

        if ActiveColor != None:
            cur = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if buttonx + width > cur[0] > buttonx and buttony + height > cur[1] > buttony:
                pygame.draw.rect(self.homeDisplay, ActiveColor, (buttonx, buttony, width, height))
                if click[0] == 1 and action != None:
                    if action == "easy":
                        self.row = 9
                        self.column = 9
                        self.no_of_mines = 10
                        self.difficulty = 'easy'
                        self.home = False
                    if action == "medium":
                        self.row = 16
                        self.column = 16
                        self.no_of_mines = 40
                        self.difficulty = 'medium'
                        self.home = False
                    if action == "hard":
                        self.row = 16
                        self.column = 30
                        self.no_of_mines = 99
                        self.difficulty = 'hard'
                        self.home = False
                    if action == 'highscore':
                        self.highscore = True
                        self.highscorePage()
            else:
                pygame.draw.rect(self.homeDisplay, buttoncolor, (buttonx, buttony, width, height))
        else:
            pygame.draw.rect(self.gameDisplay if stat==None else self.highscoreDisplay, buttoncolor, (buttonx, buttony, width, height))
        textSurf = self.font.render(str(text),1,textcolor)
        textRect = textSurf.get_rect()
        textRect.center = ((buttonx + (width / 2)), buttony + (height / 2))
        if ActiveColor!=None:
            self.homeDisplay.blit(textSurf, textRect)
        else:
            if stat == 'high':
                self.highscoreDisplay.blit(textSurf, textRect)
            else:
                self.gameDisplay.blit(textSurf, textRect)

    def homePage(self):

        self.HomeDimens = (600,400)
        self.homeDisplay = pygame.display.set_mode(self.HomeDimens)
        while self.home:
            self.homeDisplay.fill((35,35,35))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            ###
            textSurface = pygame.font.SysFont("comicsansms", 50).render('MINESWEEPER', True, (225, 255, 0))
            textRect = textSurface.get_rect()
            textRect.center = 380,50
            self.homeDisplay.blit(textSurface, textRect)
            ###
            ###
            textSurface1 = pygame.font.SysFont("comicsansms", 20).render('- MADE BY ASAD AHMED', True, (242, 255, 0))
            textRect1 = textSurface1.get_rect()
            textRect1.center = 380,100
            self.homeDisplay.blit(textSurface1, textRect1)
            ###
            self.homeDisplay.blit(self.images['mine-home'],(10 ,40))
            self.__button('EASY',50,300,100,50,(34, 177, 76),(247,247,247),(0, 255, 0),'easy')
            self.__button('MEDIUM',250,300,100,50,(200, 200, 0),(247,247,247),(255, 255, 0),'medium')
            self.__button('HARD',450,300,100,50,(200, 0, 0),(247,247,247),(255, 0, 0),'hard')
            self.__button('HIGH SCORE',400,200,180,50,(28, 18, 142),(247,247,247),(98, 84, 255),'highscore')
            pygame.display.update()

    def highscorePage(self):

        self.highscoreDimens = (600,400)
        self.highscoreDisplay = pygame.display.set_mode(self.highscoreDimens)
        self.__getHighScore()
        while self.highscore:
            self.homeDisplay.fill((35,35,35))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            textSurface1 = pygame.font.SysFont("comicsansms", 50).render('HIGH', True, (0, 255, 51))
            textRect1 = textSurface1.get_rect()
            textRect1.center =100,150
            self.highscoreDisplay.blit(textSurface1, textRect1)
            textSurface2 = pygame.font.SysFont("comicsansms", 50).render('SCORE', True, (0, 255, 51))
            textRect2 = textSurface2.get_rect()
            textRect2.center = 100,250
            self.highscoreDisplay.blit(textSurface2, textRect2)
            self.__button('EASY : '+str((self.HighScore['easy'])[0])+':'+str((self.HighScore['easy'])[1]),200,80,400,100,(35,35,35),(0, 255, 4),stat='high')
            self.__button('MEDIUM : '+str((self.HighScore['medium'])[0])+':'+str((self.HighScore['medium'])[1]),200,180,400,100,(35,35,35),(0, 255, 4),stat='high')
            self.__button('HARD : '+str((self.HighScore['hard'])[0])+':'+str((self.HighScore['hard'])[1]),200,280,400,100,(35,35,35),(0, 255, 4),stat='high')
            cur = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            homeX ,homeY = 0,10
            if homeX + self.blockSize > cur[0] > homeX and homeY + self.blockSize > cur[1] > homeY and click[0]==1:
                self.home = True
                self.highscore = False
                self.startTime = 0
                self.TimeDisplay = False
                self.gameStarted = False
                self.__init__()
            self.highscoreDisplay.blit(self.images['home'],(homeX ,homeY))
            pygame.display.update()

    def Mainloop(self):

        while not self.gameQuit:

            while not self.gameOver:
                self.gameDisplay.fill(self.white)
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                            self.gameOver = True
                            self.gameQuit = True
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        if not self.gameStarted:
                            self.startTime = pygame.time.get_ticks()
                            self.gameStarted,self.TimeDisplay = True,True
                        if pygame.mouse.get_pressed()[0]:
                            self.__clickEvent(pygame.mouse.get_pos(),0)
                        if pygame.mouse.get_pressed()[2]:
                            self.__clickEvent(pygame.mouse.get_pos(),2)
                        if pygame.mouse.get_pressed()[1]:
                            self.__clickEvent(pygame.mouse.get_pos(),1)
                    if event.type == pygame.KEYDOWN:
                        if 49 <= event.key <= 57:
                            self.stringInput += str(chr(event.key))

                self.__GUIDisplay()

                ##  CHECKING FOR GAME OVER
                for Rows in self.MineObject.OpenMap:
                    if 'GO' in Rows:
                        self.gameOver = True
                        self.mineopened = True

                ## CHECKING FOR GAME WON
                if self.MineObject.MinesCoordinate == [] and self.MineObject.Visited == ((self.row*self.column)-self.no_of_mines):
                    self.gameOver = True
                    self.gamewon = True

                    ##  FOR HIGH SCORE
                    if not self.cheatUsed:
                        if self.CurrentScore[0] < (self.HighScore[self.difficulty])[0]:
                            self.HighScore[self.difficulty]=self.CurrentScore
                            self.__storeHighScore()
                        elif self.CurrentScore[0] == (self.HighScore[self.difficulty])[0]:
                            if self.CurrentScore[1] < (self.HighScore[self.difficulty])[1]:
                                self.HighScore[self.difficulty] = self.CurrentScore
                                self.__storeHighScore()

                ##  FOR TIMER
                if not self.TimeDisplay:
                    self.__button('00:00' ,self.blockSize ,10,80,30,(242, 242, 242),(247, 39, 39))
                if self.TimeDisplay:
                    countTime = pygame.time.get_ticks() - self.startTime
                    countMins = str(countTime/60000).zfill(2)
                    countSecs = str((countTime%60000)/1000).zfill(2)
                    self.CurrentScore = [int(countMins),int(countSecs)]
                    self.__button(countMins+':'+countSecs ,self.blockSize,10,80,30,(242, 242, 242),(247, 39, 39))
                self.__button('0'+str(self.MineObject.FlaggedTile) if 10 > self.MineObject.FlaggedTile >= 0 else str(self.MineObject.FlaggedTile),self.gameDimens[0]-80,10,80,30,(242, 242, 242),(247, 39, 39))

                ##  FOR RESTART BUTTON
                cur = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                buttonX ,buttonY = (int(int(self.gameDimens[0])/2 - int(self.blockSize)/2)),(int(self.Top_bar)/2 - int(self.blockSize)/2)
                if buttonX + self.blockSize > cur[0] > buttonX and buttonY + self.blockSize > cur[1] > buttonY and click[0]==1:
                    self.MineObject = Tile_Actions(self.row,self.column,self.no_of_mines)
                    self.startTime = 0
                    self.TimeDisplay = False
                    self.gameStarted = False
                    self.cheatActivated = False
                    self.cheatUsed = False
                self.gameDisplay.blit(self.images['restart'],(buttonX ,buttonY))

                ##  FOR HOME BUTTON
                homeX ,homeY = 0,10
                if homeX + self.blockSize > cur[0] > homeX and homeY + self.blockSize > cur[1] > homeY and click[0]==1:
                    self.home = True
                    self.startTime = 0
                    self.TimeDisplay = False
                    self.gameStarted = False
                    self.cheatActivated = False
                    self.cheatUsed = False
                    self.__init__()
                self.gameDisplay.blit(self.images['home'],(homeX ,homeY))

                ##  FOR CHEAT-CODE TO DISPLAY MINES AND NOT END THE GAME
                if self.cheatCode in self.stringInput:
                    self.cheatActivated = not self.cheatActivated
                    self.cheatUsed = True
                    self.stringInput = ''

                pygame.display.update()

            for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        self.gameQuit = True

            ##  FOR RESTART BUTTON AFTER LOSING GAME
            cur = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            buttonX ,buttonY = (int(int(self.gameDimens[0])/2 - int(self.blockSize)/2)),(int(self.Top_bar)/2 - int(self.blockSize)/2)
            if buttonX + self.blockSize > cur[0] > buttonX and buttonY + self.blockSize > cur[1] > buttonY and click[0]==1:
                self.MineObject = Tile_Actions(self.row,self.column,self.no_of_mines)
                self.startTime = 0
                self.TimeDisplay = False
                self.gameStarted = False
                self.gameOver = False
                self.mineopened = False
                self.gamewon = False
                self.cheatActivated = False
                self.cheatUsed = False
            if self.mineopened :
                Temp_image = self.images['game_over']
            elif self.gamewon :
                Temp_image = self.images['game_won']
            else:
                Temp_image = self.images['restart']
            self.gameDisplay.blit(Temp_image,(buttonX ,buttonY))

            ##  FOR HOME BUTTON AFTER LOSING GAME
            homeX ,homeY = 0,10
            if homeX + self.blockSize > cur[0] > homeX and homeY + self.blockSize > cur[1] > homeY and click[0]==1:
                self.home = True
                self.startTime = 0
                self.TimeDisplay = False
                self.gameStarted = False
                self.cheatActivated = False
                self.cheatUsed = False
                self.__init__()
            self.gameDisplay.blit(self.images['home'],(homeX ,homeY))

            pygame.display.update()

        pygame.display.update()
        pygame.quit()
        quit()

if __name__ == '__main__':
    gameObject = GameBoard()
    gameObject.Mainloop()
