from utils import *


chess = Game(name="Chess 1.0", width=600, height=600, side=65)
pieces = ChessPiece(chess)
window = TkWindow(chess)
# Main Loop
while 1:
    chess.screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if   event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  
            pos = pygame.mouse.get_pos()
            
            pieces.select(list(pos)) 
            if 560<pos[0]<592 and 5<pos[1]<37:
                window.settings()     

    
    chess.draw_board()
    pieces.draw() 
    
    pygame.display.update()