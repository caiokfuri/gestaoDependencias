"""
Módulo de Catálogo e Resolvedor por Backtracking
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any
from .domain import Requirement, Package, Plan, Issue, parse_version
from ..graph.graph import Graph


class Catalog:
    """Gerencia o repositório de pacotes e suas respectivas versões."""

    def __init__(self, packages: List[Package]):
        self.packages: Dict[str, List[Package]] = {}
        for p in packages:
            self.packages.setdefault(p.name, []).append(p)
        for vers in self.packages.values():
            vers.sort(key=lambda p: parse_version(p.version), reverse=True)

    @classmethod
    def load(cls, path: str) -> Tuple["Catalog", Dict[str, str]]:
        """Carrega e valida o catálogo a partir de um arquivo JSON."""
        conteudo = json.loads(Path(path).read_text(encoding="utf-8"))
        pacotes = []
        for item in conteudo.get("pacotes", []):
            deps = tuple(Requirement(d["nome"], d.get("versao", "*")) for d in item.get("depende", []))
            conflitos = tuple(Requirement(c["nome"], c.get("versao", "*")) for c in item.get("conflita", []))
            pacotes.append(Package(item["nome"], item["versao"], deps, conflitos, item.get("descricao", "")))
        
        cat = cls(pacotes)
        instalados = conteudo.get("instalados", {})
        return cat, instalados

    def plan(self, requests: List[Requirement], installed: Dict[str, str], limit: int = 20000) -> Plan:
        """
        Busca por retrocesso (Backtracking):
        - Seleciona no máximo uma versão por pacote.
        - Descarta dependências de escolhas abandonadas.
        - Detecta incompatibilidade de versões, conflitos e dependência ausente.
        - Constrói o grafo próprio e chama o método kahn().

        Pacotes instalados que não aparecem no pedido ficam fixos na versão atual.
        Uma aresta A -> B no grafo significa que B depende de A.
        """
        class LimiteAtingido(Exception):
            pass

        requests = list(requests)
        base = dict(installed)
        solicitados = {r.name for r in requests}
        tentativas = 0
        # Falha mais profunda encontrada: (tamanho da seleção, Issue, seleção parcial)
        pior_falha: List[Any] = [None]

        def fmt(spec: str) -> str:
            return "qualquer versão" if spec in ("", "*") else spec

        def origem(o: Optional[Package]) -> str:
            return "pedido" if o is None else f"{o.name} {o.version}"

        def registrar(issue: Issue, selecao: Dict[str, Package]) -> None:
            if pior_falha[0] is None or len(selecao) > pior_falha[0][0]:
                pior_falha[0] = (len(selecao), issue, dict(selecao))

        def montar_grafo(selecao: Dict[str, Package], extras: Tuple[str, ...] = ()) -> Graph:
            g = Graph()
            for nome in list(selecao) + [n for n in extras if n]:
                g.add_vertice(nome)
            for pkg in selecao.values():
                for dep in pkg.depends:
                    g.add_aresta(dep.name, pkg.name)
            return g

        def conflito(cand: Package, selecao: Dict[str, Package]) -> Optional[Issue]:
            for c in cand.conflicts:
                outro = selecao.get(c.name)
                if outro is not None and outro.name != cand.name and c.accepts(outro.version):
                    return Issue("conflito", f"{cand.name} {cand.version} é incompatível com "
                                 f"{outro.name} {outro.version}.", (cand.name, outro.name))
            for outro in selecao.values():
                for c in outro.conflicts:
                    if c.name == cand.name and outro.name != cand.name and c.accepts(cand.version):
                        return Issue("conflito", f"{outro.name} {outro.version} é incompatível com "
                                     f"{cand.name} {cand.version}.", (outro.name, cand.name))
            return None

        def buscar(selecao: Dict[str, Package],
                   restricoes: Dict[str, List[Tuple[Requirement, Optional[Package]]]],
                   pendentes: List[str]) -> Optional[Tuple[Dict[str, Package], Graph, List[str]]]:
            nonlocal tentativas
            nome = next((n for n in pendentes if n not in selecao), None)

            if nome is None:
                # Atribuição completa: verifica ciclos com Kahn e reconstrói o ciclo com DFS.
                g = montar_grafo(selecao)
                ok, ordem, _ = g.kahn()
                if ok:
                    return selecao, g, ordem
                ciclo = g.dfs_ciclo() or []
                registrar(Issue("ciclo", "Dependência circular: " + " -> ".join(ciclo) + ".",
                                tuple(ciclo)), selecao)
                return None

            regras = restricoes.get(nome, [])
            quem_exige = tuple(o.name for _, o in regras if o is not None)

            if nome not in self.packages:
                exigido = ", ".join(origem(o) for _, o in regras) or "pedido"
                registrar(Issue("ausente", f"O pacote {nome} não existe no catálogo "
                                f"(exigido por {exigido}).", (nome,) + quem_exige), selecao)
                return None

            fixo = nome in base and nome not in solicitados
            if fixo:
                candidatos = [p for p in self.packages[nome]
                              if parse_version(p.version) == parse_version(base[nome])]
                if not candidatos:
                    registrar(Issue("ausente", f"A versão instalada {nome} {base[nome]} não existe "
                                    f"no catálogo.", (nome,)), selecao)
                    return None
            else:
                candidatos = self.packages[nome]  # Já ordenados da maior para a menor versão.

            compativeis = [p for p in candidatos if all(r.accepts(p.version) for r, _ in regras)]
            if not compativeis:
                condicoes = "; ".join(f"{fmt(r.spec)} (exigido por {origem(o)})" for r, o in regras)
                disponiveis = ", ".join(p.version for p in self.packages[nome])
                msg = f"Nenhuma versão de {nome} satisfaz: {condicoes}. Disponíveis: {disponiveis}."
                if fixo:
                    msg += (f" A versão instalada {base[nome]} é preservada; inclua {nome} no "
                            f"pedido para permitir a mudança.")
                registrar(Issue("versao", msg, (nome,) + quem_exige), selecao)
                return None

            for cand in compativeis:
                tentativas += 1
                if tentativas > limit:
                    raise LimiteAtingido()

                problema = conflito(cand, selecao)
                if problema is None:
                    # Dependências do candidato contra pacotes já escolhidos.
                    for dep in cand.depends:
                        atual = selecao.get(dep.name)
                        if atual is not None and not dep.accepts(atual.version):
                            problema = Issue("versao", f"{cand.name} {cand.version} exige "
                                             f"{dep.name} {fmt(dep.spec)}, mas a versão escolhida é "
                                             f"{atual.version}.", (dep.name, cand.name))
                            break
                if problema is not None:
                    registrar(problema, {**selecao, cand.name: cand})
                    continue

                # Cada ramo recebe cópias: voltar descarta as dependências da escolha abandonada.
                nova_selecao = {**selecao, cand.name: cand}
                novas_restricoes = {k: list(v) for k, v in restricoes.items()}
                novos_pendentes = list(pendentes)
                for dep in cand.depends:
                    novas_restricoes.setdefault(dep.name, []).append((dep, cand))
                    if dep.name not in novos_pendentes:
                        novos_pendentes.append(dep.name)

                resultado = buscar(nova_selecao, novas_restricoes, novos_pendentes)
                if resultado is not None:
                    return resultado
            return None

        restricoes_iniciais: Dict[str, List[Tuple[Requirement, Optional[Package]]]] = {}
        pendentes_iniciais: List[str] = []
        for r in requests:
            restricoes_iniciais.setdefault(r.name, []).append((r, None))
            if r.name not in pendentes_iniciais:
                pendentes_iniciais.append(r.name)
        for nome in base:
            if nome not in pendentes_iniciais:
                pendentes_iniciais.append(nome)

        try:
            resultado = buscar({}, restricoes_iniciais, pendentes_iniciais)
        except LimiteAtingido:
            parcial = pior_falha[0][2] if pior_falha[0] else {}
            issue = Issue("limite", f"Limite de {limit} tentativas atingido. Resultado inconclusivo: "
                          f"isso não prova que não existe solução.")
            return Plan(False, montar_grafo(parcial), parcial, [], [], [issue],
                        base, requests, tentativas)

        if resultado is None:
            if pior_falha[0] is None:
                issue = Issue("versao", "Nenhuma combinação de versões atende ao pedido.")
                parcial: Dict[str, Package] = {}
            else:
                _, issue, parcial = pior_falha[0]
            return Plan(False, montar_grafo(parcial, issue.nodes), parcial, [], [], [issue],
                        base, requests, tentativas)

        selecao, grafo, ordem = resultado
        acoes = [n for n in ordem if n not in base
                 or parse_version(base[n]) != parse_version(selecao[n].version)]
        return Plan(True, grafo, selecao, ordem, acoes, [], base, requests, tentativas)

    def removal_impact(self, name: str, installed: Dict[str, str]) -> Tuple[Set[str], List[str]]:
        """
        Retorna dependentes diretos e transitivos de `name`, ordem de remoção em cascata.
        A ordem remove primeiro quem depende e por último o próprio pacote.
        A consulta não altera o estado instalado.
        """
        if name not in installed:
            raise ValueError(f"O pacote {name} não está instalado.")

        g = Graph()
        for nome, versao in installed.items():
            g.add_vertice(nome)
            pkg = next((p for p in self.packages.get(nome, [])
                        if parse_version(p.version) == parse_version(versao)), None)
            if pkg is None:
                continue
            for dep in pkg.depends:
                if dep.name in installed:
                    g.add_aresta(dep.name, nome)

        afetados = g.dependentes_transitivos(name)
        ok, ordem, _ = g.kahn()
        if not ok:
            raise ValueError("O estado instalado contém dependência circular.")
        alvo = afetados | {name}
        ordem_remocao = [n for n in reversed(ordem) if n in alvo]
        return set(afetados), ordem_remocao
