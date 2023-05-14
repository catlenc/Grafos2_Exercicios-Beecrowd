# =========================================================================================================================
# Beecrowd - 1123 - desvio de Rota - Nivel 4
# =========================================================================================================================
# Teoria: Menor Caminho e Árvore geradora Mínima
# Algoritmo utilizado: Algoritmo de Dijkstra com vetor de heap minimo para armazenar as arestas candidatas
# =========================================================================================================================
# Para facilitar a correçao, foram incluidos no codigo comentarios detalhados, mesmo se desnecessarios :)
# =========================================================================================================================
# os vizinhos continuam sendo guardados em um vetor com listas encadeadas (lista de adjacencias)
# as arestas candidatas estao sendo guardadas em um vetor de heap minimo - vetor arestas_candidatas
# e a "mancha" esta sendo guardada no vetor conjunto_S
# =========================================================================================================================
import sys  # para obter o maior numero inteiro - sys.maxsize

# =========================================================================================================================
# tratamento da lista de adjacencia - vetor de listas encadeadas
# =========================================================================================================================
class Celula:
    def __init__(self, noh_destino, custo_aresta):  # construtor da classe definido com o metodo 
        self.noh_conectado = noh_destino            # atributos de cada celula
        self.custo_aresta = custo_aresta            # armazenam o noh de destino e o custo da aresta
        self.prox = None                            # aponta para NULL a principio

class ListaEncadeada:
    def __init__(self):             # construtor da classe definido com o metodo init sem parametros
        self.prox_cabeca = None     # quando a lista eh construida ela possui apenas a celula cabeca que
                                    # aponta para NULL e nao contem dado

    # metodo que recebe os parametos "noh" e "custo" e insere apos a cabeca e antes do resto da lista
    def inserir_no_inicio(self, noh, custo):
        nova_celula = Celula(noh, custo)        # instancia a nova celula com os valores passados
        nova_celula.prox = self.prox_cabeca     # faz a nova celula apontar para quem a cabeca aponta 
        self.prox_cabeca = nova_celula          # e faz a celula cabeca apontar para a nova celula

    # impressao apenas para testes durante o debug
    def imprimir(self, noh_origem):
        if self.prox_cabeca is None:                # verifica se a lista encadeada esta vazia
            print()   
        else:
            celula_atual = self.prox_cabeca         # comeca da primeira celula
            while celula_atual is not None:         # verifica se nao chegou ao fim
                print('{:>2}, ({:>1}), {:>1}'.format(celula_atual.custo_aresta, celula_atual.noh_conectado-1, noh_origem-1))
                                                    # imprime uma por uma
                celula_atual = celula_atual.prox    # passa pra proxima celula

class VetorDeListasEncadeadas:
    def __init__(self, tam):    # construtor da classe definido com o metodo init 
        self.tamanho = tam      # guarda o tamanho do vetor no atributo tamanho
        self.vetor_LE = [ListaEncadeada() for i in range(tam+1)] 
                                # cria o vetor do tamanho especificado usando o construtor
                                # e inicializando todos elementos so com celula cabeca apontando para NULL
# =========================================================================================================================

# =========================================================================================================================
# tratamento de heap minimo - vetor que simula a arvore do heap
# =========================================================================================================================
class Heap:
    def __init__(self, valor_custo, noh_onde_esta, noh_de_onde_veio):   # construtor da classe definido com o metodo init   
        self.custo = valor_custo                      # atributos da classe
        self.noh_onde_esta = noh_onde_esta
        self.noh_de_onde_veio = noh_de_onde_veio 

class Hash:
    def __init__(self, posicao):                # construtor da classe definido com o metodo init  
        self.posicao = posicao                  # atributos da classe

class VetorHeap:
    def __init__(self, tam):        # construtor da classe definido com o metodo init recebe parametro "tam" - tamanho do vetor
        self.tamanho_heap = tam     # guarda o tamanho do vetor heap no atributo tamanho
        self.tamanho_hash = tam     # guarda o tamanho do vetor hash no atributo tamanho
        self.vetor_heap = [Heap(0, 0, 0) for i in range(tam+1)] # cria o vetor do tamanho especificado usando o construtor
        self.vetor_hash = [Hash(0) for i in range(tam+1)] 
                                    
    # metodo de impressao apenas para testes durante o debug
    def imprimir_heap(self):
        for i in range(1, self.tamanho_heap + 1):
            print(f'{self.vetor_heap[i][0]}, ({self.vetor_heap[i][1]}), {self.vetor_heap[i][2]}') 

    # metodo de impressao apenas para testes durante o debug
    def imprimir_hash(self):
        for i in range(1, self.tamanho_hash + 1):
            print(f'{i} - {self.vetor_hash[i]}') 
    
    # metodo que inicializa o heap com valores maximos de int para as distancias e coloca 
    # os nohs apontando para eles mesmos 
    def inicializar_heap(self, qtde_nohs):
        for j in range(1, qtde_nohs+1):
            self.vetor_hash[j] = j
        for i in range(1, qtde_nohs+1):
            self.vetor_heap[i] = [sys.maxsize, i, i]

    # metodo que faz o noh "subir" de nivel na arvore, se ele nao estiver no lugar errado
    def shift_up_no_heap(self, indice_shift):
        # determina pai
        pai = indice_shift // 2
        if pai == 0:
            return
        elif self.vetor_heap[indice_shift][0] < self.vetor_heap[pai][0]:
            # swap
            self.vetor_heap[indice_shift], self.vetor_heap[pai] = self.troca(self.vetor_heap[indice_shift], self.vetor_heap[pai])
            self.vetor_hash[self.vetor_heap[indice_shift][1]] = indice_shift
            self.vetor_hash[self.vetor_heap[pai][1]] = pai
            indice_shift = pai
            self.shift_up_no_heap(indice_shift)
        else:
            return

    # metodo para trocar valores 
    def troca(self, origem, destino):
        aux = origem
        origem = destino
        destino = aux
        return origem, destino

        
    # metodo para fazer o noh "descer" de nivel na arvore do heap se ele estiver em local errado
    def heapify_no_heap(self, indice_heapify):
        if (indice_heapify * 2) > self.tamanho_heap:
            return
        # determina filhos
        filho_esquerdo = indice_heapify * 2
        filho_direito = (indice_heapify * 2) + 1
        # verifica qual o menor
        # o ultimo "pai" tem dois filhos - esq e dir
        if (indice_heapify * 2) + 1 <= self.tamanho_heap:
            if self.vetor_heap[filho_esquerdo][0] < self.vetor_heap[filho_direito][0]:
                menor_dos_dois_filhos = filho_esquerdo
            else:
                menor_dos_dois_filhos = filho_direito
        # o ultimo "pai" so tem o filho esquerdo
        else:
            if (indice_heapify * 2) <= self.tamanho_heap:
                menor_dos_dois_filhos = filho_esquerdo
            else:
                return
        # faz a troca se for maior
        if (self.vetor_heap[indice_heapify][0] > self.vetor_heap[menor_dos_dois_filhos][0]):
            # swap
            self.vetor_heap[indice_heapify], self.vetor_heap[menor_dos_dois_filhos] = self.troca(self.vetor_heap[indice_heapify], self.vetor_heap[menor_dos_dois_filhos])
            self.vetor_hash[self.vetor_heap[indice_heapify][1]] = indice_heapify
            self.vetor_hash[self.vetor_heap[menor_dos_dois_filhos][1]] = menor_dos_dois_filhos
            indice_heapify = menor_dos_dois_filhos
            self.heapify_no_heap(indice_heapify)
        else:
            return


    # ================================================================================================
    # algoritmo recursivo de dijkstra -  modificado para, a partir de um novo grafo com a rota incluida,
    # ao encontrar uma cidade da rota para de procurar o menor custo e segue a rota ate o destino
    # ================================================================================================
    def dikstra_adaptado(self, noh_escolhido, noh_final):
        # se alcancar o noh_final, sai da recursao
        if noh_escolhido == noh_final:
            return
        # olha os vizinhos percorrendo lista encadeada daquele noh e salva as arestas candidatas no vetor
        if grafo.vetor_LE[noh_escolhido].prox_cabeca is not None:           # verifica se a lista encadeada esta vazia
            prox_noh_vizinho = grafo.vetor_LE[noh_escolhido].prox_cabeca    # comeca da primeira celula
            #print(prox_noh_vizinho.noh_conectado)
            while prox_noh_vizinho is not None:                             # verifica se a LE nao chegou ao fim
                # verifica se o noh ja foi visitado e compara se achou um menor caminho ate ele
                # se menor, sobrescreve, se nao, nao faz nada
                # armazena por noh a informacao de menos custo
                indice_prox_noh_vizinho = self.vetor_hash[prox_noh_vizinho.noh_conectado]
                if prox_noh_vizinho.custo_aresta + conjunto_S[noh_escolhido][0] < self.vetor_heap[indice_prox_noh_vizinho][0]:
                    # insere no heap e rearranja "subindo" o noh se necessario
                    indice_inserir = self.vetor_hash[prox_noh_vizinho.noh_conectado]
                    self.vetor_heap[indice_inserir] = [prox_noh_vizinho.custo_aresta + conjunto_S[noh_escolhido][0],
                                                        prox_noh_vizinho.noh_conectado, noh_escolhido]
                    self.shift_up_no_heap(indice_inserir)
                prox_noh_vizinho = prox_noh_vizinho.prox                            # passa pra proxima celula

        # pega a raiz do MIN HEAP
        menor_custo = self.vetor_heap[1][0]
        noh_escolhido = self.vetor_heap[1][1]
        noh_anterior = self.vetor_heap[1][2]
        # se aquele noh ja entrou na "mancha", verifica se o caminho eh melhor
        if (conjunto_S[noh_escolhido] is not None):
            if conjunto_S[noh_escolhido][0] < menor_custo:
                conjunto_S[noh_escolhido] = [menor_custo, noh_anterior]
        # se nao entrou, inclui noh na "mancha"
        else:
            conjunto_S[noh_escolhido] = [menor_custo, noh_anterior]
        # "apaga" das arestas candidatas aquela do noh que foi escolhido para entrar na "mancha"
        # reorganizar heap sem apagar o noh
        self.vetor_heap[1][0] = sys.maxsize
        self.heapify_no_heap(1)
        
        # chama a funcao novamente de forma recursiva ate encontrar o noh final de interesse
        self.dikstra_adaptado(noh_escolhido, noh_final)

# ================================================================================================

# ================================================================================================
# funcao recursiva para imprimir o menor caminho encontrado
# ================================================================================================
def imprime_caminho_encontrado(noh_inicial, noh_final): # imprimir o caminho com os custos entre os nohs
        if (noh_final == noh_inicial):
            return
        noh_final = conjunto_S[noh_final][1]        # comeca do ultimo noh e vai voltando
        imprime_caminho_encontrado(noh_inicial, noh_final) # chama recursivamente ate chegar no noh inicial
        print(f'({noh_final-1})', end="->")      
        
        
        
             # como o print vem depois do fechamento da recursao, 
                                                    # imprime em "ordem inversa"
# ================================================================================================

# ================================================================================================
if __name__ == "__main__":

    # ===============================================================================
    # ENTRADA
    # ===============================================================================
    # A entrada contém vários casos de teste. A primeira linha de um caso de teste contém 
    # quatro inteiros N, M, C e K (4 ≤ N ≤ 250, 3 ≤ M ≤ N×(N−1)/2, 2 ≤ C ≤ N−1 e C ≤ K ≤ N−1), 
    # representando, respectivamente, o número de cidades do país, o número de estradas, 
    # o número de cidades na rota de serviço e a cidade em que o veículo foi consertado. 
    # As cidades são identificadas por inteiros de 0 a N−1. A rota de serviço é 0, 1, ... , C−1, 
    # ou seja, a origem é 0, de 0 passa para 1, de 1 para 2 e assim por diante, até o destino C−1.
    N, M, C, K = input().split()
    # O último caso de teste é seguido por uma linha contendo quatro zeros separados por espaço em branco.
    while N !='0' and M != '0' and C != '0' and K != '0':
        N_nohs_cidades_no_pais = int(N)
        M_qtd_arestas_estradas = int(M)
        C_nohs_cidades_rota = int(C)
        K_cidade_origem = int(K)
        ultima_cidade_rota = C_nohs_cidades_rota - 1 
        # montagem do grafo - lista de adjacencias
        grafo = VetorDeListasEncadeadas(N_nohs_cidades_no_pais)
        # As M linhas seguintes descrevem o sistema rodoviário do país. Cada uma dessas linhas 
        # descreve uma estrada e contém três inteiros U, V e P (0 ≤ U, V ≤ N−1, U ≠ V, 0 ≤ P ≤ 250), 
        # indicando que há uma estrada interligando as cidades U e V com custo de pedágio P.
        for i in range(1, M_qtd_arestas_estradas+1):
            U, V, P = input().split()
            U_noh_origem = int(U)
            V_noh_destino = int(V)
            P_custo_aresta = int(P)
            # se o noh de origem pertencer a rota, so vai incluir a aresta que liga ao no seguinte da rota
            # para atender as exigencias do problema foi criado um grafo diferente, levando em conta 
            # a rota que deve ser obedecida
            if U_noh_origem > C_nohs_cidades_rota-1:  # noh cidade fora da rota
                # noh1 -> noh2
                grafo.vetor_LE[U_noh_origem+1].inserir_no_inicio(V_noh_destino+1, P_custo_aresta)
                # noh2 -> noh 1
                grafo.vetor_LE[V_noh_destino+1].inserir_no_inicio(U_noh_origem+1, P_custo_aresta)
            else:
                if V_noh_destino == U_noh_origem + 1:
                    # noh1 -> noh2
                    grafo.vetor_LE[U_noh_origem+1].inserir_no_inicio(V_noh_destino+1, P_custo_aresta)
                else:
                    # ignora a estrada que liga as cidades da rota fora de ordem ou com outros 
                    # nohs for da rota
                    # mas nao ignora as estradas que chegam no noh da rota vindo de qq lugar
                    grafo.vetor_LE[V_noh_destino+1].inserir_no_inicio(U_noh_origem+1, P_custo_aresta)

        # ===============================================================================
        # SOLUCAO - Algoritmo de Dijkstra adaptado
        # ===============================================================================
        conjunto_S = [None] * (N_nohs_cidades_no_pais+1)
        conjunto_S[K_cidade_origem+1] = [0, K_cidade_origem+1]
        #print(conjunto_S)
        arestas_candidatas = VetorHeap(N_nohs_cidades_no_pais)  
        arestas_candidatas.inicializar_heap(N_nohs_cidades_no_pais)
        # chama a funcao que usa o algoritmo de dijkstra modificado
        arestas_candidatas.dikstra_adaptado(K_cidade_origem+1, ultima_cidade_rota+1)
        
        # ===============================================================================
        # SAIDA
        # ===============================================================================
        print(conjunto_S[ultima_cidade_rota+1][0])

        N, M, C, K = input().split()

# ================================================================================================
