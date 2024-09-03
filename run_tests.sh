#!/bin/bash

# Número de execuções para cada algoritmo
num_runs=30
output_file="test_results.csv"
input_files=("arq.txt" "arq2.txt" "arq3.txt")

# Cabeçalho do arquivo CSV
echo "Algoritmo,Arquivo de Entrada,Execução,Tempo de Execução (s),Uso de Memória (KB),Peso Total do Caminho" > $output_file

# Função para executar testes
run_test() {
    local algorithm_name=$1
    local input_file=$2

    for i in $(seq 1 $num_runs); do
        echo "Executando ${algorithm_name} com ${input_file}, Execução ${i}..."
        result=$(python3 main.py --input ${input_file} --algorithm ${algorithm_name})

        # Extraindo os resultados da string usando grep e awk
        path_cost=$(echo "$result" | grep "Peso total do caminho" | awk '{print $5}')
        mem_usage=$(echo "$result" | grep "Pico de uso de memória" | awk '{print $6}')
        exec_time=$(echo "$result" | grep "Tempo de execução" | awk '{print $4}')

        # Verificação adicional para garantir que os valores foram extraídos corretamente
        if [[ -z "$exec_time" || -z "$mem_usage" || -z "$path_cost" ]]; then
            echo "Erro ao extrair os resultados para ${algorithm_name} com ${input_file}, Execução ${i}."
            continue
        fi

        # Salvar resultados no arquivo CSV
        echo "${algorithm_name},${input_file},${i},${exec_time},${mem_usage},${path_cost}" >> $output_file
    done
}

# Executar testes para cada algoritmo e arquivo de entrada
for input_file in "${input_files[@]}"; do
    run_test "BFS" "$input_file"
    run_test "DFS" "$input_file"
    run_test "DFS_NO_BACKTRACKING" "$input_file"
    run_test "A_STAR_NO_HEURISTIC" "$input_file"
    run_test "A_STAR_WITH_HEURISTIC" "$input_file"
    run_test "IDA_STAR" "$input_file"
done

echo "Todos os testes foram concluídos. Resultados salvos em $output_file."
