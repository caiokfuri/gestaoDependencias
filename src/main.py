"""
Ponto de entrada do DepGraph — Gestão de Conflitos em Sistemas de Dependência.

Este módulo NÃO implementa algoritmos de grafos. Ele só "costura" as partes:

    data/pacotes.json  ->  Catalog.load()      (src/core/resolver.py)
                       ->  Session.analyze()   (src/core/domain.py)  -> Plan
                       ->  Graph.kahn()        (src/graph/graph.py)  -> camadas/ordem
                       ->  saída no terminal, JSON ou interface gráfica

Executar a partir da raiz do repositório (o código usa imports relativos,
por isso é "python -m src.main" e não "python src/main.py"):

    python -m src.main                              # cenário padrão (desktop) no terminal
    python -m src.main --cenario ciclo              # outro cenário de demonstração
    python -m src.main --pedidos "modern-browser, libcore>=2.0"
    python -m src.main --listar                     # catálogo completo
    python -m src.main --simular                    # executa a transação passo a passo
    python -m src.main --remover libcore            # impacto da remoção de um pacote
    python -m src.main --json saida/plano.json      # exporta o plano em JSON
    python -m src.main --gui                        # abre a interface gráfica
"""

# --- Imports -----------------------------------------------------------------
# Somente biblioteca padrão do Python + módulos do próprio projeto.
# Nenhuma biblioteca de grafos (NetworkX etc.) é usada, conforme exige o TP.
import argparse                       # leitura das opções de linha de comando
import json                           # gravação do plano em arquivo .json
import sys                            # stdout/stderr e código de saída do programa
from pathlib import Path              # caminhos de arquivo independentes de SO
from typing import Any, Dict, List, Optional

from .core.domain import Plan, Session      # Plan = resultado da análise; Session = transação
from .core.resolver import Catalog          # catálogo de pacotes + resolvedor (backtracking)

# --- Constantes --------------------------------------------------------------
# RAIZ aponta para a pasta do repositório (dois níveis acima deste arquivo:
# src/main.py -> src/ -> raiz). Assim o catálogo padrão é encontrado mesmo
# que o programa seja chamado de outra pasta.
RAIZ = Path(__file__).resolve().parent.parent
CATALOGO_PADRAO = RAIZ / "data" / "pacotes.json"

# Cenários de demonstração usados na apresentação.
# Cada chave vira uma opção de --cenario e aponta para (título, pedido).
# O pedido é o mesmo texto que o usuário digitaria: nomes separados por vírgula,
# opcionalmente com restrição de versão (ex.: "libcore>=2.0").
CENARIOS: Dict[str, tuple] = {
    "desktop": ("Ambiente gráfico", "desktop-suite"),                                    # sucesso: 17 pacotes
    "versoes": ("Versões incompatíveis", "modern-browser, legacy-backup, libcore>=2.0"), # libssl <2.0 vs >=2.0
    "conflito": ("Pacotes incompatíveis", "web-server, alternate-server"),               # conflito declarado
    "ausente": ("Dependência ausente", "broken-app"),                                    # pacote fora do catálogo
    "ciclo": ("Dependência circular", "cycle-alpha"),                                    # ciclo achado pela DFS
    "upgrade": ("Atualização explícita", "modern-browser, libcore>=2.0"),                # libcore 1.0 -> 2.0
    "instalado": ("Versão instalada fixa", "modern-browser"),                            # libcore fixa bloqueia
    "alternativa": ("Busca de outra versão", "compat-app"),                              # backtracking volta versão
}


def criar_parser() -> argparse.ArgumentParser:
    """
    Monta o leitor de argumentos da linha de comando (argparse).

    Cada add_argument define uma opção aceita pelo programa. O argparse cuida
    sozinho de validar as escolhas (ex.: --cenario só aceita chaves de CENARIOS),
    gerar o texto de ajuda (--help) e devolver tudo em um objeto `args`.
    """
    parser = argparse.ArgumentParser(
        prog="python -m src.main",
        description="DepGraph: resolve dependências e conflitos de instalação de pacotes "
                    "usando grafos implementados pelo grupo.",
    )
    parser.add_argument("--cenario", choices=list(CENARIOS), default="desktop",
                        help="Cenário de demonstração (padrão: desktop).")
    parser.add_argument("--pedidos",
                        help="Pedido livre, separado por vírgulas: 'nome, nome>=1.0'. "
                             "Substitui o pedido do cenário.")
    parser.add_argument("--catalogo", type=Path, default=CATALOGO_PADRAO,
                        help="Arquivo JSON do catálogo (padrão: data/pacotes.json).")
    parser.add_argument("--listar", action="store_true",
                        help="Lista versões, dependências e conflitos do catálogo e encerra.")
    parser.add_argument("--simular", action="store_true",
                        help="Executa a transação simulada passo a passo após o planejamento.")
    parser.add_argument("--remover", metavar="PACOTE",
                        help="Mostra o impacto da remoção de um pacote instalado e encerra.")
    parser.add_argument("--json", type=Path, metavar="ARQUIVO",
                        help="Exporta o plano analisado em JSON.")
    parser.add_argument("--gui", action="store_true",
                        help="Abre a interface gráfica com o pedido analisado.")
    return parser


def _fmt_spec(spec: str) -> str:
    """
    Formata uma restrição de versão para exibição.

    "*" ou "" significam "qualquer versão" e não são mostrados;
    qualquer outra restrição ganha um espaço na frente (ex.: " >=2.0"),
    para ficar "libcore >=2.0" ao ser concatenada ao nome.
    """
    return "" if spec in ("", "*") else f" {spec}"


def listar_catalogo(catalogo: Catalog, instalados: Dict[str, str]) -> None:
    """
    Imprime o catálogo inteiro (opção --listar).

    - catalogo.packages é um dicionário {nome: [versões]}, já ordenado da
      maior para a menor versão pelo construtor do Catalog.
    - Para cada versão mostra suas dependências e conflitos declarados.
    - Marca com [instalado] a versão presente no estado inicial do sistema.
    Não analisa nada nem monta grafo; serve para conhecer os dados.
    """
    total_versoes = sum(len(v) for v in catalogo.packages.values())
    print(f"Catálogo: {len(catalogo.packages)} pacotes, {total_versoes} versões.")
    print("Instalados: " + (", ".join(f"{n} {v}" for n, v in instalados.items()) or "nenhum"))
    print()
    for nome in sorted(catalogo.packages):
        for pkg in catalogo.packages[nome]:
            marca = " [instalado]" if instalados.get(nome) == pkg.version else ""
            print(f"{pkg.name} {pkg.version}{marca}")
            if pkg.depends:
                deps = ", ".join(d.name + _fmt_spec(d.spec) for d in pkg.depends)
                print(f"    depende: {deps}")
            if pkg.conflicts:
                confs = ", ".join(c.name + _fmt_spec(c.spec) for c in pkg.conflicts)
                print(f"    conflita: {confs}")


def plano_para_dict(plan: Plan) -> Dict[str, Any]:
    """
    Converte um Plan (objeto Python) em dicionário simples, pronto para JSON.

    O Plan guarda objetos (Package, Requirement, Graph) que o json não sabe
    gravar; aqui cada parte vira texto, número, lista ou dicionário:

    - sucesso:          True se existe plano executável.
    - pedido:           o que o usuário pediu (nome + restrição).
    - instalados_base:  estado do sistema no momento da análise.
    - selecionados:     versão escolhida pelo backtracking para cada pacote.
    - ordem_instalacao: ordem topológica (Kahn) de todos os selecionados.
    - acoes:            só o que muda: instalar novo ou atualizar existente.
    - arestas:          arestas A -> B do grafo (B depende de A).
    - diagnosticos:     motivos do bloqueio (versao/conflito/ausente/ciclo/limite).
    - tentativas:       candidatos explorados pelo backtracking (útil nos experimentos).

    Usado pelo --json e pensado para ser reaproveitado pela exportação da GUI.
    """
    return {
        "sucesso": plan.success,
        "pedido": [{"nome": r.name, "versao": r.spec} for r in plan.requests],
        "instalados_base": dict(plan.base),
        "selecionados": {n: p.version for n, p in plan.selected.items()},
        "ordem_instalacao": list(plan.order),
        "acoes": [
            {"pacote": n, "versao": plan.selected[n].version,
             "tipo": "atualizar" if n in plan.base else "instalar",
             "versao_anterior": plan.base.get(n)}
            for n in plan.actions
        ],
        "arestas": [{"de": u, "para": v} for u, v in plan.graph.arestas],
        "diagnosticos": [{"tipo": i.kind, "mensagem": i.message, "pacotes": list(i.nodes)}
                         for i in plan.issues],
        "tentativas": plan.attempts,
    }


def mostrar_plano(plan: Plan, titulo: str, pedido: str) -> None:
    """
    Imprime no terminal o resultado da análise de um pedido.

    Se o plano FALHOU: lista os diagnósticos (Issue) com o tipo entre colchetes.
    Um conflito de versão não é um ciclo; por isso cada tipo aparece separado.

    Se o plano DEU CERTO:
    1. Mostra as camadas do algoritmo de Kahn. Cada camada é um grupo de
       pacotes cujos pré-requisitos já estão nas camadas anteriores, ou seja,
       poderiam ser instalados "em paralelo". É a mesma divisão que a GUI usa
       para desenhar o grafo em níveis.
    2. Mostra só as operações necessárias (plan.actions), na ordem topológica:
       pacotes já instalados na versão certa não aparecem; os que mudam de
       versão aparecem como "atualizar".
    """
    print(f"== {titulo} ==")
    print(f"Pedido: {pedido}")
    print(f"Candidatos explorados: {plan.attempts}")
    if not plan.success:
        print("Resultado: BLOQUEADO")
        for issue in plan.issues:
            print(f"  [{issue.kind}] {issue.message}")
        return

    print(f"Resultado: OK — {len(plan.selected)} pacotes, {len(plan.graph.arestas)} dependências.")
    # kahn() devolve (sucesso, ordem, camadas); aqui só interessam as camadas.
    _, _, camadas = plan.graph.kahn()
    print("Camadas (Kahn):")
    for i, camada in enumerate(camadas or []):
        itens = ", ".join(f"{n} {plan.selected[n].version}" for n in camada)
        print(f"  {i}: {itens}")
    if plan.actions:
        print("Operações, em ordem:")
        for passo, nome in enumerate(plan.actions, 1):
            nova = plan.selected[nome].version
            if nome in plan.base:
                print(f"  {passo:2}. atualizar {nome} {plan.base[nome]} -> {nova}")
            else:
                print(f"  {passo:2}. instalar  {nome} {nova}")
    else:
        print("Nenhuma operação necessária: tudo já está instalado.")


def simular(sessao: Session) -> None:
    """
    Executa a transação simulada até o fim (opção --simular).

    Cada chamada de sessao.advance() "prepara" UM pacote, conferindo antes se
    os pré-requisitos dele já estão no estado temporário com versão aceita.
    O estado instalado real (sessao.installed) só é trocado quando o último
    pacote é preparado e o estado final inteiro é validado
    (dependências, conflitos e ausência de ciclos) — tudo ou nada.

    No fim imprime o histórico da transação e o estado final do sistema.
    Nenhum comando real de instalação é executado.
    """
    print()
    print("== Transação simulada ==")
    while not sessao.applied:
        sessao.advance()
    for linha in sessao.history:
        print(f"  {linha}")
    print("Estado final: " + ", ".join(f"{n} {v}" for n, v in sorted(sessao.installed.items())))


def mostrar_remocao(catalogo: Catalog, instalados: Dict[str, str], nome: str) -> None:
    """
    Mostra o impacto de remover um pacote instalado (opção --remover).

    catalogo.removal_impact monta o grafo dos pacotes instalados e:
    - usa BFS (Graph.dependentes_transitivos) para achar todos que dependem
      do pacote, direta ou indiretamente;
    - usa a ordem topológica INVERTIDA para dizer a ordem segura de remoção
      em cascata: primeiro quem depende, por último o próprio pacote.
    Só analisa; não remove nada do estado instalado.
    """
    afetados, ordem = catalogo.removal_impact(nome, instalados)
    print(f"== Impacto da remoção de {nome} ==")
    if afetados:
        print(f"Dependentes afetados ({len(afetados)}): {', '.join(sorted(afetados))}")
    else:
        print("Nenhum pacote instalado depende dele.")
    print("Ordem de remoção em cascata: " + " -> ".join(ordem))


def abrir_gui(sessao: Session) -> None:
    """
    Abre a interface gráfica (opção --gui) com o plano já analisado.

    O import fica DENTRO da função de propósito: o modo terminal funciona
    mesmo que a GUI (e o matplotlib) não estejam disponíveis.
    Enquanto os métodos da PackageGUI estiverem com `pass` (item I-6 do
    SPEC), esta opção não abre janela nenhuma.
    """
    from .ui.gui import PackageGUI

    gui = PackageGUI(sessao)
    if sessao.plan is not None:
        gui.draw_graph(sessao.plan)
    gui.show()


def main(argv: Optional[List[str]] = None) -> int:
    """
    Fluxo principal do programa. Devolve o código de saída:
        0 = sucesso;
        1 = plano bloqueado ou transação interrompida;
        2 = erro de entrada (catálogo inválido, pedido malformado, pacote inexistente).

    `argv` permite chamar main(["--cenario", "ciclo"]) em testes, sem terminal;
    quando é None, o argparse lê os argumentos reais da linha de comando.

    Ordem das etapas:
    1. Ajusta acentuação do console.
    2. Lê as opções.
    3. Carrega o catálogo JSON.
    4. Opções que só consultam e encerram: --listar, --remover.
    5. Escolhe o pedido (cenário ou --pedidos) e analisa com Session.analyze
       (é aqui que roda o backtracking + Kahn + DFS de ciclo).
    6. Mostra o plano; depois, opcionalmente, --json, --simular e --gui.
    """
    # 1. O console do Windows usa outra codificação por padrão e mostraria
    #    "n�o" no lugar de "não". Forçamos UTF-8 na saída normal e na de erro.
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8")

    # 2. Lê as opções digitadas.
    args = criar_parser().parse_args(argv)

    # 3. Carrega catálogo e estado instalado inicial do arquivo JSON.
    try:
        catalogo, instalados = Catalog.load(str(args.catalogo))
    except (OSError, ValueError, KeyError) as erro:
        print(f"Erro ao carregar o catálogo {args.catalogo}: {erro}", file=sys.stderr)
        return 2

    # 4. Consultas que não precisam de pedido.
    if args.listar:
        listar_catalogo(catalogo, instalados)
        return 0

    if args.remover:
        try:
            mostrar_remocao(catalogo, instalados, args.remover)
        except ValueError as erro:
            print(f"Erro: {erro}", file=sys.stderr)
            return 2
        return 0

    # 5. Define o pedido: o do cenário escolhido, ou o texto livre de --pedidos.
    titulo, pedido = CENARIOS[args.cenario]
    if args.pedidos:
        titulo, pedido = "Pedido personalizado", args.pedidos

    # A Session recebe uma CÓPIA do estado instalado (dict(...)) para que a
    # simulação nunca altere o dicionário original carregado do arquivo.
    sessao = Session(catalogo, dict(instalados))
    try:
        plan = sessao.analyze(pedido)
    except ValueError as erro:
        print(f"Pedido inválido: {erro}", file=sys.stderr)
        return 2

    # 6. Saídas.
    mostrar_plano(plan, titulo, pedido)

    if args.json:
        # Cria a pasta de destino se ainda não existir.
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(plano_para_dict(plan), ensure_ascii=False, indent=2),
                             encoding="utf-8")
        print(f"\nPlano exportado em {args.json}")

    if args.simular:
        # Só faz sentido simular um plano executável.
        if not plan.success:
            print("\nTransação não executada: o plano está bloqueado.", file=sys.stderr)
            return 1
        try:
            simular(sessao)
        except RuntimeError as erro:
            print(f"Transação interrompida: {erro}", file=sys.stderr)
            return 1

    if args.gui:
        abrir_gui(sessao)

    return 0 if plan.success else 1


# Só executa main() quando o arquivo é rodado como programa
# (python -m src.main). Se for importado por outro módulo ou teste,
# nada roda automaticamente.
if __name__ == "__main__":
    sys.exit(main())
