   
from string import ascii_uppercase
class Square(object):
  '''
  Object model of a board square

  Requires zero-based row & column indexes.
  The Piece variable holds an instance of Piece class,
  representing a piece occupying the square.
  '''
  Row = 0
  Column = 0
  Occupied = False
  Piece = None

  def __init__(self, row, column):
    ''' Square constructor requires zero-based row & column indexes '''
    self.Row = row
    self.Column = column

  def is_occupied(self):
    ''' Returns True if the square has a piece attached to it, False otherwise '''
    return self.Occupied

  def set_piece(self, piece):
    ''' Sets the piece for a square and resets the Occupied variable accordingly '''
    if piece is None:
      self.Occupied = False
    else:
      self.Occupied = True
    self.Piece = piece

  def get_piece(self):
    ''' Getter method to return the piece attached to this square instance '''
    return self.Piece

  @staticmethod
  def row_index(row):
    ''' static method that returns the zero-based row index '''
    return int(row) - 1
  
  @staticmethod
  def column_index(col):
    ''' static method that returns the zero-based column index '''
    try:
      col = int(col) - 1
    except:
      col = ascii_uppercase.index(col)
    return col

  @staticmethod
  def index_column(col):
    ''' static method that returns the column letter from zero-based column index '''
    return ascii_uppercase[col]

  @staticmethod
  def position(row, col):
    ''' 
    static method to convert zero-indexed integer coordinates to board notation 
    e.g. (0,1) -> "B1"
    '''
    return ascii_uppercase[int(col)] + str(int(row) + 1)
        
  def __str__(self):
    ''' 
    Return a string representation of the square.
    If it is occupied then return the piece info as well.
    '''
    if self.Piece is None:
      piece = ""
    else:
      piece = str(self.Piece)
    properties = {
        'piece'  : piece,
        'row'    : self.Row + 1,
        'column' : ascii_uppercase[self.Column],
      }
    return '%(piece)s(%(column)s%(row)d)' % properties
