import os, sys
import unittest
from Balance import Balance


class TestBalance(unittest.TestCase):

    def test_balance(self):
        saida_desejada = [
            '1', '2,2', '2,2', '2,2,1', '1,2,1', '2', '2', '1', '1', '0', '15']
        balance = Balance('test/input.txt', 'test/output.txt')
        file = open("test/output.txt","w")
        file.close()
        self.assertEqual(os.stat("test/output.txt").st_size, 0)
        balance.process()
        with open('test/output.txt') as f:
            resposta = [x for x in f.read().split()]
        self.assertEqual(resposta, saida_desejada)

    def test_load_file(self):
        balance = Balance('test/input.txt')
        self.assertEqual(balance.ttask, 4)
        self.assertEqual(balance.umax, 2)
        self.assertEqual(balance.inputs, [1, 3, 0, 1, 0, 1])

    def test_create_server(self):
        balance = Balance('test/input.txt')
        balance.ttask = 4
        balance.umax = 2
        self.assertEqual(balance.servers, [])
        balance._create_server()
        self.assertEqual(balance.servers, [[0, 0]])
        balance._create_server()
        self.assertEqual(balance.servers, [[0, 0], [0, 0]])

    def test_free_server(self):
        balance = Balance('test/input.txt')
        balance.servers = [[3, 4], [1, 0]]
        self.assertEqual(balance._free_server(), (1, 1))
        balance.servers = [[3, 4], [2, 1]]
        self.assertEqual(balance._free_server(), None)

    def test_tick(self):
        balance = Balance('test/input.txt')
        balance.servers = [[3, 4], [1, 0]]
        balance._tick()
        self.assertEqual(balance.servers, [[2, 3], [0, 0]])
        balance._tick()
        self.assertEqual(balance.servers, [[1, 2], [0, 0]])
        balance._tick()
        self.assertEqual(balance.servers, [[0, 1], [0, 0]])
        balance._tick()
        self.assertEqual(balance.servers, [[0, 0], [0, 0]])

    def test_delete_empty_server(self):
        balance = Balance('test/input.txt')
        balance.servers = [[1, 1], [0, 0]]
        balance._delete_empty_server()
        self.assertEqual(balance.servers, [[1, 1]])
        balance.servers = [[1, 0]]
        balance._delete_empty_server()
        self.assertEqual(balance.servers, [[1, 0]])
        balance.servers = [[0, 0]]
        balance._delete_empty_server()
        self.assertEqual(balance.servers, [])
        balance.servers = [[0, 0], [0, 0]]
        balance._delete_empty_server()
        self.assertEqual(balance.servers, [])
        balance.servers = [[4, 0], [4, 0]]
        balance._delete_empty_server()
        self.assertEqual(balance.servers, [[4, 0], [4, 0]])
        balance.servers = [[3, 4], [4, 4]]
        balance._delete_empty_server()
        self.assertEqual(balance.servers, [[3, 4], [4, 4]])

    def test_allocate_user(self):
        balance = Balance('test/input.txt')
        self.assertEqual(balance.ttask, 4)
        self.assertEqual(balance.umax, 2)
        balance._allocate_user(1)
        self.assertEqual(balance.servers, [[4, 0]])
        balance._allocate_user(1)
        self.assertEqual(balance.servers, [[4, 4]])
        balance._allocate_user(3)
        self.assertEqual(balance.servers, [[4, 4], [4, 4], [4, 0]])
        balance._allocate_user(0)
        self.assertEqual(balance.servers, [[4, 4], [4, 4], [4, 0]])

    def test_user_by_server(self):
        balance = Balance('test/input.txt')
        balance._allocate_user(1)
        balance.servers = [[4, 0]]
        self.assertEqual(balance._user_by_server(), '1')
        balance.servers = [[4, 3]]
        self.assertEqual(balance._user_by_server(), '2')
        balance.servers = [[4, 3], [2, 0]]
        self.assertEqual(balance._user_by_server(), '2,1')
        balance.servers = [[4, 3], [2, 0], [0, 2]]
        self.assertEqual(balance._user_by_server(), '2,1,1')

    def test_process(self):
        balance = Balance('test/input.txt')
        self.assertEqual(balance.ttask, 4)
        self.assertEqual(balance.umax, 2)
        self.assertEqual(balance._process_input(), (1, 1, '1'))
        self.assertEqual(balance._process_input(), (2, 3, '2,2'))
        self.assertEqual(balance._process_input(), (3, 0, '2,2'))
        self.assertEqual(balance._process_input(), (4, 1, '2,2,1'))
        self.assertEqual(balance._process_input(), (5, 0, '1,2,1'))
        self.assertEqual(balance._process_input(), (6, 1, '2'))
        self.assertEqual(balance._process_input(), (7, 0, '2'))
        self.assertEqual(balance._process_input(), (8, 0, '1'))
        self.assertEqual(balance._process_input(), (9, 0, '1'))
        self.assertEqual(balance._process_input(), (10, 0, '0'))
        self.assertEqual(balance.cost, 15)
