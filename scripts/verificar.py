"""Executa a suíte final e os cenários com importação de NetworkX bloqueada."""
import builtins
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
original_import = builtins.__import__


def without_networkx(name, *args, **kwargs):
    if name.split('.')[0] == 'networkx':
        raise ImportError('NetworkX é proibido no fluxo final do DepGraph.')
    return original_import(name, *args, **kwargs)


def main():
    builtins.__import__ = without_networkx
    try:
        suite = unittest.TestLoader().loadTestsFromNames(['test_graph', 'tests.test_graph', 'tests.test_cli', 'tests.test_packages'])
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():
            return 1
        from experiments.verificar_grafos import verify
        oracle = verify()
        print(f"Oráculo: {oracle['grafos']} grafos e {oracle['divergencias']} divergências.")
        from depgraph.app import PackagePreview, SCENARIOS
        import matplotlib.pyplot as plt
        for scenario in SCENARIOS:
            preview = PackagePreview(scenario=scenario)
            try:
                preview.fig.canvas.draw()
                plan = preview.session.plan
                if plan.success:
                    for _ in plan.actions:
                        preview.advance()
                    if not preview.session.applied:
                        preview.advance()  # Plano válido que não requer operações.
                    preview.session._validar_estado_final(preview.session.installed)
            finally:
                plt.close(preview.fig)
        print(f'{len(SCENARIOS)} cenários renderizados; planos válidos executados sem NetworkX.')
        return 0
    finally:
        builtins.__import__ = original_import


if __name__ == '__main__':
    raise SystemExit(main())
