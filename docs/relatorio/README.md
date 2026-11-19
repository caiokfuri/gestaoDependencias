# Relatório técnico

`relatorio.tex` e `relatorio.pdf` são uma versão para revisão do grupo. O PDF compilado em 12/11/2026 tem 14 páginas, incluindo referências; reconferir após cada edição. Identificação institucional e contribuições efetivas permanecem pendentes; a divisão proposta não foi convertida em atribuições já realizadas.

## Compilar

Na raiz:

```bash
tectonic -o docs/relatorio docs/relatorio/relatorio.tex
```

Ou, dentro desta pasta, executar `pdflatex relatorio.tex` duas vezes em uma instalação LaTeX completa. A primeira compilação com Tectonic pode baixar pacotes. As figuras são referenciadas por caminhos relativos dentro de `docs/`, preservados pelo empacotador.

## Origem do estilo

O enunciado indica o [SBC Conferences Template 2017](https://www.overleaf.com/latex/templates/sbc-conferences-template/blbxwjwzdngr), atribuído à Sociedade Brasileira de Computação e disponibilizado ali sob CC BY 4.0. `sbc-template.sty` preserva os créditos de Jomi F. Hübner e Rafael H. Bordini e a atualização de dezembro de 2017.

O download público dos fontes pelo Overleaf não ficou disponível nesta sessão. O arquivo foi obtido do [espelho público do estilo](https://github.com/luiz-fleite/latex-template-sbc-conferences-v2017/blob/main/styles/sbc-template.sty), sem modificações locais. Não foi utilizada a reescrita `sbc.cls` do outro repositório do mantenedor. Conferir o arquivo com a cópia oficial do Overleaf antes da entrega definitiva.

## Pendências humanas

- Confirmar instituição, curso, identificação completa dos autores e exigências adicionais da disciplina.
- Preencher e confirmar contribuições efetivas em `docs/entrega/equipe.json` e revisar a seção correspondente do artigo.
- Revisar conteúdo, linguagem, figuras e contagem final de 12–15 páginas após qualquer edição.
- Confirmar a versão do código e os resultados que acompanham a entrega.
