# Grafo e algoritmos próprios

O fluxo de pacotes usa `Graph`, em [graph.py](../graph.py), para representar e processar grafos. A implementação iniciada por Caio Alves Kfuri foi completada com Kahn, DFS e consulta de dependentes. Usa mapas, listas, conjuntos e iteradores do Python; não importa bibliotecas de grafos.

## Estruturas e contratos

`vertices` associa cada nome à lista de sucessores; `predecessores` mantém as listas inversas. `nodes` guarda atributos dos vértices e `edges` guarda atributos por par origem/destino. A propriedade `arestas` retorna uma lista dos pares. Inserções repetidas atualizam atributos sem duplicar a relação. A → B significa que B depende de A.

| Operação | Resultado |
| --- | --- |
| `add_vertice(v)` | Adiciona vértice, preservando seus vínculos existentes. |
| `add_aresta(u, v)` | Cria os extremos se necessário e adiciona relação única. |
| `vizinhos(v)` | Retorna cópia dos sucessores; ausente produz lista vazia. |
| `kahn()` | Retorna ordem topológica completa ou lança `CycleError`. |
| `geracoes()` | Retorna as camadas de Kahn usadas no layout gráfico. |
| `dfs_cicle()` | Retorna caminho fechado de um ciclo real ou lista vazia. O nome anterior foi preservado para compatibilidade. |
| `dependentes(v)` | Retorna os sucessores transitivos, excluindo a origem; ausente lança `KeyError`. |

Kahn copia graus de entrada e processa uma camada de grau zero por vez. O achatamento das camadas equivale a uma fila FIFO. Cada vértice entra uma vez e cada aresta reduz um grau uma vez. Se o total emitido for menor que o número de vértices, a ordenação é recusada integralmente.

A DFS é iterativa, com pilha de iteradores, cores branco/cinza/preto e posições no caminho ativo. Uma aresta para cinza fecha um ciclo, inclusive um laço. Todas as componentes são percorridas; dependentes apenas bloqueados não são apresentados como membros do ciclo. A forma iterativa evita o limite de recursão em cadeias longas.

A busca de dependentes usa lista com índice de leitura como fila e conjunto de visitados. As três consultas têm tempo O(V + E), memória auxiliar O(V) e não alteram o grafo. A representação ocupa O(V + E); inserção e consulta de aresta usam mapas, com custo médio constante. O backtracking de versões continua potencialmente exponencial.

## Integração e alcance

[model.py](../depgraph/model.py) usa o grafo próprio para validar estados, gerar planos, detectar ciclos e calcular impacto de remoção. [app.py](../depgraph/app.py) usa as camadas próprias para posicionar DAGs, trigonometria básica para grafos com ciclos e primitivas Matplotlib para pontos e setas.

O fluxo principal de pacotes não usa NetworkX para estrutura, processamento, layout ou desenho. Matplotlib permanece como biblioteca de interface gráfica. O exemplo histórico de tarefas em `model.py` e `app.py` continua usando NetworkX, isolado da entrada principal; sua dependência fica exclusivamente em `prototypes/networkx_preview/requirements.txt`. O arquivo `requirements.txt` da raiz contém somente Matplotlib. Esse histórico não deve compor o núcleo da entrega final.

A divisão completa em classes de resolução, catálogo e transação mostrada na UML permanece uma proposta: esta etapa implementa e integra a estrutura de grafos, sem concluir toda a reorganização arquitetural.

## Verificação

```bash
python3 -m unittest test_graph -v
MPLBACKEND=Agg python3 -m unittest test_graph tests.test_packages -v
```

A suíte própria cobre vazio, isolado, duplicação de arestas, dependências compartilhadas, invariância após consultas, ciclo desconexo com dependente bloqueado, laço e cadeia de 3.001 vértices. Os testes de pacotes verificam a integração com resolução, transações e interface. Registrar resultados efetivamente executados; existência de testes não equivale à sua aprovação.
