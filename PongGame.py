import pygame, sys
from pygame.locals import *

# @author: Ama Freeman
# @date: Dec. 17, 2016
# @purpose: Create a simple pong game for fun! :)
# Also to try to make it run using my raspberry pi and Kawaii Pong!
#Created using tutorial on: http://trevorappleton.blogspot.com/2014/04/writing-pong-using-python-and-pygame.html

# Number of Frames per Second
# Affects the speed up or down of the game
FPS = 200

# Global variables for the program
WINDOWWIDTH = 400
WINDOWHEIGHT = 300
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20

# Set up the colors
LIGHTPINK = (252, 219, 240)
DARKPURPLE = (98, 3, 124)

# Draws the arena the game will be played in
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    # Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, DARKPURPLE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    # Draw center line
    pygame.draw.line(DISPLAYSURF, DARKPURPLE, ((WINDOWWIDTH/2),0),((WINDOWWIDTH/2),WINDOWHEIGHT), 1)

# Draw the paddle
def drawPaddle(paddle):
    # Stops the paddle from moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    # Stops the paddle from moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    # Draws paddle
    pygame.draw.rect(DISPLAYSURF, DARKPURPLE, paddle)

# Draw the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, DARKPURPLE, ball)

# Moves the ball and returns new position
def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

# Checks for a collision with a wall, and 'bounces' ball off it
# Returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

# Checks for collision with middle line
#def checkPaddleLineCollision(paddle1, ):

# Checks if the ball has hit a paddle, and 'bounces' ball off it
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else: return 1

# Artificial Intelligence of computer player
def artificialIntelligence(ball, ballDirX, paddle2):
    # if the ball is moving away from paddle, center bat
    if ballDirX == -1:
        if paddle2.centery < (WINDOWHEIGHT / 2):
            paddle2.y += 1
        elif paddle2.centery > (WINDOWHEIGHT / 2):
            paddle2.y -= 1
    # if the ball is moving towards bat, tracks its movement
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -= 1
    return paddle2

# Checks to see if a point has been scored, returns new score
def checkPointScored(paddle1, ball, score, ballDirX):
    #reset points if left wall is hit
    if ball.left == LINETHICKNESS:
        return 0
    # 1 point for hitting the ball
    elif ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball .top and paddle1.bottom > ball.bottom:
        score += 1
        return score
    # 5 points for beating the other paddle
    elif ball.right == WINDOWWIDTH - LINETHICKNESS:
        score += 5
        return score
    #if no points scored, return score unchanged
    else: return score

# Displays the current score on the screen
def displayScore(score):
    resultSurf = BASICFONT.render('Score = %s' %(score), True, DARKPURPLE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 150, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

# Main Function
def main():

    # Needed to initialize pygame
    pygame.init()
    global DISPLAYSURF

    # Font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pong')

    # Initiate variable and set starting positions
    # any future changes made within rectangles
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) / 2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) / 2
    score = 0

    # Keeps track of ball direction
    ballDirX = -1 ## -1 = left, 1 = right
    ballDirY = -1 ## -1 = up, 1 = down

    #Creates rectangles for ball and paddles
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    #Draws the starting position of the arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    pygame.mouse.set_visible(0) # make cursor invisible

    while True: # The main loop of the game
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # mouse movement commands
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey
                #paddle1.x = mousex
                

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        score = checkPointScored(paddle1, ball, score, ballDirX)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
        paddle2 = artificialIntelligence(ball, ballDirX, paddle2)

        displayScore(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()




