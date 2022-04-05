import itertools
import pygame, random, sys
from pygame.locals import *


tetrominos = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 1, 1], [0, 0, 1]],
    'L': [[1, 1, 1], [1, 0, 0]],
    'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'Z': [[1, 1, 0], [0, 1, 1]]
}


class Block:
    def __init__(self, x, y, blockType):
        self.x = x
        self.y = y
        self.blockShape = tetrominos[blockType]
        
    def rotate(self):
        self.blockShape = list(zip(*self.blockShape[::-1]))
        
    def move(self, x, y):
        self.x += x
        self.y += y
        
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
    def draw(self, screen: pygame.Surface):
        for i in range(len(self.blockShape)):
            for j in range(len(self.blockShape[i])):
                if self.blockShape[i][j] == 1:
                    pygame.draw.rect(screen, (158, 173, 134), ((self.x * 20) + (j * 20), (self.y * 20) + (i * 20), 20, 20))
                    pygame.draw.rect(screen, (0, 0, 0), ((self.x * 20) + 1 + (j * 20), (self.y * 20) + 1 + (i * 20), 18, 18))
                    pygame.draw.rect(screen, (158, 173, 134), ((self.x * 20) + 3 + (j * 20), (self.y * 20) + 3 + (i * 20), 14, 14))
                    pygame.draw.rect(screen, (0, 0, 0), ((self.x * 20) + 5 + (j * 20), (self.y * 20) + 5 + (i * 20), 10, 10))
                    

class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.currentBlock = self.randomBlock()
        self.nextBlock = self.randomBlock()
        self.score = 0
        self.level = 1
        self.speed = 0.5
        
    def randomBlock(self) -> Block:
        return Block(self.width//2, 0, random.choice(list(tetrominos.keys())))
    
    def canMoveLeft(self) -> bool:
        if self.currentBlock.x == 0:
            return False
        for i in range(len(self.currentBlock.blockShape)):
            for j in range(len(self.currentBlock.blockShape[i])):
                if self.currentBlock.blockShape[i][j] == 1 and self.board[self.currentBlock.y + i][self.currentBlock.x + j - 1] == 1:
                    return False
        return True
    
    def canMoveRight(self) -> bool:
        if (self.currentBlock.x + len(self.currentBlock.blockShape[0])) == self.width :
            return False
        for i in range(len(self.currentBlock.blockShape)):
            for j in range(len(self.currentBlock.blockShape[i])):
                if self.currentBlock.blockShape[i][j] == 1 and self.board[self.currentBlock.y + i][self.currentBlock.x + j + 1] == 1:
                    return False
        return True
    
    def canMoveDown(self) -> bool:
        if self.currentBlock.y + len(self.currentBlock.blockShape) == self.height:
            return False
        for i in range(len(self.currentBlock.blockShape)):
            for j in range(len(self.currentBlock.blockShape[i])):
                if self.currentBlock.blockShape[i][j] == 1 and self.board[self.currentBlock.y + i + 1][self.currentBlock.x + j] == 1:
                    return False
        return True
    
    def canRotate(self) -> bool:
        for i in range(len(self.currentBlock.blockShape)):
            for j in range(len(self.currentBlock.blockShape[i])):
                if self.currentBlock.blockShape[i][j] == 1 and self.board[self.currentBlock.y + i][self.currentBlock.x + j] == 1:
                    return False
        return True
    
    def checkFullLine(self) -> list:
        fullLines = []
        for i in range(len(self.board)):
            full = all(self.board[i][j] != 0 for j in range(len(self.board[i])))
            if full:
                fullLines.append(i)
        return fullLines
    
    def placeBlock(self):
        for i in range(len(self.currentBlock.blockShape)):
            for j in range(len(self.currentBlock.blockShape[i])):
                if self.currentBlock.blockShape[i][j] == 1:
                    self.board[self.currentBlock.y + i][self.currentBlock.x + j] = 1
                    
    def removeFullLines(self, fullLines):
        for i in range(len(fullLines)):
            self.board.pop(fullLines[i])
            self.board.insert(0, [0 for _ in range(self.width)])
            self.score += 10
        if self.score % 500 == 0:
            self.levelUp()
            
    def removeFullLinesAnimation(self, fullLines, screen: pygame.Surface):
        s = pygame.Surface((18,18))
        s1 = pygame.Surface((10,10))
        s.fill((86,0,0))
        s1.fill((86,0,0))
        for i in fullLines:
            for j in range(len(self.board[i])):
                screen.blit(s, ((j*20)+1,(i*20)+1))
                pygame.draw.rect(screen, (158, 173, 134), ((j*20)+3, (i*20)+3, 14, 14))
                screen.blit(s1, ((j*20)+5,(i*20)+5))
            pygame.display.update()
            pygame.time.delay(150)
        s.fill((0,0,0))
        s1.fill((0,0,0))
        for i in fullLines:
            for j in range(len(self.board[i])):
                screen.blit(s, ((j*20)+1,(i*20)+1))
                pygame.draw.rect(screen, (158, 173, 134), ((j*20)+3, (i*20)+3, 14, 14))
                screen.blit(s1, ((j*20)+5,(i*20)+5))
            pygame.display.update()
            pygame.time.delay(150)
        s.fill((86,0,0))
        s1.fill((86,0,0))
        for i in fullLines:
            for j in range(len(self.board[i])):
                screen.blit(s, ((j*20)+1,(i*20)+1))
                pygame.draw.rect(screen, (158, 173, 134), ((j*20)+3, (i*20)+3, 14, 14))
                screen.blit(s1, ((j*20)+5,(i*20)+5))
            pygame.display.update()
            pygame.time.delay(150)
        self.removeFullLines(fullLines)
            
    def _drawNextBlockBg(self, screen: pygame.Surface):
        s = pygame.Surface((18,18))
        s1 = pygame.Surface((10,10))
        s.fill((0,0,0))
        s1.fill((0,0,0))
        s.set_alpha(70)
        s1.set_alpha(70)
        startY = 1
        startX = len(self.board[0]) + 3
        endY = startY + 2
        endX = startX + 4
        for i, j in itertools.product(range(startY, endY), range(startX, endX)):
            screen.blit(s, ((j*20)+1,(i*20)+1))
            pygame.draw.rect(screen, (158, 173, 134), ((j*20)+3, (i*20)+3, 14, 14))
            screen.blit(s1, ((j*20)+5,(i*20)+5))
                
    def _drawNextBlock(self, screen: pygame.Surface):
        self.nextBlock.setPosition(len(self.board[0]) + 3, 1)
        self.nextBlock.draw(screen)
        
    def _drawScore(self, screen: pygame.Surface):
        font = pygame.font.SysFont('Arial', 20)
        text = font.render(f'Score: {str(self.score)}', True, (0, 0, 0))
        startY = 100
        startX = (len(self.board[0]) + 3) * 20
        screen.blit(text, (startX, startY))
        
    def reset(self):
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.currentBlock = self.randomBlock()
        self.nextBlock = self.randomBlock()
        self.score = 0
        self.level = 1
    
    def draw(self, screen: pygame.Surface):
        screen.fill((158, 173, 134))
        s = pygame.Surface((18,18))
        s1 = pygame.Surface((10,10))
        s.fill((0,0,0))
        s1.fill((0,0,0))
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    s.set_alpha(70)
                    s1.set_alpha(70)
                else:
                    s.set_alpha(255)
                    s1.set_alpha(255)
                screen.blit(s, ((j*20)+1,(i*20)+1))
                pygame.draw.rect(screen, (158, 173, 134), ((j*20)+3, (i*20)+3, 14, 14))
                screen.blit(s1, ((j*20)+5,(i*20)+5))
        self._drawNextBlockBg(screen)
        self._drawNextBlock(screen)
        self._drawScore(screen)
        self.currentBlock.draw(screen)
        
    def levelUp(self):
        self.level += 1
        self.speed = self.speed - (self.speed * 0.1)
        
        
def hadleEvents(screen, gb, event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT and gb.canMoveLeft():
            gb.currentBlock.x -= 1
        if event.key == pygame.K_RIGHT and gb.canMoveRight():
            gb.currentBlock.x += 1
        if event.key == pygame.K_DOWN and gb.canMoveDown():
            gb.currentBlock.y += 1
        if event.key == pygame.K_UP and gb.canRotate():
            gb.currentBlock.rotate()
        if event.key == pygame.K_SPACE and gb.canMoveDown():
            while gb.canMoveDown():
                gb.currentBlock.y += 1
            gb.draw(screen)
        if event.key == pygame.K_r:
            gb.reset()


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()
    gb = GameBoard(10, 20)
    pygame.display.update()
    fall_timer = 0
    while True:
        fall_timer += clock.get_rawtime()
        clock.tick(500)
        for event in pygame.event.get():
            hadleEvents(screen, gb, event)
        if gb.canMoveDown():
            if fall_timer/1000 >= gb.speed:
                gb.currentBlock.y += 1
                fall_timer = 0
        else:
            gb.placeBlock()
            gb.removeFullLinesAnimation(gb.checkFullLine(), screen)
            gb.nextBlock.setPosition(gb.width//2, 0)
            gb.currentBlock = gb.nextBlock
            gb.nextBlock = gb.randomBlock()
        gb.draw(screen)
        pygame.display.update()
        

if __name__ == "__main__":
    main()
