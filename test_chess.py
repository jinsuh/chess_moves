from chess import *
import unittest

class PieceNameTest(unittest.TestCase):

	def test_King(self):
		k = King((0,0))
		self.assertEqual(str(k), 'K')

	def test_Queen(self):
		q = Queen((0,0))
		self.assertEqual(str(q), 'Q')

	def test_Bishop(self):
		b = Bishop((0,0))
		self.assertEqual(str(b), 'B')

	def test_Knight(self):
		kn = Knight((0,0))
		self.assertEqual(str(kn), 'N')

	def test_Rook(self):
		r = Rook((0,0))
		self.assertEqual(str(r), 'R')

	def test_Pawn(self):
		p = Pawn((0,0))
		self.assertEqual(str(p), '')

class PiecePositionTest(unittest.TestCase):

	def test(self):
		k = King((0,0))
		self.assertEqual(k.position, (0, 0))
		k = King((12, 12))
		self.assertEqual(k.position, (12, 12))

class PieceOutOfBoundsTest(unittest.TestCase):

	def test(self):
		boardSize = 4
		k = King((0, 0))
		self.assertFalse(k.outOfBounds((1, 0), boardSize))
		self.assertFalse(k.outOfBounds((1, 1), boardSize))
		self.assertTrue(k.outOfBounds((-1, 0), boardSize))
		self.assertTrue(k.outOfBounds((4, 0), boardSize))

class PieceHasCollisionTest(unittest.TestCase):

	def test(self):
		boardInfo = dict()
		boardInfo['boardSize'] = 4
		k = King((0, 0))
		boardInfo['P1'] = [k]
		boardInfo['P2'] = []
		self.assertFalse(k.hasCollision((1, 0), boardInfo, True))

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		k = King((0, 0))
		q = Queen((1, 0))
		boardInfo['P1'] = [k, q]
		boardInfo['P2'] = []
		self.assertTrue(k.hasCollision((1, 0), boardInfo, True))

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		k = King((0, 0))
		q = Queen((1, 0))
		boardInfo['P1'] = [k, q]
		boardInfo['P2'] = []
		self.assertFalse(k.hasCollision((1, 0), boardInfo, False))

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		k = King((0, 0))
		q = Queen((1, 0))
		b = Bishop((2, 1))
		boardInfo['P1'] = [k, q]
		boardInfo['P2'] = [b]
		self.assertTrue(b.hasCollision((1, 0), boardInfo, True))

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		k = King((0, 0))
		q = Queen((1, 0))
		b = Bishop((2, 1))
		boardInfo['P1'] = [k, q]
		boardInfo['P2'] = [b]
		self.assertFalse(b.hasCollision((1, 0), boardInfo, False))

class PieceSetPossiblePosition(unittest.TestCase):

	def test(self):
		boardInfo = dict()
		boardInfo['boardSize'] = 4
		p = Pawn((0, 0))
		boardInfo['P1'] = [p]
		boardInfo['P2'] = []
		possibles = [(1, 0)]
		self.assertEqual(p.setPossiblePositions(possibles, boardInfo, True), ['(1, 0)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		q = Pawn((3, 0))
		boardInfo['P1'] = [p]
		boardInfo['P2'] = []
		possibles = [(4, 0)]
		self.assertEqual(p.setPossiblePositions(possibles, boardInfo, True), [])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		k = King((2, 0))
		q = Queen((1, 0))
		b = Bishop((0, 0))
		boardInfo['P1'] = [k, q]
		boardInfo['P2'] = [b]
		possibles = [(1, 1), (2, 2), (3, 3)]
		self.assertEqual(b.setPossiblePositions(possibles, boardInfo, False), ['B(1, 1)', 'B(2, 2)', 'B(3, 3)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		k = King((2, 0))
		q = Queen((1, 0))
		b = Bishop((1, 1))
		boardInfo['P1'] = [k, q]
		boardInfo['P2'] = [b]
		possibles = [(2, 2), (3, 3), (4, 4)]
		self.assertEqual(b.setPossiblePositions(possibles, boardInfo, False), ['B(2, 2)', 'B(3, 3)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		k = King((2, 0))
		q = Queen((2, 2))
		b = Bishop((1, 1))
		boardInfo['P1'] = [k, q]
		boardInfo['P2'] = [b]
		possibles = [(2, 2), (3, 3), (4, 4)]
		self.assertEqual(b.setPossiblePositions(possibles, boardInfo, False), ['B(2, 2)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		k = King((2, 0))
		q = Queen((2, 2))
		b = Bishop((1, 1))
		boardInfo['P1'] = [k]
		boardInfo['P2'] = [b, q]
		possibles = [(2, 2), (3, 3), (4, 4)]
		self.assertEqual(b.setPossiblePositions(possibles, boardInfo, False), [])

class PossibleMovesTest(unittest.TestCase):

	def test_King(self):
		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [King((0, 0))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['K(0, 1)', 'K(1, 0)', 'K(1, 1)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [King((1, 1))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['K(0, 0)', 'K(0, 1)', 'K(0, 2)', 'K(1, 0)', 'K(1, 2)', 'K(2, 0)', 'K(2, 1)', 'K(2, 2)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [King((1, 1)), Queen((1, 2))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['K(0, 0)', 'K(0, 1)', 'K(0, 2)', 'K(1, 0)', 'K(2, 0)', 'K(2, 1)', 'K(2, 2)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [King((1, 1))]
		boardInfo['P2'] = [Queen((1, 2))]
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['K(0, 0)', 'K(0, 1)', 'K(0, 2)', 'K(1, 0)', 'K(1, 2)', 'K(2, 0)', 'K(2, 1)', 'K(2, 2)'])


	def test_Bishop(self):
		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Bishop((0, 0))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['B(1, 1)', 'B(2, 2)', 'B(3, 3)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 8
		boardInfo['P1'] = [Bishop((4, 4))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['B(5, 5)', 'B(6, 6)', 'B(7, 7)', 'B(3, 5)', 'B(2, 6)', 'B(1, 7)', 'B(5, 3)', 'B(6, 2)', 'B(7, 1)', 'B(3, 3)', 'B(2, 2)', 'B(1, 1)', 'B(0, 0)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 8
		boardInfo['P1'] = [Queen((3, 3))]
		boardInfo['P2'] = [Bishop((4, 4)), Pawn((6, 2))]
		self.assertEqual(boardInfo['P2'][0].getPossibleMoves(boardInfo, False), ['B(5, 5)', 'B(6, 6)', 'B(7, 7)', 'B(3, 5)', 'B(2, 6)', 'B(1, 7)', 'B(5, 3)', 'B(3, 3)'])

	def test_Rook(self):
		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Rook((0, 0))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['R(1, 0)', 'R(2, 0)', 'R(3, 0)', 'R(0, 1)', 'R(0, 2)', 'R(0, 3)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Rook((0, 0))]
		boardInfo['P2'] = [King((0, 1))]
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['R(1, 0)', 'R(2, 0)', 'R(3, 0)', 'R(0, 1)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 8
		boardInfo['P1'] = [Rook((4, 4))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['R(5, 4)', 'R(6, 4)', 'R(7, 4)', 'R(3, 4)', 'R(2, 4)', 'R(1, 4)', 'R(0, 4)', 'R(4, 5)', 'R(4, 6)', 'R(4, 7)', 'R(4, 3)', 'R(4, 2)', 'R(4, 1)', 'R(4, 0)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 8
		boardInfo['P1'] = [Rook((5, 4))]
		boardInfo['P2'] = [Rook((4, 4)), Rook((4, 3))]
		self.assertEqual(boardInfo['P2'][0].getPossibleMoves(boardInfo, False), ['R(5, 4)', 'R(3, 4)', 'R(2, 4)', 'R(1, 4)', 'R(0, 4)', 'R(4, 5)', 'R(4, 6)', 'R(4, 7)'])

	def test_Queen(self):
		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Queen((0, 0))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['Q(1, 1)', 'Q(2, 2)', 'Q(3, 3)', 'Q(1, 0)', 'Q(2, 0)', 'Q(3, 0)', 'Q(0, 1)', 'Q(0, 2)', 'Q(0, 3)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Queen((0, 0)), King((1, 1))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['Q(1, 0)', 'Q(2, 0)', 'Q(3, 0)', 'Q(0, 1)', 'Q(0, 2)', 'Q(0, 3)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [King((1, 1))]
		boardInfo['P2'] = [Queen((0, 0))]
		self.assertEqual(boardInfo['P2'][0].getPossibleMoves(boardInfo, False), ['Q(1, 1)', 'Q(1, 0)', 'Q(2, 0)', 'Q(3, 0)', 'Q(0, 1)', 'Q(0, 2)', 'Q(0, 3)'])

	def test_Knight(self):
		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Knight((0, 0))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['N(1, 2)', 'N(2, 1)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Knight((0, 0)), Pawn((1, 2))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['N(2, 1)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Knight((0, 0)), Pawn((1, 2)), Queen((2, 1))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), [])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Pawn((1, 2)), Queen((2, 1))]
		boardInfo['P2'] = [Knight((0, 0))]
		self.assertEqual(boardInfo['P2'][0].getPossibleMoves(boardInfo, False), ['N(1, 2)', 'N(2, 1)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 16
		boardInfo['P1'] = [Knight((4, 4))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['N(5, 6)', 'N(6, 5)', 'N(5, 2)', 'N(6, 3)', 'N(3, 6)', 'N(2, 5)', 'N(3, 2)', 'N(2, 3)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 16
		boardInfo['P1'] = [Knight((4, 4)), Pawn((3, 2)), Queen((2, 3))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['N(5, 6)', 'N(6, 5)', 'N(5, 2)', 'N(6, 3)', 'N(3, 6)', 'N(2, 5)'])

	def test_Pawn(self):
		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Pawn((0, 0))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['(0, 1)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Pawn((0, 1))]
		boardInfo['P2'] = []
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['(0, 2)', '(0, 3)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = []
		boardInfo['P2'] = [Pawn((3, 3))]
		self.assertEqual(boardInfo['P2'][0].getPossibleMoves(boardInfo, False), ['(3, 2)'])	

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Pawn((2, 2))]
		boardInfo['P2'] = [Pawn((3, 3))]
		self.assertEqual(boardInfo['P2'][0].getPossibleMoves(boardInfo, False), ['(3, 2)', '(2, 2)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Pawn((4, 2))]
		boardInfo['P2'] = [Pawn((3, 3))]
		self.assertEqual(boardInfo['P2'][0].getPossibleMoves(boardInfo, False), ['(3, 2)', '(4, 2)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Pawn((2, 2))]
		boardInfo['P2'] = [Pawn((3, 3))]
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['(2, 3)', '(3, 3)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Pawn((2, 2))]
		boardInfo['P2'] = [Pawn((1, 3)), Pawn((3, 3))]
		self.assertEqual(boardInfo['P1'][0].getPossibleMoves(boardInfo, True), ['(2, 3)', '(3, 3)', '(1, 3)'])

class AllPossibleMovesTest(unittest.TestCase):
	def test(self):
		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Pawn((0, 0))]
		boardInfo['P2'] = []
		self.assertEqual(getAllPossibleMoves(boardInfo, True), ['(0, 1)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 4
		boardInfo['P1'] = [Pawn((0, 1)), Knight((0, 0))]
		boardInfo['P2'] = []
		self.assertEqual(getAllPossibleMoves(boardInfo, True), ['(0, 2)', '(0, 3)', 'N(1, 2)', 'N(2, 1)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 8
		boardInfo['P1'] = [Pawn((1, 1)), Rook((0, 0)), Knight((1, 0)), Bishop((2, 0)), Queen((3, 0)), King((4, 0))]
		boardInfo['P2'] = []
		self.assertEqual(getAllPossibleMoves(boardInfo, True), ['(1, 2)', '(1, 3)', 'R(0, 1)', 'R(0, 2)', 'R(0, 3)', 'R(0, 4)', 'R(0, 5)', 'R(0, 6)', 'R(0, 7)', 'N(2, 2)', 'N(3, 1)', 'N(0, 2)', 'B(3, 1)', 'B(4, 2)', 'B(5, 3)', 'B(6, 4)', 'B(7, 5)', 'Q(4, 1)', 'Q(5, 2)', 'Q(6, 3)', 'Q(7, 4)', 'Q(2, 1)', 'Q(1, 2)', 'Q(0, 3)', 'Q(3, 1)', 'Q(3, 2)', 'Q(3, 3)', 'Q(3, 4)', 'Q(3, 5)', 'Q(3, 6)', 'Q(3, 7)', 'K(3, 1)', 'K(4, 1)', 'K(5, 0)', 'K(5, 1)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 8
		boardInfo['P1'] = [Pawn((0, 1)), Pawn((1, 1)), Pawn((2, 1)), Pawn((3, 1)), Pawn((4, 1)), Pawn((5, 1)), Pawn((6, 1)), Pawn((7, 1)),
							Rook((0, 0)), Knight((1, 0)), Bishop((2, 0)), Queen((3, 0)), King((4, 0)), Bishop((5, 0)), Knight((6, 0)), Rook((7, 0))]
		boardInfo['P2'] = []
		self.assertEqual(getAllPossibleMoves(boardInfo, True), ['(0, 2)', '(0, 3)', '(1, 2)', '(1, 3)', '(2, 2)', '(2, 3)', '(3, 2)', '(3, 3)', '(4, 2)', '(4, 3)',
			'(5, 2)', '(5, 3)', '(6, 2)', '(6, 3)', '(7, 2)', '(7, 3)', 'N(2, 2)', 'N(0, 2)', 'N(7, 2)', 'N(5, 2)'])

		boardInfo = dict()
		boardInfo['boardSize'] = 8
		boardInfo['P1'] = [Pawn((0, 1)), Pawn((1, 1)), Pawn((2, 1)), Pawn((3, 1)), Pawn((4, 1)), Pawn((5, 1)), Pawn((6, 1)), Pawn((7, 1)),
							Rook((0, 0)), Knight((1, 0)), Bishop((2, 0)), Queen((3, 0)), King((4, 0)), Bishop((5, 0)), Knight((6, 0)), Rook((7, 0))]
		boardInfo['P2'] = []
		self.assertEqual(getAllPossibleMoves(boardInfo, False), [])



if __name__ == '__main__':
    unittest.main()