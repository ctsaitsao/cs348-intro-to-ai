import game_manager, game_rules, signal, unittest
from multiprocessing.pool import ThreadPool
from player import makePlayer

def run_test(gm):
	gm.play()
	game_rules.printBoard(gm.board)
	print(gm.GetWinner(), "WINS")
	return gm.board

class GameTest(unittest.TestCase):

	def makeGame(self, size, player1, player2, depth):
		gm = game_manager.GameManager(
			  size
			, size
			, makePlayer(player1, 'x', depth)
			, makePlayer(player2, 'o', depth)
			, False)
		signal.signal(signal.SIGINT, gm.interrupt)
		return gm

	def test1(self):
		p1 = 'm'
		p2 = 'd'
		depth = 2
		gm = self.makeGame(4, p1, p2, depth)

		pool = ThreadPool(processes=1)
		async_result = pool.apply_async(run_test, [gm])
		result = None
		try:
			returned_value = async_result.get(2)
			self.assertEqual(returned_value, [['x', ' ', ' ', 'o'], [' ', 'x', ' ', 'x'], [' ', 'o', ' ', 'o'], ['o', 'x', 'o', 'x']])
		except Exception as e: 
			self.fail('Timed out: {}'.format(e))
		

	def test2(self):
		p1 = 'm'
		p2 = 'd'
		depth = 5
		gm = self.makeGame(4, p1, p2, depth)

		pool = ThreadPool(processes=1)
		async_result = pool.apply_async(run_test, [gm])
		result = None
		try:
			returned_value = async_result.get(5)
			self.assertEqual(returned_value, [['x', ' ', ' ', 'o'], [' ', 'x', ' ', 'x'], [' ', 'o', ' ', 'o'], ['o', 'x', 'o', 'x']])
		except Exception as e: 
			self.fail('Timed out: {}'.format(e))

	def test3(self):
		p1 = 'd'
		p2 = 'm'
		depth = 4
		gm = self.makeGame(6, p1, p2, depth)

		pool = ThreadPool(processes=1)
		async_result = pool.apply_async(run_test, [gm])
		result = None
		try:
			returned_value = async_result.get(20)
			self.assertEqual(returned_value, [[' ', 'o', ' ', 'o', ' ', 'o'], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', 'x', ' '], ['o', ' ', ' ', 'x', 'o', 'x'], [' ', ' ', 'x', ' ', 'x', 'o'], ['o', 'x', 'o', 'x', 'o', 'x']])
		except Exception as e: 
			self.fail('Timed out: {}'.format(e))

	def test4(self):
		p1 = 'd'
		p2 = 'a'
		depth = 4
		gm = self.makeGame(6, p1, p2, depth)

		pool = ThreadPool(processes=1)
		async_result = pool.apply_async(run_test, [gm])
		result = None
		try:
			returned_value = async_result.get(5)
			self.assertEqual(returned_value, [[' ', 'o', ' ', 'o', ' ', 'o'], [' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', 'x', ' '], ['o', ' ', ' ', 'x', 'o', 'x'], [' ', ' ', 'x', ' ', 'x', 'o'], ['o', 'x', 'o', 'x', 'o', 'x']])
		except Exception as e: 
			self.fail('Timed out: {}'.format(e))

	def test5(self):
		p1 = 'a'
		p2 = 'd'
		depth = 6
		gm = self.makeGame(8, p1, p2, depth)

		pool = ThreadPool(processes=1)
		async_result = pool.apply_async(run_test, [gm])
		result = None
		try:
			returned_value = async_result.get(300)
			self.assertEqual(returned_value, [['x', ' ', 'x', ' ', 'x', ' ', ' ', 'o'], [' ', ' ', ' ', 'x', ' ', ' ', ' ', 'x'], [' ', ' ', 'x', ' ', 'x', ' ', ' ', 'o'], ['o', ' ', ' ', ' ', ' ', 'x', ' ', 'x'], [' ', 'o', ' ', 'o', ' ', ' ', ' ', 'o'], ['o', ' ', 'o', ' ', ' ', ' ', 'o', 'x'], ['x', ' ', ' ', 'o', ' ', 'o', 'x', 'o'], ['o', 'x', 'o', 'x', 'o', 'x', 'o', 'x']])
		except Exception as e: 
			self.fail('Timed out: {}'.format(e))

if __name__== "__main__":
	unittest.main()
