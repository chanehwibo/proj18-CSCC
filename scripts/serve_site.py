"""Serve the generated KernelSage review site over HTTP (stdlib only).

python scripts/serve_site.py --site site --port 8000
Then open http://localhost:8000/ in a browser.

Serving over HTTP (instead of opening index.html via file://) guarantees the
report <iframe> modals load correctly in every browser.
"""

from __future__ import annotations

import argparse
import http.server
import socketserver
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serve the review site")
    parser.add_argument("--site", default=str(ROOT / "site"), help="site directory to serve")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args(argv)

    site_dir = Path(args.site).resolve()
    if not (site_dir / "index.html").exists():
        raise SystemExit(f"index.html not found in {site_dir}; run build_site.py first")

    handler = lambda *h_args, **h_kw: http.server.SimpleHTTPRequestHandler(*h_args, directory=str(site_dir), **h_kw)
    with socketserver.ThreadingTCPServer((args.host, args.port), handler) as httpd:
        httpd.allow_reuse_address = True
        print(f"serving {site_dir}")
        print(f"open http://localhost:{args.port}/  (Ctrl+C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
