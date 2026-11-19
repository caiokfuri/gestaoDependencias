# Área de Lucas Batista Duarte
**Atribuição:** Integração, conformidade e entrega (Tópico 3)

## Seus Arquivos:
- [`src/main.py`](../../src/main.py): entrada CLI integrada à aplicação funcional de `depgraph/`.
- [`requirements.txt`](../../requirements.txt): dependências do ambiente Python.
- [`checklist_entrega.md`](checklist_entrega.md): checklist para o empacotamento e envio no Canvas.

A CLI pode ser consultada com `python3 -m src.main --help`, a partir da raiz do repositório. A entrada utiliza a aplicação funcional incorporada de `trab-grafo`, com catálogo, sessão, interface e exportação. O catálogo padrão fica em `david_dias_pinto/data/pacotes.json`.

## O que você deve dominar para a apresentação:
1. **Integração dos Módulos:** Como a GUI do Rafael chama a Session do Arthur, que consulta o Catalog, monta o Graph do Caio Kfuri e obtém a ordem de instalação.
2. **Diferença entre Catálogo, Plano e Sessão:**
   - Catálogo = universo de pacotes e versões disponíveis.
   - Plano = resultado de uma análise de pedido para um estado específico.
   - Sessão = estado vivo da simulação em memória.
3. **Conformidade com o Enunciado:** Garantir que todos os itens obrigatórios do PDF do professor estão cobertos e empacotados no `.zip`.

## Perguntas que o professor pode te fazer:
- *Por que o grafo é central para resolver o problema escolhido?* (Porque determina a ordem estrita de precedência de instalação, detecta ciclos e analisa impacto de dependentes).
- *Como outra pessoa prepara o ambiente e consulta a CLI a partir do zip?* (`python3 -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt`, `python3 -m src.main --help`). Para abrir a interface, execute `python3 -m src.main`.
