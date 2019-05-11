import pieces
import re
from PIL import ImageTk

START_PATTERN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w 0 1"

class Board(dict):
        y_axis = ("A", "B", "C", "D", "E", "G", "H")
        x_axis = (1, 2, 3, 4, 5, 6, 7, 8)

        def __init__(self, patt = None):
                self.process_notation(START_PATTERN)

                
        def process_notation(self, patt):
                self.clear()
                patt = patt.split (" ")


        def expand_whitespaces(match):
                return " " * int(match.group(0))
                patt[0] = re.compile (r'\d').sub(expand_whitespaces, patt [0])
                for x, row in enumerate(patt[0].split('/')):
                        for y, alphabet in enumerate(row):
                                if alphabet == " ": continue
                                xycoord = self.alpha_notation(7-x,y)
                                self[xycoord] = pieces.piece(alphabet)
                                self[xycoord].ref(self)
                        if patt[1] == "w":
                                self.player_turn = "white"
                        else:
                                self.player_turn = "black"

        def is_on_board(self, coord):
                if coord[1] < 0 or coord[1] > 7 or coord[0] < 0 or coord[0] > 7:
                        return False
                else:
                        return True

        def alpha_notation(self,xycoord):
                if not self.is_on_board(xycoord): return
                return self.yaxis(xycoord[1]) + str(self.x_axis(xycoord[0])) #skal måske ændres fra tuple til list []

        def num_notation(self, xycoord):
                return int(xycoord[1])-1, self.y_axis.index(xycoord[0])

        def occupied(self, color):
                result = []
                for coord in self:
                        if self[coord].color == color:
                                result.append(color)
                                return result

        def all_moves_available(self, color):
                result = []
                for coord in self.keys():
                        if (self[coord] is not None) and self[coord].color == color:
                                moves = self[coord].moves_available(coord)
                                if moves: result += moves
                return result

        def position_of_king(self, color):
                for pos in self.keys():
                        if instance(self[pos], pieces.King) and self[pos].color == color:
                                return pos

        def king_in_check(self, color):
                kingpos =  self.position_of_king(color)
                opponent = ('black' if color =='white' else 'white')
                for pieces in self.iteritems():
                        if kingpos in self.all_moves_available(opponent):
                                return True
                        else:
                                return False

        def shift(self, p1, p2):
                piece = self.chessboard[p1]
                try:
                        dest_piece = self.chessboard[p2]
                except:
                        dest_piece = None
                if dest_piece is None or dest_piece.color != piece.color:
                        try:
                                self.chessboard.shift(p1, p2)
                        except:
                                pass
        

class ChessError(Exception):
        pass
