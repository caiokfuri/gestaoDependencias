"""Regressões da integração entre CLI, catálogo e interface gráfica."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from src.main import CATALOGO_PADRAO, main
from src.core.domain import Session
from src.core.resolver import Catalog


class IntegrationTests(unittest.TestCase):
    def run_cli(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return main(list(args))

    def test_simulation_and_json_export(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'plano.json'
            self.assertEqual(self.run_cli('--simular', '--json', str(target)), 0)
            plan = json.loads(target.read_text())
            self.assertTrue(plan['sucesso'])
            self.assertEqual(len(plan['selecionados']), 17)
            self.assertEqual(len(plan['acoes']), 15)
            positions = {name: i for i, name in enumerate(plan['ordem_instalacao'])}
            for edge in plan['arestas']:
                self.assertLess(positions[edge['de']], positions[edge['para']])

    def test_blocked_scenarios_and_input_errors(self):
        for scenario in ('versoes', 'conflito', 'ausente', 'ciclo', 'instalado'):
            with self.subTest(scenario=scenario):
                self.assertEqual(self.run_cli('--cenario', scenario, '--simular'), 1)
        self.assertEqual(self.run_cli('--pedidos', '???'), 2)
        self.assertEqual(self.run_cli('--catalogo', '/catalogo-inexistente.json'), 2)
        self.assertEqual(self.run_cli('--remover', 'pacote-nao-instalado'), 2)

    def test_gui_preserves_session_and_exports(self):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from src.ui.gui import PackageGUI
        catalog, installed = Catalog.load(CATALOGO_PADRAO)
        session = Session(catalog, dict(installed))
        plan = session.analyze('desktop-suite')
        session.advance()
        staged = list(session.staged)
        gui = PackageGUI(session)
        try:
            self.assertIs(gui.session, session)
            self.assertIs(gui.session.plan, plan)
            self.assertEqual(session.staged, staged)
            with tempfile.TemporaryDirectory() as directory:
                image = Path(directory) / 'plano.png'
                report = Path(directory) / 'plano.json'
                gui.export(image, report)
                self.assertTrue(image.read_bytes().startswith(b'\x89PNG'))
                self.assertTrue(json.loads(report.read_text())['sucesso'])
        finally:
            plt.close(gui.fig)


    def test_gui_recovers_after_invalid_request(self):
        import matplotlib.pyplot as plt
        from depgraph.app import PackagePreview

        gui = PackagePreview()
        try:
            gui.request_box.set_val('???')
            with self.assertRaises(ValueError) as error:
                gui.analyze()
            gui.render(str(error.exception), error=True)
            gui.fig.canvas.draw()
            self.assertIsNone(gui.session.plan)
            with self.assertRaises(ValueError):
                gui.advance()
            gui.load_scenario('desktop')
            self.assertTrue(gui.session.plan.success)
        finally:
            plt.close(gui.fig)
