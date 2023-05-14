# =========================================================================================================================
# Beecrowd - 1152 - Estradas Escuras - Nivel 5
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

# ================================================================================================
def encontrar(i):               # Função que encontra o representante do conjunto ao qual 
    global C                    # o elemento pertence
    if (C[i] == i):
        return i
    C[i] = encontrar(C[i])
    return C[i]
# ================================================================================================

# ================================================================================================
def comparar(i, j):                       # Função que verifica se dois elementos pertencem ao 
    return encontrar(i) == encontrar(j)   # mesmo conjunto
# ================================================================================================


# ================================================================================================
def unir(i, j):                        # Função que une dois conjuntos disjuntos
    C[encontrar(i)] = encontrar(j)
# ================================================================================================

# ================================================================================================
while True:                                             # Laço principal do programa

    x, y = map(int, input().split())                    # Leitura do número de vértices e arestas 
                                                        # do grafo
    if (x == 0 and y == 0):
        break
    
    Lista = []

    custo_iluminacao = 0                                # custo gasto com iluminação

    for i in range(y):                                  # Leitura das arestas do grafo e inserção 
        a, b, custo = map(int, input().split())         # em uma lista
        Lista.append((custo, (a, b)))
        custo_iluminacao = custo + custo_iluminacao
    
    Lista.sort()                                        # Ordenação da lista de arestas em ordem 
                                                        # crescente de peso

    custo_total = 0
    iniciarLista(x)                                     # Inicialização do conjunto de elementos
    
    for i in range(y):                                  # Laço para percorrer as arestas em ordem 
        custo, (a, b) = Lista[i]                        # crescente de peso
        
        if not comparar(a, b):
            unir(a, b)                                  # Se os elementos não pertencem ao mesmo 
                                                        # conjunto, une os conjuntos
            
            custo_total += custo                       # soma do custo total da arvore geradora minima
    
    print(custo_iluminacao - custo_total)               # Impressão do custo de iluminação 
                                                        # economizado

# ================================================================================================
