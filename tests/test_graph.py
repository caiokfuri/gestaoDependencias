import sys
import os
import unittest

# Garante que a pasta raiz esteja no path, permitindo rodar de qualquer lugar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.graph.graph import Graph


class TestGraphEstrutura(unittest.TestCase):

    def setUp(self):
        self.g = Graph()

    def test_inicializacao_vazia(self):
        """Verifica se o grafo inicializa sem vértices e sem arestas."""
        self.assertEqual(len(self.g.vertices), 0)
        self.assertEqual(len(self.g.predecessores), 0)
        self.assertEqual(len(self.g.arestas), 0)

    def test_adicionar_vertice(self):
        """Verifica adição de vértices isolados."""
        self.g.add_vertice("libcore")
        self.assertIn("libcore", self.g.vertices)
        self.assertIn("libcore", self.g.predecessores)
        self.assertEqual(self.g.vizinhos("libcore"), [])
        self.assertEqual(self.g.obter_predecessores("libcore"), [])

    def test_adicionar_aresta_direcionada(self):
        """
        Verifica se a aresta u -> v:
        1. Cria ambos os vértices automaticamente.
        2. Adiciona v como vizinho (sucessor) de u.
        3. Adiciona u como predecessor de v.
        """
        self.g.add_aresta("libssl", "curl")

        self.assertIn(("libssl", "curl"), self.g.arestas)
        self.assertEqual(self.g.vizinhos("libssl"), ["curl"])
        self.assertEqual(self.g.obter_predecessores("curl"), ["libssl"])

    def test_evitar_arestas_duplicadas(self):
        """Verifica se adicionar a mesma aresta duas vezes não duplica a relação."""
        self.g.add_aresta("A", "B")
        self.g.add_aresta("A", "B")

        self.assertEqual(len(self.g.arestas), 1)
        self.assertEqual(self.g.vizinhos("A"), ["B"])
        self.assertEqual(self.g.obter_predecessores("B"), ["A"])

    def test_grau_entrada(self):
        """Verifica o cálculo de pré-requisitos pendentes (grau de entrada)."""
        self.g.add_aresta("libz", "libpng")
        self.g.add_aresta("libpng", "app")
        self.g.add_aresta("libcore", "app")

        self.assertEqual(self.g.grau_entrada("libz"), 0)
        self.assertEqual(self.g.grau_entrada("libcore"), 0)
        self.assertEqual(self.g.grau_entrada("libpng"), 1)
        self.assertEqual(self.g.grau_entrada("app"), 2)

    def test_caso_borda_auto_laco(self):
        """
        CASO PROBLEMÁTICO: Pacote dependendo de si mesmo (A -> A).
        - A aresta deve ser registrada exatamente uma vez.
        - O pacote deve ser tanto predecessor quanto sucessor de si mesmo.
        - O grau de entrada DEVE ser 1.
        """
        self.g.add_aresta("pacote_bugado", "pacote_bugado")

        self.assertEqual(len(self.g.arestas), 1)
        self.assertEqual(self.g.vizinhos("pacote_bugado"), ["pacote_bugado"])
        self.assertEqual(self.g.obter_predecessores("pacote_bugado"), ["pacote_bugado"])
        self.assertEqual(self.g.grau_entrada("pacote_bugado"), 1)

    def test_caso_borda_ciclo_bidirecional(self):
        """
        CASO PROBLEMÁTICO: Dependência mútua direta (A -> B e B -> A).
        - Ambas as arestas devem coexistir.
        - Ambos os vértices devem ter grau de entrada = 1.
        """
        self.g.add_aresta("pkgA", "pkgB")
        self.g.add_aresta("pkgB", "pkgA")

        self.assertEqual(len(self.g.arestas), 2)
        self.assertEqual(self.g.grau_entrada("pkgA"), 1)
        self.assertEqual(self.g.grau_entrada("pkgB"), 1)
        self.assertEqual(self.g.vizinhos("pkgA"), ["pkgB"])
        self.assertEqual(self.g.vizinhos("pkgB"), ["pkgA"])

    def test_caso_borda_nomes_complexos_linux(self):
        """
        CASO PROBLEMÁTICO: Nomes reais de pacotes com caracteres especiais (+, -, .).
        Ex: libstdc++6, python3.11-minimal, gcc-12-base.
        """
        p1 = "gcc-12-base"
        p2 = "libstdc++6"
        p3 = "python3.11-minimal"

        self.g.add_aresta(p1, p2)
        self.g.add_aresta(p2, p3)

        self.assertEqual(self.g.grau_entrada(p1), 0)
        self.assertEqual(self.g.grau_entrada(p2), 1)
        self.assertEqual(self.g.grau_entrada(p3), 1)
        self.assertEqual(self.g.vizinhos(p1), [p2])

    def test_caso_borda_leque_estrela_stress(self):
        """
        CASO DE CARGA: Biblioteca base sendo pré-requisito de muitos pacotes.
        1 raiz com 50 dependentes diretos.
        """
        base = "libc6"
        dependentes = [f"app_{i}" for i in range(50)]
        for dep in dependentes:
            self.g.add_aresta(base, dep)

        self.assertEqual(self.g.grau_entrada(base), 0)
        self.assertEqual(len(self.g.vizinhos(base)), 50)
        for dep in dependentes:
            self.assertEqual(self.g.grau_entrada(dep), 1)
            self.assertEqual(self.g.obter_predecessores(dep), [base])

    def test_caso_borda_vertice_inexistente(self):
        """
        CASO DEFENSIVO: Consultar nós que nunca foram adicionados.
        Não deve disparar KeyError nem corromper as estruturas internas.
        """
        self.assertEqual(self.g.vizinhos("fantasma"), [])
        self.assertEqual(self.g.obter_predecessores("fantasma"), [])
        self.assertEqual(self.g.grau_entrada("fantasma"), 0)
        self.assertNotIn("fantasma", self.g.vertices)
        self.assertNotIn("fantasma", self.g.predecessores)


if __name__ == "__main__":
    unittest.main()
