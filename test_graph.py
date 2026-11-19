"""Contratos do grafo próprio, sem biblioteca de referência."""
import copy
import unittest

from graph import Graph, CycleError


class GraphTests(unittest.TestCase):
    def test_empty_isolated_and_duplicate_edges(self):
        g = Graph()
        self.assertEqual(g.kahn(), [])
        self.assertEqual(g.dfs_cicle(), [])
        g.add_vertice('isolado')
        g.add_aresta('base', 'app', constraint='>=1')
        g.add_aresta('base', 'app', constraint='>=2')
        self.assertEqual(g.arestas, [('base', 'app')])
        self.assertEqual(g.predecessores['app'], ['base'])
        self.assertEqual(g.edges['base', 'app']['constraint'], '>=2')
        self.assertEqual(set(g.kahn()), {'base', 'app', 'isolado'})

    def test_shared_dependencies_and_queries_preserve_graph(self):
        g = Graph()
        for edge in [('base', 'a'), ('base', 'b'), ('a', 'fim'), ('b', 'fim')]:
            g.add_aresta(*edge)
        before = copy.deepcopy(g.__dict__)
        order = g.kahn()
        positions = {v: i for i, v in enumerate(order)}
        for u, v in g.arestas:
            self.assertLess(positions[u], positions[v])
        self.assertEqual(g.dependentes('base'), {'a', 'b', 'fim'})
        self.assertEqual(g.dependentes('fim'), set())
        self.assertEqual(g.dfs_cicle(), [])
        neighbors = g.vizinhos('base')
        neighbors.clear()
        self.assertEqual(g.__dict__, before)
        with self.assertRaises(KeyError):
            g.dependentes('ausente')

    def test_cycle_in_disconnected_component_excludes_blocked_dependent(self):
        g = Graph()
        for u, v in [('livre', 'outro'), ('a', 'b'), ('b', 'a'), ('b', 'bloqueado')]:
            g.add_aresta(u, v)
        before = copy.deepcopy(g.__dict__)
        with self.assertRaises(CycleError):
            g.kahn()
        cycle = g.dfs_cicle()
        self.assertEqual(cycle[0], cycle[-1])
        self.assertNotIn('bloqueado', cycle)
        for u, v in zip(cycle, cycle[1:]):
            self.assertTrue(g.has_edge(u, v))
        self.assertEqual(g.dependentes('a'), {'b', 'bloqueado'})
        self.assertEqual(g.__dict__, before)

    def test_self_loop_and_deep_chain_without_recursion_limit(self):
        g = Graph()
        g.add_aresta('a', 'a')
        self.assertEqual(g.dfs_cicle(), ['a', 'a'])
        with self.assertRaises(CycleError):
            g.kahn()
        g = Graph()
        for i in range(3000):
            g.add_aresta(i, i + 1)
        self.assertEqual(g.kahn(), list(range(3001)))
        self.assertEqual(g.dfs_cicle(), [])
        g.add_aresta(3000, 2000)
        cycle = g.dfs_cicle()
        self.assertEqual(cycle, list(range(2000, 3001)) + [2000])


if __name__ == '__main__':
    unittest.main()
