"""Build runtime-only review ZIPs; does not install or publish."""
from pathlib import Path
import argparse, hashlib, json, zipfile
ROOT = Path(__file__).resolve().parents[1]

def bundle(source, destination, include):
    files = sorted(p for p in source.rglob('*') if p.is_file()
                   and '__pycache__' not in p.parts and include(p.relative_to(source)))
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(source).as_posix(), (2026, 10, 3, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise ValueError('Archive CRC check failed')
        if any(n.startswith('/') or '..' in Path(n).parts for n in archive.namelist()):
            raise ValueError('Unsafe archive path')
    return {'file': destination.name, 'files': len(files),
            'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    version = json.loads((ROOT / 'plugin.json').read_text())['version']
    plugin = bundle(ROOT, args.output_dir / f'ai-growth-studio-{version}.zip',
                    lambda p: p.as_posix() == 'plugin.json' or p.parts[0] in {'skills', 'assets'})
    skill = bundle(ROOT / 'skills/revenue-leak-audit',
                   args.output_dir / f'revenue-leak-audit-{version}.zip', lambda p: True)
    results = [plugin, skill]
    (args.output_dir / 'package-results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
