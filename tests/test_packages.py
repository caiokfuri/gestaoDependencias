"""Aceitação dos cenários sobre o catálogo e o resolvedor distribuídos."""
import unittest

from src.core.domain import Session
from src.core.resolver import Catalog
from src.main import CATALOGO_PADRAO, CENARIOS


class PackageScenarios(unittest.TestCase):
    def setUp(self):
        self.catalog, self.initial = Catalog.load(CATALOGO_PADRAO)
        self.session = Session(self.catalog, dict(self.initial))

    def test_desktop_commit_and_removal(self):
        plan = self.session.analyze('desktop-suite')
        self.assertTrue(plan.success)
        self.assertEqual((len(plan.selected), len(plan.graph.arestas), len(plan.actions)), (17, 26, 15))
        for name in plan.actions[:-1]:
            self.assertEqual(self.session.advance(), name)
            self.assertEqual(self.session.installed, self.initial)
        self.session.advance()
        self.assertTrue(self.session.applied)
        self.assertEqual(self.session.installed, {name: p.version for name, p in plan.selected.items()})
        self.assertIsNone(self.session.advance())
        affected, order = self.catalog.removal_impact('libcore', self.session.installed)
        self.assertIn('desktop-suite', affected)
        self.assertEqual(set(order), affected | {'libcore'})
        self.assertEqual(order[-1], 'libcore')
        index = {name: i for i, name in enumerate(order)}
        for prerequisite, dependent in plan.graph.arestas:
            if prerequisite in index and dependent in index:
                self.assertLess(index[dependent], index[prerequisite])

    def test_blocked_plans_keep_installed_state(self):
        expected = {'versoes': 'versao', 'conflito': 'conflito', 'ausente': 'ausente',
                    'ciclo': 'ciclo', 'instalado': 'versao'}
        for scenario, kind in expected.items():
            with self.subTest(scenario=scenario):
                plan = self.session.analyze(CENARIOS[scenario][1])
                self.assertFalse(plan.success)
                self.assertEqual(plan.issues[0].kind, kind)
                self.assertFalse(plan.actions)
                with self.assertRaises(RuntimeError):
                    self.session.advance()
                self.assertEqual(self.session.installed, self.initial)

    def test_alternative_and_explicit_upgrade(self):
        plan = self.session.analyze('compat-app')
        self.assertTrue(plan.success)
        self.assertEqual(plan.selected['compat-app'].version, '1.0')
        self.assertNotIn('missing-sdk', plan.graph.vertices)
        plan = self.session.analyze(CENARIOS['upgrade'][1])
        self.assertTrue(plan.success)
        self.assertEqual(plan.selected['libcore'].version, '2.0')

    def test_failed_final_validation_preserves_progress(self):
        from unittest.mock import patch

        plan = self.session.analyze('desktop-suite')
        for _ in plan.actions[:-1]:
            self.session.advance()
        staged = list(self.session.staged)
        history = list(self.session.history)
        with patch.object(self.session, '_validar_estado_final', side_effect=RuntimeError('recusa')):
            with self.assertRaisesRegex(RuntimeError, 'recusa'):
                self.session.advance()
        self.assertEqual(self.session.installed, self.initial)
        self.assertEqual(self.session.staged, staged)
        self.assertEqual(self.session.history, history)
        self.assertFalse(self.session.applied)
        self.assertEqual(self.session.advance(), plan.actions[-1])
        self.assertTrue(self.session.applied)

    def test_limit_is_an_inconclusive_diagnostic(self):
        from src.core.domain import Requirement

        plan = self.catalog.plan([Requirement('desktop-suite')], self.initial, limit=0)
        self.assertFalse(plan.success)
        self.assertEqual(plan.issues[0].kind, 'limite')
        self.assertFalse(plan.actions)
