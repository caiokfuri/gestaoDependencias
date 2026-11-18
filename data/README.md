# Dados

## `pacotes.json`

Catálogo **sintético** inspirado em pacotes Linux. Nomes, versões e relações são fictícios; não são metadados de uma distribuição real.

- **Origem:** catálogo de exemplo criado pelo grupo no protótipo inicial, no repositório base [caslulu/trab-grafo](https://github.com/caslulu/trab-grafo).
- **Conteúdo:** 27 nomes de pacote, 32 versões; estado inicial com `base-files 1.0` e `libcore 1.0` instalados.
- **Carregamento:** `Catalog.load("data/pacotes.json")` em `src/core/resolver.py`, que retorna `(catalogo, instalados)`.

### Formato

```json
{
  "descricao": "texto livre",
  "instalados": { "nome": "versao" },
  "pacotes": [
    {
      "nome": "app",
      "versao": "1.0",
      "descricao": "texto livre",
      "depende": [ { "nome": "libx", "versao": ">=1.0,<2.0" } ],
      "conflita": [ { "nome": "outro-app" } ]
    }
  ]
}
```

- Versões: 1 a 3 componentes numéricos (`1`, `1.2`, `1.2.3`).
- Restrição `versao` é opcional (ausente = qualquer versão); várias condições separadas por vírgula.
- `conflita` é verificado nos dois sentidos, mesmo se declarado só em um pacote.

### Pedidos que exercitam cada cenário

| Cenário | Pedido | Resultado esperado |
| --- | --- | --- |
| Ambiente gráfico | `desktop-suite` | Sucesso: 17 pacotes, 26 dependências, 15 instalações |
| Versões incompatíveis | `modern-browser, legacy-backup, libcore>=2.0` | Diagnóstico `versao` |
| Pacotes incompatíveis | `web-server, alternate-server` | Diagnóstico `conflito` |
| Dependência ausente | `broken-app` | Diagnóstico `ausente` |
| Dependência circular | `cycle-alpha` | Diagnóstico `ciclo` |
| Atualização explícita | `modern-browser, libcore>=2.0` | Sucesso com upgrade de `libcore` |
| Versão instalada fixa | `modern-browser` | Diagnóstico `versao` (libcore instalada é preservada) |
| Busca de outra versão | `compat-app` | Sucesso escolhendo `compat-app 1.0` |

Os exemplos `com_ciclo.json` e `sem_ciclo.json` do repositório base usam o formato antigo de **tarefas** e não foram copiados, pois são incompatíveis com `Catalog.load`.
