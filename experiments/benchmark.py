"""Mede construção, consultas de grafo e resolução separadamente; salva dados brutos."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import statistics
import subprocess
import time
import tracemalloc

from src.graph.graph import Graph
from src.core.domain import Package, Requirement
from src.core.resolver import Catalog

ROOT = Path(__file__).resolve().parents[1]


def make_graph(size, family):
    g = Graph()
    for vertex in range(size):
        g.add_vertice(vertex)
    window = 8 if family == 'compartilhado' else 1
    for u in range(size):
        for v in range(u + 1, min(size, u + window + 1)):
            g.add_aresta(u, v)
    if family == 'ciclo' and size:
        g.add_aresta(size - 1, 0)
    return g


def make_catalog(size, family):
    if family == 'cadeia':
        packages = [Package(f'p{i}', '1.0', (Requirement(f'p{i-1}'),) if i else ())
                    for i in range(size)]
        return Catalog(packages), [Requirement(f'p{size-1}')]
    packages = [Package(f'p{i}', version) for i in range(size) for version in ('1.0', '2.0')]
    # A restrição tardia obriga retrocesso sobre decisões anteriores.
    packages.append(Package('guard', '1.0', tuple(Requirement(f'p{i}', '==1.0') for i in range(size))))
    return Catalog(packages), [Requirement(f'p{i}') for i in range(size)] + [Requirement('guard')]


def run_graph(g, operation):
    if operation == 'dfs':
        return g.dfs_ciclo()
    if operation == 'dependentes':
        return g.dependentes_transitivos(0)
    ok, order, _ = g.kahn()
    return order if ok else None


def measure(action):
    start = time.perf_counter_ns()
    result = action()
    elapsed = time.perf_counter_ns() - start
    return result, elapsed / 1_000_000


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', type=Path, default=ROOT / 'docs/experimentos/resultados')
    parser.add_argument('--repeticoes', type=int, default=7)
    args = parser.parse_args()
    if args.repeticoes < 2:
        parser.error('Use pelo menos duas repetições para registrar dispersão.')
    args.destino.mkdir(parents=True, exist_ok=True)
    rows = []
    def record(family, size, edges, operation, repeat, elapsed, outcome='', attempts=''):
        rows.append(dict(familia=family, tamanho=size, arestas=edges, operacao=operation,
                         repeticao=repeat, ms=elapsed, resultado=outcome, tentativas=attempts))
    memory = []
    for family in ('cadeia', 'compartilhado', 'ciclo'):
        for size in (100, 1000, 5000):
            g = make_graph(size, family)
            make_graph(size, family)  # aquecimento da construção
            for operation in ('dfs', 'kahn', 'dependentes'):
                run_graph(g, operation)  # aquecimento fora das medições
            for repeat in range(args.repeticoes):
                _, elapsed = measure(lambda: make_graph(size, family))
                record(family, size, len(g.arestas), 'construcao', repeat, elapsed)
                for operation in ('dfs', 'kahn', 'dependentes'):
                    value, elapsed = measure(lambda: run_graph(g, operation))
                    if operation == 'dfs' and bool(value) != (family == 'ciclo'):
                        raise AssertionError('Diagnóstico incorreto no experimento')
                    if operation == 'kahn' and (value is None) != (family == 'ciclo'):
                        raise AssertionError('Ordenação incorreta no experimento')
                    record(family, size, len(g.arestas), operation, repeat, elapsed)
            # Medição separada para que instrumentação de memória não distorça os tempos.
            tracemalloc.start()
            measured = make_graph(size, family)
            peak = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            memory.append(dict(familia=family, vertices=len(measured.vertices), arestas=len(measured.arestas),
                               pico_construcao_bytes=peak))
    for family, sizes in [('cadeia', (16, 64, 128)), ('retrocesso', (4, 8, 12))]:
        for size in sizes:
            catalog, requests = make_catalog(size, family)
            catalog.plan(requests, {})
            for repeat in range(args.repeticoes):
                plan, elapsed = measure(lambda: catalog.plan(requests, {}))
                if not plan.success:
                    raise AssertionError(f'Caso de desempenho ficou bloqueado: {family}, {size}')
                outcome = 'valido'
                record('resolvedor_' + family, size, len(plan.graph.arestas), 'resolucao',
                       repeat, elapsed, outcome, plan.attempts)
    keys = ('familia', 'tamanho', 'arestas', 'operacao')
    grouped = {}
    for row in rows:
        grouped.setdefault(tuple(row[k] for k in keys), []).append(row)
    summary = []
    for key, samples in grouped.items():
        values = [row['ms'] for row in samples]
        summary.append(dict(zip(keys, key), repeticoes=len(values), mediana_ms=statistics.median(values),
                            minimo_ms=min(values), maximo_ms=max(values), desvio_ms=statistics.stdev(values),
                            resultado=samples[0]['resultado'], tentativas=samples[0]['tentativas']))
    for name, content in [('tempos.csv', rows), ('resumo.csv', summary), ('memoria.csv', memory)]:
        with (args.destino / name).open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(content[0]))
            writer.writeheader()
            writer.writerows(content)
    sources = ['src/graph/graph.py', 'src/core/domain.py', 'src/core/resolver.py', 'experiments/benchmark.py']
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = 'indisponivel'
    metadata = dict(data_utc=datetime.now(timezone.utc).isoformat(), python=platform.python_version(),
                    plataforma=platform.platform(), processador=platform.processor(), repeticoes=args.repeticoes, commit_base=commit,
                    fontes_sha256={name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources},
                    observacao='Fontes identificadas por hash; commit_base pode preceder mudanças locais. '
                               'Tempos sem tracemalloc; pico Python medido separadamente, uma amostra por entrada. '
                               'Sem leitura JSON, desenho ou tempo de interface nas medições.')
    (args.destino / 'ambiente.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(rows)} medições de tempo e {len(memory)} de memória salvas em {args.destino}')


if __name__ == '__main__':
    main()
