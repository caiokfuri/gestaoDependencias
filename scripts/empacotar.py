"""Monta um ZIP por lista explícita; distingue revisão de entrega final."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SUFFIXES = {'.py', '.json', '.md', '.txt', '.tex', '.sty', '.png', '.svg', '.puml', '.pdf', '.html', '.csv'}
DIRECTORIES = ('depgraph', 'src', 'tests', 'experiments', 'scripts', 'docs', 'data')
ROOT_FILES = ('README.md', 'requirements.txt', 'graph.py', 'test_graph.py', 'agent.md', 'TP.pdf')


def files_to_include():
    files = [ROOT / name for name in ROOT_FILES]
    for directory in DIRECTORIES:
        files.extend(p for p in (ROOT / directory).rglob('*') if p.is_file()
                     and p.suffix in ALLOWED_SUFFIXES and not p.is_symlink()
                     and '__pycache__' not in p.parts)
    return sorted(set(files))


def pending_items():
    pending = []
    for name in ('tests/test_packages.py', 'experiments/benchmark.py',
                 'experiments/verificar_grafos.py', 'docs/experimentos/README.md'):
        if not (ROOT / name).is_file():
            pending.append(f'Contribuição do David ainda não incorporada: {name}.')
    data = json.loads((ROOT / 'docs/entrega/equipe.json').read_text())
    for field in ('instituicao', 'curso'):
        if not data.get(field, '').strip():
            pending.append(f'Identificação: {field} não preenchido.')
    members = data.get('integrantes', [])
    if not 1 <= len(members) <= 6:
        pending.append('Quantidade de integrantes fora do intervalo permitido.')
    for member in members:
        if not (member.get('nome', '').strip() and member.get('contribuicao', '').strip()
                and member.get('evidencias') and member.get('confirmado') is True):
            pending.append(f"Contribuição efetiva não confirmada: {member.get('nome', '?')}.")
    pdf = ROOT / 'docs/relatorio/relatorio.pdf'
    if not pdf.is_file():
        pending.append('PDF do relatório ausente.')
    else:
        try:
            info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
            pages = int(next(line.split(':', 1)[1] for line in info.splitlines() if line.startswith('Pages:')))
            if not 12 <= pages <= 15:
                pending.append(f'Relatório com {pages} páginas; exigido 12–15.')
        except (OSError, subprocess.CalledProcessError, StopIteration, ValueError):
            pending.append('Contagem de páginas não verificada; instalar pdfinfo e conferir.')
    if not (ROOT / 'docs/entrega/revisao-final.json').is_file():
        pending.append('Revisão humana de relatório, apresentação, vídeo e prazo ainda não registrada.')
    else:
        review = json.loads((ROOT / 'docs/entrega/revisao-final.json').read_text())
        for field in ('relatorio_revisado', 'estilo_sbc_conferido', 'slides_revisados', 'ensaio_realizado',
                      'video_revisado', 'prazo_canvas_conferido'):
            if review.get(field) is not True:
                pending.append(f'Revisão pendente: {field}.')
        if not 12 <= review.get('duracao_video_minutos', 0) <= 18:
            pending.append('Duração do vídeo não confirmada no intervalo de 12–18 minutos.')
        if not review.get('video_local_ou_link', '').strip():
            pending.append('Vídeo final sem localização registrada.')
    if not (ROOT / 'docs/apresentacao/slides.html').is_file():
        pending.append('Slides ausentes.')
    return pending


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--rascunho', action='store_true', help='Gera pacote de revisão com pendências explícitas.')
    mode.add_argument('--final', action='store_true', help='Recusa se materiais e revisões obrigatórios estiverem pendentes.')
    args = parser.parse_args()
    pending = pending_items()
    if args.final and pending:
        parser.exit(1, 'Entrega final incompleta:\n- ' + '\n- '.join(pending) + '\n')
    files = files_to_include()
    if args.final:
        subprocess.run(['git', 'diff', '--exit-code', 'HEAD', '--', *[str(p.relative_to(ROOT)) for p in files]],
                       cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        # Arquivos novos precisam estar versionados também.
        tracked = set(subprocess.check_output(['git', 'ls-files'], cwd=ROOT, text=True).splitlines())
        untracked = [str(p.relative_to(ROOT)) for p in files if str(p.relative_to(ROOT)) not in tracked]
        if untracked:
            parser.error('Arquivos ainda sem commit: ' + ', '.join(untracked))
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    manifest = dict(tipo='revisao' if args.rascunho else 'final', commit_base=commit,
                    data_utc=datetime.now(timezone.utc).isoformat(), pendencias=pending,
                    arquivos={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
    destination = ROOT / 'dist' / ('depgraph-revisao.zip' if args.rascunho else 'depgraph-final.zip')
    destination.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, 'depgraph/' + str(path.relative_to(ROOT)))
        archive.writestr('depgraph/MANIFESTO.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise RuntimeError('ZIP corrompido')
        if any('/prototypes/' in name or '/.git/' in name or '/.venv/' in name for name in archive.namelist()):
            raise RuntimeError('Histórico executável ou arquivos locais indevidos no pacote')
    print(f'{destination}: {len(files)} arquivos; {len(pending)} pendências registradas no manifesto.')


if __name__ == '__main__':
    main()
