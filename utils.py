import pygame, random, os, sys, chess
from tkinter import*

################################################################
################################################################

class Game:   
    over = False
    paused = False
    count = 0
    color="black"
    previous = str()
    def __init__(self,name,width,height,side): 
        pygame.init()
        pygame.display.set_caption(name)
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))
        
        self.screen = pygame.display.set_mode((width, height))
        self.WIDTH, self.HEIGHT = width, height
        self.SIDE = side
        self.BORDER = ((width-side*8)/2, (height-side*8)/2)
        self.ALPHABET = pygame.image.load("assets/Board/alphabet.png")
        self.NUMBERS = pygame.image.load("assets/Board/numbers.png")
        self.SETTINGS = pygame.image.load("assets/settings.png") 
        
        self.board=chess.Board()

    def sound(self,audio):
        if audio != self.previous:
            sound = pygame.mixer.Sound(audio)
            pygame.mixer.Sound.play(sound)
            pygame.mixer.music.stop()
            self.previous = audio
            
            
    def wait_and_run(self, time):
        event = pygame.USEREVENT+self.count
        self.eventlist.append(event)
        self.count += 1
        pygame.time.set_timer(event ,time) 
        return event
        
    def draw_board(self):
        self.screen.blit(self.SETTINGS,(560,5))
        rect = ["white",self.color]
        for y in range(8):
            for x in range(8):
                pygame.draw.rect(self.screen, rect[0], pygame.Rect(x*self.SIDE+self.BORDER[0],y*self.SIDE+self.BORDER[1],self.SIDE,self.SIDE))    
                rect.reverse()
            rect.reverse()   
        self.screen.blit(self.ALPHABET,(0,560)); self.screen.blit(self.NUMBERS,(-15,0))
        pygame.draw.rect(self.screen, "grey", pygame.Rect(self.BORDER[0],self.BORDER[1],self.SIDE*8,self.SIDE*8),3)
    
    def change_colour(self,color):  self.color = color


################################################################
################################################################

class ChessPiece:
    selections = []      
    imglist = [ # White pieces
                '6(2).png','7(2).png','8(2).png','10(1).png','9(1).png','8(2).png','7(2).png','6(2).png',
                '11(8).png','11(8).png','11(8).png','11(8).png','11(8).png','11(8).png','11(8).png','11(8).png',
                # Black pieces
                '5(8).png','5(8).png','5(8).png','5(8).png','5(8).png','5(8).png','5(8).png','5(8).png',
                '0(2).png','1(2).png','2(2).png','3(1).png','4(1).png','2(2).png','1(2).png','0(2).png']  
    curpos = [None]
    player = ["black","white",]
    moveable = 0
    gained = ""
    def __init__(self,game):
        self.GAME = game
        self.WIDTH, self.HEIGHT = 45, game.SIDE
        self.SELECTION = pygame.transform.scale( pygame.image.load("assets/selection.png"), (game.SIDE,)*2)
        self.REDMARK = pygame.transform.scale( pygame.image.load("assets/redmark.png"), (game.SIDE,)*2)
        
        self.xcor = [game.BORDER[0]+x*game.SIDE for x in range(8)]
        self.ycor = [game.BORDER[1]+y*game.SIDE for y in range(8)]
        self.all_cell_cor = {"abcdefgh"[x]+"12345678"[y]:(self.xcor[x], self.ycor[y]) for y in range(8) for x in range(8)}
        self.pieces = {(list(self.all_cell_cor.values())[:16]+list(self.all_cell_cor.values())[-16:])[cor]:\
                       f"assets/Piece/{self.imglist[cor]}" for cor in range(32)}
    
    def draw(self): 
        win = TkWindow(self.GAME)
        if self.GAME.board.is_checkmate():  
            win.mate_window(f"{self.player[0].title()} won the game","Checkmate")
            self.GAME.sound("assets/sounds/victory.wav")
        if self.GAME.board.is_stalemate():  
            win.mate_window(f"Game is draw","Stalemate")
            self.GAME.sound("assets/sounds/victory.wav")
        if self.GAME.board.is_check():
            if self.player[0] == "white": 
                cor = list(self.pieces.keys())[list(self.pieces.values()).index("assets/Piece/4(1).png")]
                self.GAME.screen.blit(self.REDMARK,cor)
            else:
                cor = list(self.pieces.keys())[list(self.pieces.values()).index("assets/Piece/9(1).png")]
                self.GAME.screen.blit(self.REDMARK,cor)
            self.GAME.sound("assets/sounds/check.wav")
            
                
        for s   in self.selections: self.GAME.screen.blit(self.SELECTION,s)
        for cor in self.pieces:  self.GAME.screen.blit(pygame.transform.scale(pygame.image.load(self.pieces[cor]), (self.WIDTH,self.HEIGHT)),cor)
            
    def select(self,pos):
        p = list(pos)
        if 40<=pos[0]<=560 and 40<=pos[1]<=560:
            self.xcor.append(pos[0]); self.ycor.append(pos[1])
            self.xcor.sort(); self.ycor.sort()
            pos = self.xcor[self.xcor.index(pos[0])-1], self.ycor[self.ycor.index(pos[1])-1]
            self.selections = [pos]
            self.xcor.remove(p[0]); self.ycor.remove(p[1])
                        
            lgl_mvs = self.GAME.board.legal_moves 
            
            if self.moveable == 1: self.move(tuple(pos))          
            self.selections = [] 
            for m in lgl_mvs:
                if not str(m)[-1].isdigit(): self.gained=str(m)[-1]; self.selections.append(self.all_cell_cor[str(m)[-3:-1]])
                elif pos == self.all_cell_cor[str(m)[:2]]: self.selections.append(self.all_cell_cor[str(m)[-2:]])
            if self.selections!=[]: self.moveable = 1 
            
            
            self.curpos.append(tuple(pos))
        else: self.selections = []; self.movable = 0
        
    def move(self,pos): 
        m = list(self.all_cell_cor.keys())[list(self.all_cell_cor.values()).index(self.curpos[-1])] + \
            list(self.all_cell_cor.keys())[list(self.all_cell_cor.values()).index(pos)]+self.gained
            
        try: 
            self.GAME.board.push_san(m)
            img = self.pieces.pop(self.curpos[-1])
            self.curpos.pop()
            self.pieces.update({pos:img})
            self.player.reverse()
            self.moveable = 0
            self.gained = ""
        except ValueError: 
            self.moveable = 0
################################################################
################################################################

class TkWindow:
    def __init__(self,game):
        self.game = game
    
    def settings(self):
        root  = Tk()
        root.title("Settings")
        root.geometry("510x220")
        root.config(bg="black")
        
        appearance = Label(root, text="Change Appearance",bg="black", font="broadway",fg="blue",padx=10)
        color1 = Button(root, bg="blue",padx=10, command=lambda : self.game.change_colour("blue"))
        color2 = Button(root, bg="#2e0706",padx=10, command=lambda : self.game.change_colour("#2e0706"))
        color3 = Button(root, bg="#545755",padx=10, command=lambda: self.game.change_colour("#545755"))
        color4 = Button(root, bg="black",borderwidth=2,padx=10, command=lambda: self.game.change_colour("black"))
        color5 = Button(root, bg="#16a13b",padx=10, command=lambda: self.game.change_colour("#16a13b"))
        color6 = Button(root, bg="#50157a",padx=10, command=lambda: self.game.change_colour("#50157a"))
        color7 = Button(root, bg="#a6a316",padx=10, command=lambda: self.game.change_colour("#a6a316"))
        color8 = Button(root, bg="#16a682",padx=10, command=lambda: self.game.change_colour("#16a682"))
        color9 = Button(root, bg="#c45206",padx=10, command=lambda: self.game.change_colour("#c45206"))
        
        appearance.grid(row=0,column=0)
        color1.grid(row=0,column=1); color2.grid(row=0,column=2) 
        color3.grid(row=0,column=3); color4.grid(row=0,column=4)
        color5.grid(row=0,column=5); color6.grid(row=0,column=6)
        color7.grid(row=0,column=7); color8.grid(row=0,column=8)
        color9.grid(row=0,column=9)
        
        apply = Button(root,command=root.destroy,text="Apply",bg="red",fg="white")
        apply.grid(row=4,column=10)
        root.mainloop()
    
    def mate_window(self,msg,heading):
        root = Tk()
        root.title(heading)
        root.geometry("500x150")
        root.config(bg="black")
        Label(root,text=msg,font=("broadway",18,"normal"),fg="white",bg="black").pack()
        root.mainloop()

################################################################
################################################################