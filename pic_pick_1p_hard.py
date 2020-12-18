'''
Inspired by a game in the Chinese Variety Show called 'Detective School
(名侦探学院)'.

RULES:
- Target shapes are shown on the right of the screen
- Target shapes are hidden under the white grid, and may be in different orientations
- Click on the cells to reveal what is underneath 
- GOAL is to find all the HEADs in as fewer steps as possible

- Gray means you missed, and the target could be elsewhere
- Blue means you have clicked on the target BODY, but not the Head
- Red means you have Successfully found the target HEAD
- Try to deduce the correct positions of the HEADs from the sample target shapes and revealed cells
'''

import pygame 
import random 
pygame.init() 

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (30,144,255)
RED = (255, 0, 0)
CYAN = (100,255,255)

# WIDTH and HEIGHT of each grid location
WIDTH = 50
HEIGHT = 50

# margin between each cell
MARGIN = 5

# Define Window size
ROWS = 12
COLUMNS = 10
SIDEWIDTH = 280
WIN_SIZE = [(WIDTH + MARGIN) * COLUMNS + MARGIN + SIDEWIDTH, 
            (HEIGHT + MARGIN) * ROWS + MARGIN]

# Define font to use
STAT_FONT = pygame.font.SysFont("comicsans", 50)
SMALL_FONT = pygame.font.SysFont("comicsans", 30)


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

def genTail1(head_row, head_column, dir):
    tail1 = []
    # generate tail1 grids based on different direction
    # arrow pointing up:
    if dir == 'up':
        for i in range(1,3):
            tail1.append((head_row + i, head_column + i))
            tail1.append((head_row + i, head_column - i))
        for j in range(1,5):
            tail1.append((head_row + j, head_column))
    # arrow pointing down:
    elif dir == 'down':
        for i in range(1,3):
            tail1.append((head_row - i, head_column + i))
            tail1.append((head_row - i, head_column - i))
        for j in range(1,5):
            tail1.append((head_row - j, head_column))
    elif dir == 'right':
        for i in range(1,3):
            tail1.append((head_row - i, head_column - i))
            tail1.append((head_row + i, head_column - i))
        for j in range(1,5):
            tail1.append((head_row, head_column - j))
    else: # left
        for i in range(1,3):
            tail1.append((head_row - i, head_column + i))
            tail1.append((head_row + i, head_column + i))
        for j in range(1,5):
            tail1.append((head_row, head_column + j))
    return tail1

def genTail2(head_row, head_column, dir):
    tail2 = []
    # generate tail2 grids based on different direction
    # arrow pointing up:
    if dir == 'up':
        tail2.append((head_row + 2, head_column + 1))
        tail2.append((head_row + 1, head_column + 2))
        tail2.append((head_row + 2, head_column - 1))
        tail2.append((head_row + 1, head_column - 2))
        for j in range(1,5):
            tail2.append((head_row + j, head_column))
    # arrow pointing down:
    elif dir == 'down':
        tail2.append((head_row - 2, head_column + 1))
        tail2.append((head_row - 1, head_column + 2))
        tail2.append((head_row - 2, head_column - 1))
        tail2.append((head_row - 1, head_column - 2))
        for j in range(1,5):
            tail2.append((head_row - j, head_column))
    elif dir == 'right':
        tail2.append((head_row - 2, head_column - 1))
        tail2.append((head_row - 1, head_column - 2))
        tail2.append((head_row + 2, head_column - 1))
        tail2.append((head_row + 1, head_column - 2))
        for j in range(1,5):
            tail2.append((head_row, head_column - j))
    else: # left
        tail2.append((head_row - 2, head_column + 1))
        tail2.append((head_row - 1, head_column + 2))
        tail2.append((head_row + 2, head_column + 1))
        tail2.append((head_row + 1, head_column + 2))
        for j in range(1,5):
            tail2.append((head_row, head_column + j))
    return tail2

def genTail3(head_row, head_column, dir):
    tail3 = []
    # generate tail3 grids based on different direction
    # arrow pointing up:
    if dir == 'up':
        tail3.append((head_row + 4, head_column - 1))
        tail3.append((head_row + 4, head_column + 1))
        for i in range(1,3):
            tail3.append((head_row + 2, head_column - i))
            tail3.append((head_row + 2, head_column + i))
        for j in range(1,4):
            tail3.append((head_row + j, head_column))
    # arrow pointing down:
    elif dir == 'down':
        tail3.append((head_row - 4, head_column - 1))
        tail3.append((head_row - 4, head_column + 1))
        for i in range(1,3):
            tail3.append((head_row - 2, head_column - i))
            tail3.append((head_row - 2, head_column + i))
        for j in range(1,4):
            tail3.append((head_row - j, head_column))
    elif dir == 'left':
        tail3.append((head_row - 1, head_column + 4))
        tail3.append((head_row + 1, head_column + 4))
        for i in range(1,3):
            tail3.append((head_row - i, head_column + 2))
            tail3.append((head_row + i, head_column + 2))
        for j in range(1,4):
            tail3.append((head_row, head_column + j))
    else: # right
        tail3.append((head_row - 1, head_column - 4))
        tail3.append((head_row + 1, head_column - 4))
        for i in range(1,3):
            tail3.append((head_row - i, head_column - 2))
            tail3.append((head_row + i, head_column - 2))
        for j in range(1,4):
            tail3.append((head_row, head_column - j))
    return tail3

def genArrow1():
    # 0 is WHITE, 1 is BLUE, and 2 is target RED
    # generate blue arrow shapes, and the head of the arrow is RED

    # make lists of head and tail to store (row, column) of heads and tails
    head1 = []
    tail1 = []
    
    while not head1 or not tail1 or \
        any([i[0] not in range(0, ROWS) or i[1] not in range(0, COLUMNS) for i in tail1]):
        head1 = []
        tail1 = []
        head1_row = random.randrange(ROWS)
        head1_column = random.randrange(COLUMNS)
        # append head1
        head1.append((head1_row, head1_column))
        # append tail1 
        dir = random.choice(['up','down','right','left'])
        tail1 = genTail1(head1_row, head1_column, dir)    
        
    return head1, tail1

def genArrow2(head1, tail1):
    # make lists of head and tail to store (row, column) of heads and tails
    head2 = []
    tail2 = []
    
    while not head2 or not tail2 or head2 == head1 or head2[0] in tail1 or \
        any([i[0] not in range(0, ROWS) or i[1] not in range(0, COLUMNS) or i in head1 or i in tail1 for i in tail2]):
        head2 = []
        tail2 = []
        head2_row = random.randrange(ROWS)
        head2_column = random.randrange(COLUMNS)
        # append head2
        head2.append((head2_row, head2_column))
        # append tail2 
        dir = random.choice(['up','down','right','left'])
        tail2 = genTail2(head2_row, head2_column, dir)    
        
    return head2, tail2       

def genArrow3(head1, tail1, head2, tail2):
    # make lists of head and tail to store (row, column) of heads and tails
    head3 = []
    tail3 = []
    
    while not head3 or not tail3 or head3 == head1 or head3 == head2 or head3[0] in tail1 or head3[0] in tail2 or\
        any([i[0] not in range(0, ROWS) or i[1] not in range(0, COLUMNS) or \
            i in head1 or i in tail1 or i in head2 or i in tail2 for i in tail3]):
        head3 = []
        tail3 = []
        head3_row = random.randrange(ROWS)
        head3_column = random.randrange(COLUMNS)
        # append head3
        head3.append((head3_row, head3_column))
        # append tail3 
        dir = random.choice(['up','down','right','left'])
        tail3 = genTail3(head3_row, head3_column, dir)    
        
    return head3, tail3       

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
                found += 1
            pygame.draw.rect(win, color, [(MARGIN + WIDTH) * column + MARGIN,
                                          (MARGIN + HEIGHT) * row + MARGIN,
                                          WIDTH,
                                          HEIGHT])
    # Jump to endScreen if found the HEAD
    if found == 3:
        endScreen(win, steps)        
                
    # show steps taken
    stepsText = STAT_FONT.render('Steps: ' + str(steps), 1, (0,200,0))
    win.blit(stepsText, (WIN_SIZE[0] - (SIDEWIDTH + stepsText.get_width())//2, 10))
    
    pygame.display.update()
    
def clickGrid(win, grid, head, tail, steps):
    # User clicks the mouse. Get the position
    pos = pygame.mouse.get_pos()
    # Change the (x, y) screen coordinates to grid coordinates
    column = pos[0] // (WIDTH + MARGIN)
    row = pos[1] // (HEIGHT + MARGIN)

    # User clicked the head
    if (row, column) in head: 
        grid[row][column] = 2
        steps += 1
        pygame.time.delay(100)
        # found = True
        print("head!")
        # endScreen(win, steps)
    # User clicked the tail
    elif (row, column) in tail:
        grid[row][column] = 1
        steps += 1
        print("tail!")
    # User clicked empty space
    else: 
        # Make sure only register when user clicked inside the grid space
        if 0 <= row <= ROWS-1 and 0 <= column <= COLUMNS-1:
            grid[row][column] = 9
            steps += 1
            print("empty")
    # print("Click ", pos, "Grid coordinates: ", row, column)  

    return grid

def drawSampleHead(win, head_row):
    # function to draw sample heads
    # Rescale to smaller sizes
    pygame.draw.rect(win, RED, [((MARGIN + WIDTH)*(COLUMNS + 2) + MARGIN),
                                ((MARGIN + HEIGHT)*head_row + MARGIN)//2 + HEIGHT,
                                WIDTH//2,
                                HEIGHT//2])

def drawSampleTail(win, t):
    # function to draw sample tails
    for (r, c) in t:
        # Rescale to smaller sizes
        pygame.draw.rect(win, BLUE, [((MARGIN + WIDTH)*c + MARGIN)//2 + ((MARGIN + WIDTH)*(COLUMNS+1))//2 + (WIDTH)//2 + MARGIN,
                                    ((MARGIN + HEIGHT)*r + MARGIN)//2 + HEIGHT,
                                    WIDTH//2,
                                    HEIGHT//2])

def drawSampleArrow(win):
    # draw a target shape on the right of the screen for reference
    # sample shapes with UP direction
    t1 = genTail1(head_row=4, head_column=COLUMNS+2, dir='up')
    t2 = genTail2(head_row=10, head_column=COLUMNS+2, dir='up')
    t3 = genTail3(head_row=16, head_column=COLUMNS+2, dir='up')
    
    # sample 1
    drawSampleHead(win, head_row=4)
    drawSampleTail(win, t1)
    # sample 2
    drawSampleHead(win, head_row=10)
    drawSampleTail(win, t2)
    # sample 3
    drawSampleHead(win, head_row=16)
    drawSampleTail(win, t3)
    # add text
    text = STAT_FONT.render('Target Shapes', 1, RED)
    answerText = SMALL_FONT.render('Hold R to reveal answer', 1, CYAN)
    # position the text at the center of right side screen
    win.blit(text, (WIN_SIZE[0] - (SIDEWIDTH + text.get_width())//2, 60))
    win.blit(answerText, (WIN_SIZE[0] - (SIDEWIDTH + text.get_width())//2, 110))
    
    pygame.display.update()

def showAnswer(win, grid, head, tail):
    # Reveal the answer
    for (row, column) in head:
        color = RED
        pygame.draw.rect(win, color, [(MARGIN + WIDTH) * column + MARGIN, 
                                      (MARGIN + HEIGHT) * row + MARGIN, 
                                      WIDTH, 
                                      HEIGHT])
    for (row, column) in tail:
        color = CYAN
        pygame.draw.rect(win, color, [(MARGIN + WIDTH) * column + MARGIN, 
                                      (MARGIN + HEIGHT) * row + MARGIN, 
                                      WIDTH, 
                                      HEIGHT])
    
    pygame.display.update()
    
def endScreen(win, steps):
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                pygame.quit()
            # if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                # Pause for 1 sec
                pygame.time.delay(1000)
            
        finish = SMALL_FONT.render('You found all the HEADs in', 1, (255,0,0))
        win.blit(finish, (WIN_SIZE[0] - (SIDEWIDTH + finish.get_width())//2, 115))
        finishStep = SMALL_FONT.render(str(steps) + ' steps', 1, (255,0,0))
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
    head1, tail1 = genArrow1()
    head2, tail2 = genArrow2(head1, tail1)
    head3, tail3 = genArrow3(head1, tail1, head2, tail2)
    head = head1 + head2 + head3
    tail = tail1 + tail2 + tail3
    steps = 0
    
    run = True
    found = 0
    while run: 
        drawSampleArrow(win)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            showAnswer(win, grid, head, tail)
                
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clickGrid(win, grid, head, tail, steps)
                steps += 1
          
        drawGrid(win, grid, steps, found)
        
    pygame.quit()
    quit()
               
               
if __name__ == "__main__":
    main()