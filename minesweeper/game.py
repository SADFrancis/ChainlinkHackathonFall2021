import pygame
import os
from time import sleep


class Game:
    def __init__(self, board, screenSize):
        self.board = board
        self.screenSize = screenSize
        # screen size/board size (width,height) == screen width / columns, screen height / rows
        self.pieceSize = (
            self.screenSize[0] // self.board.getSize()[1],
            self.screenSize[1] // self.board.getSize()[0],
        )
        # double slash // for integer division
        self.loadImages()

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
        running = True
        while running:  # main loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    # index #2 is right clic for the pygame function
                    rightClick = pygame.mouse.get_pressed()[2]
                    self.handleClick(position, rightClick)
            self.draw()
            pygame.display.flip()
            if self.board.getWon():
                sound = pygame.mixer.Sound("Banner.mp3")
                sound.play()
                sleep(4)
                running = False
        pygame.quit()

    def draw(self):
        topLeft = (0, 0)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                image = self.getImage(piece)
                # image = self.images["empty-block"]
                self.screen.blit(image, topLeft)  # draw image ontop screen
                # increment and draw from left to right
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            # reset "pointer" to the left and position down a row
            topLeft = 0, topLeft[1] + self.pieceSize[1]

    def loadImages(self):
        self.images = {}
        for fileName in os.listdir("images"):
            if not fileName.endswith(".png"):
                continue
            image = pygame.image.load(r"images/" + fileName)
            image = pygame.transform.scale(image, self.pieceSize)
            self.images[fileName.split(".")[0]] = image

    def getImage(self, piece):
        string = None
        if piece.getClicked():
            if piece.getClicked():
                string = (
                    "bomb-at-clicked-block"
                    if piece.getHasBomb()
                    else str(piece.getNumAround())
                )
        else:
            string = "flag" if piece.getFlagged() else "empty-block"
        # string = "unclicked-bomb" if piece.getHasBomb() else str(piece.getNumAround())
        return self.images[string]

    def handleClick(self, position, rightClick):
        # rows,column - get the index of the square that the mouse clicked on the board
        # position is the pygame.mouse.get_pos() coordinate of the mouse click and pieceSize is the size of the board
        # integer divide by pieceSize because pieceSize is the number of pixels (row,col or y,x)
        # index will be the index of the button clicked on
        if self.board.getLost():
            return
        index = position[1] // self.pieceSize[1], position[0] // self.pieceSize[0]
        piece = self.board.getPiece(index)
        self.board.handleClick(piece, rightClick)
