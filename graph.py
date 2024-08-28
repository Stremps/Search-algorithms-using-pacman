class Graph:
    def __init__(self):
        self.nodes = {}
        self.coordinates = {}  # Se necessário para outras heurísticas
        self.heuristics = {}  # Novo dicionário para armazenar heurísticas

    def add_edge(self, origin, destination, cost):
        if origin not in self.nodes:
            self.nodes[origin] = []
        self.nodes[origin].append((destination, cost))
        if destination not in self.nodes:
            self.nodes[destination] = []

    def add_heuristic(self, node, end_node, heuristic_value):
        """Adiciona uma heurística para um nó específico até o nó final"""
        if node not in self.heuristics:
            self.heuristics[node] = {}
        self.heuristics[node][end_node] = heuristic_value

    def get_heuristic(self, node, end_node):
        """Retorna a heurística de um nó para o nó final"""
        return self.heuristics.get(node, {}).get(end_node, 0)

    def __str__(self):
        graph_str = ""
        for node, edges in self.nodes.items():
            edge_str = ", ".join(f"({dest}, {cost})" for dest, cost in edges)
            graph_str += f"{node}: {edge_str if edge_str else 'Sem arestas de saída'}\n"
        return graph_str


def read_file(file):
    graph = Graph()
    start_point = None
    end_point = None

    with open(file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith('ponto_inicial'):
            start_point = line.split('(')[1].split(')')[0]
        elif line.startswith('ponto_final'):
            end_point = line.split('(')[1].split(')')[0]
        elif line.startswith('pode_ir'):
            try:
                data = line.split('(')[1].split(')')[0].split(',')
                origin = data[0].strip()
                destination = data[1].strip()
                cost = int(data[2].strip())
                graph.add_edge(origin, destination, cost)
            except ValueError as e:
                print(f"Erro ao processar a linha: {line}\nErro: {e}")
        elif line.startswith('h'):  # Ler a heurística do arquivo
            try:
                data = line.split('(')[1].split(')')[0].split(',')
                node = data[0].strip()
                end_node = data[1].strip()
                heuristic_value = float(data[2].strip())
                graph.add_heuristic(node, end_node, heuristic_value)
            except ValueError as e:
                print(f"Erro ao processar a linha de heurística: {line}\nErro: {e}")

    return start_point, end_point, graph