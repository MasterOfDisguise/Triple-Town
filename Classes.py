import pygame
import random

screen_height = 600
screen_width = 600
num_slots_across = 6
slot_width = screen_width / num_slots_across
slot_height = screen_height / num_slots_across
screen = pygame.display.set_mode((screen_height, screen_width))


class Game:

    def __init__(self, surface):
        self.surface = surface
        self.board = Board(self)
        self.current_piece = self.random_piece()
        self.once = True

    def place_piece(self, x, y):
        self.current_piece.placed = True
        col = int(x / (screen_width / num_slots_across))
        row = int(y / (screen_height / num_slots_across))
        if self.board.contents[col][row] == 0:
            self.board.add_piece(col, row, self.current_piece.size)
            self.current_piece = self.random_piece()
            self.once = True

    def random_piece(self):
        x = random.random()
        size = 1
        if 0.65 <= x <= 0.85:
            size = 2
        elif 0.85 <= x <= 1:
            size = 3
        return Piece(self, size)

    def update(self):
        self.board.update()
        self.current_piece.update()


class Board:

    def __init__(self, manager):
        self.manager = manager
        self.x_width = num_slots_across
        self.y_width = num_slots_across
        self.contents = []
        self.num = 0
        self.setup()

    def setup(self):
        for x in range(self.x_width + 1):
            self.contents.append([])
            for y in range(self.y_width):
                self.contents[x - 1].append(0)
        self.random_board()

    def check_combine(self, piece, pieces):
        if piece not in pieces:
            pieces.append(piece)
        if piece.col - 1 >= 0:
            if self.contents[piece.col - 1][piece.row] != 0:
                target = self.contents[piece.col - 1][piece.row]
                if target.size == piece.size and target not in pieces:
                    self.check_combine(target, pieces)
        if piece.row + 1 < num_slots_across:
            if self.contents[piece.col][piece.row + 1] != 0:
                target = self.contents[piece.col][piece.row + 1]
                if target.size == piece.size and target not in pieces:
                    self.check_combine(target, pieces)
        if piece.col + 1 < num_slots_across:
            if self.contents[piece.col + 1][piece.row] != 0:
                target = self.contents[piece.col + 1][piece.row]
                if target.size == piece.size and target not in pieces:
                    self.check_combine(target, pieces)
        if piece.row - 1 >= 0:
            if self.contents[piece.col][piece.row - 1] != 0:
                target = self.contents[piece.col][piece.row - 1]
                if target.size == piece.size and target not in pieces:
                    self.check_combine(target, pieces)
        return pieces

    def add_piece(self, col, row, size):
        piece = Piece(self.manager, size)
        piece.placed = True
        piece.col = col
        piece.row = row
        piece.rect.x, piece.rect.y = col * 100, row * 100
        self.contents[piece.col][piece.row] = piece
        self.num += 1
        self.combine(self.check_combine(piece, []), piece)
        print self.num

    def combine(self, pieces, piece):
        if len(pieces) >= 3:
            for thing in pieces:
                self.contents[thing.col][thing.row] = 0
            self.add_piece(piece.col, piece.row, piece.size + 1)
            self.num -= len(pieces)

    def random_board(self):
        for col in range(num_slots_across):
            print True
            for row in range(num_slots_across):
                x = random.random()
                if x <= .60:
                    pass
                if .65 <= x <= .85:
                    self.add_piece(col, row, 1)
                if .85 <= x <= .95:
                    self.add_piece(col, row, 2)
                if .95 <= x <= 1:
                    self.add_piece(col, row, 3)

    def update(self):
        for row in self.contents:
            for slot in row:
                if slot != 0:
                    slot.update()
        if self.num == 1 and self.manager.once:
            for col in self.contents:
                for row in col:
                    if row != 0:
                        if row.size == 1:
                            print "YOU WIN!"

class Piece(pygame.sprite.Sprite):

    def __init__(self, manager, size):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.size = size
        self.sprite = self.select_image()
        self.rect = self.sprite.get_rect()
        self.rect.x, self.rect.y = pygame.mouse.get_pos()
        self.rect.x -= 50
        self.rect.y -= 50
        self.col = 0
        self.row = 0
        self.placed = False

    def select_image(self):
        if self.size > 3:
            self.size = 1
        if self.size == 1:
            return pygame.image.load("1.png").convert()
        if self.size == 2:
            return pygame.image.load("2.png").convert()
        if self.size == 3:
            return pygame.image.load("3.png").convert()

    def draw(self):
        self.manager.surface.blit(self.sprite, self.rect)

    def move(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = mouse_pos[0] - 50
        self.rect.y = mouse_pos[1] - 50

    def update(self):
        self.draw()
        if not self.placed:
            self.move()


# to do:
# 1. random board
# 2. score
# 3. random pieces