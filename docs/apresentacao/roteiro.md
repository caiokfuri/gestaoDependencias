# Roteiros para ensaio e gravação

Antes do ensaio, cada integrante deve estudar o [material preparatório da equipe](preparacao-equipe.md), também disponível em [PDF](preparacao-equipe.pdf). Ele desenvolve os conceitos e exemplos de cada área; os roteiros abaixo organizam o ensaio e a gravação.

Os slides em [slides.html](slides.html) abrem localmente, sem bibliotecas nem conexão. Navegar com as setas ou os botões. A impressão inclui todas as páginas em formato paisagem. As imagens usam caminhos relativos; manter esta pasta dentro de `docs/`.

## Apresentação presencial — 10 minutos

Divisão sugerida, sujeita às contribuições reais e ao ensaio. Todos devem participar; não afirmar que uma funcionalidade foi produzida por alguém antes da confirmação.

| Tempo | Responsável sugerido | Conteúdo |
| --- | --- | --- |
| 0:00–1:00 | Lucas | Slides 1–2: objetivo, entrada, saída e escopo. |
| 1:00–2:00 | Joao | Slides 3–4: orientação das arestas e módulos reais. |
| 2:00–3:30 | Caio | Slide 5: Kahn, DFS, dependentes e complexidade. |
| 3:30–5:00 | Arthur Chaves Viana Leão | Slide 6: seleção de versões e confirmação segura. |
| 5:00–7:00 | Rafael | Slide 7: demonstração ao vivo, com pedido válido e diagnósticos. |
| 7:00–9:00 | David Dias Pinto | Slides 8–9: testes, oráculo e resultados medidos. |
| 9:00–10:00 | Lucas, com conclusão acordada pelo grupo | Slide 10: limitações e conclusão. |

Preparar a janela antes do início. Na demonstração principal: `desktop`, um avanço, conclusão, `versoes`, `ciclo`, `alternativa`. Se os dois minutos ficarem curtos, priorizar instalação, versões e ciclo; explicar remoção verbalmente. Ensaiar com cronômetro e guardar capturas como apoio para falha do ambiente.

## Vídeo — roteiro de 15 minutos

O enunciado exige de 12 a 18 minutos, foco no funcionamento e explicação das funcionalidades produzidas por cada aluno. O roteiro é uma base de gravação; não substitui o vídeo final.

| Tempo | Responsável sugerido | Demonstração e explicação |
| --- | --- | --- |
| 0:00–2:00 | Lucas | Abrir a aplicação; mostrar comando de execução, catálogo e pedido; contextualizar o problema. |
| 2:00–4:00 | Joao | Mostrar as classes e os módulos implementados e relacioná-los aos controles da interface. |
| 4:00–6:30 | Caio | Explicar setas do plano, ordem de instalação e caminho do ciclo; apontar o algoritmo próprio correspondente. |
| 6:30–9:00 | Arthur Chaves Viana Leão | Mostrar incompatibilidade de versões, alternativa viável, atualização explícita e confirmação da transação. |
| 9:00–11:30 | Rafael | Inspecionar pacote, preparar/concluir transação, consultar remoção e exportar JSON/PNG. |
| 11:30–14:00 | David Dias Pinto | Executar a verificação; mostrar dados brutos, gráfico e limitação da busca. |
| 14:00–15:00 | Grupo | Fechar com resultados, limitações e contribuições efetivas confirmadas. |

Antes de gravar, ajustar os trechos a quem efetivamente contribuiu, conferir legibilidade da tela e som, evitar dados pessoais desnecessários e ensaiar a transição entre participantes. Depois, conferir duração, participação dos seis e acesso ao arquivo no local exigido pelo Canvas.

## Pendências

- Confirmar participação e contribuições; nomes completos atualizados em 13/11/2026.
- Ensaiar e ajustar os tempos.
- Gravar e revisar o vídeo final.
- Confirmar no Canvas como enviar slides e vídeo.

## Reprodução do material preparatório em PDF

Na raiz, com Pandoc e Tectonic instalados:

```bash
pandoc docs/apresentacao/preparacao-equipe.md --standalone --toc --toc-depth=1 --number-sections --pdf-engine=tectonic -V papersize=a4 -V fontsize=11pt -V geometry:margin=2.4cm -V colorlinks=true -V linkcolor=blue -V urlcolor=blue -o docs/apresentacao/preparacao-equipe.pdf
```

Essas ferramentas são dependências de geração de documentos, separadas das dependências da aplicação. A primeira compilação pode baixar pacotes LaTeX. O PDF preparatório não substitui o relatório SBC nem está sujeito ao limite de páginas dele.
