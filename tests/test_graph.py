import sys
import os
import unittest

# Garante que a pasta raiz esteja no path, permitindo rodar de qualquer lugar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.graph.graph import Graph


class TestGraphEstrutura(unittest.TestCase):

    #Inicialização e teste da estrutura inicial do grafo
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


    # TESTES DO ALGORITMO DE KAHN (ORDENAÇÃO TOPOLÓGICA)

    def test_kahn_cadeia_linear(self):
        """Testa ordenação de dependências lineares A -> B -> C."""
        self.g.add_aresta("libz", "libpng")
        self.g.add_aresta("libpng", "app")

        sucesso, ordem, camadas = self.g.kahn()

        self.assertTrue(sucesso)
        self.assertEqual(ordem, ["libz", "libpng", "app"])
        self.assertEqual(camadas, [["libz"], ["libpng"], ["app"]])

    def test_kahn_paralelismo_camadas(self):
        """
        Testa dependências convergentes com camadas paralelas:
        Camada 1: libz e libcore (grau 0)
        Camada 2: libpng (depende de libz) e libnet (depende de libcore)
        Camada 3: browser (depende de libpng e libnet)
        """
        self.g.add_aresta("libz", "libpng")
        self.g.add_aresta("libcore", "libnet")
        self.g.add_aresta("libpng", "browser")
        self.g.add_aresta("libnet", "browser")

        sucesso, ordem, camadas = self.g.kahn()

        self.assertTrue(sucesso)
        self.assertEqual(len(camadas), 3)
        # Camada 1 tem que ter libz e libcore
        self.assertEqual(set(camadas[0]), {"libz", "libcore"})
        # Camada 2 tem que ter libpng e libnet
        self.assertEqual(set(camadas[1]), {"libpng", "libnet"})
        # Camada 3 tem que ter o browser
        self.assertEqual(camadas[2], ["browser"])

        # Garante que cada pré-requisito aparece antes do seu dependente na ordem
        self.assertLess(ordem.index("libz"), ordem.index("libpng"))
        self.assertLess(ordem.index("libcore"), ordem.index("libnet"))
        self.assertLess(ordem.index("libpng"), ordem.index("browser"))
        self.assertLess(ordem.index("libnet"), ordem.index("browser"))

    def test_kahn_componentes_desconexas(self):
        """Testa grafos com pacotes totalmente independentes entre si."""
        self.g.add_aresta("pkgA", "pkgB")
        self.g.add_aresta("pkgC", "pkgD")

        sucesso, ordem, camadas = self.g.kahn()

        self.assertTrue(sucesso)
        self.assertEqual(len(ordem), 4)
        self.assertLess(ordem.index("pkgA"), ordem.index("pkgB"))
        self.assertLess(ordem.index("pkgC"), ordem.index("pkgD"))

    def test_kahn_falha_com_ciclo(self):
        """Testa se Kahn detecta ciclo e recusa ordenação completa (A -> B -> C -> A)."""
        self.g.add_aresta("A", "B")
        self.g.add_aresta("B", "C")
        self.g.add_aresta("C", "A")

        sucesso, ordem, camadas = self.g.kahn()

        self.assertFalse(sucesso, "Kahn deve retornar False na presença de ciclo")
        self.assertIsNone(ordem)
        self.assertIsNone(camadas)

    def test_kahn_falha_com_auto_laco(self):
        """Testa se pacote dependendo de si mesmo (A -> A) é detectado como ciclo."""
        self.g.add_aresta("loop", "loop")

        sucesso, ordem, camadas = self.g.kahn()

        self.assertFalse(sucesso)
        self.assertIsNone(ordem)
        self.assertIsNone(camadas)

    def test_kahn_grafo_vazio(self):
        """Testa Kahn em grafo sem nenhum vértice."""
        sucesso, ordem, camadas = self.g.kahn()
        self.assertTrue(sucesso)
        self.assertEqual(ordem, [])
        self.assertEqual(camadas, [])


    # TESTES DE DETECÇÃO DE CICLO COM DFS

    def test_dfs_cicle_sem_ciclo(self):
        """Grafo acíclico normal (A -> B -> C) não deve ter ciclo."""
        self.g.add_aresta("libz", "libpng")
        self.g.add_aresta("libpng", "app")

        ciclo = self.g.dfs_ciclo()
        self.assertIsNone(ciclo, "Não deve encontrar ciclo em grafo acíclico")

    def test_dfs_cicle_detecta_ciclo_fechado(self):
        """Testa se detecta o caminho fechado A -> B -> C -> A."""
        self.g.add_aresta("A", "B")
        self.g.add_aresta("B", "C")
        self.g.add_aresta("C", "A")

        ciclo = self.g.dfs_ciclo()
        self.assertIsNotNone(ciclo, "Deveria encontrar um ciclo")
        # Garante que o ciclo fecha nele mesmo (primeiro elemento == último)
        self.assertEqual(ciclo[0], ciclo[-1])
        # Garante que os nós A, B e C estão no ciclo
        self.assertIn("A", ciclo)
        self.assertIn("B", ciclo)
        self.assertIn("C", ciclo)

    def test_dfs_cicle_auto_laco(self):
        """Testa se pacote apontando para si mesmo (loop -> loop) é detectado."""
        self.g.add_aresta("loop", "loop")

        ciclo = self.g.dfs_ciclo()
        self.assertIsNotNone(ciclo)
        self.assertEqual(ciclo, ["loop", "loop"])

    def test_dfs_cicle_ciclo_em_componente_distante(self):
        """Testa ciclo escondido em uma componente desconexa separada."""
        # Componente 1: saudável (X -> Y)
        self.g.add_aresta("X", "Y")
        # Componente 2: com ciclo (M -> N -> M)
        self.g.add_aresta("M", "N")
        self.g.add_aresta("N", "M")

        ciclo = self.g.dfs_ciclo()
        self.assertIsNotNone(ciclo)
        self.assertEqual(ciclo[0], ciclo[-1])
        self.assertIn("M", ciclo)
        self.assertIn("N", ciclo)

if __name__ == "__main__":
    unittest.main()
