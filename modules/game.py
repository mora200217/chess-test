from random import randint
from .board import Board
from .square import Square


import os
import sys
import signal
import re
from string import ascii_uppercase
from time import time
from random import randint
import argparse
import select

class Game(object):
  board = None
  user_white = None
  user_black = None  
  CurrentPlayer = 'white'
  Timers = {
      'white' : {
        'timer'     : 0,
        'first_run' : True,
      },
      'black' : {
        'timer'     : 0,
        'first_run' : True,
      }
    }

  def __init__(self):
    '''
    Game object model    
    '''
    ''' Randomly assign the color to a player '''
    if randint(1, 2) == 1:
      self.user_white = "Jugador 1"
      self.user_black = "Jugador 2"
    else:
      self.user_white = "Jugador 2"
      self.user_black = "Jugador 1"
    ''' Instantiate a board for our game '''
    self.board = Board()
    self.board.setup()

  def time_format(self, t, user, start_time):
    ''' Display elapsed seconds for the user in human readable format '''
    current = int(t - start_time) + self.Timers[user]['timer']
    minutes = current/60
    seconds = current - 60*minutes
    if minutes < 10:
      minutes = '0' + str(minutes)
    if seconds < 10:
      seconds = '0' + str(seconds)
    return str(minutes) + ':' + str(seconds)

  def parse_time(self, t):
    ''' Convert time from string (human readable - MM:SS) format to seconds '''
    t = t.split(':')
    return int(t[0])*60 + int(t[1])

  def start_timer(self):
    user = self.CurrentPlayer
    ''' Get the current user for displaying purposes '''
    if user == 'white':
      display_username = self.user_white
    else:
      display_username = self.user_black
    print('NOW PLAYING: %s' % display_username)
    start_time = time()
    last_sec = int(start_time)
    while True:
      t = int(time())
      ''' Check when the second has changed '''
      if t != last_sec:
        if not self.Timers[user]['first_run']:
          ''' 
          Send 5 backspaces (we assume that no game lasts more than 99:99x2) 
          to rewrite the time.
          The first_run key shows that the first time the timer is displayed 
          we must not print backspaces (we would send the cursor to the previous line).
          '''
          sys.stdout.write("\b"*5)
        if self.Timers[user]['first_run']:
          self.Timers[user]['first_run'] = False
        ''' Just pring the time '''
        sys.stdout.write(self.time_format(t, user, start_time))
        ''' 
        We must call flush() or close() in order to display 
        the buffered contents of the open file.
        '''
        sys.stdout.flush()
        last_sec = t
        ''' Request user input (with timeout) '''
        r, w, x = select.select([ sys.stdin ], [], [], 1)
        if r:
          btn = r[0].readline().strip()
          ''' Check if the user just hit "Enter" and stop the timer if so. '''
          if btn == '':
            self.Timers[user]['timer'] = int(t - start_time) + 1
            self.Timers[user]['first_run'] = True
            break

  def move_piece(self):
    user = self.CurrentPlayer
    ''' Get the move from the user input '''
    move = input(user.upper() + ' >> ')
    if move.lower() == 'quit':
      ''' Terminate the game if a player enters "quit" '''
      if user == 'white':
        display_username = self.user_white
      else:
        display_username = self.user_black
      print("%s quits" % display_username)
#       x()
    ''' Parse the move piece and its' new position '''
    try:
      piece, new_position = re.sub('\s+', '', move).split('->')
    except:
      ''' Handle any possible errors in user input by prompting for a move again '''
      return (False, 'MOVES ARE ENTERED "PIECE_SQUARE->TARGET_SQUARE" E.G. "B2->B3"',)
    piece = piece.upper()
    new_position = new_position.upper()
    piece_notation = piece
    new_position_notation = new_position
    square = self.board.Squares[new_position]
    ''' check if piece can make this move to start with '''
    piece_square = self.board.Squares[piece]
    if not piece_square.is_occupied():
      return (False, 'NO PIECE IN SQUARE',)
    piece = piece_square.get_piece()
    ''' Check if piece belongs to the user '''
    if not piece.Color == user:      
      return (False, 'PIECE BELONGS TO THE OTHER USER',)
    ''' Calculate row & column distance to new position '''
    column_diff = abs(Square.column_index(piece_notation[0]) - Square.column_index(new_position_notation[0]))
    row_diff = abs(Square.row_index(piece_notation[1]) - Square.row_index(new_position_notation[1]))
    ''' Check if the move is in straight line '''
    straight_line = ( bool(piece_notation[0] != new_position_notation[0]) + bool(piece_notation[1] != new_position_notation[1]) ) == 1
    diagonal_line = False
    if not straight_line:
      if column_diff == row_diff:
        diagonal_line = True
    ''' Check for L-shaped move (or gamma from the Greek letter Γ) '''
    gamma_move = False
    if column_diff == 2 or row_diff == 2:
      if column_diff == 2:
        if row_diff == 1:
          gamma_move = True
      if row_diff == 2:
        if column_diff == 1:
          gamma_move = True
    if gamma_move and not piece.DirectionGamma:
      return (False, 'L-SHAPED MOVES NOT PERMITTED FOR THIS PIECE',)    
    if not diagonal_line and not straight_line and not gamma_move:
      return ( False, 'ILLEGAL MOVE',)
    ''' Build the path consisting of the squares required for the move '''
    if not piece.LeapOverPiece:
      move_path = []
      min_row = min(Square.row_index(piece_notation[1]), Square.row_index(new_position_notation[1]))
      max_row = max(Square.row_index(piece_notation[1]), Square.row_index(new_position_notation[1]))
      min_col = min(Square.column_index(piece_notation[0]), Square.column_index(new_position_notation[0]))
      max_col = max(Square.column_index(piece_notation[0]), Square.column_index(new_position_notation[0]))
      ''' If movement happens in a straight line decide if move is vertical or horizontal '''
      if straight_line:
        if column_diff == 0:
          ''' Vertical move '''
          column = Square.column_index(piece_notation[0])
          for r in range(min_row + 1, max_row):
            move_path.append(Square.position(r, column))
        else:
          ''' Horizontal move '''      
          row = Square.column_index(piece_notation[1])
          for c in range(min_col + 1, max_col):
            move_path.append(Square.position(row, c))
      ''' 
      For diagonal movement we need to loop both rows and columns.
      Piece will have to cross squares where row offset equals 
      column offset from starting position.
      '''
      if diagonal_line:
        for c in range(min_col + 1, max_col):
          for r in range(min_row + 1, max_row):
            if (r - min_row) == (c - min_col):
              move_path.append(Square.position(r, c))
    ''' Check move length and reject if exceeds permitted number '''
    if not gamma_move and piece.MaxSquares > 0 and (len(move_path) + 1) > piece.MaxSquares:
      return (False, 'PIECE HAS LIMITED SQUARE NUMBER PER MOVE',)
    ''' Check if any squares in the move path are occupied '''
    for path_square in move_path:
      if self.board.Squares[path_square].is_occupied():
        return ( False, 'MOVE PATH IS BLOCKED', )
    ''' Check if the square is occupied from the same player's pieces '''
    if square.is_occupied():
      if square.get_piece().Color == user:
        return ( False, 'TARGET SQUARE ALREADY OCCUPIED WITH USER PIECE', )
    ''' Remove the piece from its current position '''
    self.board.Squares[piece_notation].set_piece(None)
    ''' Place the piece in the target square '''
    self.board.Squares[new_position_notation].set_piece(piece)
    ''' Change the player '''
    self.change_player()
    return ( True, '', )

  def change_player(self):
    ''' Perform any actions necessary to change the current player '''
    if self.CurrentPlayer == 'white':
      self.CurrentPlayer = 'black'
    else:
      self.CurrentPlayer = 'white'

  def __str__(self):
    ''' Fetch the board representation at the current state. '''
    b = str(self.board) # Get the board string representation
    l = len(b.split("\n")[0]) # find the length of the first line
    ''' 
    Use format to display the usernames centered on top and bottom respectively 
    (depending which color each player is assigned) 
    '''
    user = "{user:^%d}\n" % l     
    ''' Add usernames to the board '''
    board = user.format(user=self.user_black)
    board += b + '\n'
    board += user.format(user=self.user_white)
    return board    