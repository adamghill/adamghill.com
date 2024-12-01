import? 'adamghill.justfile'
import? '../dotfiles/just/justfile'

# List commands
_default:
    just --list --unsorted --justfile {{ justfile() }} --list-heading $'Available commands:\n'

# Grab default `adamghill.justfile` from GitHub
fetch:
  curl https://raw.githubusercontent.com/adamghill/dotfiles/master/just/justfile > adamghill.justfile

serve port='8020':
  uv run --all-extras coltrane play --port {{ port }}

serve-adamghill:
  uv run --all-extras coltrane play --port 8020

serve-alldjango:
  uv run --all-extras coltrane play --port 8021
