"""
Grafo direcionado implementado sem uso de bibliotecas externas. Contém métodos de busca e ordenação topológica. Cada vértice representa um pacote e cada aresta direcionada representa uma dependência entre pacotes.
A implementação é baseada em listas de adjacência para armazenar sucessores e predecessores, permitindo consultas eficientes sobre dependências e pré-requisitos. O grafo suporta a adição de vértices e arestas, evitando duplicações e garantindo a integridade das relações de dependência.

Complexidade: espaço O(V + E); inserção de vértice e de aresta em O(1) amortizado;
Kahn, DFS de ciclo e BFS de dependentes em O(V + E).
"""

from collections import deque


class Graph:
    def __init__(self):
        # Lista de adjacência de sucessores: {u: [v1, v2]} -> guarda quem depende de u
        self.vertices = {}
        # Lista de adjacência inversa (predecessores): {v: [u1, u2]} -> guarda pré-requisitos de v
        self.predecessores = {}
        # Lista com todas as arestas do grafo no formato (origem, destino), em ordem de inserção
        self.arestas = []
        # Conjunto auxiliar das arestas: checagem de duplicata em O(1) em vez de O(E)
        self._arestas_set = set()

    def add_vertice(self, v):
        """Adiciona um novo vértice ao grafo caso ele ainda não exista."""
        if v not in self.vertices:
            self.vertices[v] = []
            self.predecessores[v] = []

    def add_aresta(self, u, v):
        """
        Adiciona uma aresta direcionada u -> v (v depende de u).
        Garante que ambos os vértices existam e evita duplicar arestas.
        """
        self.add_vertice(u)
        self.add_vertice(v)
        aresta = (u, v)
        if aresta not in self._arestas_set:
            self._arestas_set.add(aresta)
            self.arestas.append(aresta)
            self.vertices[u].append(v)        # u aponta para v (v é dependente de u)
            self.predecessores[v].append(u)   # u é pré-requisito de v

    def vizinhos(self, v):
        """Retorna a lista de sucessores (pacotes que dependem de v)."""
        return self.vertices.get(v, [])

    def obter_predecessores(self, v):
        """Retorna a lista de predecessores (pré-requisitos diretos de v)."""
        return self.predecessores.get(v, [])

    def grau_entrada(self, v):
        """
        Retorna o grau de entrada de v (quantidade de pré-requisitos pendentes).
        Vértices com grau 0 são pacotes base e podem ser instalados primeiro.
        """
        return len(self.predecessores.get(v, []))

    def __repr__(self):
        return f"Graph(V={len(self.vertices)}, E={len(self.arestas)})"

    def kahn(self):
        """
        Implementa o algoritmo de Kahn para ordenação topológica.
        Retorna (True, ordem, camadas) para um grafo acíclico.
        Quando há ciclo, retorna (False, None, None).
        """
        graus = {v: self.grau_entrada(v) for v in self.vertices}
        fila = [v for v in self.vertices if graus[v] == 0]
        ordem = []
        camadas = []

        while fila:
            camada_atual = list(fila)
            camadas.append(camada_atual)

            proximo_fila = []
            for u in camada_atual:
                ordem.append(u)
                for v in self.vizinhos(u):
                    graus[v] -= 1
                    if graus[v] == 0:
                        proximo_fila.append(v)
            fila = proximo_fila

        if len(ordem) == len(self.vertices):
            return True, ordem, camadas
        return False, None, None

    def dfs_ciclo(self):
        """
        Detecta e reconstrói o caminho de um ciclo usando DFS com 3 estados.
        Retorna uma lista com o ciclo fechado [A, B, ..., A] ou None se for acíclico.
        
        Estados:
            0 = Não visitado (branco)
            1 = Ativo na pilha de busca atual (cinza)
            2 = Encerrado/processado (preto)

        Implementação iterativa (pilha explícita de iteradores): não depende do limite
        de recursão do Python, então funciona em cadeias longas (milhares de vértices).
        `posicao` guarda o índice de cada vértice cinza em `caminho`, permitindo
        recortar o ciclo em O(1) para localizar o início (em vez de caminho.index, O(V)).
        A ordem de visita é a mesma da versão recursiva.
        """
        estado = {v: 0 for v in self.vertices}

        for origem in self.vertices:
            if estado[origem] != 0:
                continue

            estado[origem] = 1  # Cinza (ativo na busca atual)
            caminho = [origem]
            posicao = {origem: 0}
            pilha = [iter(self.vertices[origem])]

            while pilha:
                avancou = False
                for v in pilha[-1]:
                    if estado[v] == 1:
                        # Aresta de retorno para vértice cinza: encontrou ciclo!
                        return caminho[posicao[v]:] + [v]
                    if estado[v] == 0:
                        estado[v] = 1
                        posicao[v] = len(caminho)
                        caminho.append(v)
                        pilha.append(iter(self.vertices[v]))
                        avancou = True
                        break

                if not avancou:
                    # Todos os sucessores processados: vértice encerrado.
                    u = caminho.pop()
                    del posicao[u]
                    estado[u] = 2  # Preto (encerrado)
                    pilha.pop()
        return None
        
    def dependentes_transitivos(self, v):
        """
        Retorna um conjunto (set) com todos os pacotes que dependem de v
        direta ou indiretamente (efeito cascata de remoção).
        Utiliza Busca em Largura (BFS).
        """
        if v not in self.vertices:
            return set()

        # Uma origem alcançada por um caminho não vazio também é visitada.
        visitados = set(self.vertices[v])
        fila = deque(self.vertices[v])
        while fila:
            atual = fila.popleft()
            for proximo in self.vertices[atual]:
                if proximo not in visitados:
                    visitados.add(proximo)
                    fila.append(proximo)
        return visitados
