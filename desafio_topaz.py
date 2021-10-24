import unittest
import os


class Balance:

    def __init__(self, name_file, output_file='output.txt'):
        self.servers = []
        self.historico = []
        self.total_tick = 0
        self.cost = 0
        self.output_file = output_file
        self._load_file(name_file)

    def process(self):
        if len(self.inputs):
            self._process_input()
        while len(self.servers) > 0:
            self._process_input()
        self._write_file()

    def _process_input(self):
        self._tick()
        self._delete_empty_server()
        input = self._return_inputs()
        self._allocate_user(input)
        self._calculate_cost()
        self.historico.append(self._user_by_server())
        return (self.total_tick, input, self._user_by_server())

    def _load_file(self, name_file):
        with open(name_file) as f:
            lines = [int(x) for x in f.read().split()]
        self.ttask = lines[0]
        self.umax = lines[1]
        self.servers = []
        self.inputs = lines[2:]

    def _tick(self):
        for idx_server, server in enumerate(self.servers):
            for idx_celula, celula in enumerate(server):
                if celula > 0:
                    self.servers[idx_server][idx_celula] -= 1
        self.total_tick += 1

    def _delete_empty_server(self):
        self.servers = list(
            filter(lambda celula: celula != [0, 0], self.servers))

    def _return_inputs(self):
        if len(self.inputs):
            return self.inputs.pop(0)
        return 0

    def _allocate_user(self, new_users):
        while new_users > 0:
            free_space = self._free_server()
            if free_space:
                self.servers[free_space[0]][free_space[1]] = 4
                new_users -= 1
            else:
                self._create_server()

    def _calculate_cost(self):
        self.cost += len(self.servers)

    def _write_file(self):
        file = open(self.output_file, 'w')
        for linha in self.historico:
            file.write(linha + '\n')
        file.write(str(self.cost) + '\n')
        file.close()

    def _create_server(self):
        self.servers.append([0 for _ in range(self.umax)])

    def _free_server(self):
        resposta = None
        for idx_server, server in enumerate(self.servers):
            for idx_celula, celula in enumerate(server):
                if celula == 0:
                    return (idx_server, idx_celula)
        return resposta

    def _user_by_server(self):
        total_usuario = []
        for server in self.servers:
            total_usuario.append(sum([1 for celula in server if celula > 0]))
        resposta = ','.join(str(usuarios) for usuarios in total_usuario)
        return resposta if resposta != '' else '0'


class TestBalance(unittest.TestCase):

    def test_balance(self):
        saida_desejada = [
            '1', '2,2', '2,2', '2,2,1', '1,2,1', '2', '2', '1', '1', '0', '15']
        balance = Balance('input.txt', 'output.txt')
        file = open("output.txt","w")
        file.close()
        self.assertEqual(os.stat("output.txt").st_size, 0)
        balance.process()
        with open('output.txt') as f:
            resposta = [x for x in f.read().split()]
        self.assertEqual(resposta, saida_desejada)

    def test_load_file(self):
        balance = Balance('input.txt')
        self.assertEqual(balance.ttask, 4)
        self.assertEqual(balance.umax, 2)
        self.assertEqual(balance.inputs, [1, 3, 0, 1, 0, 1])

    def test_create_server(self):
        balance = Balance('input.txt')
        balance.ttask = 4
        balance.umax = 2
        self.assertEqual(balance.servers, [])
        balance._create_server()
        self.assertEqual(balance.servers, [[0, 0]])
        balance._create_server()
        self.assertEqual(balance.servers, [[0, 0], [0, 0]])

    def test_free_server(self):
        balance = Balance('input.txt')
        balance.servers = [[3, 4], [1, 0]]
        self.assertEqual(balance._free_server(), (1, 1))
        balance.servers = [[3, 4], [2, 1]]
        self.assertEqual(balance._free_server(), None)

    def test_tick(self):
        balance = Balance('input.txt')
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
        balance = Balance('input.txt')
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
        balance = Balance('input.txt')
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
        balance = Balance('input.txt')
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
        balance = Balance('input.txt')
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


if __name__ == '__main__':
    unittest.main()
