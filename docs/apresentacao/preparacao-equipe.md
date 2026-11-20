---
title: "DepGraph — Material preparatório da equipe"
subtitle: "Fundamentação para cada integrante preparar sua apresentação"
lang: pt-BR
date: "12 de novembro de 2026"
---

# Finalidade e forma de estudo

Este documento reúne o conteúdo que cada integrante precisa compreender para preparar sua participação. Cada seção desenvolve conceitos, relaciona decisões ao código e oferece perguntas de autoavaliação. A pessoa pode selecionar os pontos mais relevantes e explicá-los com suas próprias palavras, usando os slides e a aplicação como apoio.

A divisão segue as atribuições acordadas: Lucas integra e contextualiza; Caio explica grafos; Arthur Chaves Viana Leão explica resolução e transação; Rafael explica a interação; David Dias Pinto fundamenta a avaliação; João relaciona modelagem e implementação. **Responsabilidade de apresentação não comprova autoria do código.** As contribuições efetivamente realizadas precisam ser confirmadas pelo grupo antes de constarem como autoria individual no relatório ou no vídeo.

A preparação deve começar pela leitura da visão comum abaixo. Em seguida, cada pessoa aprofunda sua área, consulta os arquivos indicados e verifica os exemplos na aplicação. Estar preparado significa conseguir explicar a decisão, apontar uma evidência e reconhecer seu limite. Decorar nomes de métodos ou números sem entender sua origem não basta.

O [roteiro de ensaio](roteiro.md) e os [slides](slides.html) são materiais complementares. Este documento não fixa falas, turnos ou duração por pessoa.

# Conhecimentos que todos precisam compartilhar

## O que o projeto resolve

O DepGraph é um simulador de gestão de dependências entre pacotes, alinhado ao tema 9 do enunciado. Recebe um catálogo, um estado instalado e um pedido. Procura versões compatíveis, verifica dependências e conflitos e produz uma ordem segura para a simulação. Se não puder concluir um plano válido, apresenta um diagnóstico.

O grafo é dirigido e representa precedência: **A → B significa que B depende de A**. Assim, a ordenação topológica coloca A antes de B. Uma biblioteca compartilhada aparece uma vez na seleção, mesmo quando vários programas dependem dela. O catálogo guarda as alternativas de versão; o grafo de um plano guarda as versões selecionadas.

Ausência de ciclo é necessária para a precedência estrita adotada, mas não garante viabilidade do pedido. Dois programas podem exigir intervalos de versão incompatíveis da mesma biblioteca. Essa verificação pertence à resolução de restrições e precisa ocorrer além da análise do grafo.

## O que existe hoje

A aplicação principal está em `depgraph/`, com entrada `python -m depgraph`. O grafo próprio integrado está em `src/graph/graph.py`. A interface usa Matplotlib para controles e desenho; estrutura, Kahn, DFS, busca de dependentes e posicionamento do grafo não são delegados ao NetworkX. O exemplo histórico que usa essa biblioteca fica separado em `prototypes/` e não integra o ZIP de revisão.

O catálogo é sintético: 27 nomes, 32 versões e dois pacotes inicialmente instalados. No cenário `desktop`, são selecionados 17 pacotes e 26 arestas. Como dois já estavam instalados, existem 15 operações novas. Esses números pertencem a esse cenário; não são limites de capacidade nem resultados gerais de desempenho.

As instalações e atualizações acontecem somente em memória. O programa não instala software no computador. A remoção é uma consulta de impacto; não há desinstalação efetiva. O modelo usa versões numéricas simplificadas e não implementa todas as regras de uma distribuição Linux.

## Evidências e limites que todos devem saber distinguir

A validação final contém 41 testes e exercita oito cenários com a importação de NetworkX bloqueada. Um oráculo independente conferiu 4.627 grafos pequenos sem divergências. Os experimentos guardam 294 amostras de tempo e nove medições de memória. Esses conjuntos avaliam aspectos diferentes: testes funcionais, comparação com uma decisão independente e desempenho.

Kahn, DFS e busca de dependentes têm tempo O(V + E), sendo V a quantidade de vértices e E a quantidade de arestas. **A resolução completa de versões pode ter custo exponencial.** Nenhum integrante deve atribuir o custo linear dos percursos a toda a aplicação, nem apresentar testes finitos como garantia de ausência de qualquer defeito.

# Lucas Batista Duarte — Integração, conformidade e entrega

## Conteúdo a dominar

Lucas precisa compreender a aplicação como um conjunto: qual problema recebe, como os módulos colaboram e quais saídas justificam a solução. O principal vínculo com a disciplina é que o grafo determina a precedência, a detecção de ciclos e a análise de dependentes; ele participa da decisão e não serve apenas como ilustração.

A integração começa na interface, que recebe o pedido e encaminha a análise à sessão. A sessão chama o catálogo, que valida a base, explora versões e constrói o grafo. O plano volta à interface para visualização. Quando o usuário avança, a sessão verifica pré-requisitos e prepara operações. A confirmação só ocorre após a validação final.

É útil conhecer a distinção entre três objetos: catálogo é o universo de versões disponíveis; plano é o resultado de uma análise para determinada base; sessão é o estado vivo da simulação. Misturar esses papéis dificulta explicar por que um novo pedido exige nova análise ou por que o catálogo pode conter um pacote que não aparece no plano atual.

## Relação com o enunciado

O tema pede dependências entre tarefas ou pacotes, ciclos, visualização e execução segura por ordenação topológica. A escolha de pacotes está dentro dessa descrição. O protótipo funcional usa Python, interface gráfica e algoritmos próprios. As dependências finais da aplicação ficam no `requirements.txt` da raiz, que declara Matplotlib; o requisito de implementação própria se aplica à criação e ao processamento do grafo.

Lucas também deve distinguir funcionamento técnico de entrega acadêmica. Além do software, são exigidos relatório SBC em LaTeX com 12–15 páginas, código e histórico Git, slides, apresentação de dez minutos, vídeo de 12–18 minutos e entrega individual no Canvas. Os materiais produzidos para revisão não comprovam que ensaio, gravação ou envio foram realizados.

## Exemplo para compreender a integração

Em `desktop`, o pedido contém `desktop-suite`, mas a seleção chega a 17 pacotes porque inclui dependências transitivas e a base preservada. Durante os primeiros avanços, há pacotes preparados e o estado instalado permanece com dois. No último passo válido, a sessão confirma o estado de 17. A interface mostra uma decisão do núcleo; ela não escolhe arbitrariamente a ordem.

A distribuição de revisão exclui os protótipos executáveis. Seu manifesto identifica arquivos por hash e registra pendências. Um ZIP existir não significa que seja o pacote final aprovado para entrega.

## Perguntas para autoavaliação

- Por que o grafo é central para resolver o problema escolhido?
- Qual a diferença entre catálogo, plano e sessão?
- Por que 17 pacotes selecionados resultam em 15 operações novas no cenário principal?
- Como outra pessoa instala e executa a aplicação a partir dos arquivos entregues?
- Quais requisitos já têm evidência técnica e quais dependem de confirmação ou ação do grupo?

Uma resposta consistente relaciona entrada, decisão e saída, e reconhece que a ferramenta simula instalações. Não precisa prometer compatibilidade com um gerenciador Linux real.

## Referências para estudo

Consultar o [README](../../README.md), os [módulos implementados](../modelagem/imagens/04-componentes.svg), a [conformidade](../conformidade-enunciado.md) e as [instruções de entrega](../entrega/README.md). No código, acompanhar a entrada [__main__.py](../../depgraph/__main__.py), `PackagePreview.analyze`, `Session.analyze` e `Session.advance`.

# Caio Alves Kfuri — Grafo próprio, algoritmos e complexidade

## Conteúdo a dominar

Caio precisa explicar a representação e por que os algoritmos resolvem as consultas exigidas. `Graph` mantém listas de sucessores em `vertices`, listas inversas em `predecessores` e atributos em `nodes` e `edges`. A inserção de uma aresta garante a existência dos extremos e evita duplicar a relação. Mapas, listas, conjuntos e iteradores são estruturas básicas usadas pela implementação própria.

A orientação é a decisão mais importante: se `libpng` depende de `libz`, a aresta aponta de `libz` para `libpng`. Desse modo, percorrer sucessores permite localizar dependentes. A orientação contrária também poderia representar dependência em outro projeto, mas exigiria ajustar as consultas e a interpretação da ordem. Aqui, todos precisam usar a convenção documentada.

## Kahn e a razão de sua correção

Kahn começa com os vértices de grau de entrada zero. Eles não têm predecessores pendentes e podem ser emitidos. Ao processar um vértice, o algoritmo reduz os graus dos sucessores; aqueles cujo grau chega a zero ficam disponíveis. O código usa camadas e as achata para obter a ordem, sem alterar as relações originais.

A propriedade preservada é que cada vértice emitido já teve todos os seus predecessores processados. Portanto, toda dependência aparece antes do dependente. Uma ordem válida não é necessariamente única: programas independentes podem trocar de posição. A validação deve conferir as arestas, sem exigir uma sequência única sem justificativa.

Se o total emitido for menor que V, não existe ordem completa. Os vértices restantes incluem um ciclo e podem incluir dependentes bloqueados que não pertencem a ele. Essa distinção explica por que Kahn detecta a impossibilidade, mas a DFS é usada para exibir um caminho real do ciclo.

## DFS e busca de dependentes

A DFS marca vértices como não visitados, ativos e encerrados. Uma aresta para um vértice ativo alcança um ancestral no caminho atual e fecha um ciclo. A implementação retorna esse trecho com o primeiro vértice repetido ao final. Ela percorre todas as componentes e também trata um laço, cujo caminho tem a forma `[v, v]`.

A DFS usa uma pilha explícita de iteradores, evitando a recursão em cadeias profundas. Isso é diferente da busca de versões, que é recursiva. A consulta de dependentes usa uma fila e um conjunto de visitados sobre sucessores, registrando vértices alcançados por caminhos de comprimento positivo. Para sugerir uma remoção em cascata, os dependentes devem aparecer antes de seus pré-requisitos na ordem inversa pertinente.

## Exemplo e complexidade

A cadeia real `base-files -> libcore -> libz -> libpng` permite explicar precedência e alcance. `base-files` deve preceder os demais; consultar dependentes de `libcore` alcança pacotes transitivos. O ciclo `cycle-alpha`, `cycle-beta` e `cycle-gamma` permite mostrar uma sequência fechada de arestas de precedência na interface.

Cada percurso examina vértices e arestas um número limitado de vezes: O(V + E) em tempo e O(V) de memória auxiliar. A representação ocupa O(V + E). Esse argumento depende da implementação por adjacência; não deriva somente de um gráfico de tempos. Também não se estende automaticamente à seleção de versões.

## Perguntas para autoavaliação

- Por que um vértice com grau de entrada zero pode ser processado?
- Por que uma ordem parcial de Kahn é recusada?
- Qual a diferença entre estar bloqueado por ciclo e fazer parte do ciclo?
- Por que uma aresta para um vértice ativo da DFS indica ciclo?
- Como as consultas preservam o grafo e tratam componentes desconexas?

Consultar [graph.py](../../src/graph/graph.py), os [testes do grafo](../../tests/test_graph.py) e a [explicação dos algoritmos](../grafo-proprio.md). O oráculo independente, estudado com David Dias Pinto, ajuda a relacionar o argumento teórico às evidências executadas.

# Arthur Chaves Viana Leão — Resolução de versões, conflitos e transações

## Conteúdo a dominar

Arthur Chaves Viana Leão precisa explicar por que ordenar os pacotes é apenas parte da solução. Cada versão disponível possui dependências e possíveis conflitos. O resolvedor deve selecionar no máximo uma versão por nome e combinar os requisitos impostos por todos os pacotes escolhidos. Uma dependência transitiva pode tornar inválida uma escolha que parecia adequada isoladamente.

`Requirement` verifica condições numéricas de versão. O modelo aceita de um a três componentes e normaliza sua comparação; `1.0` e `1.0.0` são equivalentes. Isso evita tratar versões como textos ordenados alfabeticamente, mas não implementa o formato completo Debian/RPM.

## Busca com retrocesso e política de atualização

`Catalog.plan` prefere versões maiores e tenta alternativas quando um ramo falha. Cada chamada recebe uma nova seleção e novos requisitos. Abandonar uma versão também abandona as dependências que ela introduziu. Caso contrário, uma tentativa descartada poderia bloquear injustamente uma solução posterior.

O catálogo contém um exemplo direto: `compat-app 2.0` exige `missing-sdk`, ausente no catálogo. A busca pode voltar e escolher `compat-app 1.0`, cuja dependência é viável. Preferir versões maiores não significa instalar sempre a mais recente, nem minimizar globalmente a quantidade de operações.

A política preserva a versão de nomes instalados que não aparecem no pedido. `modern-browser` sozinho é bloqueado pela necessidade de uma versão de `libcore` que não foi liberada para atualização. O pedido `modern-browser, libcore>=2.0` libera essa escolha, desde que a seleção final continue compatível. Mesmo uma atualização explicitamente pedida não pode quebrar um dependente preservado.

## Diagnósticos distintos

O cenário `versoes` combina exigências incompatíveis de `libssl`: o navegador moderno leva à versão maior e o backup legado exige versão menor que 2. O problema é de restrição de versão. No cenário `conflito`, `web-server` declara incompatibilidade com `alternate-server`, mesmo que as dependências individualmente sejam atendidas. No cenário `ausente`, `broken-app` requer um nome inexistente. Em `ciclo`, não existe a precedência estrita exigida pela política do simulador.

Também existe o diagnóstico `limite`. A busca padrão interrompe ao atingir o limite de tentativas ou o patamar de seleção definido no código. Isso significa que a análise não concluiu a decisão; não comprova que nenhuma solução exista. O custo combinatório pode ser exponencial, além dos custos de copiar e validar estruturas.

## Preparação e confirmação

`Session` mantém `installed`, `plan`, `staged`, `applied` e `history`. Um avanço confere pré-requisitos em um estado temporário formado por instalados e preparados. Pacotes intermediários entram na preparação, mas não no estado confirmado.

Antes de registrar o último preparo, o catálogo valida o estado final. Se houver recusa, os instalados, o progresso e o histórico daquele passo ficam preservados, permitindo tentar novamente sem pular uma operação. Um plano sem ações também valida o estado e conclui. Essa segurança vale para a simulação em memória; não é uma transação de arquivos ou de banco de dados.

A interface bloqueia avanço se o texto do pedido mudar. A sessão bloqueia uma base instalada diferente da usada no plano. Uma nova análise que retorna resultado redefine o progresso; uma exceção de sintaxe não apaga automaticamente o plano anterior. Conhecer essa divisão evita atribuir à sessão verificações que hoje estão na interface.

## Perguntas para autoavaliação

- Como uma seleção acíclica ainda pode ter versões incompatíveis?
- O que precisa ser descartado ao abandonar um ramo de busca?
- Por que a aplicação pode escolher uma versão mais antiga?
- Qual a diferença entre falha comprovada dentro da política e resultado inconclusivo?
- Em que instante `installed` muda e o que acontece se a validação final recusar?

Consultar [resolvedor](../../src/core/resolver.py) e [domínio](../../src/core/domain.py), os [testes de pacotes](../../tests/test_packages.py) e as sequências de [planejamento](../modelagem/imagens/05-sequencia-planejamento.svg) e [confirmação](../modelagem/imagens/06-sequencia-transacao.svg).

# Rafael Abras Lessa Freitas — Interface, visualização e demonstração

## Conteúdo a dominar

Rafael precisa tornar os resultados compreensíveis para quem vê a ferramenta pela primeira vez. A interface apresenta pedido, grafo, resumo da análise e registro das operações. Sua explicação deve ligar cada controle à decisão correspondente do núcleo, sem confundir uma mudança visual com uma instalação real.

O campo de pedido aceita nomes e comparações simples. “Analisar instalação” produz um plano ou diagnóstico. “Próximo pacote” prepara uma operação do plano válido e atual. “Reiniciar plano” solicita nova análise do pedido atual e descarta a preparação quando essa análise retorna. Os botões de cenário restauram a base didática, permitindo repetir exemplos de forma comparável.

## Como interpretar o desenho

Setas indicam pré-requisito para dependente. Rótulos identificam nomes e versões; cores e realces ajudam a distinguir situações da análise. Uma linha de conflito pode ser desenhada para explicar incompatibilidade, mas não passa a ser uma aresta de precedência usada por Kahn.

Para grafos acíclicos, o posicionamento usa as gerações do próprio Kahn. Quando há ciclos, usa disposição circular. Matplotlib desenha pontos, setas, rótulos e controles. Portanto, desenhar com uma biblioteca gráfica não equivale a delegar a ela a estrutura ou os algoritmos de grafos.

Clicar em um vértice abre informações sobre o pacote. O painel de diagnóstico deve ser interpretado pelo tipo de falha e pelos requisitos apresentados; simplesmente apontar que algo ficou vermelho não explica a causa. A visualização de um grafo parcial em caso de falha também não autoriza execução.

## Experiências que precisam ser compreendidas

No cenário `desktop`, verificar a lista de operações, preparar um pacote e observar que o estado instalado continua preservado. Depois da conclusão, a seleção de 17 pacotes torna-se o estado confirmado. Nos cenários `versoes` e `ciclo`, identificar por que as causas do bloqueio são diferentes. Em `alternativa`, observar a escolha de `compat-app 1.0` e relacioná-la ao retrocesso explicado por Arthur Chaves Viana Leão.

Para consultar remoção, primeiro concluir uma instalação que contenha dependentes, informar apenas o nome do pacote, como `libcore`, e usar “Impacto da remoção”. Essa consulta informa afetados e ordem sugerida, sem remover nada. Editar o campo para essa consulta também altera o texto do pedido: antes de voltar a avançar uma instalação, será necessária nova análise.

O botão de exportação grava `outputs/depgraph/pacotes.json` e `pacotes.png`, substituindo os arquivos anteriores. O JSON registra a análise e a execução; não é o catálogo de entrada nem um mecanismo de restaurar sessão. Essa diferença importa ao explicar o destino dos arquivos para o avaliador.

## Preparação prática

Rafael deve abrir a aplicação no computador que será usado, conferir janela, escala, leitura dos textos, clique em vértices e acesso aos arquivos exportados. Os testes de renderização sem janela não substituem essa verificação no ambiente da apresentação. As [capturas da aplicação](../prototipo-networkx/README.md) servem como apoio e referência de comportamento.

O comando é `python -m depgraph` após ativar o ambiente e instalar as dependências da raiz. Também é possível exportar uma tela pela linha de comando com `--exportar`. A opção de exportação usa desenho sem janela, apropriado à documentação, mas não comprova a interação com mouse e teclado no computador de apresentação.

## Perguntas para autoavaliação

- Como o usuário distingue plano, progresso parcial e conclusão?
- Como explicar um conflito sem chamá-lo de ciclo?
- O que muda quando um cenário é carregado?
- Qual a diferença entre consultar remoção e remover pacotes?
- Onde ficam os arquivos exportados e o que cada um contém?

Consultar [app.py](../../depgraph/app.py), especialmente os controles, `load_scenario`, `advance`, `removal`, `save` e a renderização. Relacionar o uso da interface às regras do núcleo, sem prometer funcionalidades ausentes.

# David Dias Pinto — Dados, testes, experimentos e interpretação

## Conteúdo a dominar

David Dias Pinto precisa explicar o que foi avaliado, como foi medido e até onde os resultados sustentam as conclusões. O catálogo da interface é sintético e foi criado para tornar casos de sucesso e falha compreensíveis. Houve consulta a fontes Debian, mas não importação de uma base real. Não apresentar os nomes e versões fictícios como dados coletados de uma distribuição.

Os experimentos usam famílias determinísticas geradas pelo projeto. Cadeias avaliam profundidade; grafos com até oito sucessores por vértice avaliam compartilhamento; cadeias fechadas por uma aresta avaliam ciclos. Essa família de compartilhamento tem E proporcional a V; não representa um grafo denso arbitrário.

## Três tipos de evidência

A suíte soma 28 testes do grafo integrado, quatro da implementação de referência, cinco de cenários de pacotes e quatro de integração. Há casos como laços, componentes desconexas, cadeia longa, versões, alternativas, base alterada e recusa na confirmação. Os onze testes do exemplo histórico ficam separados e não devem ser somados como cobertura adicional do núcleo final.

O oráculo independente compara a existência de uma ordem topológica com a enumeração de permutações dos vértices. São todos os grafos de zero a três vértices, incluindo laços, e os de quatro sem laços, totalizando 4.627. Para cada entrada, também são verificadas as arestas do ciclo devolvido. Zero divergências é uma evidência forte nesse conjunto finito; não é uma enumeração de todos os grafos possíveis nem uma prova completa do resolvedor de versões.

A avaliação de desempenho mede custos observados. Tempos, memória e testes não são intercambiáveis: passar nos testes não demonstra rapidez; um tempo pequeno não demonstra correção.

## Como as medições foram produzidas

São 42 configurações, com um aquecimento e sete repetições por configuração, totalizando 294 amostras de tempo. Construção, DFS, Kahn e dependentes são medidos separadamente em grafos com 100, 1.000 e 5.000 vértices. O resolvedor recebe cadeias de 16, 64 e 128 pacotes e casos com quatro, oito e doze escolhas binárias de versão.

As restrições tardias usam um pacote adicional que exige as versões menores depois de escolhas anteriores. No CSV, “tamanho” conta as escolhas binárias; o catálogo dessa família tem tamanho+1 nomes. Esse detalhe evita descrever doze escolhas como um catálogo de exatamente doze nomes.

O relógio é `perf_counter_ns`. As tabelas incluem mediana, mínimo, máximo e desvio amostral. A medição do resolvedor inclui `Catalog.plan` completo, mas exclui leitura JSON, importações, interface e desenho. Nove medições separadas de memória usam `tracemalloc` na construção dos grafos: são alocações Python, não a memória total do processo, e não possuem repetições para estimar dispersão.

## O que os resultados permitem concluir

Nas restrições tardias, quatro escolhas exigiram 46 tentativas e mediana próxima de 0,49 ms. Com oito escolhas foram 766 tentativas e 8,08 ms. Com doze foram 12.286 tentativas e 144,22 ms. Todos esses casos encontraram solução. Os números ilustram o crescimento da busca e não representam uma garantia de latência para qualquer entrada ou computador.

A cadeia de 128 pacotes teve mediana de aproximadamente 21,92 ms para a resolução completa. Mesmo sem alternativas, agrupamentos e verificações são refeitos durante a busca; não se deve deduzir linearidade desse fluxo. O argumento O(V + E) dos algoritmos de grafo é apresentado por Caio e se refere aos percursos isolados.

O ambiente e os hashes das fontes medidas ficam registrados. As medições usam o mesmo grafo e resolvedor da CLI e da interface. Uma máquina, poucos tamanhos e dados sintéticos limitam a generalização. Não houve benchmark de interface, comparação com gerenciadores reais ou avaliação de um repositório Debian completo.

## Perguntas para autoavaliação

- O que é sintético e o que foi efetivamente consultado em fontes externas?
- Por que o oráculo é independente de Kahn e DFS?
- Qual a diferença entre configuração, repetição e amostra?
- Quais custos ficaram fora dos tempos e da memória medidos?
- Por que os resultados não permitem afirmar que toda a aplicação é linear ou que funciona em qualquer escala?

Consultar [dados](../dados.md), o [protocolo experimental](../experimentos/README.md), as [tabelas](../experimentos/tabelas.md), o [ambiente](../experimentos/resultados/ambiente.json) e os módulos em [experiments](../../experiments/). Não é necessário decorar os CSVs; é necessário saber localizar e explicar a origem dos números citados.

# Joao Vitor Heleno Marinho — Modelagem UML e organização acadêmica

## Conteúdo a dominar

João precisa explicar como a modelagem expressa as decisões do projeto e como elas correspondem à implementação. As fontes atuais descrevem `Requirement`, `Package`, `Catalog`, `Plan`, `Issue`, `Graph`, `Session` e `PackagePreview`. A proposta anterior de classes separadas de resolvedor e transação foi preservada como histórico e não deve ser apresentada como arquitetura já implementada.

Uma responsabilidade lógica não exige uma classe exclusiva. Hoje, `Catalog` concentra validação, resolução e consulta de remoção; `Session` concentra a transação. Os diagramas refletem essa escolha. Separações adicionais podem melhorar manutenção no futuro, mas não são requisitos que já tenham sido implementados.

## Como ler as oito vistas

| Vista | Informação a compreender |
| --- | --- |
| Casos de uso | Objetivos do usuário e fronteira do simulador. |
| Classes de domínio | Informações representadas e referências entre objetos. |
| Classes do núcleo | Distribuição real das responsabilidades entre as classes. |
| Componentes | Dependências entre entrada, interface, modelo, grafo e arquivos. |
| Sequência de planejamento | Colaboração durante uma análise e seus resultados. |
| Sequência de transação | Verificações antes de preparar e confirmar o estado. |
| Estados | Situações observáveis derivadas dos atributos da sessão. |
| Atividade | Decisões de uma chamada recursiva da busca de versões. |

As fontes são PlantUML e as figuras existem em PNG e SVG. PNG facilita inserção em documentos; SVG permite ampliar os rótulos. PlantUML é uma ferramenta de documentação e não participa dos algoritmos da aplicação.

## Cardinalidades e abstrações importantes

A multiplicidade fica na extremidade de destino: `Session -> Plan` com `0..1` significa que cada sessão pode não ter plano ou ter um plano atual. `Plan -> Graph` com `1` indica um grafo por plano, inclusive um grafo parcial de diagnóstico em caso de falha. `Package -> Requirement` com `0..*` admite uma versão sem dependências ou com várias.

As associações são referências navegáveis e não afirmam composição exclusiva. O mesmo objeto de pacote pode ser referenciado pelo catálogo e por planos. A omissão de multiplicidade inversa não autoriza concluir exclusividade. As figuras de domínio e núcleo repetem algumas relações para facilitar a leitura; a repetição não cria outra referência no programa.

O diagrama de estados é uma abstração das combinações de `plan`, `issues`, `staged` e `applied`. Não existe uma enumeração de estados correspondente no código. A atividade representa a busca recursiva de versões; a DFS usada para detectar ciclos é outro algoritmo e usa pilha explícita. Essas distinções mostram compreensão além da aparência das figuras.

## Organização dos materiais

O relatório compilado tem 14 páginas nesta revisão, dentro da faixa de 12–15. A versão identifica Engenharia de Software, PUC Minas, e registra as contribuições com referências ao Git. O arquivo de estilo foi obtido de um espelho público e a conferência com o template oficial continua registrada como pendência.

João pode coordenar a consistência entre texto, figuras, resultados e slides, mas cada colega precisa fornecer e revisar o conteúdo da própria área. Os slides e os roteiros já existem como base de preparação; a participação de todos, o ensaio e a gravação precisam acontecer de fato. Após editar o artigo, é necessário recompilar e reconferir páginas e legibilidade.

## Perguntas para autoavaliação

- Qual diferença cada vista acrescenta à explicação do sistema?
- Como interpretar `0..1`, `0..*` e `1` na extremidade de uma associação?
- Que partes são classes implementadas, abstrações explicativas e propostas históricas?
- Como provar que o diagrama de transação acompanha o comportamento atual?
- O que precisa ser revisado no relatório antes de ele se tornar a versão final?

Consultar a [galeria UML](../modelagem/modelagens-principais.md), a [revisão das figuras](../modelagem/revisao-dos-diagramas.md), o [guia de notação](../modelagem/guia-de-notacao.md), o [relatório](../relatorio/relatorio.pdf) e as [instruções de compilação](../relatorio/README.md).

# Preparação conjunta e critérios de prontidão

Cada integrante estará preparado quando conseguir explicar sua área sem depender de texto decorado, usar um exemplo real e responder às perguntas de autoavaliação. Também deve compreender a ligação com as outras áreas: Caio fornece precedência; Arthur Chaves Viana Leão escolhe versões e controla confirmação; Rafael torna isso observável; David Dias Pinto avalia as evidências; João verifica a representação; Lucas integra e contextualiza.

Antes da apresentação, o grupo precisa executar a ferramenta no computador escolhido, conferir legibilidade dos diagramas e telas e ensaiar a participação dos seis dentro dos dez minutos. O vídeo tem exigência diferente, de 12–18 minutos, com funcionamento e contribuições efetivas. Ter um documento preparatório e um roteiro não substitui essas atividades.

## Situação verificada em 12/11/2026

| Item | Situação |
| --- | --- |
| Aplicação, grafo próprio, resolução e interface | Implementados; 41 testes e oito cenários aprovados na conferência desta revisão. |
| Oráculo independente | Reexecutado: 4.627 grafos, zero divergências. |
| Desempenho | Experimentos e dados brutos disponíveis; números citados pertencem à execução documentada. |
| UML e documentação técnica | Disponíveis com fontes editáveis; revisão final de leitura e apresentação cabe ao grupo. |
| Relatório | PDF de 14 páginas com afiliação, fontes e contribuições registradas. |
| Slides e materiais de preparação | Disponíveis para estudo e ensaio. |
| Identificação e contribuições efetivas | Afiliação preenchida e contribuições registradas com os commits. Conferência dos seis integrantes pendente. |
| Conferência final do estilo SBC e dos materiais | Pendente de revisão do grupo. |
| Ensaio e demonstração na máquina de apresentação | Sem confirmação registrada. |
| Vídeo final com todos | Sem gravação ou revisão final registrada. |
| Prazo e envios individuais no Canvas | Sem confirmação registrada. |

**Conclusão da conferência:** a base técnica e os materiais de preparação estão disponíveis. A entrega acadêmica completa ainda depende das pendências acima; não há evidência para declarar que tudo está finalizado. O empacotador final recusa a conclusão enquanto essas pendências documentadas permanecerem.

O registro de [responsabilidades](../entrega/responsabilidades.md) distingue atribuições de contribuições realizadas. O [plano de entrega](../plano-entrega.md) contém a lista de fechamento. O grupo deve usar esses registros para concluir a entrega, sem transformar automaticamente uma proposta em trabalho já executado.
