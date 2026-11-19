# Conferência com o enunciado original

Data da conferência: 11/11/2026. Fonte: [TP.pdf](../TP.pdf), páginas 1–3, lido diretamente nesta revisão. Evidências: código local, documentos, histórico Git e verificações executadas abaixo.

## Atualização em 12/11/2026

A matriz abaixo preserva a auditoria de 11/11 como registro. Desde então:

- A aplicação passou para `depgraph/`, com comando próprio e dependências sem NetworkX. Protótipos históricos ficam fora do ZIP de revisão.
- Instalação limpa, 24 testes finais e oito cenários foram validados com importação de NetworkX bloqueada.
- Experimentos reproduzíveis produziram 294 medições de tempo e nove de memória; a conferência de 4.627 grafos foi transformada em script.
- UML e documentação foram sincronizadas com as classes implementadas, preservando a proposta antiga como histórico.
- Relatório LaTeX/PDF, slides, roteiro e empacotador foram preparados para revisão; identificação, contribuições reais, conferência final de formato, ensaio, vídeo e envios continuam pendentes.

Consulte o [plano atualizado](plano-entrega.md), os [experimentos](experimentos/README.md), o [relatório](relatorio/README.md) e as [instruções de entrega](entrega/README.md). Atribuições sugeridas não foram registradas como trabalho concluído.

## Parecer original de 11/11

**O DepGraph está alinhado ao tema 9. O fluxo principal implementa os comportamentos centrais pedidos. A entrega acadêmica completa ainda não está concluída.**

O item 9, na página 2, admite dependências entre tarefas **ou pacotes**. Portanto, escolher um simulador de pacotes não depende de autorização para variar o tema. Versões, incompatibilidades e atualização explícita detalham esse problema e mantêm o grafo como estrutura central.

A versão atual simula a execução em memória e verifica a precedência antes de confirmar o estado final. O tema não exige instalar software real. A apresentação deve identificar claramente esse comportamento como simulação e explicar as simplificações adotadas.

Esta conferência sustenta o parecer técnico dentro das evidências examinadas. Não certifica ausência de qualquer defeito nem substitui a avaliação do professor ou a verificação de entrega no Canvas.

## Requisitos e evidências

| Exigência | Situação local | Evidência e pendência |
| --- | --- | --- |
| Problema aplicado com grafos como estrutura central — p. 1 | Atendido no fluxo principal | Dependências determinam expansão, validação de ciclos, ordem de instalação e impacto de remoção. |
| Tema 9: dependências entre tarefas ou pacotes — p. 2 | Atendido | Catálogo, versões e estado instalado modelam dependências entre pacotes. |
| Detecção de ciclos — p. 2 | Atendido | DFS própria retorna caminho fechado, incluindo laço e ciclo desconexo. |
| Visualização de dependências — p. 2 | Atendido | Interface apresenta vértices, versões, setas, diagnósticos e inspeção. |
| Execução segura por ordenação topológica — p. 2 | Atendido como simulação | Kahn próprio gera precedência; a sessão prepara operações, verifica pré-requisitos e confirma o estado final. |
| Estrutura e processamento próprios, sem bibliotecas prontas de grafos — p. 3 | Atendido no fluxo de pacotes; pacote final pendente | `graph.py`, `package_model.py` e `package_app.py` não usam NetworkX. O exemplo histórico e `requirements.txt` ainda o incluem. Não entregar esse exemplo como parte da solução final; a exceção do PDF é comparação de desempenho. |
| C/C++, Java ou Python — p. 1 | Atendido | Implementação em Python. |
| Interface gráfica — pp. 2–3 | Atendido | Matplotlib é usado para interface e primitivas de desenho; não cria nem processa o grafo do domínio. O enunciado não limita framework de frontend. |
| Documento do problema, justificativa e plano — p. 2 | Produzido, com atualização necessária | Documentação consolidada cobre esses itens. Algumas seções anteriores ainda descrevem a fase NetworkX; alinhar o texto e as classes propostas à implementação final. |
| UML avaliada na modelagem — p. 2 | Produzido, parcialmente proposto | Oito figuras revisadas com fontes editáveis. A arquitetura desenhada separa classes ainda concentradas em `Catalog` e `Session`. Não apresentá-la integralmente como implementada. |
| Levantamento de dados e procura de bases — p. 2 | Parcial | Existe catálogo sintético documentado. Falta registrar pesquisa de bases externas e justificar seleção, transformação ou opção por dados sintéticos. O PDF não determina uso exclusivo de dados reais nem de Kaggle. |
| Demonstrar correção — p. 1 | Evidências iniciais presentes | 33 testes aprovados e conferência independente de 4.627 grafos. Incorporar argumentos e resultados ao relatório. |
| Análise de complexidade e limitações — p. 1 | Documentada; relatório pendente | Documentos distinguem O(V + E) dos algoritmos de grafo e custo potencialmente exponencial da busca de versões. |
| Análise de resultados e avaliação de desempenho — p. 3 | Pendente | Não foi encontrado conjunto de experimentos com métricas, repetições e resultados. Testes funcionais não substituem avaliação de desempenho. |
| Código versionado e commits individuais — pp. 2–3 | Parcial | Existe histórico com contribuições identificadas. A implementação própria mais recente e seus testes estão modificados localmente, ainda sem commit nesta revisão. Não foi verificada contribuição dos seis integrantes. |
| Relatório LaTeX, template SBC, 12–15 páginas — p. 3 | Pendente | Não foram encontrados fontes `.tex` nem relatório final PDF. Markdown não substitui esse entregável. |
| Responsabilidades reais dos integrantes — p. 1 | Pendente de consolidação | Lista de integrantes existe; faltam responsabilidades finais registradas no relatório. |
| Slides, apresentação de 10 minutos e participação de todos — p. 3 | Pendente | Não encontrados slides nem evidência de ensaio e participação. |
| Vídeo de 12–18 minutos — p. 3 | Pendente | Não encontrado vídeo de funcionamento e contribuições. |
| ZIP com código, fontes do relatório e PDF — p. 1 | Pendente | Não há pacote final completo. |
| Entrega individual no Canvas e prazo — p. 1 | Externo, não verificado | PDF traz 22/11 sem ano no cabeçalho e remete à data do Canvas, às 23:59. Confirmar na tarefa; cada integrante deve entregar sua cópia. |

## Verificações executadas

1. Leitura integral do texto do PDF original, com identificação das exigências por página.
2. Busca por imports e chamadas de NetworkX no repositório: encontrados apenas no exemplo histórico de tarefas, além da dependência compartilhada. O fluxo principal de pacotes usa `Graph` próprio.
3. Execução de `test_graph`, `test_packages` e `test_preview`: **33 testes aprovados**. Desse total, quatro são do grafo próprio, 18 de pacotes e 11 do histórico de tarefas; não atribuir os 11 históricos ao núcleo novo.
4. Conferência independente de **4.627 grafos**: todos os grafos dirigidos de zero a três vértices, incluindo laços, e todos os grafos dirigidos de quatro vértices sem laços. Para cada grafo, enumeradas todas as permutações dos vértices até encontrar uma ordem válida ou esgotá-las. O resultado foi comparado com Kahn e DFS; caminhos de ciclo também foram verificados aresta por aresta. Nenhuma divergência encontrada.

Esse conjunto reforça a correção dos algoritmos em entradas pequenas e cobre casos de borda e cadeias longas na suíte própria. Não constitui prova exaustiva para qualquer entrada do resolvedor de versões ou para toda interação possível da interface.

## Prioridades para fechar a conformidade

1. Separar a distribuição final do exemplo histórico que usa NetworkX e fornecer dependências próprias para o fluxo final. Preservar o histórico Git; não confundir preservação histórica com inclusão no executável entregue.
2. Versionar os algoritmos e os testes recentes e sincronizar documentação e UML com a arquitetura efetivamente adotada.
3. Registrar a pesquisa dos dados e realizar experimentos de desempenho reproduzíveis, separando resolução, algoritmos e desenho.
4. Produzir relatório SBC, responsabilidades, slides, vídeo e pacote ZIP completos.
5. Conferir a tarefa do Canvas e realizar a entrega individual de todos.

O PDF informa que a falta de item obrigatório impede a avaliação e resulta em nota zero. Por isso, o funcionamento do simulador, sozinho, não permite declarar o trabalho inteiro pronto para entrega.
