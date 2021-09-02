from modules.game import Game


if __name__ == '__main__':
  game = Game()
  print(game)
  # Game 
  while True:
    # game.start_timer()
    move_legal, message = game.move_piece()

    # Es legal ? 
    if move_legal:
      print(game  )
    else:
      print('%s, PLEASE PLAY AGAIN' % (message,))
  

