from TicTacToe import Game
user = input('Who would you like to be?(X always starts first)\t')
while user.upper() != 'X' and user.upper() != 'O':
	user = input('Sorry! We only accept X or O.\nWho would you like to be?\t')
g = Game('X',user)
g.play()