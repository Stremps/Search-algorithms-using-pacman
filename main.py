import tkinter as tk
from ui import App
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Executar algoritmos de busca.')
    parser.add_argument('--input', type=str, help='Arquivo de entrada contendo o grafo.')
    parser.add_argument('--algorithm', type=str, help='Algoritmo de busca a ser executado.',
                        choices=['BFS', 'DFS', 'DFS_NO_BACKTRACKING', 'A_STAR_NO_HEURISTIC', 'A_STAR_WITH_HEURISTIC', 'IDA_STAR'])
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    if args.input and args.algorithm:
        root = tk.Tk()
        app = App(root)
        
        # Carregar o grafo a partir do arquivo de entrada
        app.load_file(args.input)
        
        # Executar o algoritmo especificado
        if args.algorithm == 'BFS':
            result = app.run_bfs()
        elif args.algorithm == 'DFS':
            result = app.run_dfs()
        elif args.algorithm == 'DFS_NO_BACKTRACKING':
            result = app.run_dfs_no_backtracking()
        elif args.algorithm == 'A_STAR_NO_HEURISTIC':
            result = app.run_a_star()
        elif args.algorithm == 'A_STAR_WITH_HEURISTIC':
            result = app.run_a_star_with_heuristic()
        elif args.algorithm == 'IDA_STAR':
            result = app.run_ida_star()

        # Imprimir resultados para que o script Bash possa capturar
        print(result)
    else:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
