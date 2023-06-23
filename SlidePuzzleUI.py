# coding=ISO8859-2
# Trabalho final de MATA64 - Intelig?ncia Artifical
# Professora: Tatiane N. Rios
# Aluno: Daniel da Rocha Carneiro

# C�digo para resolu��o do problema dos blocos deslizantes atrav�s do algoritmo de busca A*, usando a heur�stica de dist�ncia de Manhattan


# Interface gr�fica adaptada da solu��o proposta por Al Sweigart:

# Slide Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame, sys, random
from pygame.locals import *
import copy
from solveBoard import solveBoardFun

# Create the constants (go ahead and experiment with different values)
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 60
BLANK = None
ANIMSPEED = 6 

BOARDWIDTH = 4  # number of columns in the board
BOARDHEIGHT = BOARDWIDTH # number of rows in the board

if BOARDWIDTH == 3:
    LOADEDBOARD = [[ 1, BLANK, 6],[ 2, 8, 5],[3, 7, 4]]	
    NUMBEROFSCRAMBLES = 80
else:
    LOADEDBOARD = [[ 5, 2, 9, 13],[ 8, 1, 14, 12],[ 6, 7, 10, 11],[ 3, 4, 15, BLANK]]	
    NUMBEROFSCRAMBLES = 60    
		

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
GREY  =         (90, 90, 90)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
ORANGE =        (255, 165,   0)

BGCOLOR = GREY
TILECOLOR = ORANGE
TEXTCOLOR = BLACK
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, STEPS_SURF, STEPS_RECT, COMPSTEPS_SURF, COMPSTEPS_RECT
    global stepCount, allMoves
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Jogo dos 15 - Trabalho de Intelig�ncia Artificial')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    stepCount = 0
    stepString = "Passos: " + str(stepCount)
    compStepCount = 0
    compStepString = "Passos computados: " + str(stepCount)
    STEPS_SURF, STEPS_RECT = makeText(stepString,    WHITE, BGCOLOR, 10 , WINDOWHEIGHT - 60)
    COMPSTEPS_SURF, COMPSTEPS_RECT = makeText(compStepString,    WHITE, BGCOLOR, 10 , WINDOWHEIGHT - 30)

    #LOAD_SURF, LOAD_RECT = makeText('Load Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 120)
    NEW_SURF,   NEW_RECT   = makeText('Novo jogo', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)
    RESET_SURF, RESET_RECT = makeText('Resetar',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = makeText('Solucionar',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)

    

    mainBoard, solutionSeq = getLoadedBoard()
    SOLVEDBOARD = getStartingBoard() # a solved board is the same as the board in a start state.
    allMoves = [] # list of moves made from the solved configuration


    while True: # main game loop
        slideTo = None # the direction, if any, a tile should slide
        msg = 'Clique em um bloco ou use as setas para mover.' # contains the message to show in the upper left corner.
        if mainBoard == SOLVEDBOARD:
            msg = 'Resolvido!'

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves) # clicked on Reset button
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(NUMBEROFSCRAMBLES) # clicked on New Game button
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        msg = 'Buscando solu��o...' # contains the message to show in the upper left corner.
                        drawBoard(mainBoard, msg)
                        solve(mainBoard, allMoves)
                        msg = 'Solu��o encontrada. Resolvendo...' # contains the message to show in the upper left corner.
                        drawBoard(mainBoard, msg)
                else:
                    # check if the clicked tile was next to the blank spot

                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Clique em um bloco ou use as setas para mover. (Movendo)', 12) # show slide on screen
            stepCount = stepCount + 1
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # record the slide
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def getStartingBoard():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    
    return board

def getLoadedBoard():
    # Carrega um tabuleiro conforme preenchido na constante LOADEDBOARD, instanciada no �nicio desse aquivo
    
    board = LOADEDBOARD
    sequence = []
    return (board, sequence)


def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]

def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


    #Contador de steps realizados
    stepString = "Passos: " + str(len(allMoves))
    STEPS_SURF, STEPS_RECT = makeText(stepString,    WHITE, BGCOLOR, 10 , WINDOWHEIGHT - 60)
    DISPLAYSURF.blit(STEPS_SURF, STEPS_RECT)

    computatedMoves = remove_repeated_elements(allMoves)

    #Contador de steps computados realizados (multiplos passos em uma mesma dire��o contam apenas como 1)
    compStepString = "Passos computados: " + str(len(computatedMoves))
    COMPSTEPS_SURF, COMPSTEPS_RECT = makeText(compStepString,    WHITE, BGCOLOR, 10 , WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(COMPSTEPS_SURF, COMPSTEPS_RECT)


def remove_repeated_elements(array):
    result = []
    i = 0
    while i < len(array):
        result.append(array[i])
        if i < len(array) - 1 and array[i] == array[i+1]:
            while i < len(array) - 1 and array[i] == array[i+1]:
                i += 1
        i += 1
    return result
    


def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500) # pause 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Gerando novo tabuleiro...', animationSpeed=int(TILESIZE / 2))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:] # gets a copy of the list
    revAllMoves.reverse()
    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT 
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 1))
        makeMove(board, oppositeMove)

def solveAnimation(board, solutionMoves):
    # Originalmente, o c�digo do UI realizava a invers�o de todos os movimentos feitos desde que o tabuleiro foi inicializado e embaralhado
    # Essa fun��o foi adaptada para realizar os passos calculados pelo algoritmo de busca
    revAllMoves = solutionMoves[:] # gets a copy of the list  
    for move in revAllMoves:
        slideAnimation(board, move, 'Resolvendo atrav�s de busca...', animationSpeed=int(ANIMSPEED))
        makeMove(board, move)  
        allMoves.append(move)


    # Converte o estilo de lista utilizado pela UI para o estilo de lista em uma dimens�o usado para o algoritmo A*
def uiBoardToArray(mainboard):
    board = copy.deepcopy(mainboard)
    for sublist in board:
        for i in range(len(sublist)):
            if sublist[i] is None:
                sublist[i] = 0
    flattened_list = []

    for sublist in zip(*board):
        flattened_list.extend((sublist)) 
    return flattened_list             

    # Fun��o respons�vel por preparar, solucionar via A* e animar a resolu��o do tabuleiro
def solve(board, allMoves):
    array = uiBoardToArray(board)
    solutionMoves = solveBoardFun(array, BOARDWIDTH) #chama a fun��o no arquivo solveBoard.py 
    #print(solutionMoves)
    solveAnimation(board, solutionMoves)
    return
    




if __name__ == '__main__':
    main()