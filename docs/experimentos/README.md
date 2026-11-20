# Avaliação do DepGraph integrado

A avaliação usa `src.graph.graph.Graph` e `src.core.resolver.Catalog`, os mesmos módulos chamados pela ferramenta. O ambiente e os hashes das fontes medidas estão em [ambiente.json](resultados/ambiente.json).

## Reproduzir

Na raiz, depois de instalar as dependências:

```bash
MPLBACKEND=Agg python3 scripts/verificar.py
python3 -m experiments.verificar_grafos
python3 -m experiments.benchmark
python3 -m experiments.apresentar
```

A suíte cobre grafos, resolução, transações, CLI e interface. A verificação exercita oito cenários com NetworkX bloqueado. O oráculo compara DFS e Kahn com enumeração de ordens em todos os grafos dirigidos de zero a três vértices com laços e de quatro vértices sem laços. Ele confere também a ordem, as camadas e as arestas do ciclo produzido. Resultado registrado em [oraculo.json](resultados/oraculo.json).

## Protocolo

- Grafo: cadeias, cadeias fechadas em ciclo e grafos com até oito sucessores por vértice. Tamanhos de 100, 1.000 e 5.000 vértices. São medidas construção, DFS, Kahn e BFS separadamente.
- Resolvedor: cadeias de 16, 64 e 128 pacotes e restrições tardias com 4, 8 e 12 pacotes com duas versões. A restrição só aparece depois das escolhas iniciais e provoca retrocesso.
- Um aquecimento e sete medições por configuração. Os tempos usam `perf_counter_ns`. O pico de alocações Python na construção é medido separadamente, com `tracemalloc` e uma amostra por família e tamanho.
- A medição exclui leitura do catálogo, interface e desenho. Os valores dependem da máquina e da carga do sistema. Os grafos de vizinhança limitada não representam grafos densos arbitrários.

A execução registrada produziu **294 tempos** e **9 medições de pico Python**. Consulte [tabelas](tabelas.md), [gráfico](desempenho.png), [amostras](resultados/tempos.csv), [resumo](resultados/resumo.csv) e [memória](resultados/memoria.csv).
