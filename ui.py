import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from graph import read_file
from search_algorithms import execute_searches
import timeit

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

        self.dfs_no_backtracking_button = tk.Button(self.frame, text="Executar DFS Sem Backtracking", command=self.run_dfs_no_backtracking)
        self.dfs_no_backtracking_button.pack(side=tk.LEFT)

        self.a_star_button = tk.Button(self.frame, text="Executar A* sem Heurística/UCS", command=self.run_a_star)
        self.a_star_button.pack(side=tk.LEFT)

        self.a_star_with_heuristic_button = tk.Button(self.frame, text="Executar A*", command=self.run_a_star_with_heuristic)
        self.a_star_with_heuristic_button.pack(side=tk.LEFT)

        self.ida_star_button = tk.Button(self.frame, text="Executar IDA*", command=self.run_ida_star)
        self.ida_star_button.pack(side=tk.LEFT)

        self.show_graph_button = tk.Button(self.frame, text="Exibir Grafo", command=self.show_graph)
        self.show_graph_button.pack(side=tk.LEFT)

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

        start_time = timeit.default_timer()
        result = execute_searches(self.start_point, self.end_point, self.graph, "BFS")
        time_taken = timeit.default_timer() - start_time

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, result)
        self.text_area.insert(tk.END, f"Tempo de execução BFS: {time_taken:.6f} segundos\n")

    def run_dfs(self):
        if not self.graph:
            messagebox.showerror("Erro", "Carregue um arquivo primeiro!")
            return

        start_time = timeit.default_timer()
        result = execute_searches(self.start_point, self.end_point, self.graph, "DFS")
        time_taken = timeit.default_timer() - start_time

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, result)
        self.text_area.insert(tk.END, f"Tempo de execução DFS: {time_taken:.6f} segundos\n")

    def run_dfs_no_backtracking(self):
        if not self.graph:
            messagebox.showerror("Erro", "Carregue um arquivo primeiro!")
            return

        start_time = timeit.default_timer()
        result = execute_searches(self.start_point, self.end_point, self.graph, "DFS_NO_BACKTRACKING")
        time_taken = timeit.default_timer() - start_time

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, result)
        self.text_area.insert(tk.END, f"Tempo de execução DFS Sem Backtracking: {time_taken:.6f} segundos\n")

    def show_graph(self):
        if not self.graph:
            messagebox.showerror("Erro", "Carregue um arquivo primeiro!")
            return

        self.text_area.delete(1.0, tk.END)
        graph_str = str(self.graph)
        wrapped_graph_str = '\n'.join([graph_str[i:i+800] for i in range(0, len(graph_str), 800)])
        self.text_area.insert(tk.END, f"Ponto Inicial: {self.start_point}\n")
        self.text_area.insert(tk.END, f"Ponto Final: {self.end_point}\n")
        self.text_area.insert(tk.END, wrapped_graph_str)

    def run_a_star(self):
        if not self.graph:
            messagebox.showerror("Erro", "Carregue um arquivo primeiro!")
            return

        start_time = timeit.default_timer()
        result = execute_searches(self.start_point, self.end_point, self.graph, "A_STAR_WITHOUT_HEURISTIC")
        time_taken = timeit.default_timer() - start_time

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, result)
        self.text_area.insert(tk.END, f"Tempo de execução A*/UCS: {time_taken:.6f} segundos\n")

    def run_a_star_with_heuristic(self):
        if not self.graph:
            messagebox.showerror("Erro", "Carregue um arquivo primeiro!")
            return

        start_time = timeit.default_timer()
        result = execute_searches(self.start_point, self.end_point, self.graph, "A_STAR")
        time_taken = timeit.default_timer() - start_time

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, result)
        self.text_area.insert(tk.END, f"Tempo de execução A* c/ Heurística: {time_taken:.6f} segundos\n")
        
    def run_ida_star(self):
        if not self.graph:
            messagebox.showerror("Erro", "Carregue um arquivo primeiro!")
            return

        start_time = timeit.default_timer()
        result = execute_searches(self.start_point, self.end_point, self.graph, "IDA_STAR")
        time_taken = timeit.default_timer() - start_time

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, result)
        self.text_area.insert(tk.END, f"Tempo de execução IDA*: {time_taken:.6f} segundos\n")