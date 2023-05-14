# =========================================================================================================================
# Beecrowd - 2404 - Reduzindo Detalhes em um Mapa - Nivel 3
# =========================================================================================================================
# Teoria: Menor Caminho e Árvore geradora Mínima
# Algoritmo utilizado: Algoritmo de Prim otimizado com heap para armazenar e ordenar as arestas candidatas
# =========================================================================================================================
# Para facilitar a correçao, foram incluidos no codigo comentarios detalhados, mesmo se desnecessarios :)
# =========================================================================================================================
# os vizinhos continuam sendo guardados em um vetor com listas encadeadas (lista de adjacencias)
# as arestas candidatas estao sendo guardadas em um vetor de heap minimo - vetor arestas_candidatas
# e a "mancha" ou o corte esta sendo guardado no vetor conjunto_S
# =========================================================================================================================
import sys  # para pegar o maior numero inteiro possivel

# =========================================================================================================================
# tratamento da lista de adjacencia - vetor de listas encadeadas
# =========================================================================================================================
class Celula:
    def __init__(self, noh_destino, custo_aresta):  # construtor da classe definido com o metodo 
        self.noh_conectado = noh_destino            # atributos de cada celula 
        self.custo_aresta = custo_aresta            # armazenam para onde o noh vai e a qual custo 
        self.prox = None                            

# ================================================================================================
class ListaEncadeada:
    def __init__(self):             # construtor da classe definido com o metodo init sem parametros
        self.prox_cabeca = None     # quando a lista eh construida ela possui apenas a celula cabeca que
                                    # aponta para NULL e nao contem dado

    # metodo que recebe os parametos e insere apos a cabeca e antes do resto da lista
    def inserir_no_inicio(self, noh, custo):
        nova_celula = Celula(noh, custo)    # instancia a nova celula com os valores passados
        nova_celula.prox = self.prox_cabeca # faz a nova celula apontar para quem a cabeca aponta 
        self.prox_cabeca = nova_celula      # e faz a celula cabeca apontar para a nova celula

    # metodo de impressao apenas para debug
    def imprimir(self, noh_origem):
        if self.prox_cabeca is None:                # verifica se a lista encadeada esta vazia
            print()   
        else:
            celula_atual = self.prox_cabeca         # comeca da primeira celula
            while celula_atual is not None:         # verifica se nao chegou ao fim
                print('{:>2}, ({:>1}), {:>1}'.format(celula_atual.custo_aresta, 
                                                     celula_atual.noh_conectado, noh_origem))
                                                    # imprime uma por uma
                celula_atual = celula_atual.prox    # passa pra proxima celula

# ================================================================================================
class VetorDeListasEncadeadas:
    def __init__(self, tam):    # construtor da classe definido com o metodo init 
        self.tamanho = tam      # guarda o tamanho do vetor no atributo tamanho
        self.vetor_LE = [ListaEncadeada() for i in range(tam)] 
                                # cria o vetor do tamanho especificado usando o construtor
                                # e inicializando todos elementos so com celula cabeca apontando para NULL

# =========================================================================================================================
# tratamento de heap minimo - vetor que simula a arvore do heap
# =========================================================================================================================
class Heap:
    def __init__(self, valor_custo, aresta, noh_de_onde_veio):   # construtor da classe definido com o metodo init   
        self.custo = valor_custo                      # atributos da classe
        self.aresta = aresta
        self.noh_de_onde_veio = noh_de_onde_veio 

class Hash:
    def __init__(self, posicao):                # construtor da classe definido com o metodo init  
        self.posicao = posicao                  # atributos da classe

class VetorHeap:
    def __init__(self, tam):        # construtor da classe definido com o metodo init recebe parametro "tam" que eh o tamanho do vetor
        self.tamanho_heap = tam          # guarda o tamanho do vetor no atributo tamanho
        self.tamanho_hash = tam          # guarda o tamanho do vetor no atributo tamanho
        self.vetor_heap = [Heap(0, 0, 0) for i in range(tam+1)] # cria o vetor do tamanho especificado usando o construtor
        self.vetor_hash = [Hash(0) for i in range(tam+1)] 
                                    
    # metodo de impressao apenas para testes durante o debug
    def imprimir_heap(self):
        for i in range(1, self.tamanho_heap + 1):
            print(f'{self.vetor_heap[i][0]}, {self.vetor_heap[i][1]}')
        return 

    # metodo de impressao apenas para testes durante o debug
    def imprimir_hash(self):
        for i in range(1, self.tamanho_hash + 1):
            print(f'{i} - {self.vetor_hash[i]}')
        return 
    
    # metodo que inicializa o heap com valores maximos de int para as distancias e coloca 
    # os nohs apontando para eles mesmos 
    def inicializar_heap(self, qtde_nohs):
        for j in range(1, qtde_nohs+1):
            self.vetor_hash[j] = j
        for i in range(1, qtde_nohs+1):
            self.vetor_heap[i] = [sys.maxsize, chr(i+64)+chr(i+64), i]
        return

    def inserir_no_heap(self, valor_custo, aresta, noh_onde_esta):
        indice_inserir = self.vetor_hash[noh_onde_esta]
        if self.vetor_heap[indice_inserir][0] > valor_custo:
            self.vetor_heap[indice_inserir] = [valor_custo, aresta]
        else:
            return
        self.shift_up_no_heap(indice_inserir)
        return

    def shift_up_no_heap(self, indice_shift):
        # determina pai
        pai = indice_shift // 2
        if pai == 0:
            return
        elif self.vetor_heap[indice_shift][0] < self.vetor_heap[pai][0]:
            # swap
            self.vetor_heap[indice_shift], self.vetor_heap[pai] = self.troca(self.vetor_heap[indice_shift], self.vetor_heap[pai])
            #print(self.vetor_heap[indice_shift][1])
            indice = ord(self.vetor_heap[indice_shift][1][1:])-64
            indice_pai = ord(self.vetor_heap[pai][1][1:])-64
            self.vetor_hash[indice] = indice_shift
            self.vetor_hash[indice_pai] = pai
            indice_shift = pai
            self.shift_up_no_heap(indice_shift)
        else:
            return

    def troca(self, origem, destino):
        aux = origem
        origem = destino
        destino = aux
        return origem, destino

    def reorganizar_heap(self, indice_reorganizar):
        self.vetor_heap[indice_reorganizar][0] = sys.maxsize
        self.heapify_no_heap(indice_reorganizar)
        return
        
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
            menor_dos_dois_filhos = filho_esquerdo
        # faz a troca se for maior
        if (self.vetor_heap[indice_heapify][0] > self.vetor_heap[menor_dos_dois_filhos][0]):
            # swap
            self.vetor_heap[indice_heapify], self.vetor_heap[menor_dos_dois_filhos] = self.troca(self.vetor_heap[indice_heapify], self.vetor_heap[menor_dos_dois_filhos])
            indice = ord(self.vetor_heap[indice_heapify][1][1:])-64
            indice_menor_filho = ord(self.vetor_heap[menor_dos_dois_filhos][1][1:])-64
            self.vetor_hash[indice] = indice_heapify
            self.vetor_hash[indice_menor_filho] = menor_dos_dois_filhos
            indice_heapify = menor_dos_dois_filhos
            self.heapify_no_heap(indice_heapify)
        else:
            return

    def prim_com_heap(self, noh_escolhido, qtde_nohs, custo_total):

            # olha os vizinhos percorrendo lista encadeada daquele noh e salva as arestas candidatas no vetor
            if grafo.vetor_LE[noh_escolhido].prox_cabeca is not None:           # verifica se a lista encadeada esta vazia
                prox_noh_vizinho = grafo.vetor_LE[noh_escolhido].prox_cabeca        # comeca da primeira celula
                while prox_noh_vizinho is not None:             # verifica se a LE nao chegou ao fim
                    #print(prox_noh_vizinho.noh_conectado)
                    if conjunto_S[prox_noh_vizinho.noh_conectado] is None:
                        self.inserir_no_heap(prox_noh_vizinho.custo_aresta, 
                                                chr(noh_escolhido+64) + chr(prox_noh_vizinho.noh_conectado+64), prox_noh_vizinho.noh_conectado)
                    prox_noh_vizinho = prox_noh_vizinho.prox                            # passa pra proxima celula
            
            menor_custo = self.vetor_heap[1][0]
            aresta_escolhida = self.vetor_heap[1][1]
            noh_que_vai_para_S = self.vetor_heap[1][1][1:]
            noh_escolhido = ord(noh_que_vai_para_S)-64
            # se aquele noh ja entrou na "mancha", verifica se o caminho eh melhor
            if (conjunto_S[noh_escolhido] is not None):
                conjunto_S[noh_escolhido] = noh_que_vai_para_S
                arestas_T.append(aresta_escolhida)
            # se nao entrou, inclui noh na "mancha"
            else:
                conjunto_S[noh_escolhido] = noh_que_vai_para_S
                arestas_T.append(aresta_escolhida)
            self.reorganizar_heap(1)
            custo_total = custo_total + menor_custo
        
            if len(arestas_T) == qtde_nohs-1:
                return custo_total
            else:
                # chama a funcao novamente de forma recursiva ate encontrar o noh final de interesse
                return self.prim_com_heap(noh_escolhido, qtde_nohs, custo_total)

# ================================================================================================


# ================================================================================================
if __name__ == "__main__":

        # ===============================================================================
        # ENTRADA
        # ===============================================================================
        # A primeira linha da entrada contém dois números N (1 ≤ N ≤ 500) e M ( 1 ≤ M ≤ 124750 )
        # que representam onúmero de cidades e o número de rodovias respectivamente.
        N, M = input().split()
        N_qtd_nohs = int(N)
        M_qtd_arestas = int(M)
        noh_inicial = 1
        grafo = VetorDeListasEncadeadas(N_qtd_nohs + 1)
        # Cada uma das próximas M linhas é composta portrês inteiros U, V (1 ≤ U, V ≤ N e U ≠ V) 
        # e C (1 ≤ C ≤ 500) que indiciam que existe uma rodovia decomprimento C que liga 
        # as cidades U e V.
        # montagem do grafo - lista de adjacencias
        for i in range(1, M_qtd_arestas + 1):
            noh_origem, noh_destino, custo_aresta = input().split()
            # noh1 -> noh2
            grafo.vetor_LE[int(noh_origem)].inserir_no_inicio(int(noh_destino), int(custo_aresta))
            # noh2 -> noh1
            grafo.vetor_LE[int(noh_destino)].inserir_no_inicio(int(noh_origem), int(custo_aresta))

        # ===============================================================================
        # SOLUCAO - Algoritmo de Prim otimizado com heap
        # ===============================================================================
        conjunto_S = [None] * (N_qtd_nohs + 1)
        conjunto_S[noh_inicial] = chr(noh_inicial+64)
        arestas_candidatas = VetorHeap(N_qtd_nohs)  
        arestas_candidatas.inicializar_heap(N_qtd_nohs)
        arestas_T = []
        # comeca do noh inicial
        noh_escolhido = noh_inicial
        custo_total = 0
        # chama a funcao que usa o algoritmo de dijkstra
        custo_total = arestas_candidatas.prim_com_heap(noh_escolhido, N_qtd_nohs, custo_total)

        # ===============================================================================
        # SAIDA
        # ===============================================================================
        # A saída consiste em apenas uma linha contendo a soma do comprimento das rodovias selecionadas.
        print(custo_total)
        
# ================================================================================================