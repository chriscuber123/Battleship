"""
15-110 Hw6 - Battleship Project
Name: Christopher Chi
AndrewID: cbchi
"""

#import hw6_battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
#5 [Check6-1] & #3 [Check6-2] & #3 [Hw6] & #4 [Hw6]
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"] = 10
    data["cols"] = 10
    data["boardsize"] = 500
    data["cellsize"] = 50
    data["userships"] = 5
    data["compships"] = 5
    data["userboard"] = emptyGrid(data["rows"],data["cols"])
    data["compboard"] = emptyGrid(data["rows"],data["cols"])
    data["compboard"] = addShips(data["compboard"], data["compships"])
    data["tempship"] = []
    data["numships"] = 0
    data["winner"] = None
    data["maxturns"] = 50
    data["currentturns"] = 0
    return None


'''
makeView(data, userCanvas, compCanvas)
#6 [Check6-1] & #2 [Check6-2] & #3 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data["userboard"], True)
    drawGrid(data, compCanvas, data["compboard"], False)
    drawShip(data, userCanvas, data["tempship"])
    drawGameOver(data, userCanvas)
    return None


'''
keyPressed(data, events)
#5 [Hw6]
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym == "Return":
        makeModel(data)
        return None
    else:
        return None


'''
mousePressed(data, event, board)
#5 [Check6-2] & #1 [Hw6] & #3 [Hw6]
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    click = getClickedCell(data, event)
    if board == "user" and data["winner"] == None:
        clickUserBoard(data,click[0],click[1])
    if board == "comp":
        runGameTurn(data,click[0],click[1])
    return None

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
#1 [Check6-1]
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            grid[i].append(EMPTY_UNCLICKED)
    return grid


'''
createShip()
#2 [Check6-1]
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    import random
    shipRow = random.choice(range(1,9))
    shipCol = random.choice(range(1,9))
    shipOrient = random.choice(range(0,2))
    if shipOrient == 0:
        ship = [[shipRow-1, shipCol], [shipRow,shipCol], [shipRow+1,shipCol]]
    else:
        ship = [[shipRow,shipCol-1],[shipRow,shipCol],[shipRow,shipCol+1]]
    return ship


'''
checkShip(grid, ship)
#3 [Check6-1]
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    empty = True
    for cell in ship:
        if grid[cell[0]][cell[1]] != EMPTY_UNCLICKED:
            empty = False
    return empty


'''
addShips(grid, numShips)
#4 [Check6-1]
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count = 0
    while True:
        ship = createShip()
        if checkShip(grid,ship) == True:
            for cell in ship:
                grid[cell[0]][cell[1]] = SHIP_UNCLICKED
            count = count + 1
        if count == numShips:
            break


    return grid
'''
drawGrid(data, canvas, grid, showShips)
#6 [Check6-1] & #1 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for i in range(0, data["boardsize"], data["cellsize"]):
        for j in range(0, data["boardsize"], data["cellsize"]):
            if grid[int(j/data["cellsize"])][int(i/data["cellsize"])] == SHIP_UNCLICKED and showShips == True:
                canvas.create_rectangle(i, j, i+data["cellsize"], j+data["cellsize"], fill="yellow")
            elif grid[int(j/data["cellsize"])][int(i/data["cellsize"])] == SHIP_UNCLICKED and showShips == False:
                canvas.create_rectangle(i, j, i+data["cellsize"], j+data["cellsize"], fill="blue")
            elif grid[int(j/data["cellsize"])][int(i/data["cellsize"])] == EMPTY_UNCLICKED:
                canvas.create_rectangle(i, j, i+data["cellsize"], j+data["cellsize"], fill="blue")
            elif grid[int(j/data["cellsize"])][int(i/data["cellsize"])] == SHIP_CLICKED:
                canvas.create_rectangle(i, j, i+data["cellsize"], j+data["cellsize"], fill="red")
            elif grid[int(j/data["cellsize"])][int(i/data["cellsize"])] == EMPTY_CLICKED:
                canvas.create_rectangle(i, j, i+data["cellsize"], j+data["cellsize"], fill="white")
    return None


### WEEK 2 ###

'''
isVertical(ship)
#1 [Check6-2]
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    shipRow = [ship[0][0], ship[1][0], ship[2][0]]
    shipRow.sort()
    if (ship[0][1] == ship[1][1] == ship[2][1]) and (shipRow[0]+2 == shipRow[1]+1 == shipRow[2]):
        return True
    else:
        return False


'''
isHorizontal(ship)
#1 [Check6-2]
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    shipRow = [ship[0][1], ship[1][1], ship[2][1]]
    shipRow.sort()
    if (ship[0][0] == ship[1][0] == ship[2][0]) and (shipRow[0]+2 == shipRow[1]+1 == shipRow[2]):
        return True
    else:
        return False


'''
getClickedCell(data, event)
#2 [Check6-2]
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    row = int(event.y/data["cellsize"])
    col = int(event.x/data["cellsize"])
    return [row,col]


'''
drawShip(data, canvas, ship)
#3 [Check6-2]
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for cell in ship:
        canvas.create_rectangle(cell[1]*data["cellsize"], cell[0]*data["cellsize"], cell[1]*data["cellsize"]+data["cellsize"], cell[0]*data["cellsize"]+data["cellsize"], fill="white")
    return None


'''
shipIsValid(grid, ship)
#4 [Check6-2]
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if checkShip(grid,ship) == True and (isVertical(ship) == True or isHorizontal(ship) == True) and len(ship) == 3:
        return True
    else:
        return False


'''
placeShip(data)
#4 [Check6-2]
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["userboard"], data["tempship"]) == True and data["numships"] < 5:
        for cell in data["tempship"]:
            data["userboard"][cell[0]][cell[1]] = SHIP_UNCLICKED
            data["tempship"] = []
        data["numships"] += 1
    else:
        print("This ship isn't valid")
        data["tempship"] = []
    return None


'''
clickUserBoard(data, row, col)
#4 [Check6-2]
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["numships"] == 5:
        return None
    if [row,col] in data["tempship"]:
        return None
    else:
        data["tempship"].append([row,col])
        if len(data["tempship"]) == 3:
            placeShip(data)
    if data["numships"] == 5:
        print("You have added 5 ships, begin playing")


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
#1 [Hw6] & #3 [Hw6]
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == SHIP_UNCLICKED:
        board[row][col] = SHIP_CLICKED
    elif board[row][col] == EMPTY_UNCLICKED:
        board[row][col] = EMPTY_CLICKED
    if isGameOver(board) == True:
        data["winner"] = player
    return None


'''
runGameTurn(data, row, col)
#1 [Hw6] & #2 [Hw6] & #4 [Hw6]
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["compboard"][row][col] == SHIP_CLICKED or data["compboard"][row][col] == EMPTY_CLICKED:
        return None
    elif data["currentturns"] == data["maxturns"]:
        data["winner"] = "draw"
        return None
    else:
        updateBoard(data,data["compboard"],row,col,"user")
        compguess = getComputerGuess(data["userboard"])
        updateBoard(data,data["userboard"],compguess[0],compguess[1],"comp")
        data["currentturns"] += 1
        return None



'''
getComputerGuess(board)
#2 [Hw6]
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    while True:
        row = random.randint(0,9)
        col = random.randint(0,9)
        if board[row][col] == SHIP_UNCLICKED or board[row][col] == EMPTY_UNCLICKED:
            return [row,col]


'''
isGameOver(board)
#3 [Hw6]
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    gameOver = True
    for i in range(0,10):
        for j in range(0,10):
            if board[i][j] == SHIP_UNCLICKED:
                gameOver = False
    return gameOver


'''
drawGameOver(data, canvas)
#3 [Hw6] & #4 [Hw6] & #5 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"] == "user":
        canvas.create_text(250,170,text="You won!",font="Times 64",fill="spring green")
        canvas.create_text(250,250,text="Press enter to play again",font="Times 32",fill="turquoise")
    elif data["winner"] == "comp":
        canvas.create_text(250,170,text="You lost!",font="Times 64",fill="red2")
        canvas.create_text(250,250,text="Press enter to play again",font="Times 32",fill="turquoise")
    elif data["winner"] == "draw":
        canvas.create_text(250,180,text="You're out of moves, draw!",font="Times 32",fill="orange")
        canvas.create_text(250,250,text="Press enter to play again",font="Times 32",fill="turquoise")
    return None


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    #test.week1Tests()

    ## Uncomment these for Week 2 ##

    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    #test.week2Tests()


    ## Uncomment these for Week 3 ##

    print("\n" + "#"*15 + " WEEK 3 TESTS " +  "#" * 16 + "\n")
    #test.week3Tests()


    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
