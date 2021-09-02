from .square import Square
from .piece import Piece

class Board(object):
  '''
  Object model of the board

  Described by a dictionary (Squares) which keys are square positions 
  in their string representations (e.g. A1),
  and values the corresponding Square instances.
  '''
  Squares = {}
  ''' 
  The initial setup of the board. 
  The way that the setup is given makes it easier to 
  implement "Save Game" & "Load Game" features.
  '''
  Setup = {
      'Pawn'   : 'A2:H2|A7:H7',
      'Rook'   : 'A1,H1|A8,H8',
      'Bishop' : 'C1,F1|C8,F8',
      'Knight' : 'B1,G1|B8,G8',
      'King'   : 'E1|E8',
      'Queen'  : 'D1|D8',
    }  

  def __init__(self):
    ''' Simply construct the 64 squares '''
    for i in range(8):
      for j in range(8):
        self.Squares[Square.position(i, j)] = Square(i, j)

  def setup(self):
    ''' 
    Setup our board by assigning pieces to the squares!
    A separate method makes it easier to implement
    "Save" & "Load" features
    '''
    for piece_type, piece_range in self.Setup.items():
      white, black = piece_range.split('|')
      for p in self.__parse_range(white):
        self.add_piece('white', piece_type, p[0], p[1])
      for p in self.__parse_range(black):
        self.add_piece('black', piece_type, p[0], p[1])
 
  def __parse_range(self, r):
    '''
    Parse setup ranges (from the Setup dictionary) 
    and return a list of tuples with the square coordinates 
    to be assigned to the piece type.
    '''
    ''' Check if distinct positions are given '''
    distinct = not ( ':' in r )
    separator = None
    if ':' in r:
      separator = ':'
    elif ',' in r:
      separator = ','
    ''' Distinct and single position (e.g. Queens) have essentially the same implementation '''
    if separator is None:
      r = [ r ]
    else:
      r = r.split(separator)
    if distinct:
      return [ ( Square.row_index(p[1]), Square.column_index(p[0]), ) for p in r ]
    else:
      ''' Find starting-ending rows & columns for this range '''
      start_column = Square.column_index(r[0][0])
      stop_column = Square.column_index(r[1][0])
      start_row = Square.row_index(r[0][1])
      stop_row = Square.row_index(r[1][1])
      r = []
      if ( stop_column - start_column ) > 0:
        for column in range(start_column, stop_column - start_column + 1):
          r.append( ( start_row, column, ) )
      elif ( stop_row - start_row ) > 0:
        for row in range(start_row, stop_row - start_row + 1):
          r.append( ( row, start_column, ) )
      return r
  
  def add_piece(self, color, piece_type, row, column):    
    ''' Add a piece to a square in the board '''
    self.Squares[Square.position(row, column)].set_piece(Piece(Type=piece_type, Color=color))

  def __str__(self):
    '''
    String representation of the board at its current state.
    '''
    column_display = '  %s  '*8 % tuple( [ Square.index_column(c) for c in list(range(8)) ] )
    board_display = "  %s\n" % (column_display,)
    board_display += '  ' + '-'*len(column_display) + "\n"
    for row in range(7, -1, -1):
      row_display = str(row + 1)
      for col in range(8):
        if self.Squares[Square.position(row, col)].is_occupied():
          piece = str(self.Squares[Square.position(row, col)].get_piece())
        else:
          piece = "  "
        row_display += '| %s ' % (piece,)
      row_display += "| %d\n" % (row + 1,)
      board_display += row_display
      board_display += '  ' + '-'*len(column_display) + "\n"
    board_display += ' ' + column_display
    return board_display
                     