#!/usr/bin/env bash
set -euo pipefail

sudo apt install -y pipx
pipx install 'python-lsp-server[all]'

cargo install --git https://github.com/euclio/mdpls
