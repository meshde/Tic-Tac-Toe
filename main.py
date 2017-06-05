from TicTacToe import Game
from TicTacToe import User
from TicTacToe import RandomPlayer
from TicTacToe import QPlayer
from TicTacToe import MiniMax
first = input('Who plays first?(X or O)\t')
while first.upper() != 'X' and first.upper() != 'O':
	first = input('Sorry! We only accept X or O.\nWho would you like to be?\t')
g = Game(first)
u = User('O')
cpu = MiniMax('O')
q = QPlayer('X')
g.trainQ(q,cpu)
enough = 'N'
while enough != 'Y':
	g.play(u,q)
	enough = input('Had enough?(Y/N)')
#g.play(u,cpu)