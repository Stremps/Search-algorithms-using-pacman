from heapq import heappop, heappush
import tracemalloc
from collections import deque

def calculate_path_cost(graph, path):
    cost = 0
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        for (neighbor, weight) in graph.nodes[current]:
            if neighbor == next_node:
                cost += weight
                break
    return cost

def bfs(start_point, end_point, graph):
    tracemalloc.start()
    queue = deque([(start_point, [start_point])])
    visited = set()
    in_queue = set([start_point])
    iteration = 1
    result = ""

    while queue:
        result += f"Iteração {iteration}:\n"
        queue_str = ", ".join([node for node, _ in queue])
        result += f"Fila: {queue_str}\n"
        (current, path) = queue.popleft()
        in_queue.remove(current)
        result += f"Nó a ser visitado: {current}\n"
        path_cost = calculate_path_cost(graph, path)
        result += f"peso total do caminho : {path_cost}\n\n"

        if current in visited:
            continue

        visited.add(current)

        if current == end_point:
            result += f"Fim da execução\nDistância: {len(path) - 1}\nCaminho: {' -> '.join(path)}\nPeso total do caminho: {path_cost}\n"
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            result += f"Pico de uso de memória: {peak_mem / 1024:.2f} KB\n"
            tracemalloc.stop()
            return result

        for (neighbor, _) in graph.nodes.get(current, []):
            if neighbor not in visited and neighbor not in in_queue:
                queue.append((neighbor, path + [neighbor]))
                in_queue.add(neighbor)

        iteration += 1

    result += "Nenhum caminho encontrado\n"
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    result += f"Pico de uso de memória: {peak_mem / 1024:.2f} KB\n"
    tracemalloc.stop()
    return result

def dfs(start_point, end_point, graph):
    tracemalloc.start()
    stack = [(start_point, [start_point])]
    visited = set()
    in_stack = set([start_point])
    iteration = 1
    result = ""

    while stack:
        result += f"Iteração {iteration}:\n"
        stack_str = ", ".join([node for node, _ in stack])
        result += f"Pilha: {stack_str}\n"
        (current, path) = stack.pop()
        in_stack.remove(current)
        result += f"Nó a ser visitado: {current}\n"
        path_cost = calculate_path_cost(graph, path)
        result += f"peso total do caminho : {path_cost}\n\n"

        if current in visited:
            continue

        visited.add(current)

        if current == end_point:
            result += f"Fim da execução\nDistância: {len(path) - 1}\nCaminho: {' -> '.join(path)}\nPeso total do caminho: {path_cost}\n"
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            result += f"Pico de uso de memória: {peak_mem / 1024:.2f} KB\n"
            tracemalloc.stop()
            return result

        for (neighbor, _) in reversed(graph.nodes.get(current, [])):
            if neighbor not in visited and neighbor not in in_stack:
                stack.append((neighbor, path + [neighbor]))
                in_stack.add(neighbor)

        iteration += 1

    result += "Nenhum caminho encontrado\n"
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    result += f"Pico de uso de memória: {peak_mem / 1024:.2f} KB\n"
    tracemalloc.stop()
    return result

def dfs_no_backtracking(start_point, end_point, graph):
    tracemalloc.start()
    current = start_point
    path = [current]
    visited = set([current])
    iteration = 1
    result = ""

    while True:
        result += f"Iteração {iteration}:\n"
        result += f"Nó atual: {current}\n"
        result += f"Caminho: {' -> '.join(path)}\n"
        path_cost = calculate_path_cost(graph, path)
        result += f"peso total do caminho : {path_cost}\n\n"

        if current == end_point:
            result += f"Fim da execução\nDistância: {len(path) - 1}\nCaminho: {' -> '.join(path)}\nPeso total do caminho: {path_cost}\n"
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            result += f"Pico de uso de memória: {peak_mem / 1024:.2f} KB\n"
            tracemalloc.stop()
            return result

        unvisited_neighbors = [neighbor for (neighbor, _) in graph.nodes.get(current, []) if neighbor not in visited]
        if unvisited_neighbors:
            current = unvisited_neighbors[0]
            path.append(current)
            visited.add(current)
        else:
            result += "Nenhum caminho encontrado\n"
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            result += f"Pico de uso de memória: {peak_mem / 1024:.2f} KB\n"
            tracemalloc.stop()
            return result

        iteration += 1

def heuristic(node, end_point, graph, source):
    """Retorna a heurística lida do arquivo (source == 1) ou heurística igual a 0 (source == 0)"""
    if(source == 1):
        return graph.get_heuristic(node, end_point)
    elif(source == 0):
        return 0

def a_star_search(start_point, end_point, graph):
    tracemalloc.start()
    open_set = []
    heappush(open_set, (0, start_point, [start_point]))  # (custo_total_estimado, nó_atual, caminho)
    g_scores = {start_point: 0}
    visited = set()
    iteration = 1
    result = ""

    while open_set:
        result += f"Iteração {iteration}:\n"
        open_set_str = ", ".join([f"({node}: {g_scores[node]} + 0 = {g_scores[node]})" for _, node, _ in open_set])
        result += f"Fila de prioridade (Open Set): {open_set_str}\n"

        current_f_cost, current, path = heappop(open_set)
        current_g_score = g_scores[current]
        result += f"Nó a ser visitado: {current}\n"
        path_cost = calculate_path_cost(graph, path)
        result += f"peso total do caminho : {path_cost}\n\n"

        if current in visited:
            continue

        visited.add(current)

        if current == end_point:
            result += f"Fim da execução\nDistância: {len(path) - 1}\nCaminho: {' -> '.join(path)}\nPeso total do caminho: {path_cost}\n"
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            result += f"Pico de uso de memória: {peak_mem / 1024:.2f} KB\n"
            tracemalloc.stop()
            return result

        for (neighbor, cost) in graph.nodes.get(current, []):
            tentative_g_score = current_g_score + cost
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                f_score = tentative_g_score  # Sem heurística, h(n) = 0
                heappush(open_set, (f_score, neighbor, path + [neighbor]))

        iteration += 1

    result += "Nenhum caminho encontrado\n"
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    result += f"Pico de uso de memória: {peak_mem / 1024:.2f} KB\n"
    tracemalloc.stop()
    return result


def a_star_search_with_file_heuristic(start_point, end_point, graph):
    tracemalloc.start()
    open_set = []
    heappush(open_set, (0, start_point, [start_point]))  # (custo_total_estimado, nó_atual, caminho)
    g_scores = {start_point: 0}
    visited = set()
    iteration = 1
    result = ""

    while open_set:
        result += f"Iteração {iteration}:\n"
        open_set_str = ", ".join([f"({node}: {g_scores[node]} + {heuristic(node, end_point, graph, 1)} = {g_scores[node] + heuristic(node, end_point, graph, 1)})" for _, node, _ in open_set])
        result += f"Fila de prioridade (Open Set): {open_set_str}\n"

        current_f_cost, current, path = heappop(open_set)
        current_g_score = g_scores[current]
        result += f"Nó a ser visitado: {current}\n"
        path_cost = calculate_path_cost(graph, path)
        result += f"peso total do caminho : {path_cost}\n\n"

        if current in visited:
            continue

        visited.add(current)

        if current == end_point:
            result += f"Fim da execução\nDistância: {len(path) - 1}\nCaminho: {' -> '.join(path)}\nPeso total do caminho: {path_cost}\n"
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            result += f"Pico de uso de memória: {peak_mem / 1024:.2f} KB\n"
            tracemalloc.stop()
            return result

        for (neighbor, cost) in graph.nodes.get(current, []):
            tentative_g_score = current_g_score + cost
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, end_point, graph, 1)
                heappush(open_set, (f_score, neighbor, path + [neighbor]))

        iteration += 1

    result += "Nenhum caminho encontrado\n"
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    result += f"Pico de uso de memória: {peak_mem / 1024:.2f} KB\n"
    tracemalloc.stop()
    return result


def ida_star_search(start_point, end_point, graph):
    def search(path, g, threshold, result, iteration):
        node = path[-1]
        h = heuristic(node, end_point, graph, 1)
        f = g + h
        result += f"Iteração {iteration}:\n"
        result += f"Fila: ({node}: {g} + {h} = {f})\n"

        if f > threshold:
            return f, None, result
        
        if node == end_point:
            return g, path, result
        
        min_threshold = float('inf')
        for (neighbor, cost) in graph.nodes.get(node, []):
            if neighbor not in path:  # Evitar ciclos
                path.append(neighbor)
                result += f"Explorando vizinho: {neighbor}, Custo: {cost}\n"
                t, result_path, result = search(path, g + cost, threshold, result, iteration + 1)
                
                if result_path is not None:
                    return t, result_path, result
                
                if t < min_threshold:
                    min_threshold = t
                
                path.pop()
        return min_threshold, None, result
    
    tracemalloc.start()
    # Início da Busca IDA*
    threshold = heuristic(start_point, end_point, graph, 1)
    path = [start_point]
    result = ""
    iteration = 1
    
    while True:
        result += f"Iniciando nova iteração com limiar: {threshold}\n"
        t, result_path, result = search(path, 0, threshold, result, iteration)
        
        if result_path is not None:
            result += f"Fim da execução\nDistância: {len(result_path) - 1}\nCaminho: {' -> '.join(result_path)}\nPeso total do caminho: {t}\n"
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Adicionar informação de memória ao resultado
            result += f"Pico de uso de memória: {peak / 1024:.2f} KB\n"
            
            return result
        
        if t == float('inf'):
            result += "Nenhum caminho encontrado\n"
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Adicionar informação de memória ao resultado
            result += f"Pico de uso de memória: {peak / 1024:.2f} KB\n"
            return result
        
        result += f"Iteração {iteration} finalizada. Novo limiar definido: {t}\n\n"
        threshold = t
        iteration += 1


def execute_searches(start_point, end_point, graph, search_type):
    if search_type == "BFS":
        return bfs(start_point, end_point, graph)
    elif search_type == "DFS":
        return dfs(start_point, end_point, graph)
    elif search_type == "DFS_NO_BACKTRACKING":
        return dfs_no_backtracking(start_point, end_point, graph)
    elif search_type == "A_STAR_WITHOUT_HEURISTIC":
        return a_star_search(start_point, end_point, graph)
    elif search_type == "A_STAR":
        return a_star_search_with_file_heuristic(start_point, end_point, graph)
    elif search_type == "IDA_STAR":
        return ida_star_search(start_point, end_point, graph)
    else:
        return "Tipo de busca desconhecido"