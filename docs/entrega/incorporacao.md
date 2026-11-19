# Incorporação de trab-grafo

Foram incorporados a aplicação funcional (`depgraph/`), o grafo próprio (`graph.py`), seus testes (`test_graph.py`), scripts de verificação e empacotamento, workflow de CI, enunciado, guia, modelagem, relatório SBC e apresentação. Os módulos anteriores de `src/` foram preservados, com a entrada `src/main.py` delegando à aplicação funcional.

## Escopo reservado ao David

Não foram copiados o catálogo de `depgraph/examples/`, `tests/test_packages.py`, `experiments/`, `docs/experimentos/` nem `docs/dados.md`. A pasta `david_dias_pinto/` não foi alterada. Seu catálogo é usado pela aplicação. Testes funcionais, oráculo, benchmark, resultados e documentação dos dados aguardam a contribuição dele. Os testes com `pass` de sua pasta não são contados como validação funcional.

Os testes de grafo foram incorporados junto ao algoritmo, para verificar a implementação usada pela interface. A verificação também renderiza todos os cenários e conclui os planos válidos; não substitui a suíte de pacotes do David.

Relatório, slides e documentos da origem contêm referências a resultados experimentais e caminhos que serão fornecidos pelo David. Esses números são registros da origem, sem reprodução nesta incorporação. Revisar e recompilar o relatório após sua contribuição. O PDF importado corresponde ao LaTeX de origem.

O empacotador inclui o catálogo atual do David, necessário para executar a aplicação, e exclui seu código de testes/experimentos ainda pendente. A pasta `trab-grafo/`, com seu Git interno, fica fora do versionamento e da distribuição.

## Merge com os commits do David (19/11/2026)

Foram integrados os commits `a1eeeba` (catálogo e documentação em `data/`), `55e7004` (arestas com conjunto auxiliar, DFS iterativa, BFS com deque e testes de 20 mil vértices) e `5e6d304` (CLI com simulação, remoção, JSON e códigos de saída).

O conflito em `src/main.py` foi resolvido preservando a CLI do David e adicionando exportação PNG. `--gui` utiliza a interface funcional incorporada, mantendo a mesma sessão, plano e progresso. A interface em `depgraph/app.py` passou a usar `src/core/` e `src/graph/`, de modo que CLI e GUI executam os mesmos algoritmos. `graph.py` e `depgraph/model.py` são referências preservadas da origem, fora do fluxo principal.

O catálogo oficial é agora `data/pacotes.json`; a distribuição inclui `data/`. A pasta local `david_dias_pinto/` não foi alterada nem incluída nos commits da integração. Os trechos anteriores deste registro descrevem a incorporação inicial. Testes de integração cobrem transação, JSON, códigos de saída e preservação da sessão na GUI. A suíte de pacotes, oráculo e experimentos completos continuam pendentes; não foram publicados nesses três commits.
