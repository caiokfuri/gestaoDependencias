# Revisão dos diagramas principais

Revisão de 20/11/2026 contra `src/core/`, `depgraph/app.py` e `src/graph/graph.py`. As oito fontes atuais foram renderizadas em PNG/SVG com PlantUML 1.2026.4. As propostas anteriores foram preservadas em `historico/uml/` e deixaram de ser a representação da aplicação entregue.

| Figura | Conferência e ajuste |
| --- | --- |
| 01 — Casos de uso | Mantidos ator, fronteira e seis objetivos existentes. Remoção continua sendo apenas consulta. |
| 02 — Domínio | Nomes reais de classes e atributos; removida enumeração inexistente de resultado. Sete multiplicidades de destino. `requests` usa 0..* no contrato de construção da classe, embora a interface exija entrada não vazia. |
| 03 — Núcleo | Representa Catalog e Session concentrando responsabilidades; exclui classes inexistentes de resolvedor e transação. Cinco multiplicidades, incluindo plano opcional e grafo obrigatório. Layout ELK separa rótulos e cardinalidades. |
| 04 — Componentes | Representa as duas entradas, os módulos integrados, o catálogo e a exportação. Biblioteca gráfica separada do processamento de domínio. |
| 05 — Planejamento | Mostra a interpretação do pedido, a invalidação por erro de sintaxe e a chamada de Session para Catalog. |
| 06 — Transação | Último passo valida antes de registrar progresso e confirmar; falha preserva installed, staged e history. Ramos de ação intermediária, última ação e zero ações separados. |
| 07 — Estados | Identificada como abstração de situações observáveis; não promete enumeração armazenada. Reanálise e exceções descritas em notas. |
| 08 — Atividade | Representa uma chamada recursiva, com seleção e requisitos privados por ramo. Não confunde busca de versões recursiva com DFS iterativa de ciclos. Saídas de decisões rotuladas. |

## Cardinalidades

As sete relações da figura 02 são Catalog → Package (0..*), Package → Requirement/depends (0..*), Package → Requirement/conflicts (0..*), Plan → Requirement/requests (0..*), Plan → Package/selected (0..*), Plan → Issue/issues (0..*) e Plan → Graph (1).

As cinco da figura 03 são PackagePreview → Session (1), PackagePreview → Catalog (1), Session → Catalog (1), Session → Plan (0..1) e Plan → Graph (1). Esta última repete a mesma relação da vista de domínio; não é uma segunda referência. A multiplicidade vale na extremidade de destino por objeto de origem. Omissão inversa não afirma exclusividade. As associações não são composição.

## Alcance da revisão

Foram inspecionadas as figuras de classes, componentes, planejamento, transação, estados e atividade, além do caso de uso preservado; SVGs também podem ser ampliados. Os valores das cardinalidades e a validade XML foram conferidos separadamente. O relatório inclui as figuras em tamanho reduzido; a revisão final do grupo deve verificar sua legibilidade no meio de apresentação escolhido e usar os SVGs ou fontes completos quando necessário.

A semântica foi conferida contra os caminhos implementados. Diagramas omitem detalhes locais para explicar o comportamento, sem constituir prova de ausência de qualquer erro. A suíte final tem 41 testes, e a verificação adicional bloqueia NetworkX durante oito cenários. Evidências de execução e medições estão separadas em [experimentos](../experimentos/README.md).
