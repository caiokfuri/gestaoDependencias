# Comportamento implementado

As fontes e figuras atuais são as vistas 05 a 08 de [modelagens-principais.md](modelagens-principais.md). Esta página aponta para essa referência única para evitar divergência entre sequências Mermaid antigas e PlantUML atual.

- Planejamento: `PackagePreview.analyze` → `Session.analyze` → `Catalog.plan`, com chamadas recursivas de `search` e consultas ao `Graph` próprio.
- Execução: `PackagePreview.advance` verifica o texto do pedido; `Session.advance` verifica plano, conclusão, base e pré-requisitos. Antes de confirmar a última operação, valida o estado final.
- Falhas: análise não modifica instalados; falha de confirmação não modifica instalados, preparação nem histórico daquele passo.
- Reanálise: um novo resultado substitui o plano e limpa a preparação. O histórico permanece na sessão. Uma entrada inválida invalida o plano.
- Estados: são situações observáveis derivadas dos atributos, não uma enumeração implementada.
- Remoção: consulta dependentes e ordem inversa, sem aplicar remoções.

A proposta anterior foi preservada em [historico/uml](historico/uml/). As classes separadas de resolução e transação daquele desenho são uma possibilidade futura, não uma exigência para o funcionamento atual.
