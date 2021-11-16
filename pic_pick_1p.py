'''
Inspired by a game in the Chinese Variety Show called 'Detective School (名侦探学院)'.

RULES:
- Target shape is shown on the right of the screen
- Target shape is hidden under the white grid, and may be in different orientations
- Click on the cells to reveal what is underneath 
- GOAL is to find the HEAD of the shape in as fewer steps as possible

- Gray means you missed, and the target could be elsewhere
- Blue means you have clicked on the target BODY, but not the Head
- Red means you have Successfully found the target HEAD
- Try to deduce the correct position of the HEAD from the shape of the target and revealed cells
'''

import pygame 
import random 
import sys
pygame.init() 

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (30,144,255)
RED = (255, 0, 0)
# LIGHTBLUE = (30,144,255)

# WIDTH and HEIGHT of each grid location
WIDTH = 50
HEIGHT = 50

# margin between each cell
MARGIN = 5

# Define Window size
ROWS = 8
COLUMNS = 7
SIDEWIDTH = 280
WIN_SIZE = [(WIDTH + MARGIN) * COLUMNS + MARGIN + SIDEWIDTH, 
            (HEIGHT + MARGIN) * ROWS + MARGIN]

# Define font to use
# STAT_FONT = pygame.font.SysFont("comicsans", 50)
# SMALL_FONT = pygame.font.SysFont("comicsans", 30)
STAT_FONT = pygame.font.SysFont("SimHei", 35)
SMALL_FONT = pygame.font.SysFont("SimHei", 25)


def genGrid():
    # Create a 2 dimensional array. 
    grid = []
    for row in range(ROWS):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(COLUMNS):
            grid[row].append(0)  # Append a cell
    return grid


def genTail(head_row, head_column, dir):
    tail = []
    # generate tail grids based on different direction
    # arrow pointing up:
    if dir == 'up':
        for i in range(1,3):
            tail.append((head_row + i, head_column + i))
            tail.append((head_row + i, head_column - i))
        for j in range(1,5):
            tail.append((head_row + j, head_column))
    # arrow pointing down:
    elif dir == 'down':
        for i in range(1,3):
            tail.append((head_row - i, head_column + i))
            tail.append((head_row - i, head_column - i))
        for j in range(1,5):
            tail.append((head_row - j, head_column))
    elif dir == 'right':
        for i in range(1,3):
            tail.append((head_row - i, head_column - i))
            tail.append((head_row + i, head_column - i))
        for j in range(1,5):
            tail.append((head_row, head_column - j))
    else: # left
        for i in range(1,3):
            tail.append((head_row - i, head_column + i))
            tail.append((head_row + i, head_column + i))
        for j in range(1,5):
            tail.append((head_row, head_column + j))
    return tail


def genArrow():
    # 0 is WHITE, 1 is BLUE, and 2 is target RED
    # generate blue arrow shapes, and the head of the arrow is RED
    grid = genGrid()
    # make lists of head and tail to store (row, column) of heads and tails
    head = []
    tail = []
    
    while not head or not tail or \
        any([i[0] not in range(0, ROWS) or i[1] not in range(0, COLUMNS) for i in tail]):
        head = []
        tail = []
        head_row = random.randrange(ROWS)
        head_column = random.randrange(COLUMNS)
        # append head
        head.append((head_row, head_column))
        # append tail 
        dir = random.choice(['up','down','right','left'])
        tail = genTail(head_row, head_column, dir)    
        
    return head, tail
        

def drawGrid(win, grid, steps, found):
    # Set the screen background
    win.fill(BLACK)
    # Draw the grid:
    for row in range(ROWS):
        for column in range(COLUMNS):
            color = WHITE
            if grid[row][column] == 9:
                color = GRAY
            if grid[row][column] == 1:
                color = BLUE
            if grid[row][column] == 2:
                color = RED
                found = True
            pygame.draw.rect(win, color, [(MARGIN + WIDTH) * column + MARGIN,
                                          (MARGIN + HEIGHT) * row + MARGIN,
                                          WIDTH,
                                          HEIGHT])
    # Jump to endScreen if found the HEAD
    if found == True:
        endScreen(win, steps)        
                
    # show steps taken
    stepsText = STAT_FONT.render('Steps: ' + str(steps), 1, (0,200,0))
    win.blit(stepsText, (WIN_SIZE[0] - (SIDEWIDTH + stepsText.get_width())//2, 10))
    
    pygame.display.update()
    
    
def clickGrid(win, grid, head, tail):
    # User clicks the mouse. Get the position
    pos = pygame.mouse.get_pos()
    # Change the (x, y) screen coordinates to grid coordinates
    column = pos[0] // (WIDTH + MARGIN)
    row = pos[1] // (HEIGHT + MARGIN)

    # Make sure only register when user clicked inside the grid space
    # user clicked a new grid
    steps = 0
    if 0 <= row <= ROWS-1 and 0 <= column <= COLUMNS-1 and grid[row][column] == 0:
        # User clicked the head
        if (row, column) in head: 
            grid[row][column] = 2
            steps = 1
            pygame.time.delay(100)
            # found = True
            print("head!")
            # endScreen(win, steps)
        # User clicked the tail
        elif (row, column) in tail:
            grid[row][column] = 1
            steps = 1
            print("tail!")
        # User clicked empty space
        else: 
            # # Make sure only register when user clicked inside the grid space
            # if 0 <= row <= ROWS-1 and 0 <= column <= COLUMNS-1:
            grid[row][column] = 9
            steps = 1
            print("empty")
        # print("Click ", pos, "Grid coordinates: ", row, column)  

    # return grid
    return steps


def drawSampleArrow(win):
    # draw a target shape on the right for reference
    # sample a up direction shape
    t = genTail(head_row=2, head_column=COLUMNS+2, dir='up')
    
    # head
    pygame.draw.rect(win, RED, [((MARGIN + WIDTH) * (COLUMNS + 2) + MARGIN),
                                ((MARGIN + HEIGHT) * 2 + MARGIN)/2 + 50,
                                WIDTH/2,
                                HEIGHT/2])
    
    # tail
    for (r, c) in t:
        pygame.draw.rect(win, BLUE, [((MARGIN + WIDTH) * c + MARGIN)/2 + 250,
                                    ((MARGIN + HEIGHT) * r + MARGIN)/2 + 50,
                                    WIDTH/2,
                                    HEIGHT/2])
    
    # add text
    text = STAT_FONT.render('Target Shape', 1, (200,0,0))
    # position the text at the center of right side screen
    win.blit(text, (WIN_SIZE[0] - (SIDEWIDTH + text.get_width())//2, 65))
    
    pygame.display.update()


def endScreen(win, steps):
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                pygame.quit()
                
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        
        stp = ' step!' if steps == 1 else ' steps!'
        finish = SMALL_FONT.render('You found the HEAD in', 1, (255,0,0))
        win.blit(finish, (WIN_SIZE[0] - (SIDEWIDTH + finish.get_width())//2, 115))
        finishStep = SMALL_FONT.render(str(steps) + stp, 1, (255,0,0))
        win.blit(finishStep, (WIN_SIZE[0] - (SIDEWIDTH + finishStep.get_width())//2, 150))
        playAgain = SMALL_FONT.render('Press ANY KEY to restart', 1, (0,255,0))
        win.blit(playAgain, (WIN_SIZE[0] - (SIDEWIDTH + playAgain.get_width())//2, 190))
        
        pygame.display.update()
        
    main()


def main():
    win = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Pic Pick")
    clock = pygame.time.Clock()
    
    grid = genGrid()
    head, tail = genArrow()
    steps = 0
    
    run = True
    found = False
    while run: 
        drawSampleArrow(win)
        clock.tick(10)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                steps += clickGrid(win, grid, head, tail)
                # steps += 1
            
        drawGrid(win, grid, steps, found)
    
    pygame.display.quit()
    pygame.quit()
    sys.exit()
    # quit()
               
# if __name__ == "__main__":
main()               
