# Lista de trabalho para concluir o DepGraph

Conferência e atualização: 12/11/2026. Base: [enunciado original](../TP.pdf), [auditoria de conformidade](conformidade-enunciado.md) e estado local do repositório. Esta lista organiza o trabalho restante; não altera a implementação.

Atualização: há implementação própria isolada, medições reproduzíveis, UML atualizada e materiais acadêmicos para revisão. Um item marcado como produzido não certifica participação do grupo nem entrega no Canvas.

Legenda: `[x]` produzido, sujeito à revisão final; `[ ]` pendente ou ainda sem evidência suficiente. Os critérios de conclusão abaixo são verificações propostas para o projeto, não exigências adicionais atribuídas ao professor.

## 1. Base já produzida

- [x] Escolha do tema 9: gestão de conflitos em dependências entre pacotes.
- [x] Catálogo sintético, restrições de versão, conflitos e dependências transitivas.
- [x] Estrutura própria de grafo dirigido, DFS para ciclos e Kahn para ordenação topológica.
- [x] Busca de versões compatíveis por backtracking e análise de dependentes afetados pela remoção.
- [x] Interface gráfica com visualização e execução simulada de uma transação.
- [x] Testes automatizados: 4 do grafo próprio e 20 de pacotes; outros 11 pertencem ao exemplo histórico.
- [x] Documentação em Markdown, guia de notação e oito diagramas UML com fontes editáveis.
- [x] Repositório Git e publicação anterior da documentação no GitHub.

A validação atual aprovou 24 testes finais, oito cenários sem NetworkX e o oráculo de 4.627 grafos. O ZIP de revisão foi extraído em outra pasta e passou pela suíte final no ambiente limpo. A revisão humana da janela e dos materiais acadêmicos permanece pendente.

## 2. Fechar a versão de código que será entregue — prioridade imediata

Obrigatório pelo enunciado: estrutura e processamento próprios, interface e protótipo funcional versionado.

- [x] Definir a pasta e o comando oficiais de execução da solução final; atualizar nomes que ainda sugerem que o fluxo principal usa NetworkX.
- [x] Separar o exemplo histórico com NetworkX da distribuição executável final e de suas dependências. Preservar o histórico Git; se houver uso para comparação de desempenho, identificá-lo explicitamente como comparação.
- [x] Fornecer dependências da aplicação final sem NetworkX e instruções de instalação coerentes.
- [x] Conferir importações diretas e indiretas para assegurar que nenhuma biblioteca pronta cria ou processa o grafo da solução. Matplotlib pode continuar desenhando a interface.
- [x] Validar instalação e execução em ambiente virtual limpo, usando apenas os arquivos e dependências da entrega.
- [x] Validar os fluxos demonstráveis: instalação válida; dependência transitiva; versões incompatíveis; conflito declarado; dependência ausente; ciclo; versão alternativa; atualização explícita; impacto de remoção; transação concluída.
- [x] Conferir que falhas e planos desatualizados não confirmam alterações no estado instalado e que atingir o limite de busca informa resultado inconclusivo.
- [x] Executar os testes do grafo e dos pacotes sobre a versão final e registrar comando, ambiente e resultado. Testes do exemplo histórico devem ficar identificados separadamente.
- [ ] Fazer uma verificação manual da interface, incluindo cliques, mensagens, setas e exportações; corrigir defeitos encontrados antes de capturar as telas finais.
- [ ] Versionar as alterações locais de algoritmos, integração, testes e documentação; publicar a versão revisada no GitHub.

**Concluído quando:** uma pessoa consegue instalar e demonstrar a aplicação a partir da distribuição final, sem NetworkX no fluxo principal, e os testes pertinentes passam nessa mesma versão.

## 3. Sincronizar documentação e diagramas — prioridade alta

Obrigatório pelo enunciado: descrição do problema, justificativa da modelagem, plano de desenvolvimento e modelagem com UML avaliada.

- [x] Revisar README, guia geral e documentos para retirar descrições desatualizadas que atribuam ao núcleo atual o processamento por NetworkX.
- [x] Definir claramente o problema, entradas, saídas, escopo e justificativa para usar grafos.
- [x] Consolidar a definição formal: grafo dirigido, significado dos vértices e arestas, convenção `A → B` indicando que B depende de A, tratamento de versões e conflitos.
- [x] Distinguir grafo de dependências, restrições de versão e conflitos de coexistência; explicar por que ausência de ciclo não garante um pedido viável.
- [x] Conferir os oito diagramas contra a implementação final: casos de uso, classes de domínio, classes do núcleo, componentes, sequência de planejamento, sequência de transação, estados e atividade da resolução.
- [x] Corrigir classes, métodos, relações, cardinalidades e fluxos divergentes. Classes propostas ainda não implementadas devem ser identificadas como proposta ou substituídas pela estrutura atual.
- [x] Atualizar os documentos de comportamento para corresponder à preparação das operações e à confirmação do estado ao fim da transação.
- [x] Regenerar PNG/SVG após alterações nas fontes e revisar visualmente títulos, setas, cardinalidades, legibilidade e recortes no tamanho de uso no relatório.
- [x] Manter o guia de notação coerente com as fontes finais e registrar como reproduzir os diagramas.
- [ ] Atualizar as capturas de tela para a interface com grafo próprio e conferir os links internos da documentação.
- [ ] Consolidar o plano de desenvolvimento e registrar o que foi realizado e o que permanece como trabalho futuro.

**Concluído quando:** documentos, figuras e demonstração descrevem a mesma versão, com distinção explícita entre implementado e proposto. Não é necessário implementar todas as classes da arquitetura proposta apenas para preservar um desenho anterior.

## 4. Documentar os dados e a pesquisa de bases — prioridade alta

O enunciado pede levantamento de dados e orienta procurar bases em sites como Kaggle; não determina uso exclusivo de dados reais nem de Kaggle.

- [x] Pesquisar fontes de dados de dependências de pacotes e registrar fontes consultadas, acesso, formato e adequação ao escopo.
- [x] Decidir entre manter o catálogo sintético, incorporar uma base externa ou combinar ambos; justificar a escolha.
- [x] Documentar a origem e construção do catálogo atual, seus campos, restrições, tamanho e cenários representados.
- [ ] Se houver dados externos, registrar licença, recorte, transformações e simplificações utilizadas, com procedimento reproduzível.
- [x] Preparar entradas válidas e inválidas representativas para testes, experimentos e demonstração.

**Concluído quando:** o relatório explica de onde vêm os dados, por que são adequados e quais limitações introduzem.

## 5. Demonstrar correção e avaliar desempenho — prioridade alta

Obrigatório pelo enunciado: correção, complexidade, resultados, desempenho e limitações. O desenho experimental abaixo é uma forma proposta de atender a isso.

- [x] Descrever os invariantes da solução: precedência de dependências, uma versão por pacote, compatibilidade das restrições e preservação do estado em caso de falha.
- [x] Explicar por que Kahn produz uma ordem válida ou identifica impossibilidade por ciclo e por que a DFS retorna um caminho de ciclo real.
- [x] Relacionar cada comportamento importante a uma evidência de teste, evitando atribuir os testes históricos ao núcleo novo.
- [x] Tornar reproduzível a conferência independente dos grafos pequenos, se os números dessa verificação forem utilizados no relatório.
- [x] Documentar tempo e espaço das estruturas e algoritmos. Separar os custos lineares dos algoritmos de grafo do custo potencialmente exponencial da resolução de versões.
- [x] Criar um procedimento reproduzível de medição com tamanhos crescentes, cadeias, dependências compartilhadas, ciclos e alternativas de versão, dentro dos limites suportados.
- [x] Medir separadamente construção do grafo, DFS, Kahn, resolução de versões e, se avaliado, desenho da interface.
- [x] Registrar tamanho das entradas, número de versões/restrições, repetições, ambiente, unidade de tempo e resumo das variações observadas; escolher uma métrica de memória se ela entrar na análise.
- [x] Guardar entradas ou geradores, sementes quando aplicáveis, scripts e resultados brutos; produzir tabelas e gráficos a partir deles.
- [x] Discutir resultados, casos difíceis, limites de busca, escalabilidade e simplificações da simulação, sem confundir limite de busca com prova de inexistência de solução.

**Concluído quando:** resultados e conclusões podem ser reproduzidos e sustentam as afirmações de correção e desempenho. Comparar com NetworkX é opcional; sua utilização é permitida pelo PDF apenas para comparação de performance.

## 6. Produzir o relatório final — obrigatório

- [ ] Conferir o estilo SBC obtido de espelho público com o template oficial indicado no enunciado. Os fontes e recursos de compilação já foram preparados.
- [x] Redigir contextualização, problema, objetivos e justificativa do tema.
- [x] Apresentar dados, modelagem formal, requisitos e diagramas legíveis.
- [x] Descrever a implementação própria, os algoritmos e o funcionamento da interface.
- [x] Demonstrar a correção e analisar complexidade, experimentos, resultados e limitações.
- [x] Incluir telas, diagramas e resultados produzidos; organizar figuras extensas e artefatos de apoio de modo compatível com o limite de páginas e com as orientações do professor.
- [x] Escrever conclusões e trabalhos futuros sem apresentar propostas como funcionalidades já entregues.
- [ ] Registrar referências e responsabilidades reais de cada integrante.
- [ ] Revisar com o grupo o PDF compilado e atualizar os dados pendentes: **12 a 15 páginas**, formato SBC, figuras e tabelas legíveis, referências e links consistentes.
- [ ] Confirmar que o relatório compila a partir dos arquivos incluídos na entrega, sem depender de caminhos locais da máquina do autor.

**Concluído quando:** existem fontes `.tex`, recursos de compilação e PDF final revisado, com todos os conteúdos exigidos e a extensão de páginas correta. Markdown não substitui esse relatório.

## 7. Consolidar participação e histórico Git — obrigatório

- [ ] Confirmar a identificação dos seis integrantes e registrar as contribuições reais de cada um.
- [ ] Distribuir as pendências entre os integrantes e acompanhar as entregas efetivas.
- [ ] Conferir autoria dos commits e histórico de desenvolvimento: o professor avaliará commits individuais. Não criar contribuições fictícias nem atribuir trabalho de outra pessoa.
- [ ] Conferir se a versão utilizada no relatório, nas telas e na demonstração corresponde à versão publicada no repositório.
- [ ] Registrar o commit escolhido para a entrega, facilitando a reprodução e a conferência dos materiais.

**Concluído quando:** responsabilidades, histórico e apresentação são coerentes com a participação real do grupo.

## 8. Preparar slides e apresentação presencial — obrigatório

- [x] Criar slides cobrindo problema, modelagem, algoritmos próprios, demonstração, resultados e conclusões.
- [x] Escolher uma demonstração que evidencie dependências, conflito/ciclo e execução segura por ordenação topológica.
- [ ] Distribuir a apresentação entre **todos os integrantes**.
- [ ] Ensaiar o roteiro completo para caber em **10 minutos**, incluindo a demonstração.
- [ ] Preparar o ambiente e os arquivos usados na demonstração; como precaução recomendada, guardar capturas ou gravação para eventual falha do ambiente.

**Concluído quando:** slides revisados e ensaio comprovam participação de todos e duração adequada.

## 9. Produzir o vídeo — obrigatório

- [x] Preparar roteiro centrado no funcionamento e na explicação das funcionalidades produzidas por cada aluno.
- [ ] Garantir participação de todos e identificação das contribuições.
- [ ] Gravar a demonstração da versão final, com texto, interface e áudio compreensíveis.
- [ ] Revisar e ajustar para **12 a 18 minutos**.
- [ ] Conferir o formato, o local de envio e o acesso ao vídeo conforme a tarefa do Canvas.

**Concluído quando:** vídeo final acessível, com duração correta, funcionamento demonstrado e participação do grupo.

## 10. Montar e conferir a entrega — obrigatório

- [ ] Confirmar no Canvas o prazo completo e as instruções de envio. O PDF indica **22/11**, sem ano no cabeçalho, e determina envio até **23:59** da data da tarefa.
- [ ] Montar o `.zip` contendo **código-fonte, fontes do relatório `.tex` e PDF do relatório**, incluindo arquivos auxiliares necessários à execução e à compilação.
- [ ] Disponibilizar slides e vídeo conforme as instruções da tarefa; não presumir o canal de envio sem conferi-lo.
- [x] Incluir instruções de instalação, execução, testes e reprodução dos resultados, com identificação da versão entregue.
- [ ] Conferir o conteúdo do ZIP e excluir arquivos desnecessários, ambientes virtuais, caches e dados privados.
- [ ] Extrair o ZIP em outra pasta e verificar os comandos documentados, os arquivos do relatório e a presença dos materiais.
- [ ] Revisar todos os itens obrigatórios com o grupo. O enunciado informa nota zero se faltar item obrigatório.
- [ ] Cada integrante realizar **sua própria entrega no Canvas**, mesmo que outro integrante já tenha enviado.
- [ ] Cada integrante conferir os arquivos enviados e guardar a confirmação de entrega.

**Concluído quando:** todos os materiais exigidos foram conferidos e cada integrante confirmou seu próprio envio no prazo.

## 11. Melhorias opcionais, após fechar as obrigações

- [ ] Separar melhor responsabilidades de `Catalog`, `Session`, resolvedor e apresentação, caso isso facilite manutenção; não é necessário reescrever o sistema apenas para seguir a arquitetura proposta.
- [ ] Melhorar o posicionamento visual para grafos maiores e reduzir cruzamentos de setas e rótulos.
- [ ] Automatizar testes e verificações no GitHub.
- [ ] Ampliar o catálogo e o suporte a formatos de versões, sem comprometer o prazo e as validações existentes.
- [ ] Comparar desempenho com uma biblioteca de referência em experimento separado, se houver tempo e utilidade para a análise.

Publicar como site, instalar pacotes reais no sistema e adicionar novos algoritmos sem necessidade do problema não são entregáveis exigidos pelo enunciado.

## Ordem sugerida de execução

1. Fechar a distribuição e validar o núcleo próprio (seção 2).
2. Sincronizar modelagem/documentação e documentar os dados (seções 3–4).
3. Produzir experimentos e evidências reproduzíveis (seção 5).
4. Consolidar o relatório e as contribuições reais (seções 6–7).
5. Finalizar slides, ensaio e vídeo (seções 8–9).
6. Conferir o pacote e realizar as entregas individuais (seção 10).

Confirmar prazo e dividir responsabilidades deve ocorrer desde o início. A estrutura do relatório, a pesquisa de dados e o roteiro de apresentação também podem avançar enquanto o código é fechado; resultados, figuras e gravações finais devem usar a versão validada.
