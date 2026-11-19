# Área de Rafael Abras Lessa Freitas
**Atribuição:** Interface, visualização e demonstração (Tópico 6)

## Seus Arquivos:
- `gui.py`: Classe `PackageGUI`, renderização do grafo, eventos de clique, cenários didáticos e exportação.

## O que você deve dominar para a apresentação:
1. **Layout e Posicionamento:**
   - Em grafos acíclicos: posicionamento em camadas horizontais usando a lista de camadas retornada pelo algoritmo de Kahn de Caio Kfuri.
   - Em grafos com ciclo: disposição circular para evidenciar o ciclo fechado.
2. **Cores dos Vértices:**
   - **Cinza:** pacote já instalado no sistema.
   - **Roxo:** dependência necessária a ser preparada.
   - **Verde:** pacote já preparado na transação atual.
   - **Vermelho:** pacote envolvido em erro ou diagnóstico de bloqueio.
   - **Tracejado Vermelho:** aresta de incompatibilidade declarada (não entra no Kahn).
3. **Interatividade:** Clique sobre um vértice abre versões e metadados no painel inferior.

## Perguntas que o professor pode te fazer:
- *Como o usuário distingue plano, progresso parcial e conclusão?* (Pelas cores dos nós e pelo histórico no painel).
- *Como explicar um conflito de versão sem chamá-lo de ciclo?* (Explicando que é incompatibilidade lógica de intervalos de versão de uma mesma biblioteca).
- *Onde ficam os arquivos exportados e o que cada um contém?* (PNG com a imagem em alta resolução e JSON com o plano de instalação completo).

## Integração funcional

`PackageGUI` reutiliza a interface incorporada em `depgraph/app.py` e preserva a sessão criada pela CLI. Execute `python3 -m src.main --gui` ou `python3 -m depgraph`. Ambas as entradas usam o núcleo em `src/core/`, os algoritmos em `src/graph/` e o catálogo em `data/pacotes.json`.
