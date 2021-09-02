
class Piece(object):
  '''
  Object model of a chess piece
  
  We keep information on what kind of movements the piece is able to make (straight, diagonal, gamma),
  how many squares it can cross in a single move, its type (of course) and the color (white or black).     
  '''
  DirectionDiagonal = False
  DirectionStraight = False
  DirectionGamma = False
  LeapOverPiece = False
  MaxSquares = 0
  Color = None
  Type = None
  AvailableTypes = [ 'Rook', 'Knight', 'Pawn', 'King', 'Queen', 'Bishop' ]
  Types_Direction_Map = {
      'Rook'   : [ 'straight' ],
      'Knight' : [ 'gamma' ],
      'Pawn'   : [ 'straight' ],
      'King'   : [ 'straight', 'diagonal' ],
      'Queen'  : [ 'straight', 'diagonal' ],
      'Bishop' : [ 'diagonal' ]
    }
  Types_MaxSquares_Map = {
    'Rook'   : 0,
    'Pawn'   : 1,
    'King'   : 1,
    'Queen'  : 0,
    'Bishop' : 0,
    'Knight' : -1,
  }

  def __init__(self, **kwargs):
    self.Type = kwargs['Type']
    if not self.Type in self.AvailableTypes:
      raise Exception('Unknown Piece Type')
      x(1)
    self.Color = kwargs['Color']
    directions = self.Types_Direction_Map[self.Type]
    self.DirectionDiagonal = 'diagonal' in directions
    self.DirectionGamma = 'gamma' in directions
    self.DirectionStraight = 'straight' in directions
    self.MaxSquares = self.Types_MaxSquares_Map[self.Type]
    if self.Type == 'Knight':
      self.LeapOverPiece = True

  def __str__(self):
    return self.Color[0].lower() + self.Type[0].upper()