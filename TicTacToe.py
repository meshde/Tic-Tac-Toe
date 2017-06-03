import os
class State(object):
	"""Each State Represents a state of the game(a particular configuration of X's and O's in the game)"""
	def __init__(self,player,mat=None,rem=9):
		if not mat:
			""" '-' represents an unmarked cell
				if no matrix is provided in the constructor, initialise a blank matrix"""
			self.matrix = [['-']*3 for z in range(3)]
		else:
			self.matrix = mat
		# The player attribute represents the player (X or O) whose chance it is to play in the current state
		self.player = player
		# The chosen attribute represents the best possible move the current player can make 
		self.chosen = None
		# The children attribute represnets the list of possible moves the current player can make
		self.children = []
		# The points attrubute represents the points that the player can get by choosing to play the move that leads to this state
		self.points = None
		# The remaining attribute specifies the no of blank cells left in this state
		self.remaining = rem
		# The winner attribute specifies the winner in the current state, if any
		self.winner = 0
	def get_other_player(self):
		if self.player == 'X':
			return 'O'
		return 'X'
	def generate(self):
		""" This function is used to generate the state space subtree of the game with the current state as root """
		for i,x in enumerate(self.matrix):
			for j,y in enumerate(x):
				if y == '-':
					# The following line copies the matrix of the state into another variable
					mat = [[w for w in z] for z in self.matrix]
					# The current player makes a move 
					mat[i][j] = self.player
					# Create a child node with the new matrix mat
					child = State(self.get_other_player(),mat,self.remaining-1)
					# Recursively generate the children of the child node
					child.generate()
					# Add the child node to the children list
					self.children.append(child)
	def is_over(self):
		if self.get_winner():
			return True
		return self.remaining == 0
	def get_winner(self):
		m = self.matrix
		if self.winner != 0:
			""" If winner already computed, simply return the winner. Value of 0 was the default value, meaning winner if this state was not computed """
			return self.winner 
		for x in ['X','O']:
			if m[0][0] == x and m[0][1] == x and m[0][2] == x:
				self.winner = x
				return x
			if m[1][0] == x and m[1][1] == x and m[1][2] == x:
				self.winner = x
				return x
			if m[2][0] == x and m[2][1] == x and m[2][2] == x:
				self.winner = x
				return x
			if m[0][0] == x and m[1][0] == x and m[2][0] == x:
				self.winner = x
				return x
			if m[0][1] == x and m[1][1] == x and m[2][1] == x:
				self.winner = x
				return x
			if m[0][2] == x and m[1][2] == x and m[2][2] == x:
				self.winner = x
				return x
			if m[0][0] == x and m[1][1] == x and m[2][2] == x:
				self.winner = x
				return x
			if m[2][0] == x and m[1][1] == x and m[0][2] == x:
				self.winner = x
				return x
		""" No winner in this state """
		self.winner = None
		return None
	def get_points(self):
		""" This is the minimax algo """
		if self.points:
			""" If points already computed, directly return value """
			return self.points
		#print('Points for:')
		#self.print_state()
		#print(self.children)
		if self.is_over():
			winner = self.get_winner()
			if winner == None:
				return 0
			if winner == 'X':
				"""The game is assumed to be rooted for player X. 
					So if player X wins, he receives +10 points and if he loses he recieves -10 points or loses 10 points """
				return 10
			return -10
		if self.player == 'X':
			""" Player X would want to choose the child that gives him the maximum points """
			maxi = None
			chosen = None
			for child in self.children:
				if maxi == None or maxi < child.get_points():
					#print('Here')
					maxi = child.get_points()
					chosen = child
			self.chosen = chosen
			self.points = maxi
		else:
			""" Player O would want to choose a child that minimises X's points (since the game is rooted for X) """
			mini = None
			chosen = None
			for child in self.children:
				if mini == None or mini > child.get_points():
					mini = child.get_points()
					chosen = child
			self.chosen = chosen
			self.points = mini
		return self.points
	def is_same(self,mat):
		return self.matrix == mat
	def get_child(self,mat):
		for child in self.children:
			if child.is_same(mat):
				return child
		return None
	def get_matrix(self):
		return self.matrix
	def get_player(self):
		return self.player
	def get_chosen(self):
		return self.chosen
	def print_state(self):
		os.system('cls')
		print('\t \t|\t \t|\t \t')
		print('\t'+str(self.matrix[0][0])+'\t|\t'+str(self.matrix[0][1])+'\t|\t'+self.matrix[0][2]+'\t')
		print('\t \t|\t \t|\t \t')
		print('------------------------------------------------')
		print('\t \t|\t \t|\t \t')
		print('\t'+str(self.matrix[1][0])+'\t|\t'+str(self.matrix[1][1])+'\t|\t'+self.matrix[1][2]+'\t')
		print('\t \t|\t \t|\t \t')
		print('------------------------------------------------')
		print('\t \t|\t \t|\t \t')
		print('\t'+str(self.matrix[2][0])+'\t|\t'+str(self.matrix[2][1])+'\t|\t'+self.matrix[2][2]+'\t')
		print('\t \t|\t \t|\t \t')

class Game(object):
	def __init__(self,player,user):
		self.state = State(player)
		self.state.generate()
		self.state.get_points()
		#while self.state.get_chosen() != None:
		#	self.state = self.state.get_chosen()
		#	self.state.print_state()
		#print(self.state.get_chosen())

		# The map attribute is used for user input. The user is asked to enter a number from 1 to 9 where 1 represents cell (0,0), 2 represents cell (0,1), 3 represents cell (0,2) and so on
		self.map = [None,(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
		self.user = user
	def get_state_from_user(self):
		u = int(input('Enter the index of the block:\t'))
		mat = [[w for w in z] for z in self.state.get_matrix()]
		x,y = self.map[u]
		mat[x][y] = self.user
		return self.state.get_child(mat)
	def play(self):
		while not self.state.is_over():
			self.state.print_state()
			if self.state.get_player() == self.user:
				self.state = self.get_state_from_user()
			else:
				print('CPU made a move')
				self.state = self.state.get_chosen()
		self.state.print_state()
		win = self.state.get_winner()
		if not win:
			print('DRAW')
		elif self.user == win:
			print('You Won!')
		else:
			print('You Lost!')