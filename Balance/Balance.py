class Balance:

    def __init__(self, name_file, output_file='output.txt'):
        self.servers = []
        self.historic = []
        self.total_tick = 0
        self.cost = 0
        self.output_file = output_file
        self.ttask = None
        self.umax = None
        self.inputs = None
        self._load_file(name_file)

    def process(self):
        """ 
            Processa os dados contidos no input.txt e gera um 
            arquivo com o resutado no output.txt
        """
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
        self.historic.append(self._user_by_server())
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
        for linha in self.historic:
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
