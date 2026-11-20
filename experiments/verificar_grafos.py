"""Compara Kahn e DFS com enumeração independente de ordens em 4.627 grafos."""
import itertools
import json
from src.graph.graph import Graph


def verify():
    checked = 0
    for size in range(5):
        possible = [(u, v) for u in range(size) for v in range(size) if size < 4 or u != v]
        for mask in range(1 << len(possible)):
            graph = Graph()
            for vertex in range(size):
                graph.add_vertice(vertex)
            edges = set()
            for bit, (u, v) in enumerate(possible):
                if mask & (1 << bit):
                    edges.add((u, v))
                    graph.add_aresta(u, v)
            if set(graph.arestas) != edges or len(graph.arestas) != len(edges):
                raise AssertionError(f'Construção divergiu: {size=}, {mask=}')
            feasible = False
            for permutation in itertools.permutations(range(size)):
                position = {v: i for i, v in enumerate(permutation)}
                if all(position[u] < position[v] for u, v in edges):
                    feasible = True
                    break
            cycle = graph.dfs_ciclo()
            if bool(cycle) == feasible:
                raise AssertionError(f'DFS divergiu: {size=}, {mask=}')
            if cycle and (cycle[0] != cycle[-1] or not all(
                    (u, v) in edges for u, v in zip(cycle, cycle[1:]))):
                raise AssertionError(f'Caminho de ciclo inválido: {cycle}')
            ok, order, layers = graph.kahn()
            if not ok:
                if feasible:
                    raise AssertionError('Kahn rejeitou um DAG')
            else:
                position = {v: i for i, v in enumerate(order)}
                if not feasible or set(order) != set(range(size)) or len(order) != size or not all(
                        position[u] < position[v] for u, v in edges):
                    raise AssertionError('Kahn aceitou uma ordem inválida')
                depth = {v: i for i, layer in enumerate(layers) for v in layer}
                if [v for layer in layers for v in layer] != order or any(
                        depth[u] >= depth[v] for u, v in edges):
                    raise AssertionError('Camadas incompatíveis com a precedência')
            checked += 1
    return {'grafos': checked, 'divergencias': 0,
            'escopo': 'n=0..3 com laços; n=4 sem laços; permutações como oráculo'}


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
