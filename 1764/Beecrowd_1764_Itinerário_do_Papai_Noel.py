# =========================================================================================================================
# Beecrowd - 1764 - Itinerário do Papai Noel - Nivel 3
# =========================================================================================================================
# Teoria: Menor Caminho e Árvore geradora Mínima
# Algoritmo utilizado: Algoritmo de Kruskal
# =========================================================================================================================
# Para facilitar a correçao, foram incluidos no codigo comentarios detalhados, mesmo se desnecessarios :)
# =========================================================================================================================

# ================================================================================================
def iniciarLista(N):            # Função que inicializa o conjunto de elementos
    global C                    
    C = [0]*N
    for i in range(N):
        C[i] = i

# ================================================================================================
def encontrar(i):               # Função que encontra o representante do conjunto ao qual 
    global C                    # o elemento pertence
    if (C[i] == i):
        return i
    C[i] = encontrar(C[i])
    return C[i]

# ================================================================================================
def unir(i, j):                             # Função que une dois conjuntos disjuntos
    C[encontrar(i)] = encontrar(j)

# ================================================================================================
def comparar(i, j):                         # Função que verifica se dois elementos pertencem ao 
    return encontrar(i) == encontrar(j)     # mesmo conjunto

# ================================================================================================
if __name__ == "__main__":
    while True:                                             # Laço principal do programa
        x, y = map(int, input().split())                    # Leitura do número de vértices e arestas 
                                                            # do grafo
        if (x == 0 and y == 0):
            break
        Lista = []
        for i in range(y):                                  # Leitura das arestas do grafo e inserção 
            a, b, custo = map(int, input().split())         # em uma lista
            Lista.append((custo, (a, b)))
        Lista.sort()                                        # Ordenação da lista de arestas em ordem 
                                                            # crescente de peso
        custo_total = 0
        iniciarLista(x)                                     # Inicialização do conjunto de elementos
        for i in range(y):                                  # Laço para percorrer as arestas em ordem 
            custo, (a, b) = Lista[i]                        # crescente de peso
            if not comparar(a, b):
                unir(a, b)                                  # Se os elementos não pertencem ao mesmo 
                                                            # conjunto, une os conjuntos
                custo_total += custo                        # soma do custo total
        print(custo_total)                                  # Impressão do custo total da árvore geradora 
                                                            # mínima
    # ================================================================================================
