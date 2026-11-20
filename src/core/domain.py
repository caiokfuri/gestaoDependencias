"""
Módulo de Domínio de Pacotes e Transações
"""

from dataclasses import dataclass, field
import re
from typing import Dict, List, Tuple, Set, Optional, Any


def parse_version(v: str) -> Tuple[int, int, int]:
    """Normaliza versões numéricas de 1 a 3 componentes (ex: '1.0' -> (1, 0, 0))."""
    if not isinstance(v, str) or not re.fullmatch(r"\d+(?:\.\d+){0,2}", v):
        raise ValueError(f"Versão inválida: {v!r}")
    partes = tuple(int(x) for x in v.split("."))
    return partes + (0,) * (3 - len(partes))


@dataclass(frozen=True)
class Requirement:
    """Restrição sobre a versão de um pacote requerido (ex: 'libssl >= 2.0')."""
    name: str
    spec: str = "*"

    def accepts(self, version: str) -> bool:
        """Verifica se uma versão atende às condições numéricas da restrição."""
        if self.spec in ("", "*"):
            return True
        alvo = parse_version(version)
        for cond in self.spec.split(","):
            m = re.fullmatch(r"\s*(>=|<=|==|=|>|<)\s*(\d+(?:\.\d+){0,2})\s*", cond)
            if not m:
                continue
            op, val = m[1], parse_version(m[2])
            ops = {">=": alvo >= val, "<=": alvo <= val, ">": alvo > val,
                   "<": alvo < val, "=": alvo == val, "==": alvo == val}
            if not ops.get(op, False):
                return False
        return True


@dataclass(frozen=True)
class Package:
    """Representação de um pacote disponível no catálogo com suas versões e regras."""
    name: str
    version: str
    depends: Tuple[Requirement, ...] = ()
    conflicts: Tuple[Requirement, ...] = ()
    description: str = ""


@dataclass
class Issue:
    """Diagnóstico de erro durante a análise de resolução."""
    kind: str  # 'versao', 'conflito', 'ausente', 'ciclo', 'limite'
    message: str
    nodes: Tuple[str, ...] = ()


@dataclass
class Plan:
    """Resultado gerado pela análise do catálogo para um determinado pedido."""
    success: bool
    graph: Any  # Objeto Graph
    selected: Dict[str, Package]
    order: List[str]
    actions: List[str]  # Pacotes que exigem nova instalação ou upgrade
    issues: List[Issue]
    base: Dict[str, str]
    requests: List[Requirement]
    attempts: int = 0


@dataclass
class Session:
    """
    Máquina de estados da transação em memória.
    Garante que instalações ocorram passo a passo com validação de pré-requisitos,
    atualizando o estado do sistema apenas após a validação do último pacote.
    """
    catalog: Any
    installed: Dict[str, str]
    plan: Optional[Plan] = None
    staged: List[str] = field(default_factory=list)
    applied: bool = False
    history: List[str] = field(default_factory=list)

    def analyze(self, text_request: str) -> Plan:
        padrao = r"\s*([A-Za-z0-9][A-Za-z0-9._+-]*)\s*(?:(>=|<=|==|=|>|<)\s*(\d+(?:\.\d+){0,2}))?\s*"
        requests: List[Requirement] = []
        try:
            if not isinstance(text_request, str) or not text_request.strip():
                raise ValueError("Informe ao menos um pacote no pedido.")
            for item in text_request.split(","):
                m = re.fullmatch(padrao, item)
                if not m:
                    raise ValueError(f"Item de pedido inválido: {item.strip()!r}.")
                spec = f"{m[2]}{m[3]}" if m[2] else "*"
                requests.append(Requirement(m[1], spec))
        except ValueError:
            # Pedido editado com erro: o plano anterior deixa de ser executável.
            self.plan = None
            self.staged = []
            self.applied = False
            raise

        self.staged = []
        self.applied = False
        self.plan = self.catalog.plan(requests, dict(self.installed))
        return self.plan

    def advance(self) -> Optional[str]:
        """
        Retorna o nome do pacote preparado neste avanço, ou None quando não há operação
        pendente (plano sem operações ou transação já concluída). O estado instalado só é
        substituído depois que a última operação é preparada e o estado final é validado.
        Situações que impedem o avanço geram RuntimeError sem alterar `installed`.
        """
        plan = self.plan
        if plan is None:
            raise RuntimeError("Não há plano analisado; execute uma nova análise.")
        if not plan.success:
            raise RuntimeError("O plano atual não é executável; corrija o pedido e analise novamente.")

        esperado = dict(plan.base)
        if self.applied:
            esperado.update({n: plan.selected[n].version for n in plan.actions})
        if self.installed != esperado:
            raise RuntimeError("O estado instalado mudou desde a análise; execute uma nova análise.")
        if self.applied:
            return None

        temporario = dict(self.installed)
        temporario.update({n: plan.selected[n].version for n in self.staged})

        preparado: Optional[str] = None
        pendentes = [n for n in plan.actions if n not in self.staged]
        if pendentes:
            nome = pendentes[0]
            pkg = plan.selected[nome]
            for dep in pkg.depends:
                versao = temporario.get(dep.name)
                if versao is None or not dep.accepts(versao):
                    raise RuntimeError(f"Pré-requisito não atendido para {nome} {pkg.version}: "
                                       f"{dep.name} {dep.spec}.")
            temporario[nome] = pkg.version
            if len(pendentes) == 1:
                self._validar_estado_final(temporario)
            self.staged.append(nome)
            acao = "Atualizado" if nome in plan.base else "Preparado"
            self.history.append(f"{acao}: {nome} {pkg.version}")
            preparado = nome
            if len(pendentes) > 1:
                return preparado

        if not pendentes:
            self._validar_estado_final(temporario)
        self.installed = temporario
        self.applied = True
        self.history.append("Transação concluída.")
        return preparado

    def _validar_estado_final(self, estado: Dict[str, str]) -> None:
        """Confere existência, dependências, conflitos e ausência de ciclos no estado final."""
        from ..graph.graph import Graph

        pacotes: Dict[str, Package] = {}
        for nome, versao in estado.items():
            pkg = next((p for p in self.catalog.packages.get(nome, [])
                        if parse_version(p.version) == parse_version(versao)), None)
            if pkg is None:
                raise RuntimeError(f"Validação final falhou: {nome} {versao} não existe no catálogo.")
            pacotes[nome] = pkg

        g = Graph()
        for pkg in pacotes.values():
            g.add_vertice(pkg.name)
            for dep in pkg.depends:
                if dep.name not in estado or not dep.accepts(estado[dep.name]):
                    raise RuntimeError(f"Validação final falhou: {pkg.name} exige "
                                       f"{dep.name} {dep.spec}.")
                g.add_aresta(dep.name, pkg.name)
            for c in pkg.conflicts:
                if c.name in estado and c.name != pkg.name and c.accepts(estado[c.name]):
                    raise RuntimeError(f"Validação final falhou: {pkg.name} é incompatível com "
                                       f"{c.name} {estado[c.name]}.")
        if not g.kahn()[0]:
            raise RuntimeError("Validação final falhou: dependência circular no estado final.")
