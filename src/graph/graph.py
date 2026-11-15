"""
Grafo direcionado implementado sem uso de bibliotecas externas.
"""

class Graph:
    def __init__(self):
        # Lista de adjacência de sucessores: {u: [v1, v2]} -> guarda quem depende de u
        self.vertices = {}
        # Lista de adjacência inversa (predecessores): {v: [u1, u2]} -> guarda pré-requisitos de v
        self.predecessores = {}
        # Lista com todas as arestas do grafo no formato (origem, destino)
        self.arestas = []

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
        if aresta not in self.arestas:
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