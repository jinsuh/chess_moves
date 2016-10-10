from abc import ABCMeta, abstractmethod

"""
Give all the possible moves from one player based on board information and whose turn it is
Piece classes give possible moves from each piece
Board info is a dictionary with keys, 'P1' and 'P2'
Values are the pieces each player has

Moves do not take into account castling or checks
"""

class Move(object):
	"""Move class"""
	def __init__(self, piece, position):
		self.piece = piece
		self.position = position

	def __str__(self):
		return str(self.piece) + str(self.position)


class Piece:
	__metaclass__ = ABCMeta

	""" Piece class (Abstract) """
	def __init__(self, position):
		self.position = position

	@abstractmethod
	def __str__(self):
		""" Convert to string for readability """

	@abstractmethod
	def getPossibleMoves(self, boardSize, isP1Piece):
		""" Get all possible moves from this piece """

	""" Check if piece position is out of bounds """
	def outOfBounds(self, checkPosition, boardSize):
		return (checkPosition[0] >= boardSize or checkPosition[0] < 0
			or checkPosition[1] >= boardSize or checkPosition[1] < 0)

	""" Check if colliding with p1 or p2 pieces """
	def hasCollision(self, checkPosition, boardInfo, checkP1Piece):
		if checkP1Piece:
			piecesToCheck = boardInfo['P1']
		else:
			piecesToCheck = boardInfo['P2']
		for i in xrange(len(piecesToCheck)):
			piece = piecesToCheck[i]
			if (piece.position == checkPosition):
				return True
		return False

	"""Make sure move is valid"""
	def isValidMove(self, checkPosition, boardInfo, isP1Piece):
		return not (self.outOfBounds(checkPosition, boardInfo['boardSize']) or self.hasCollision(checkPosition, boardInfo, isP1Piece))

	"""
	Iterate through positions and add as possible move if valid
	Positions are to be in a line
	Stopped if blocked by own pieces or if capturing an enemy piece
	"""
	def setPossiblePositions(self, positions, boardInfo, isP1Piece):
		possibleMoves = []
		for i in xrange(len(positions)):
			if not self.isValidMove(positions[i], boardInfo, isP1Piece):
				break
			else:
				possibleMoves.append(Move(self, positions[i]))
				if (self.hasCollision(positions[i], boardInfo, not isP1Piece)):
					break;
		return possibleMoves

	"""
	Iterates through all positions and add as possible move if valid
	Does not stop if blocked by own pieces
	"""
	def setPossiblePositionsNoBlocking(self, positions, boardInfo, isP1Piece):
		possibleMoves = []
		for i in xrange(len(positions)):
			if self.isValidMove(positions[i], boardInfo, isP1Piece):
				possibleMoves.append(Move(self, positions[i]))
		return possibleMoves


class King(Piece):
	def __str__(self):
		return 'K'

	""" Checks neighboring spaces """
	def getPossibleMoves(self, boardInfo, isP1Piece):
		possibleMoves = []
		checkMoves = [(self.position[0] + row, self.position[1] + col) for row in xrange(-1, 2) for col in xrange(-1, 2) if not ((row == 0) and col == 0)]
		return self.setPossiblePositionsNoBlocking(checkMoves, boardInfo, isP1Piece)


class Queen(Piece):
	def __str__(self):
		return 'Q'

	""" Checks union of Bishop + Rook moves """
	def getPossibleMoves(self, boardInfo, isP1Piece):
		b = Bishop(self.position)
		possibleMoves = b.getPossibleMoves(boardInfo, isP1Piece)
		r = Rook(self.position)
		possibleMoves.extend(r.getPossibleMoves(boardInfo, isP1Piece))
		possibleMoves[:] = [Move(self, st.position) for st in possibleMoves]
		return possibleMoves

class Bishop(Piece):
	def __str__(self):
		return 'B'

	""" Checks diagonal lines """
	def getPossibleMoves(self, boardInfo, isP1Piece):
		boardSize = boardInfo['boardSize']
		possibleMoves = []

		upperRightPositions = [(self.position[0] + i, self.position[1] + i) for i in xrange(1, boardSize)]
		possibleMoves.extend(self.setPossiblePositions(upperRightPositions, boardInfo, isP1Piece))

		upperLeftPositions = [(self.position[0] - i, self.position[1] + i) for i in xrange(1, boardSize)]
		possibleMoves.extend(self.setPossiblePositions(upperLeftPositions, boardInfo, isP1Piece))

		lowerRightPositions = [(self.position[0] + i, self.position[1] - i) for i in xrange(1, boardSize)]
		possibleMoves.extend(self.setPossiblePositions(lowerRightPositions, boardInfo, isP1Piece))

		lowerLeftPositions = [(self.position[0] - i, self.position[1] - i) for i in xrange(1, boardSize)]
		possibleMoves.extend(self.setPossiblePositions(lowerLeftPositions, boardInfo, isP1Piece))

		return possibleMoves

class Knight(Piece):
	def __str__(self):
		return 'N'

	""" Checks all possible L moves """
	def getPossibleMoves(self, boardInfo, isP1Piece):
		possibleMoves = []
		boardSize = boardInfo['boardSize']
		toCheckPositions = []
		toCheckPositions.extend([(self.position[0] + 1, self.position[1] + 2),
			(self.position[0] + 2, self.position[1] + 1),
			(self.position[0] + 1, self.position[1] - 2),
			(self.position[0] + 2, self.position[1] - 1),
			(self.position[0] - 1, self.position[1] + 2),
			(self.position[0] - 2, self.position[1] + 1),
			(self.position[0] - 1, self.position[1] - 2),
			(self.position[0] - 2, self.position[1] - 1)])

		return self.setPossiblePositionsNoBlocking(toCheckPositions, boardInfo, isP1Piece)	

class Rook(Piece):
	def __str__(self):
		return 'R'

	""" Checks each horizontal/vertical line movement """
	def getPossibleMoves(self, boardInfo, isP1Piece):
		
		boardSize = boardInfo['boardSize']
		possibleMoves = []

		right = [(self.position[0] + i, self.position[1]) for i in xrange(1, boardSize)]
		possibleMoves.extend(self.setPossiblePositions(right, boardInfo, isP1Piece))

		left = [(self.position[0] - i, self.position[1]) for i in xrange(1, boardSize)]
		possibleMoves.extend(self.setPossiblePositions(left, boardInfo, isP1Piece))

		up = [(self.position[0], self.position[1] + i) for i in xrange(1, boardSize)]
		possibleMoves.extend(self.setPossiblePositions(up, boardInfo, isP1Piece))

		down = [(self.position[0], self.position[1] - i) for i in xrange(1, boardSize)]
		possibleMoves.extend(self.setPossiblePositions(down, boardInfo, isP1Piece))
		return possibleMoves

class Pawn(Piece):
	def __str__(self):
		return ''

	""" Check forward movements and also diagonal attacking moves """
	def getPossibleMoves(self, boardInfo, isP1Piece):
		
		# Determine if moving forward or "backwards" depending on player 1 or player 2
		if (isP1Piece):
			displacement = 1
		else:
			displacement = -1
		forwardPositions = [(self.position[0], self.position[1] + displacement)]

		# add forward 2-move if starting position
		if (self.startingPosition(isP1Piece, boardInfo)):
			forwardPositions.append((self.position[0], self.position[1] + (displacement * 2)))

		#iterate through possibilities	
		possibleMoves = self.setPossiblePositions(forwardPositions, boardInfo, isP1Piece)

		#add diagonal positions to check
		diagonalPositions = [(self.position[0] + displacement, self.position[1] + displacement),
			(self.position[0] - displacement, self.position[1] + displacement)]

		#check if enemy piece is on diagonal position
		for position in diagonalPositions:
			if (self.hasCollision(position, boardInfo, not isP1Piece)):
				possibleMoves.append(str(self) + str(position))
		return possibleMoves

	""" Check if pawn is at starting position """
	def startingPosition(self, isP1Piece, boardInfo):
		
		if (isP1Piece):
			return self.position[1] == 1
		else:
			return self.position[1] == boardInfo['boardSize'] - 2


	""" Checks if there is no collision with any piece """
	def isValidMove(self, checkPosition, boardInfo, isP1Piece):
		return not (self.outOfBounds(checkPosition, boardInfo['boardSize']) or self.hasCollision(checkPosition, boardInfo, isP1Piece)) or self.hasCollision(checkPosition, boardInfo, not isP1Piece)

	""" Checks the two forward possible positions and adds the moves if not blocked by any piece """
	def setPossiblePositions(self, positions, boardInfo, isP1Piece):
		possibleMoves = []
		for i in xrange(len(positions)):
			if not self.isValidMove(positions[i], boardInfo, isP1Piece):
				break
			else:
				possibleMoves.append(Move(self, positions[i]))
		return possibleMoves

""" Iterate through all of players pieces and get all possible moves """
def getAllPossibleMoves(boardInfo, isFirstPlayer):
	if isFirstPlayer:
		pieces = boardInfo['P1']
	else:
		pieces = boardInfo['P2']
	moves = []
	for piece in pieces:
		moves.extend(piece.getPossibleMoves(boardInfo, isFirstPlayer))
	return moves
