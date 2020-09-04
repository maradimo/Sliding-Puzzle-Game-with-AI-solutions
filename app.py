
from tkinter import *
from tkinter.ttk import Entry,Button,OptionMenu
from PIL import Image, ImageTk
import random
from tkinter import filedialog
import os 


class Tiles():
    def __init__(self, grid):
        
        self.tiles = []
        self.tiles_dict = dict()
        self.grid = grid
        self.gap = None
        self.moves = 0

    '''
    Adds a Tile object to a list of Tiles
    '''   
    def add(self,tile):
        self.tiles.append(tile)

    '''
    Returns a tile object based on position
    '''    
    def get_tile(self,*pos):
        try:
            return self.tiles_dict[pos]
        except KeyError:
            pass

    def get_tiles_around_gap(self):
        row = self.gap.pos[0]
        col = self.gap.pos[1]
        return self.get_tile(row-1,col),self.get_tile(row+1,col),self.get_tile(row,col+1),self.get_tile(row,col-1)

    '''
    Changes the position of the gap and the position of the tile moved
    '''
    def slide_gap(self,tile):
        try:
            pos = self.gap.pos
            self.tiles_dict[pos] = tile
            self.tiles_dict[tile.pos] = self.gap
            self.gap.pos = tile.pos 
            tile.pos = pos
            self.moves+=1
        except:
            pass
    
    '''
    Slides gap based on key input
    '''
    def slide(self,key):
        up,down,right,left = self.get_tiles_around_gap()
        if key == 'Up':
            self.slide_gap(up)
        elif key == 'Down': 
            self.slide_gap(down)
        elif key == 'Right':
            self.slide_gap(right)
        elif key == 'Left':
            self.slide_gap(left)
        self.show()


    '''
    Shuffles the list of tiles
    '''
    def shuffle(self):
        random.shuffle(self.tiles)
        i = 0
        for row in range(self.grid):
            for col in range(self.grid):
                self.tiles[i].pos = (row,col)
                self.tiles_dict[(row,col)] = self.tiles[i]
                i+=1
    
    '''
    Shows the tiles
    '''
    def show(self):
        for tile in self.tiles:
            if self.gap.pos != tile.pos:
                tile.show()

    def set_gap(self, index):
        self.gap = self.tiles[index]

    '''
    Check if tile is placed correctly
    '''       
    def is_correct(self):
        for tile in self.tiles:
            if not tile.is_correct_pos():
                return False
        return True 

class Tile(Label):
    def __init__(self,parent, image,pos):
        Label.__init__(self,parent,image=image)
        self.image = image
        self.pos, self.curpos = pos, pos
    
    def show(self):
        self.grid(row=self.pos[0], column=self.pos[1])

    '''
    Check if a tile is at the correct positon
    '''
    def is_correct_pos(self):
        return self.pos == self.curpos

class Board(Frame):
    MAX_BOARD_SIZE = 2000
    def __init__(self,parent,image,grid,win):
        Frame.__init__(self,parent)
 
        self.parent = parent 
        self.image = self.open_image(image)
        self.grid = grid 
        self.win = win
        self.tileSize = self.image.size[0]/self.grid
        self.tiles = self.create_tiles()
        self.tiles.shuffle()
        self.tiles.show()
        self.bind_keys()

    def open_image(self,image):
        im = Image.open(image)

        #if image is larger than maximum board size crop it
        if min(im.size) > self.MAX_BOARD_SIZE:
            im = im.resize((self.MAX_BOARD_SIZE,self.MAX_BOARD_SIZE),Image.ANTIALIAS)
        
        # if image not square crop it
        if im.size[0] !=  im.size[1]:
            im= im.crop((0,0,im.size[0],im.size[0]))
        return im
    def bind_keys(self):
        self.bind_all('<Key-Up>',self.slide)
        self.bind_all('<Key-Down>',self.slide)
        self.bind_all('<Key-Right>',self.slide)
        self.bind_all('<Key-Left>',self.slide)
    
    def slide(self,event):
        self.tiles.slide(event.keysym)
        if self.tiles.is_correct():
            print("tile is correct")
            self.win(self.tiles.moves)
    

    
    def create_tiles(self):
        tiles = Tiles(self.grid)
        for row in range(self.grid):
            for col in range(self.grid):
                x0 = row*self.tileSize 
                y0 = col*self.tileSize 
                x1 = x0 + self.tileSize 
                y1 = y0 + self.tileSize
                tileImage = ImageTk.PhotoImage(self.image.crop((x0,y0,x1,y1)))
                tile = Tile(self,tileImage,(row,col))
                tiles.add(tile)
        tiles.set_gap(-1)
        return tiles




class Main():
    def __init__(self,parent):
        self.parent = parent 
        self.image = StringVar()
        self.winText = StringVar()
        self.grid = IntVar()
        self.create_main_frame()

    def create_main_frame(self):
        #create main frame and labels and buttons
        self.mainFrame  = Frame(self.parent,background='Rosy Brown1')
        Label(self.mainFrame,text='N-Puzzle Game and AI', font=("Courier", 40, "bold"), fg='Pale Violet Red3',background='Rosy Brown2').pack(padx=10, pady=10)
        frame = Frame(self.mainFrame,background='Rosy Brown1')
        Entry(frame,textvariable=self.image, width=50).grid(row=1, column=1, padx=10, pady=10, sticky=W)
        Button(frame, text='Choose Image', command=self.browse).grid(row=0,column=2,pady=10,padx=10)
        OptionMenu(frame,self.grid,*[3,4,5]).grid(row=1,column=1,padx=10,pady=10,sticky=W)
        frame.pack()
        Button(self.mainFrame,text='Let\'s Play!',  command=self.start).pack(padx=10,pady=10)
        Button(self.mainFrame, text='Get AI Solution A*', command=self.play_ai_ast).pack(padx=10,pady=10)
        Button(self.mainFrame, text='Get AI Solution BFS', command=self.play_ai_bfs).pack(padx=10,pady=10)
        Button(self.mainFrame, text='Get AI Solution DFS', command=self.play_ai_dfs).pack(padx=10,pady=10)
        self.mainFrame.pack()

        #create board frame after the game has started
        self.board = Frame(self.parent)

        #create win frame
        self.winFrame = Frame(self.parent, background='Rosy Brown1')
        Label(self.winFrame, textvariable=self.winText, font=("Courier", 40, "bold"), fg='Pale Violet Red3',background='Rosy Brown2').pack(padx=10,pady=10)
        Button(self.winFrame,text='Play Again', command=self.play_again).pack(padx=10,pady=10)
        Button(self.winFrame, text='Get AI Solution A*', command=self.play_ai_ast).pack(padx=10,pady=10)
        Button(self.winFrame, text='Get AI Solution BFS', command=self.play_ai_bfs).pack(padx=10,pady=10)
        Button(self.winFrame, text='Get AI Solution DFS', command=self.play_ai_dfs).pack(padx=10,pady=10)

    def start(self):
        image = self.image.get()
        grid = self.grid.get()
        if os.path.exists(image):
            self.board = Board(self.parent,image,grid,self.win)
            self.mainFrame.pack_forget()
            self.board.pack()

    def browse(self):
        self.image.set(filedialog.askopenfilename(title="Select Image", filetype=(("png File","*.png"),("jpg File","*.jpg"))))

    def win(self,moves):
        self.board.pack_forget()
        self.winText.set('You win with {} moves!'.format(moves))
        self.winFrame.pack()

    def play_again(self):
        self.winFrame.pack_forget()
        self.mainFrame.pack()

    def play_ai_ast(self):
        game = str([1,3,5,0,4,2,6,7,8]).replace('[','').replace(']','')
        os.system('python puzzle.py ast 1,3,5,0,4,2,6,7,8')
        f = open('output.txt','r')
        newWindow = Toplevel(self.mainFrame)
        Label(newWindow,text='A* solution for N-Puzzle Game', font=("Courier", 20, "bold"), fg='Pale Violet Red3').pack(padx=10, pady=10)
        Label(newWindow,text=f.read(), font=("Courier", 10), fg='Pale Violet Red3').pack(padx=10, pady=10)

    def play_ai_bfs(self):
        game = str([1,3,5,0,4,2,6,7,8]).replace('[','').replace(']','')
        os.system('python puzzle.py bfs 1,3,5,0,4,2,6,7,8')
        f = open('output.txt','r')
        newWindow = Toplevel(self.mainFrame)
        Label(newWindow,text='BFS solution for N-Puzzle Game', font=("Courier", 20, "bold"), fg='Pale Violet Red3').pack(padx=10, pady=10)
        Label(newWindow,text=f.read(), font=("Courier", 10), fg='Pale Violet Red3').pack(padx=10, pady=10)

    def play_ai_dfs(self):
        game = str([1,3,5,0,4,2,6,7,8]).replace('[','').replace(']','')
        os.system('python puzzle.py dfs 1,3,5,0,4,2,6,7,8')
        f = open('output.txt','r')
        newWindow = Toplevel(self.mainFrame)
        Label(newWindow,text='DFS solution for N-Puzzle Game', font=("Courier", 20, "bold"), fg='Pale Violet Red3').pack(padx=10, pady=10)
        Label(newWindow,text=f.read(), font=("Courier", 10), fg='Pale Violet Red3').pack(padx=10, pady=10)


if __name__ == '__main__':
    root = Tk()
    Main(root)
    root.mainloop()