---
title: "DepGraph — Roteiro de gravação"
subtitle: "Grafos: modelagem, implementação e demonstração"
date: "20 de novembro de 2026"
lang: pt-BR
---

# Objetivo e formato

**Duração planejada: 15 minutos. Participação falada dos seis integrantes.**

O TP.pdf, página 3, estabelece vídeo de **12 a 18 minutos**, com foco no funcionamento e na explicação das funcionalidades produzidas por cada aluno. Também exige demonstrar os resultados e a participação de todos. Os 10 minutos se referem à apresentação presencial.

Este roteiro conecta cada contribuição aos grafos: dados, modelagem, estrutura, algoritmos, resolução, execução e visualização. As falas são sugestões para ensaio; os intervalos incluem narração, navegação, execução e transições. Não é necessário preencher todo o tempo com leitura.

**Autoria:** cada participante deve iniciar sua parte identificando sua contribuição real, em uma frase confirmada por ele. A divisão abaixo é de exposição técnica e não atribui automaticamente autoria exclusiva. Por exemplo: “Sou [nome]; minha contribuição foi [alteração efetivamente realizada], e vou demonstrar [resultado]”.

# Divisão do vídeo

| Intervalo | Participante | Foco |
|---|---|---|
| 00:00–02:00 | Lucas Batista Duarte | Integração: pedido, catálogo, grafo e plano |
| 02:00–04:00 | Joao Vitor Heleno Marinho | Modelagem e correspondência com a implementação |
| 04:00–07:00 | Caio Alves Kfuri | Estrutura própria, Kahn e DFS |
| 07:00–10:00 | Arthur Chaves Viana Leão | Resolução de versões e execução segura |
| 10:00–12:30 | Rafael Abras Lessa Freitas | Visualização, BFS de impacto e exportação |
| 12:30–15:00 | David Dias Pinto | Dados, otimizações, testes e conclusão |

# Preparação antes de gravar

- Abrir o terminal na raiz e ativar o ambiente Python com as dependências instaladas.
- Separar os arquivos indicados em cada bloco no editor; aumentar a fonte para leitura na gravação.
- Abrir o diagrama de classes e o de componentes em `docs/modelagem/imagens/`.
- Preparar a janela da aplicação e os slides em `docs/apresentacao/slides.html`. Usar slides apenas como apoio às demonstrações.
- Executar previamente `MPLBACKEND=Agg python3 scripts/verificar.py`. A primeira execução do Matplotlib pode preparar o cache de fontes; fazer isso antes da gravação.
- Identificar o nome de quem fala na tela. Gravar voz dos seis; o PDF não especifica câmera obrigatória.
- Ensaiar com cronômetro. Se faltar tempo, reduzir a navegação pelo código e manter os resultados visíveis; se sobrar tempo, explicar uma aresta ou um passo do algoritmo.

Comando para abrir a interface:

```bash
python3 -m src.main --gui
```

# 1. Lucas — Integração do fluxo (00:00–02:00)

**Tela:** terminal, `src/main.py` e interface no cenário Ambiente gráfico.

## 00:00–00:35 — Apresentar a ferramenta

**Fala sugerida:**

“Este é o DepGraph, nosso trabalho de gestão de conflitos em sistemas de dependência. O problema é descobrir quais pacotes precisam ser instalados, se as dependências são compatíveis e em qual ordem a instalação pode acontecer. O grafo dirigido é a estrutura central para representar a precedência entre os pacotes. A aplicação é uma simulação em memória; ela não instala programas no computador.”

**Ação:** executar o comando de abertura e mostrar o pedido `desktop-suite`.

## 00:35–01:25 — Mostrar a integração no código

**Fala sugerida:**

“O fluxo começa no pedido do usuário. O catálogo fornece versões e relações de dependência. A sessão chama o resolvedor, que seleciona versões e constrói o grafo do plano. Os algoritmos verificam se existe uma ordem topológica. Depois, a sessão controla a preparação dos pacotes. A interface e o terminal utilizam o mesmo núcleo e o mesmo catálogo.”

**Ação:** em `src/main.py`, apontar `Catalog.load`, a criação de `Session`, `sessao.analyze` e `abrir_gui`. Mostrar somente essas chamadas, sem ler o arquivo inteiro.

## 01:25–02:00 — Conferir uma saída concreta

**Fala sugerida:**

“No exemplo desktop-suite, o plano reúne 17 pacotes e 26 dependências. Dois pacotes já estão instalados, então o plano exige 15 instalações. O grafo representa as dependências do plano; a lista de ações contém apenas os pacotes que precisam mudar. Agora o Joao vai explicar como essa representação foi modelada.”

**Resultado a mostrar:** plano válido e seus totais na interface.

# 2. Joao — Modelagem do grafo (02:00–04:00)

**Tela:** diagrama de classes, `Package`, `Plan` e o grafo exibido na interface.

## 02:00–02:45 — Justificar a representação

**Fala sugerida:**

“O grafo é dirigido porque a relação de dependência tem sentido. Se B depende de A, representamos A apontando para B. Essa convenção permite que a ordem topológica apresente primeiro o pré-requisito e depois o dependente. Cada vértice do plano identifica um pacote, associado à versão escolhida pelo resolvedor. Não colocamos todas as versões do catálogo como instalações simultâneas.”

**Ação:** apontar uma aresta real do desenho e nomear os dois pacotes. Conferir previamente que a origem é o pré-requisito.

## 02:45–03:25 — Conectar UML e objetos implementados

**Fala sugerida:**

“Na modelagem, catálogo, plano e sessão têm funções distintas. O catálogo guarda as alternativas disponíveis. O plano guarda a seleção de versões, o grafo, a ordem, as ações e os diagnósticos. A sessão guarda o estado instalado e o progresso. Essa separação permite analisar um pedido sem executar a instalação.”

**Ação:** mostrar o diagrama de classes e os campos de `Plan` e `Session` em `src/core/domain.py`.

## 03:25–04:00 — Explicar o limite da modelagem por arestas

**Fala sugerida:**

“Uma dependência determina precedência. Já um conflito de coexistência ou de versões determina se uma seleção é permitida. Essas restrições são verificadas pelo resolvedor e não viram arestas comuns de precedência. Portanto, não basta o grafo ser acíclico: as versões também precisam ser compatíveis. O Caio vai mostrar como verificamos a estrutura e a ordenação do grafo.”

**Resultado a mostrar:** correspondência entre uma relação do domínio, uma aresta e os objetos do plano.

# 3. Caio — Estrutura, Kahn e DFS (04:00–07:00)

**Tela:** `src/graph/graph.py`, cenário Ambiente gráfico e cenário Dependência circular.

## 04:00–04:45 — Estrutura própria

**Fala sugerida:**

“A implementação do grafo usa estruturas do próprio Python. O dicionário de sucessores guarda quem depende de cada vértice, e o de predecessores guarda seus pré-requisitos. Ao adicionar uma aresta, registramos as duas relações. Também existe um conjunto auxiliar para verificar duplicatas sem percorrer a lista inteira de arestas. Não usamos NetworkX no processamento da aplicação.”

**Ação:** mostrar `__init__` e `add_aresta`. Explicar um exemplo pequeno: adicionar A para B insere B nos sucessores de A e A nos predecessores de B.

## 04:45–05:50 — Ordenação topológica

**Fala sugerida:**

“Kahn começa calculando o grau de entrada de cada vértice. Os vértices de grau zero não têm pré-requisitos pendentes e formam a primeira camada. Quando um vértice é processado, diminuímos o grau dos seus sucessores. Quem chega a zero pode entrar na próxima camada. O algoritmo trabalha com uma cópia dos graus, preservando o grafo original.

A propriedade que garante a ordem é esta: um pacote só é liberado quando todos os seus predecessores já foram processados. Se o número de vértices processados for igual ao total, encontramos uma ordenação topológica completa.”

**Ação:** mostrar `kahn` e relacionar duas camadas consecutivas ao desenho. Apontar um pré-requisito antes do dependente.

## 05:50–07:00 — Detectar e explicar um ciclo

**Ação:** selecionar Dependência circular e mostrar o diagnóstico. Voltar ao editor em `dfs_ciclo`.

**Fala sugerida:**

“Se Kahn não processa todos os vértices, existe um ciclo, mas os vértices restantes podem incluir também dependentes bloqueados. Por isso usamos DFS para reconstruir um ciclo específico. A busca distingue vértices não visitados, ativos e encerrados. Uma aresta para um vértice ativo fecha um ciclo no caminho atual.

Nossa DFS utiliza pilha explícita, evitando o limite de recursão em cadeias longas. Neste cenário, a mensagem apresenta o caminho circular e o plano fica bloqueado. Kahn e DFS percorrem vértices e arestas com custo O(V + E). O Arthur vai explicar as verificações de versões que acontecem além desses algoritmos.”

**Resultado a mostrar:** ordem válida em um cenário e caminho fechado do ciclo em outro.

# 4. Arthur — Resolução e execução segura (07:00–10:00)

**Tela:** `Catalog.plan` em `src/core/resolver.py`, cenários Versões incompatíveis, Busca de outra versão e Atualização explícita; `Session.advance` em `src/core/domain.py`.

## 07:00–07:45 — Um DAG pode representar uma seleção inviável

**Ação:** selecionar Versões incompatíveis e apontar as exigências de versões no diagnóstico.

**Fala sugerida:**

“A ausência de ciclos resolve a precedência, mas não garante que as versões possam coexistir. Neste pedido, bibliotecas compartilhadas recebem exigências incompatíveis. O resolvedor confere as restrições e os conflitos antes de aceitar uma combinação. O diagnóstico de versão é diferente do diagnóstico de ciclo.”

## 07:45–08:40 — Backtracking e construção do grafo

**Ação:** selecionar Busca de outra versão. No código, apontar o laço de candidatos, as cópias por ramo e `montar_grafo`.

**Fala sugerida:**

“O resolvedor testa candidatos de versão e propaga suas dependências. Cada ramo recebe cópias da seleção e das restrições. Quando uma escolha falha, o retorno da busca descarta as dependências daquela tentativa. Em compat-app, a versão 2.0 depende de um pacote ausente; a busca pode retornar e selecionar a versão 1.0.

Com uma seleção completa, construímos o grafo das dependências e chamamos Kahn. Se houver ciclo, a DFS fornece o diagnóstico. Portanto, a seleção define quais dependências estarão no grafo aceito. O backtracking pode ter custo exponencial; O(V + E) descreve os algoritmos de grafos, não toda a resolução.”

## 08:40–10:00 — Segurança na execução do plano

**Ação:** selecionar Atualização explícita. Mostrar o pedido com `libcore>=2.0`, avançar duas operações e apontar o progresso. Mostrar o trecho de `advance` que verifica pré-requisitos e valida o estado final.

**Fala sugerida:**

“Um pacote já instalado mantém sua versão quando não foi explicitamente solicitado para mudança. Aqui permitimos atualizar libcore no próprio pedido. A sessão recebe a ordem calculada e prepara os pacotes um a um.

Antes de preparar cada pacote, verificamos se seus pré-requisitos estão presentes com versões aceitas no estado temporário. Preparar ainda não significa confirmar a instalação: o estado instalado só é substituído após a validação final da transação. Um plano bloqueado não pode ser executado. Assim conectamos a ordenação topológica às verificações concretas da execução. O Rafael vai mostrar como esses estados aparecem na interface.”

**Resultado a mostrar:** diagnóstico de versão, alternativa 1.0 selecionada e progresso de uma transação válida.

# 5. Rafael — Visualização, BFS e exportação (10:00–12:30)

**Tela:** interface funcional, `_draw_graph` em `depgraph/app.py` e `Catalog.removal_impact`.

## 10:00–10:50 — Tecnologia da interface e visualização do grafo

**Ação:** carregar novamente Ambiente gráfico e clicar em um vértice.

**Fala sugerida:**

“A interface é uma aplicação desktop feita em Python com Matplotlib. Usamos a biblioteca para desenhar os vértices e as setas, criar botões e o campo de texto e tratar cliques. O processamento do grafo fica na nossa implementação própria.

O desenho usa as camadas de Kahn para posicionar os vértices e uma disposição circular quando há ciclo. As cores indicam os estados dos pacotes; as incompatibilidades são desenhadas separadamente das dependências. Ao clicar em um pacote, consultamos suas versões e relações.”

**Orientação de tempo:** reservar cerca de 15 segundos para o primeiro parágrafo, sobre a tecnologia da interface, e usar o restante para relacionar o desenho ao grafo.

**Ação:** apontar rapidamente o uso de `graph.kahn()` em `_draw_graph`; voltar à janela.

## 10:50–11:55 — Impacto de remoção por alcançabilidade

**Ação:** concluir as 15 preparações do cenário Ambiente gráfico; se necessário, acelerar apenas a repetição de cliques na edição. Digitar `libcore` e clicar em Impacto da remoção, sem executar uma nova análise de instalação.

**Fala sugerida:**

“Agora que o ambiente foi instalado na simulação, podemos consultar o impacto de remover libcore. Seguimos as arestas no sentido dos dependentes, usando BFS para encontrar os pacotes alcançáveis direta ou indiretamente. A lista de visitados evita processar repetidamente um mesmo vértice.

Para apresentar uma ordem de remoção em cascata, o sistema inverte a ordem topológica e filtra os pacotes afetados. Assim os dependentes aparecem antes dos seus pré-requisitos. Essa função apenas informa o impacto; não efetua a remoção.”

**Ação:** mostrar `dependentes_transitivos` em `src/graph/graph.py` e a inversão da ordem em `Catalog.removal_impact`. Explicar que BFS também tem custo O(V + E).

## 11:55–12:30 — Guardar os resultados

**Ação:** clicar em Salvar relatório JSON + imagem PNG e abrir `outputs/depgraph/pacotes.png` e `outputs/depgraph/pacotes.json`.

**Fala sugerida:**

“A exportação guarda a imagem e um relatório com os pacotes selecionados, as ações e o estado da transação. Esses arquivos permitem conferir os resultados depois da demonstração. O David vai mostrar os dados de entrada e os testes usados para verificar o comportamento.”

**Resultado a mostrar:** camadas coerentes com dependências, conjunto de dependentes afetados e arquivos exportados.

# 6. David — Dados, eficiência e validação (12:30–15:00)

**Tela:** `data/pacotes.json`, `tests/test_graph.py`, `tests/test_cli.py` e terminal.

## 12:30–13:05 — Dados que exercitam a modelagem

**Fala sugerida:**

“O catálogo é sintético, inspirado em pacotes Linux. São 27 nomes e 32 versões, com base-files e libcore inicialmente instalados. Cada registro informa nome, versão, dependências e conflitos. Os cenários foram organizados para exercitar grafos válidos, ciclos, dependências ausentes e incompatibilidades. Esses dados não são uma base real de uma distribuição Linux.”

**Ação:** mostrar um registro com dependência e outro com conflito. Relacionar a dependência à criação de uma aresta.

## 13:05–13:50 — Melhorias que preservam a complexidade

**Fala sugerida:**

“Na inserção de arestas, o conjunto auxiliar evita procurar duplicatas em toda a lista. A BFS usa deque, cuja remoção no início tem custo constante, e a DFS é iterativa. Essas escolhas evitam custos adicionais e o limite de recursão da implementação anterior.

Os testes de grande escala usam uma cadeia com 20 mil arestas e 20.001 vértices. Verificam ordenação, alcançabilidade, detecção de um ciclo longo e ausência de arestas duplicadas. Passar nesses testes mostra o comportamento nesses casos; não substitui uma análise formal nem uma medição de desempenho.”

**Ação:** apontar `TestGraphGrandeEscala`, o tamanho da cadeia e duas asserções. Não apresentar esses testes como benchmark.

## 13:50–14:35 — Executar a verificação

**Ação:** executar na raiz:

```bash
MPLBACKEND=Agg python3 scripts/verificar.py
```

**Fala sugerida:**

“A verificação executa os testes disponíveis e bloqueia a importação de NetworkX. Os testes de integração também conferem se cada aresta aponta de um pacote anterior para um posterior na ordem exportada. Outros casos verificam pedidos bloqueados e a preservação da sessão na interface.

Depois, o script renderiza os oito cenários e conclui as transações válidas, validando o estado final.”

**Resultado esperado nesta versão:** 35 testes aprovados e oito cenários renderizados. Na gravação, ler o resultado efetivamente exibido; se a suíte mudar, atualizar o número. Não atribuir ao projeto um oráculo exaustivo ou medições ainda não incorporados e reproduzidos.

## 14:35–15:00 — Fechamento

**Fala sugerida:**

“Demonstramos como o grafo representa as dependências, como Kahn estabelece a ordem, como DFS identifica ciclos e como BFS calcula o impacto de remoção. O resolvedor complementa essa análise com restrições de versão e conflitos. A ferramenta é didática, com catálogo sintético e versões simplificadas; a busca de versões pode crescer exponencialmente. Esses são os resultados e os limites da implementação apresentada.”

# Conferência da gravação

- Os seis integrantes falam e identificam suas contribuições reais.
- O vídeo final dura entre 12 e 18 minutos; a meta de ensaio é 15 minutos.
- Cada bloco conecta modelagem ou código a um resultado na ferramenta.
- Ficam visíveis a orientação das arestas, a ordem válida, um ciclo, um conflito de versões e a análise por BFS.
- As falas distinguem preparação de confirmação da transação e análise de remoção de remoção efetiva.
- Código, terminal e diagnósticos estão legíveis; áudio e transições foram revisados.
- Resultados de testes correspondem à versão gravada. Não aparecem números experimentais sem evidência reproduzida.
- Conferir no Canvas o canal de envio do vídeo e dos slides. O vídeo não substitui relatório SBC, fontes, histórico individual e os demais itens da atividade.

# Referências locais e geração do PDF

Fonte dos requisitos: `TP.pdf`, especialmente tema 9 na página 2 e observações na página 3. Código e cenários conferidos no repositório integrado, commit de referência `6d18590`.

Regerar este documento, na raiz do repositório, com Pandoc e Tectonic:

```bash
pandoc docs/apresentacao/roteiro-video.md \
  --standalone --pdf-engine=tectonic \
  -V papersize=a4 -V fontsize=11pt \
  -V geometry:margin=2.2cm \
  -V colorlinks=true -V urlcolor=blue \
  -o docs/apresentacao/roteiro-video.pdf
```
