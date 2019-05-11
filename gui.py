from tkinter import *
from PIL import ImageTk
import pieces
import chessboard


#self.color1 = self.white
#self.color2 = self.black
class GUI():
        rows = 8
        columns = 8
        white = "#FFFFFF"
        black = "#00ACA0"
        dim_square = 64
        pieces = {}
        selected_piece = None
        focused = None

        def __init__(self, parent):
                self.parent = parent
                canvas_width = self.columns * self.dim_square
                canvas_height = self.rows * self.dim_square
                self.canvas = Canvas(parent, width = canvas_width, height=canvas_height, background="grey")
                self.canvas.pack(padx=8, pady=8)
                self.draw_board()
                self.canvas.bind("<Button-1>", self.square_clicked)

        highlightcolor = "khaki"
        def draw_board(self):
                color = self.white
                for r in range(self.rows):
                        #color = self.white
                        if color == self.white:
                                color = self.black

                        else:
                                color = self.white #skifter mellem de to farver på brættet
                                                                
                        for c in range(self.columns):
                                x1 = (c * self.dim_square)
                                y1 = ((7-r) * self.dim_square)
                                x2 = x1 + self.dim_square
                                y2 = y1 + self.dim_square
                                if(self.focused is not None and (row, col) in self.focused):
                                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.highlightcolor, tags="area")
                                else:
                                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="area")
                                if color == self.white:
                                        color = self.black
                                else:
                                        color = self.white

                for name in self.pieces:
                        self.pieces[name] = (self.pieces[name][0], self.pieces[name][1])
                        x0 = (self.pieces[name][1] * self.dim_square) + int(self.dim_square/2)
                        y0 = ((7-self.pieces[name][0]) * self.dim_square) + int(self.dim_square/2)
                        self.canvas.coords(name, x0, y0)
                self.canvas.tag_raise("occupied")
                self.canvas.tag_lower("area")


                                        
        
        def draw_pieces(self):
                self.canvas.delte("occupied")
                for xycoord, piece in self.chessboard.iteritems():
                        x,y = self.chessboard.num_notation(xycoord)
                        if piece is not None:
                                filename = "{}{}.png".format(piece.shortname.lower(), piece.color)
                                piecename = "{}{}{}".format(piece.shortname, x, y)
                                if (filename not in self.images):
                                        self.images[filename] = ImageTk.PhotoImage(file = filename)
                                        self.canvas.create_image(0,0,image = self.images[filename], tags = (piecename, "occupied"), anchor = "c")
                                        x0 = (y * self.dim_square) + int(self.dim_square/2)
                                        y0 = ((7-x) * self.dim_square) + int(self.dim_square/2)
                                        self.canvas.coords(piecename, x0, y0)
#        def draw_board(self):
 #               color = self.black
  #              for row in range(self.rows):
   #                     if color == self.white:
    #                            color = self.black
#
 #                       else:
  #                              color = self.white
   #                     for col in range(self.columns):
    #                            x1 = (col * self.dim_square)
     #                           y1 = ((7-row) * self.dim_square)
      #                          x2 = x1 + self.dim_square
       #                         y2 = y1 + self.dim_square
                                #if(self.focused is not None and (row, col) in self.focused):
                                 #       self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.highlightcolor, tags="area")
                                #else:
                                 #       self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="area")
        #                        if color == self.white:
         #                               color = self.black
          #                      else:
           #                             color = self.white
            #    for name in self.pieces:
             #           self.pieces[name] = (self.pieces[name][0], self.pieces[name][1])
              #          x0 = (self.pieces[name][1] * self.dim_square) + int(self.dim_square/2)
               #         y0 = ((7-self.pieces[name][0]) * self.dim_square) + int(self.dim_square/2)
                #        self.canvas.coords(name, x0, y0)
                #self.canvas.tag_raise("occupied")
                #self.canvas.tag_lower("area")

        

                                        
        def show(self, pat):
                self.clear()
                pat = pat.split(" ")
                def expand(match):
                        return " " * int(match.group(0))
                pat[0] = re.compile(r"/d").sub(expand, pat[0])
                for x, row in enumerate(pat[0].split("/")):
                        for y, letter in enumerate(row):
                                if letter == " ":
                                        continue
                                coord = self.alpha_notation((7-x,y))
                                self[coord] = pieces.create_pice(letter)
                                self[coord].place(self)
                if pat[1] == "w":
                        self.player_turn = "white"
                else:
                        self.player_turn = "black"
                self.halfmove_clock = int(pat[2])
                self.fullmove_number = int(pat[3])

        def square_clicked(self, event):
                col_size = row_size = self.dim_square
                selected_column = event.x / col_size
                selcted_row = 7 - (event.y / row_size)
                pos = self.chessboard.alpha_notation(selected_row, selected_column)
                try:
                        piece = self.chessboard[pos]
                except:
                        pass
                if self.selected_piece:
                        self.shift(self.selected_piece[1], pos)
                        self.selected_piece = None
                        self.focues = None
                        self.pieces = {}
                        self.draw_board()
                        self.draw_pieces()
                self.focus(pos)
                self.draw_board

        def focus(self, pos):
                try:
                        piece = self.chessboard[pos]
                except:
                        piece = None
                if piece is not None and (piece.color == self.chessboard.player_turn):
                        self.selected_piece = (self.chessboard[pos], pos)
                        self.focused = map(self.chessboard.num_notation, (self.chessboard[pos].moves_available(pos)))
                        
                                        

def main():
        root = Tk()
        root.title("Chess")
        gui = GUI(root)
        root.mainloop()
if __name__ == "__main__":
        main()
