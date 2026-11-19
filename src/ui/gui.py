"""Interface do Tópico 6, integrada à sessão do núcleo em src/core.

Reutiliza os controles e o desenho funcional incorporados de trab-grafo.
"""

from depgraph.app import PackagePreview


class PackageGUI(PackagePreview):
    """Interface que preserva o plano e o progresso de uma sessão existente."""

    def __init__(self, session):
        super().__init__(session=session)

    def draw_graph(self, plan):
        self.session.plan = plan
        self.render()

    def show(self):
        import matplotlib.pyplot as plt
        plt.show()

    def export(self, png_path, json_path):
        import json
        from pathlib import Path
        from src.main import plano_para_dict
        for path in (png_path, json_path):
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(json_path).write_text(
            json.dumps(plano_para_dict(self.session.plan), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self.fig.savefig(png_path, dpi=150, facecolor=self.fig.get_facecolor())
