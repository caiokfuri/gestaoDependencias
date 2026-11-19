"""Grafo dirigido próprio, iniciado por Caio Alves Kfuri, sem biblioteca de grafos.

A → B significa que B depende de A. Consultas têm custo O(V + E).
"""


class CycleError(ValueError):
    """Não existe ordenação topológica completa."""


class Graph:
    def __init__(self):
        self.vertices = {}
        self.nodes = {}
        self.edges = {}
        self.predecessores = {}

    @property
    def arestas(self):
        return list(self.edges)

    def __iter__(self):
        return iter(self.vertices)

    def __len__(self):
        return len(self.vertices)

    def __contains__(self, v):
        return v in self.vertices

    def add_vertice(self, v, **atributos):
        if v not in self.vertices:
            self.vertices[v] = []
            self.predecessores[v] = []
            self.nodes[v] = {}
        self.nodes[v].update(atributos)

    def add_aresta(self, u, v, **atributos):
        self.add_vertice(u)
        self.add_vertice(v)
        if (u, v) not in self.edges:
            self.vertices[u].append(v)
            self.predecessores[v].append(u)
            self.edges[u, v] = {}
        self.edges[u, v].update(atributos)

    # Nomes mantidos para os consumidores do protótipo; implementação própria.
    add_node = add_vertice
    add_edge = add_aresta

    def add_nodes_from(self, vertices):
        for v in vertices:
            self.add_vertice(v)

    def has_edge(self, u, v):
        return (u, v) in self.edges

    def number_of_edges(self):
        return len(self.edges)

    def vizinhos(self, v):
        return list(self.vertices.get(v, []))

    def geracoes(self):
        """Kahn com fila por camadas e cópia dos graus, sem alterar o grafo."""
        graus = {v: len(self.predecessores[v]) for v in self.vertices}
        camada = [v for v in self.vertices if graus[v] == 0]
        resultado = []
        processados = 0
        while camada:
            resultado.append(camada)
            processados += len(camada)
            proxima = []
            for u in camada:
                for v in self.vertices[u]:
                    graus[v] -= 1
                    if graus[v] == 0:
                        proxima.append(v)
            camada = proxima
        if processados != len(self):
            raise CycleError("O grafo contém um ciclo; não há ordem completa.")
        return resultado

    def kahn(self):
        """Ordem topológica FIFO; rejeita ciclos em qualquer componente."""
        return [v for camada in self.geracoes() for v in camada]

    def dfs_cicle(self):
        """DFS iterativa branco/cinza/preto; retorna um ciclo fechado ou []."""
        cores = {v: 0 for v in self.vertices}
        for inicio in self.vertices:
            if cores[inicio]:
                continue
            caminho = [inicio]
            posicoes = {inicio: 0}
            cores[inicio] = 1
            pilha = [(inicio, iter(self.vertices[inicio]))]
            while pilha:
                u, vizinhos = pilha[-1]
                try:
                    v = next(vizinhos)
                except StopIteration:
                    pilha.pop()
                    cores[u] = 2
                    posicoes.pop(u)
                    caminho.pop()
                    continue
                if cores[v] == 1:
                    return caminho[posicoes[v]:] + [v]
                if cores[v] == 0:
                    cores[v] = 1
                    posicoes[v] = len(caminho)
                    caminho.append(v)
                    pilha.append((v, iter(self.vertices[v])))
        return []

    def dependentes(self, origem):
        """Sucessores transitivos, excluindo a origem mesmo quando há ciclo."""
        if origem not in self:
            raise KeyError(origem)
        visitados = {origem}
        fila = [origem]
        indice = 0
        while indice < len(fila):
            u = fila[indice]
            indice += 1
            for v in self.vertices[u]:
                if v not in visitados:
                    visitados.add(v)
                    fila.append(v)
        visitados.remove(origem)
        return visitados

    def __repr__(self):
        return f"Graph(V={len(self)}, E={len(self.edges)})"
