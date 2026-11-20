# Revisão e empacotamento

O [cadastro da equipe](equipe.json) contém afiliação e contribuições com evidências do Git. Cada integrante deve conferir seu registro.

## Pacote para revisão

```bash
python scripts/empacotar.py --rascunho
```

Gera `dist/depgraph-revisao.zip` com código, testes, experimentos, dados, documentação, fontes LaTeX, PDF e slides. Exclui os protótipos executáveis com NetworkX, ambientes virtuais e caches. O manifesto informa pendências e hashes dos arquivos; o commit de base pode preceder modificações locais no pacote de revisão.

Na cópia extraída, executar os comandos do README. O gerador não instala dependências nem publica ou envia arquivos.

## Fechamento da entrega final

Conferir as contribuições com os integrantes e recompilar o relatório caso haja ajustes. O limite é de 12–15 páginas. Ensaiar a apresentação e gravar o vídeo com participação dos seis. Criar `docs/entrega/revisao-final.json` com os campos abaixo **somente após realizar as verificações**:

```json
{
  "relatorio_revisado": false,
  "estilo_sbc_conferido": false,
  "slides_revisados": false,
  "ensaio_realizado": false,
  "video_revisado": false,
  "prazo_canvas_conferido": false,
  "duracao_video_minutos": 0,
  "video_local_ou_link": ""
}
```

Registrar onde o vídeo será entregue conforme as instruções da tarefa. O script não analisa o conteúdo do vídeo nem substitui a revisão humana; um caminho informado não prova que o arquivo foi enviado. Vídeos não são adicionados automaticamente ao ZIP. O PDF exige código, fontes `.tex` e PDF no ZIP; slides e vídeo devem ser disponibilizados pelo canal indicado no Canvas.

Com os materiais revisados e versionados, executar:

```bash
python scripts/verificar.py
python scripts/empacotar.py --final
```

A opção final recusa pendências documentadas, PDF fora do limite ou fontes alteradas sem commit. Requer `pdfinfo` para conferir páginas. O ZIP final ainda deve ser extraído e conferido. Cada integrante precisa fazer sua própria entrega no Canvas e guardar o comprovante.

Os campos de revisão são um controle de conclusão do grupo, não uma certificação automática do conteúdo nem uma nova exigência atribuída ao professor.
