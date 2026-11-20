# Levantamento e escolha dos dados

Foram consultados o [diretório oficial de pacotes Debian](https://www.debian.org/distrib/packages), que permite explorar listas e versões por distribuição, e a [Debian Policy sobre relações entre pacotes](https://www.debian.org/doc/debian-policy/ch-relationships.html), que descreve dependências, alternativas e conflitos.

A equipe adotou um [catálogo sintético de 27 nomes e 32 versões](../data/README.md). Usar dados Debian diretamente exigiria transformar alternativas, pacotes virtuais, regras de arquitetura e a sintaxe de versões em relações compatíveis com o modelo. O catálogo controlado permite escolher de antemão entradas que resultam em sucesso, ciclo, requisito ausente, conflito de versões e conflito declarado.

O formato e os pedidos reproduzíveis estão documentados junto ao catálogo. A avaliação de desempenho usa também famílias sintéticas geradas em memória para controlar vértices, arestas e alternativas de versão. Esses dados avaliam a ferramenta sob condições conhecidas. A frequência de conflitos e o desempenho de um repositório real ficam fora do alcance das medições.
