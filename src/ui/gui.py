"""
Módulo de Interface Gráfica e Visualização
==========================================
Responsável: Rafael Abras Lessa Freitas
Atribuição acadêmica: Interface, visualização e demonstração (Tópico 6)
"""

from typing import Optional, Dict, Any


class PackageGUI:
    """Janela interativa desenvolvida com Matplotlib."""

    def __init__(self, session: Any):
        self.session = session
        # Rafael: configurar figura, eixos, botões e campo de texto

    def setup_layout(self) -> None:
        """
        Rafael: criar botões:
        - 'Analisar instalação'
        - 'Próximo pacote' (avança transação)
        - 'Reiniciar plano'
        - 'Impacto da remoção'
        """
        pass

    def draw_graph(self, plan: Any) -> None:
        """
        Rafael: desenha os nós e arestas:
        - Layout em camadas baseado nas camadas do Kahn de Caio Kfuri.
        - Disposição circular se houver ciclos.
        - Cores: Cinza (instalado), Roxo (a preparar), Verde (preparado), Vermelho (em falha).
        - Arestas tracejadas vermelhas para incompatibilidades explícitas.
        """
        pass

    def on_node_click(self, node_name: str) -> None:
        """Rafael: exibe no painel inferior os detalhes da versão e dependências do pacote clicado."""
        pass

    def load_scenario(self, scenario_name: str) -> None:
        """
        Rafael: botões de cenários rápidos:
        'desktop', 'versoes', 'conflito', 'ausente', 'ciclo', 'upgrade', 'alternativa'.
        """
        pass

    def export(self, png_path: str, json_path: str) -> None:
        """Rafael: exportar imagem PNG e arquivo JSON da análise atual."""
        pass

    def show(self) -> None:
        """Abre a janela gráfica interativa."""
        pass
