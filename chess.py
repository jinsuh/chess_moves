from abc import ABCMeta, abstractmethod

class Piece:
	__metaclass__ = ABCMeta

	def __init__(self, position):
		self.position = position

	@abstractmethod
	def __str__(self):
		pass

	@abstractmethod
	def getPossibleMoves(self, boardSize, isP1Piece):
		pass

	def outOfBounds(self, checkPosition, boardSize):
		"""Check if piece position is out of bounds"""
		return (checkPosition[0] >= boardSize or checkPosition[0] < 0
			or checkPosition[1] >= boardSize or checkPosition[1] < 0)

	def hasCollision(self, checkPosition, boardInfo, checkP1Piece):
		"""Check if colliding with p1 or p2 pieces"""
		if checkP1Piece:
			piecesToCheck = boardInfo['P1']
		else:
			piecesToCheck = boardInfo['P2']
		for i in xrange(len(piecesToCheck)):
			piece = piecesToCheck[i]
			if (piece.position == checkPosition):
				return True
		return False

	def isValidMove(self, checkPosition, boardInfo, isP1Piece):
		return not (self.outOfBounds(checkPosition, boardInfo['boardSize']) or self.hasCollision(checkPosition, boardInfo, isP1Piece))

	def setPossiblePositions(self, positions, boardInfo, isP1Piece):
		"""Iterate through positions and add as possible move if valid
		Positions are to be in a line
		Stopped if blocked by own pieces or if capturing an enemy piece
		"""
		possibleMoves = []
		for i in xrange(len(positions)):
			if not self.isValidMove(positions[i], boardInfo, isP1Piece):
				break
			else:
				possibleMoves.append(str(self) + str(positions[i]))
				if (self.hasCollision(positions[i], boardInfo, not isP1Piece)):
					break;
		return possibleMoves

	def setPossiblePositionsNoBlocking(self, positions, boardInfo, isP1Piece):
		"""Iterates through all positions and add as possible move if valid
		Does not stop if blocked by own pieces
		"""
		possibleMoves = []
		for i in xrange(len(positions)):
			if self.isValidMove(positions[i], boardInfo, isP1Piece):
				possibleMoves.append(str(self) + str(positions[i]))
		return possibleMoves


class King(Piece):
	def __str__(self):
		return 'K'

	def getPossibleMoves(self, boardInfo, isP1Piece):
		possibleMoves = []
		checkMoves = [(self.position[0] + row, self.position[1] + col) for row in xrange(-1, 2) for col in xrange(-1, 2) if not ((row == 0) and col == 0)]
		return self.setPossiblePositionsNoBlocking(checkMoves, boardInfo, isP1Piece)


class Queen(Piece):
	def __str__(self):
		return 'Q'

	def getPossibleMoves(self, boardInfo, isP1Piece):
		""" Union of Bishop and Rook moves """
		b = Bishop(self.position)
		possibleMoves = b.getPossibleMoves(boardInfo, isP1Piece)
		r = Rook(self.position)
		possibleMoves.extend(r.getPossibleMoves(boardInfo, isP1Piece))
		possibleMoves[:] = [str(self) + st[1:] for st in possibleMoves]
		return possibleMoves

class Bishop(Piece):
	def __str__(self):
		return 'B'

	def getPossibleMoves(self, boardInfo, isP1Piece):
		""" Checks each diagonal line """
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

	def getPossibleMoves(self, boardInfo, isP1Piece):
		""" Checks all possible L moves """
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

	def getPossibleMoves(self, boardInfo, isP1Piece):
		""" Checks each horizontal/vertical line movement """
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

	def getPossibleMoves(self, boardInfo, isP1Piece):
		"""Check forward movements and also diagonal attacking moves"""
		
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

	def startingPosition(self, isP1Piece, boardInfo):
		"""Check if pawn is at starting position"""
		if (isP1Piece):
			return self.position[1] == 1
		else:
			return self.position[1] == boardInfo['boardSize'] - 2


	def isValidMove(self, checkPosition, boardInfo, isP1Piece):
		"""Checks if there is no collision with any piece"""
		return not (self.outOfBounds(checkPosition, boardInfo['boardSize']) or self.hasCollision(checkPosition, boardInfo, isP1Piece)) or self.hasCollision(checkPosition, boardInfo, not isP1Piece)

	def setPossiblePositions(self, positions, boardInfo, isP1Piece):
		"""Checks the two forward possible positions and adds the moves if not blocked by any piece"""
		possibleMoves = []
		for i in xrange(len(positions)):
			if not self.isValidMove(positions[i], boardInfo, isP1Piece):
				break
			else:
				possibleMoves.append(str(self) + str(positions[i]))
		return possibleMoves

def getAllPossibleMoves(boardInfo, isFirstPlayer):
	"""Iterate through all of players pieces and get all possible moves"""
	if isFirstPlayer:
		pieces = boardInfo['P1']
	else:
		pieces = boardInfo['P2']
	moves = []
	for piece in pieces:
		moves.extend(piece.getPossibleMoves(boardInfo, isFirstPlayer))
	return moves
