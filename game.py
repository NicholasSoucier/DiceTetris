from ursina import *
from ursina.prefabs.trail_renderer import TrailRenderer
from ursina.prefabs.sky import Sky
import random

POINTZERO = (-1.75, 3.75, 0)
SCORE = 0
level = 0

class DiceGrid:
    def __init__(self):
        self.dicegrid = [[0 for x in range(16)] for y in range(8)]
        self.gridModels = [[]]
        for x in range(8):
            self.gridModels.append([])
            for y in range(16):
                self.gridModels[x].append(Dice((-1.75 + (x*0.5)), (3.75 + -(y*0.5)), 1))
                setattr(self.gridModels[x][y], "visible", False)

    def getDie(self, xPos, yPos):
        return self.dicegrid[xPos][yPos]

    def getDieEntity(self, xPos, yPos):
        return self.gridModels[xPos][yPos]

    def setDie(self, xPos, yPos, value):
        #print("Setting value of", xPos, yPos, "to", value)
        if value > 0:
            self.dicegrid[xPos][yPos] = value
            #self.gridModels[xPos][yPos].enable()
            setattr(self.gridModels[xPos][yPos], "visible", True)
            self.gridModels[xPos][yPos].setValue(value)
        elif value == 0:
            self.dicegrid[xPos][yPos] = value
            #self.gridModels[xPos][yPos].disable()
            setattr(self.gridModels[xPos][yPos], "visible", False)



class GridEntity(Entity):
    def __init__(self):
        super().__init__(
            model=Grid(8, 16),
            thickness=2,
            scale=(4, 8, 0),
            color=color.green
        )

class AddIndicator(Text):
    def __init__(self, value, xPos, yPos):
        global goalNum
        self.addText = str(value)
        super().__init__(
            text=self.addText,
            color=color.orange,
            position=(POINTZERO + ((xPos*0.5), (yPos*0.5), 0)),
            size=2
        )
        print("Adding Addition Thing: " + str(value))
        if value == goalNum: self.color=color.green
        self.fade_out(duration=0.5)
        self.animate_position((self.x, self.y+1, self.z), duration=0.5)


class GameBG(Entity):
    def __init__(self):
        self.background1 = Entity(model='quad', scale=(5, 5, 1))
        self.background2 = Entity(model='quad', scale=(5, 5, 1))

    def update(self):
        self.background1.position += (0, 0.02, 0)

class DiceQueue(Entity):
    def __init__(self):
        self.queue = []
        for x in range(4):
            self.queue.append(random.randint(1,6))
        self.nextDice = Dice(3, 3, self.queue[0])
        self.dice1 = Dice(3, 2, self.queue[1])
        self.dice1.scale = (0.15, 0.15, 0.15)
        self.dice2 = Dice(3, 1, self.queue[2])
        self.dice2.scale = (0.125, 0.125, 0.125)
        self.dice3 = Dice(3, 0, self.queue[3])
        self.dice3.scale = (0.1, 0.1, 0.1)

    def getNextValue(self):
        return self.queue[0]

    def step(self):
        self.queue.pop(0)
        self.queue.append(random.randint(1,6))
        self.nextDice.setValue(self.queue[0])
        self.dice1.setValue(self.queue[1])
        self.dice2.setValue(self.queue[2])
        self.dice3.setValue(self.queue[3])

class Dice(Entity):
    def __init__(self, xPos, yPos, val):
        super().__init__(
            model='diceblock',
            texture='dice',
            scale=(0.2, 0.2, 0.2),
            rotation=(0, 0, 0),
            position=(xPos, yPos, 0)
        )
        self.value = val
        self.setValue(val)

    def getValue(self): return self.value
    def setValue(self, val):
        self.value = val
        if val == 0:
            setattr(self, "visible", False)
        if val > 0:
            setattr(self, "visible", True)
        if val == 1:
            self.rotation = (0, -90, 0)
        if val == 2:
            self.rotation = (180, 0, 0)
        if val == 3:
            self.rotation = (90, 0, 0)
        if val == 4:
            self.rotation = (0, 0, 0)
        if val == 5:
            self.rotation = (-90, 0, 0)
        if val == 6:
            self.rotation = (0, 90, 0)
    def breakEntity(self):
        destroy(self)

class GameDice(Entity):
    def __init__(self, xPos, yPos, val):
        global POINTZERO
        super().__init__(
            model='diceblock',
            texture='dice',
            scale=(0.2, 0.2, 0.2),
            rotation=(0, 0, 0),
            position=(POINTZERO + ((xPos*0.5), (yPos*0.5), 0))
        )
        self.value = val
        self.setValue(val)
        self.x_p = xPos
        self.y_p = yPos

    def getValue(self): return self.value
    def setValue(self, val):
        self.value = val
        if val == 1:
            self.rotation = (0, -90, 0)
        if val == 2:
            self.rotation = (180, 0, 0)
        if val == 3:
            self.rotation = (90, 0, 0)
        if val == 4:
            self.rotation = (0, 0, 0)
        if val == 5:
            self.rotation = (-90, 0, 0)
        if val == 6:
            self.rotation = (0, 90, 0)

    def getX(self): return self.x_p
    def getY(self): return self.y_p
    def setX(self, xVal):
        self.x_p = xVal
        self.position = (POINTZERO + ((self.getX()*0.5), -(self.getY()*0.5), 0))
    def setY(self, yVal):
        self.y_p = yVal
        self.position = (POINTZERO + ((self.getX()*0.5), -(self.getY()*0.5), 0))
    def moveLeft(self):
        self.x_p -= 1
        newPos = (self.x_p, self.y_p, 0)
        self.animate_position(newPos, duration=0.15)
        self.x -= 0.5
    def moveRight(self):
        self.x_p += 1
        newPos = (self.x_p, self.y_p, 0)
        self.animate_position(newPos, duration=0.15)
        self.x += 0.5
    def moveDown(self):
        self.y_p += 1
        newPos = (self.x_p, self.y_p, 0)
        self.animate_position(newPos, duration=0.15)


#############################
##                         ##
## APP INITIALIZATION AREA ##
##                         ##
#############################

app = Ursina()
window.borderless=False
sky = Sky()
setattr(sky, "texture", "HDbg.jpg")
sky.scale += (100, 100, 100)

dicegrid = DiceGrid()
gridEntity = GridEntity()
dqueue = DiceQueue()
camera.position = (0, 0, -27)
inPlay = GameDice(4, 0, random.randint(1, 6))
goalNum = random.randint(3, 18)
progressTimer = 50

goalText = dedent('''<scale:2><green>Goal: ''') +  str(goalNum)
scoreText = dedent('''<scale:2><green>Score: ''') + str(SCORE)
goalDisplay = Text(text=goalText)
scoreDisplay = Text(text=scoreText)
goalDisplay.x=-0.6
goalDisplay.y=0.4
scoreDisplay.x=-0.6
scoreDisplay.y=0.3

def input(key):
    global progressTimer
    if key == 'left arrow' and inPlay.getX() > 0:
        inPlay.setX(inPlay.getX()-1)
    if key == 'right arrow' and inPlay.getX() < 7:
        inPlay.setX(inPlay.getX()+1)
    if key == 'up arrow':
        holdDie()

holdmodel = Dice(-3, 0, 0)
setattr(holdmodel, "color", color.rgb(156, 243, 255))
def holdDie():
    global inPlay
    if holdmodel.getValue() == 0:
        holdmodel.setValue(inPlay.getValue())
        inPlay.setValue(dqueue.getNextValue())
        dqueue.step()
    else:
        temp = inPlay.getValue()
        inPlay.setValue(holdmodel.getValue())
        holdmodel.setValue(temp)

def update():
    #Run the progress timer, and when it hits 0, check to see if
    #the space under the block is empty, if so, push the die down.
    #if it is not empty, run the directional addition checks.
    #if one direction of the addition checks adds up to the goal number,
    #then destroy the three die in that direction and reroll the goal.
    #If none of the directions contains a goal, then set the die in the grid.
    #After all of this, make a new inPlay die.
    global inPlay, goalNum, progressTimer, level
    setattr(inPlay, "color", color.rgb(173, 255, 176))
    sky.rotation += (0, 0.005, 0)
    #Timer Block
    if progressTimer > 0:
        progressTimer -= 30 * time.dt
        #print(progressTimer)
        if held_keys['down arrow']: progressTimer -= 80 * time.dt
    else:
        progressTimer = 50 - level
        #Check what's under the die
        if inPlay.getY() < 15:
            spaceUnder = dicegrid.getDie(inPlay.getX(), inPlay.getY()+1)
        else: spaceUnder = 1
        if spaceUnder == 0 and inPlay.getY() < 15:
            inPlay.setY(inPlay.getY()+1)
            #print("Clear Down, Die Pos:", inPlay.getX(), inPlay.getY())
        #Check to see if the block is on the bottom
        elif inPlay.getY() == 15:
            #print("Placing on bottom of screen")
            dicegrid.setDie(inPlay.getX(), inPlay.getY(), inPlay.getValue())
            performChecks(inPlay.getX(), inPlay.getY())
            destroy(inPlay)
            inPlay = GameDice(4, 0, dqueue.getNextValue())
            dqueue.step()
        else:
            #Place die block on grid, perform checks
            #print("Placing on other die")
            dicegrid.setDie(inPlay.getX(), inPlay.getY(), inPlay.getValue())
            performChecks(inPlay.getX(), inPlay.getY())
            destroy(inPlay)
            inPlay = GameDice(4, 0, dqueue.getNextValue())
            dqueue.step()

def performChecks(xPos, yPos):
    global goalNum
    sum = 0
    dicegrid.getDieEntity(xPos, yPos).color = color.rgb(255, 253, 138)
    dicegrid.getDieEntity(xPos, yPos).animate_color(color.white, duration=0.5)
    #Down Check
    if yPos+2 < 16:
        sum += dicegrid.getDie(xPos, yPos)
        sum += dicegrid.getDie(xPos, yPos+1)
        sum += dicegrid.getDie(xPos, yPos+2)
        dicegrid.getDieEntity(xPos, yPos+1).color = color.rgb(255, 253, 138)
        dicegrid.getDieEntity(xPos, yPos+2).color = color.rgb(255, 253, 138)
        dicegrid.getDieEntity(xPos, yPos+1).animate_color(color.white, duration=0.5)
        dicegrid.getDieEntity(xPos, yPos+2).animate_color(color.white, duration=0.5)
        adin = AddIndicator(sum, xPos, yPos+1)
        #print("Down: ", sum, " | Goal: ", goalNum)
        if sum == goalNum:
            clearDown(xPos, yPos)
            return
    #Left Check
    sum = 0
    if xPos-2 > -1:
        sum += dicegrid.getDie(xPos, yPos)
        sum += dicegrid.getDie(xPos-1, yPos)
        sum += dicegrid.getDie(xPos-2, yPos)
        dicegrid.getDieEntity(xPos-1, yPos).color = color.rgb(255, 253, 138)
        dicegrid.getDieEntity(xPos-2, yPos).color = color.rgb(255, 253, 138)
        dicegrid.getDieEntity(xPos-1, yPos).animate_color(color.white, duration=0.5)
        dicegrid.getDieEntity(xPos-2, yPos).animate_color(color.white, duration=0.5)
        adin = AddIndicator(sum, xPos-1, yPos)
        #print("Left: ", sum, " | Goal: ", goalNum)
        if sum == goalNum:
            clearLeft(xPos, yPos)
            return
    #Right Check
    sum = 0
    if xPos+2 < 8:
        sum += dicegrid.getDie(xPos, yPos)
        sum += dicegrid.getDie(xPos+1, yPos)
        sum += dicegrid.getDie(xPos+2, yPos)
        dicegrid.getDieEntity(xPos+1, yPos).color = color.rgb(255, 253, 138)
        dicegrid.getDieEntity(xPos+2, yPos).color = color.rgb(255, 253, 138)
        dicegrid.getDieEntity(xPos+1, yPos).animate_color(color.white, duration=0.5)
        dicegrid.getDieEntity(xPos+2, yPos).animate_color(color.white, duration=0.5)
        adin = AddIndicator(sum, xPos+1, yPos)
        #print("Right: ", sum, " | Goal: ", goalNum)
        if sum == goalNum:
            clearRight(xPos, yPos)
            return

def clearDown(xPos, yPos):
    global goalNum, SCORE, level
    dicegrid.setDie(xPos, yPos, 0)
    dicegrid.setDie(xPos, yPos+1, 0)
    dicegrid.setDie(xPos, yPos+2, 0)
    SCORE += goalNum*100
    level += 1
    scoreText = dedent('''<scale:2><green>Score: ''') + str(SCORE)
    scoreDisplay.text = scoreText
    goalNum = random.randint(3, 18)
    goalText = dedent('''<scale:2><green>Goal: ''') +  str(goalNum)
    goalDisplay.text = goalText
def clearLeft(xPos, yPos):
    global goalNum, SCORE, level
    dicegrid.setDie(xPos, yPos, 0)
    dicegrid.setDie(xPos-1, yPos, 0)
    dicegrid.setDie(xPos-2, yPos, 0)
    SCORE += goalNum*100
    level += 1
    scoreText = dedent('''<scale:2><green>Score: ''') + str(SCORE)
    scoreDisplay.text = scoreText
    goalNum = random.randint(3, 18)
    goalText = dedent('''<scale:2><green>Goal: ''') +  str(goalNum)
    goalDisplay.text = goalText
def clearRight(xPos, yPos):
    global goalNum, SCORE, level
    dicegrid.setDie(xPos, yPos, 0)
    dicegrid.setDie(xPos+1, yPos, 0)
    dicegrid.setDie(xPos+2, yPos, 0)
    SCORE += goalNum*100
    level += 1
    scoreText = dedent('''<scale:2><green>Score: ''') + str(SCORE)
    scoreDisplay.text = scoreText
    goalNum = random.randint(3, 18)
    goalText = dedent('''<scale:2><green>Goal: ''') +  str(goalNum)
    goalDisplay.text = goalText

app.run()
