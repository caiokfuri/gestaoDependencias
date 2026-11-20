# Grafo e algoritmos próprios

A CLI e a interface usam [Graph](../src/graph/graph.py). Uma aresta A → B indica que A é pré-requisito de B. O grafo guarda sucessores, predecessores e uma lista ordenada de arestas. Um conjunto auxiliar evita duplicatas. O plano mantém a versão escolhida de cada nome.

| Operação | Contrato |
| --- | --- |
| `add_vertice(v)` | Garante a existência do vértice e preserva seus vínculos. |
| `add_aresta(u, v)` | Garante os extremos e adiciona a relação uma vez. |
| `vizinhos(v)` e `obter_predecessores(v)` | Consultam as listas de adjacência. Um vértice ausente gera lista vazia. |
| `kahn()` | Retorna `(True, ordem, camadas)` em um DAG ou `(False, None, None)` em presença de ciclo. |
| `dfs_ciclo()` | Retorna um ciclo fechado real ou `None`. |
| `dependentes_transitivos(v)` | Retorna nomes alcançáveis por caminhos de comprimento positivo. |

Kahn copia os graus de entrada. Um vértice só é emitido após todos os predecessores. Uma ordem incompleta indica ciclo. A interface usa as camadas do resultado para posicionar os vértices.

A DFS usa uma pilha de iteradores, três estados e posições no caminho ativo. Uma aresta para um vértice ativo fecha um ciclo. A busca percorre componentes desconexas e trata laços.

A BFS marca os vértices ao enfileirar, usando `deque`. Cada vértice alcançável entra na fila uma vez. Em um grafo cíclico, a origem pode ser alcançada de volta. Na remoção, o catálogo usa a ordem topológica inversa do estado instalado e filtra os afetados.

A representação ocupa O(V + E). Os três percursos têm tempo O(V + E) e memória auxiliar O(V). A busca de versões pode explorar um número exponencial de combinações. O [protocolo experimental](experimentos/README.md) descreve como esses custos foram medidos separadamente.
