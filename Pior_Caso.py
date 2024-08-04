import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from collections import deque

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_edge(self, origin, destination, cost):
        if origin not in self.nodes:
            self.nodes[origin] = []
        self.nodes[origin].append((destination, cost))

    def __str__(self):
        return f"Grafo: {self.nodes}"

def read_file(file):
    graph = Graph()
    start_point = None
    end_point = None

    with open(file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespace
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
    
    return start_point, end_point, graph

def bfs(start_point, end_point, graph):
    queue = deque([(start_point, [start_point])])
    visited = set()
    in_queue = set([start_point])  # Conjunto para rastrear nós na fila
    iteration = 1
    result = ""

    while queue:
        result += f"Iteração {iteration}:\n"
        queue_str = ", ".join([node for node, _ in queue])
        result += f"Fila: {queue_str}\n"
        
        (current, path) = queue.popleft()
        in_queue.remove(current)  # Remove da fila
        result += f"Nó a ser visitado: {current}\n"
        result += f"Medida de desempenho: {len(visited):.1f}\n\n"

        if current in visited:
            continue

        visited.add(current)

        if current == end_point:
            result += f"Fim da execução\nDistância: {len(path) - 1}\nCaminho: {' -> '.join(path)}\nMedida de desempenho: {len(visited):.1f}\n"
            return result

        for (neighbor, _) in graph.nodes.get(current, []):
            if neighbor not in visited and neighbor not in in_queue:
                queue.append((neighbor, path + [neighbor]))
                in_queue.add(neighbor)  # Adiciona ao conjunto de nós na fila

        iteration += 1

    result += "Nenhum caminho encontrado\n"
    return result

def dfs(start_point, end_point, graph):
    stack = [(start_point, [start_point])]
    visited = set()
    in_stack = set([start_point])  # Conjunto para rastrear nós na pilha
    iteration = 1
    result = ""

    while stack:
        result += f"Iteração {iteration}:\n"
        stack_str = ", ".join([node for node, _ in stack])
        result += f"Pilha: {stack_str}\n"
        
        (current, path) = stack.pop()
        result += f"Nó a ser visitado: {current}\n"
        result += f"Medida de desempenho: {len(visited):.1f}\n\n"

        if current in visited:
            continue

        visited.add(current)

        if current == end_point:
            result += f"Fim da execução\nDistância: {len(path) - 1}\nCaminho: {' -> '.join(path)}\nMedida de desempenho: {len(visited):.1f}\n"
            return result

        for (neighbor, _) in reversed(graph.nodes.get(current, [])):  # Inverte a ordem dos vizinhos
            if neighbor not in visited and neighbor not in in_stack:
                stack.append((neighbor, path + [neighbor]))
                in_stack.add(neighbor)  # Adiciona ao conjunto de nós na pilha

        iteration += 1

    result += "Nenhum caminho encontrado\n"
    return result

def execute_searches(start_point, end_point, graph, search_type):
    if search_type == "BFS":
        return bfs(start_point, end_point, graph)
    elif search_type == "DFS":
        return dfs(start_point, end_point, graph)
    else:
        return "Tipo de busca desconhecido"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Busca em Grafos")
        self.file_path = None
        self.start_point = None
        self.end_point = None
        self.graph = None

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.load_button = tk.Button(self.frame, text="Carregar Arquivo", command=self.load_file)
        self.load_button.pack(side=tk.LEFT)

        self.bfs_button = tk.Button(self.frame, text="Executar BFS", command=self.run_bfs)
        self.bfs_button.pack(side=tk.LEFT)

        self.dfs_button = tk.Button(self.frame, text="Executar DFS", command=self.run_dfs)
        self.dfs_button.pack(side=tk.LEFT)

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.NONE, width=100, height=30)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not self.file_path:
            return

        try:
            self.start_point, self.end_point, self.graph = read_file(self.file_path)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Ponto Inicial: {self.start_point}\n")
            self.text_area.insert(tk.END, f"Ponto Final: {self.end_point}\n")
            self.text_area.insert(tk.END, f"{self.graph}\n")
            messagebox.showinfo("Sucesso", "Arquivo carregado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")

    def run_bfs(self):
        if not self.graph:
            messagebox.showerror("Erro", "Carregue um arquivo primeiro!")
            return

        result = execute_searches(self.start_point, self.end_point, self.graph, "BFS")
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, result)

    def run_dfs(self):
        if not self.graph:
            messagebox.showerror("Erro", "Carregue um arquivo primeiro!")
            return

        result = execute_searches(self.start_point, self.end_point, self.graph, "DFS")
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
