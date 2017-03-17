from Classes import *
pygame.init()
clock = pygame.time.Clock()
running = 1
black = (0, 0, 0)
white = (255, 255, 255)
game = Game(screen)

while running:
    screen.fill(black)
    game.update()
    for i in range(1, 6):
        pygame.draw.line(screen, white, (0, i * 100), (screen_width, i * 100))
        pygame.draw.line(screen, white, (i * 100, 0), (i * 100, screen_height))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            game.place_piece(x, y)
    pygame.display.flip()
    clock.tick(100)
