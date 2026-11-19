# Documentação do projeto

A aplicação funcional foi incorporada de `trab-grafo`. Consulte o [registro da incorporação](entrega/incorporacao.md) para o escopo reservado ao David. As referências a dados e experimentos aguardam sua contribuição; números do relatório e slides são registros da versão de origem. O guia de empacotamento está em [entrega/empacotamento.md](entrega/empacotamento.md).

O foco atual é o **DepGraph**, simulador de conflitos em dependências entre pacotes inspirado no Linux.

## Índice

| Documento | Conteúdo |
| --- | --- |
| [Material preparatório da equipe](apresentacao/preparacao-equipe.md) | Explicações por integrante, exemplos reais, perguntas de estudo e situação da prontidão. |
| [Material preparatório em PDF](apresentacao/preparacao-equipe.pdf) | Versão para leitura e compartilhamento entre os integrantes. |
| [Materiais de entrega](entrega/README.md) | Empacotamento, manifesto e pendências humanas. |
| [Relatório técnico](relatorio/README.md) | Fontes LaTeX, PDF e instruções de compilação para revisão. |
| [Apresentação](apresentacao/roteiro.md) | Slides locais e roteiros de apresentação e vídeo. |
| [Responsabilidades propostas](entrega/responsabilidades.md) | Divisão sugerida entre os seis integrantes e registro separado das contribuições reais. |
| [Dados](dados.md) | Pesquisa de fontes e justificativa do catálogo sintético. |
| [Experimentos](experimentos/README.md) | Protocolo, medições brutas, tabelas, gráfico e verificação independente. |
| [Lista de trabalho para a entrega](plano-entrega.md) | Pendências por prioridade, critérios de conclusão, materiais obrigatórios e ordem sugerida de execução. |
| [Conferência com o enunciado](conformidade-enunciado.md) | Parecer por exigência do PDF, evidências executadas e pendências da entrega. |
| [Grafo próprio](grafo-proprio.md) | Implementação e integração de Kahn, DFS e busca de dependentes sem biblioteca de grafos. |
| [Documentação completa da aplicação](modelagem/documentacao-completa.md) | Escopo, requisitos, casos de uso, oito diagramas UML, cardinalidades, contratos, algoritmos e validação. |
| [Protótipo de pacotes](prototipo-networkx/README.md) | Instalação, funcionamento, restrições de versão, conflitos, transações, dez imagens e limitações. |
| [Guia geral](../agent.md) | Requisitos do enunciado e planejamento da entrega acadêmica com grafos próprios. |
| [Modelagem e diagramas](modelagem/README.md) | Requisitos, casos de uso, classes atuais e propostas, componentes, sequências, estados e atividade. |
| [Principais modelagens UML](modelagem/modelagens-principais.md) | Oito diagramas renderizados em PNG/SVG, fontes PlantUML e reprodução local. |
| [Guia de notação da modelagem](modelagem/guia-de-notacao.md) | Como escrever e interpretar os documentos e diagramas em Markdown e Mermaid, com limites em relação à UML formal. |
| [Enunciado](../TP.pdf) | PDF original do professor. |
| [Apresentação](../README.md) | Integrantes, objetivo e início rápido. |
| [Histórico do exemplo de tarefas](prototipo-networkx/tarefas-historico.md) | Primeira exploração, substituída pelo foco em pacotes. |

## Organização

```text
docs/
├── README.md
├── modelagem/  (requisitos e diagramas editáveis)
└── prototipo-networkx/
    ├── README.md
    ├── tarefas-historico.md
    ├── imagens/
    │   ├── pacotes-01-plano-instalacao.png
    │   ├── ...
    │   ├── pacotes-10-impacto-remocao.png
    │   └── imagens anteriores de tarefas
    ├── sem-ciclo.png  (histórico)
    └── com-ciclo.png  (histórico)
```

Centralizar os novos guias e artefatos em subpastas temáticas de `docs/`, com suas imagens próximas ao documento correspondente e links neste índice. Usar nomes em minúsculas, sem espaços nem acentos, e links relativos.

Distinguir funcionalidades implementadas, propostas da versão final e registros históricos. Documentar a origem dos dados e a reprodução de imagens e resultados. O `agent.md` e o PDF original permanecem na raiz.
