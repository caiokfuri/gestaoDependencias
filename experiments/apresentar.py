"""Produz tabelas Markdown e gráfico a partir dos CSVs, sem inventar resultados."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1] / 'docs/experimentos'


def main():
    with (ROOT / 'resultados/resumo.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    lines = ['# Resultados medidos', '', 'Gerado por `python -m experiments.apresentar`. '
             'Tempos em milissegundos; ambiente e resultados brutos em `resultados/`.', '',
             '| Família | Tamanho | E | Operação | Mediana (ms) | Mín.–máx. (ms) | Desvio (ms) | Resultado | Tentativas |',
             '| --- | ---: | ---: | --- | ---: | ---: | ---: | --- | ---: |']
    for r in rows:
        lines.append(f"| {r['familia']} | {r['tamanho']} | {r['arestas']} | {r['operacao']} | "
                     f"{float(r['mediana_ms']):.4f} | {float(r['minimo_ms']):.4f}–{float(r['maximo_ms']):.4f} | "
                     f"{float(r['desvio_ms']):.4f} | {r['resultado']} | {r['tentativas']} |")
    (ROOT / 'tabelas.md').write_text('\n'.join(lines) + '\n')
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for op in ('construcao', 'dfs', 'kahn', 'dependentes'):
        selected = [r for r in rows if r['familia'] == 'compartilhado' and r['operacao'] == op]
        axes[0].loglog([int(r['tamanho']) for r in selected], [float(r['mediana_ms']) for r in selected], 'o-', label=op)
    axes[0].set(title='Grafo com até oito sucessores por vértice', xlabel='Vértices', ylabel='Mediana (ms)')
    selected = [r for r in rows if r['familia'] == 'resolvedor_retrocesso']
    axes[1].semilogy([int(r['tamanho']) for r in selected], [float(r['mediana_ms']) for r in selected], 'o-')
    axes[1].set(title='Restrições tardias no resolvedor', xlabel='Pacotes com duas versões', ylabel='Mediana (ms)')
    for ax in axes:
        ax.grid(alpha=.25)
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(ROOT / 'desempenho.png', dpi=160)
    plt.close(fig)


if __name__ == '__main__':
    main()
