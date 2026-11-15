#!/bin/sh
# Read-only vault locator and search, shared by the obsidian-knowledge skill
# and the SessionStart hook. POSIX sh; the macOS path uses no Python.
#
#   vault.sh locate                     one absolute vault path per line, exit 0
#   vault.sh search <vault> <word...>   one absolute note path per line, exit 0
#
# locate: OBSIDIAN_VAULT (os.pathsep-separated) replaces the registry; else
# Obsidian's obsidian.json (OBSIDIAN_CONFIG_DIR overrides its directory),
# newest-opened first. Only existing directories are printed.
# search: the Obsidian CLI when it exists and the vault is the one the app has
# open; otherwise BSD grep. Both join the query words with OR.

set -u

config_dir() {
    if [ -n "${OBSIDIAN_CONFIG_DIR:-}" ]; then
        printf '%s\n' "$OBSIDIAN_CONFIG_DIR"
    elif [ "$(uname -s)" = "Darwin" ]; then
        printf '%s\n' "$HOME/Library/Application Support/obsidian"
    else
        base=${XDG_CONFIG_HOME:-$HOME/.config}
        printf '%s\n' "$base/obsidian"
    fi
}

# Emit each registry candidate, newest ts first.
plutil_vaults() {
    file=$1
    ids=$(plutil -extract vaults json -o - "$file" 2>/dev/null \
        | grep -oE '"[^"]+":\{' | sed 's/"//g;s/:{$//')
    [ -n "$ids" ] || return 0
    for id in $ids; do
        path=$(plutil -extract "vaults.$id.path" raw -o - "$file" 2>/dev/null) \
            || continue
        ts=$(plutil -extract "vaults.$id.ts" raw -o - "$file" 2>/dev/null)
        [ -n "$ts" ] || ts=0
        printf '%s %s\n' "$ts" "$path"
    done | sort -s -k1,1nr | cut -d' ' -f2-
}

# Best-effort registry read on platforms without plutil. UNVERIFIED.
python_registry_vaults() {
    python3 - "$1" 2>/dev/null <<'EOF' || return 0
import json, sys
try:
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    entries = [v for v in data.get("vaults", {}).values() if isinstance(v, dict)]
    entries.sort(key=lambda v: v.get("ts") if isinstance(v.get("ts"), (int, float)) else 0, reverse=True)
    for v in entries:
        if isinstance(v.get("path"), str):
            print(v["path"])
except Exception:
    pass
EOF
}

# Print the path only if it is a safe, existing, absolute directory.
emit_vault() {
    p=$1
    [ -n "$p" ] || return 0
    case $p in
        "~") p=$HOME ;;
        "~/"*) p=$HOME${p#"~"} ;;
    esac
    while :; do
        case $p in
            /) break ;;
            */) p=${p%/} ;;
            *) break ;;
        esac
    done
    case $p in
        *[[:cntrl:]]*) return 0 ;;
    esac
    case $p in
        /*) ;;
        *) return 0 ;;
    esac
    [ -d "$p" ] || return 0
    printf '%s\n' "$p"
}

do_locate() {
    if [ -n "${OBSIDIAN_VAULT:-}" ]; then
        IFS=:
        for p in $OBSIDIAN_VAULT; do
            emit_vault "$p"
        done
        unset IFS
    else
        reg=$(config_dir)/obsidian.json
        if [ -r "$reg" ]; then
            if command -v plutil >/dev/null 2>&1; then
                plutil_vaults "$reg"
            else
                python_registry_vaults "$reg"
            fi | while read -r p; do
                emit_vault "$p"
            done
        fi
    fi | awk '!seen[$0]++'
    return 0
}

do_search() {
    [ $# -ge 2 ] || { echo "usage: vault.sh search <vault> <word...>" >&2; exit 1; }
    vault=$1
    shift

    cli=${OBSIDIAN_CLI_BIN:-}
    if [ -z "$cli" ]; then
        for c in /Applications/Obsidian.app/Contents/MacOS/obsidian-cli obsidian; do
            if command -v "$c" >/dev/null 2>&1; then
                cli=$c
                break
            fi
        done
    fi
    reg=$(config_dir)/obsidian.json
    open_vault=""
    if [ -n "$cli" ] && [ -r "$reg" ] && command -v plutil >/dev/null 2>&1; then
        for id in $(plutil -extract vaults json -o - "$reg" 2>/dev/null \
                | grep -oE '"[^"]+":\{' | sed 's/"//g;s/:{$//'); do
            [ "$(plutil -extract "vaults.$id.open" raw -o - "$reg" 2>/dev/null)" = "true" ] || continue
            open_vault=$(plutil -extract "vaults.$id.path" raw -o - "$reg" 2>/dev/null)
            break
        done
    fi
    if [ -n "$cli" ] && [ "$open_vault" = "$vault" ]; then
        query=""
        for w in "$@"; do
            [ -z "$query" ] && query=$w || query="$query OR $w"
        done
        out=$("$cli" search "query=$query" "vault=$vault" 2>/dev/null) || out=""
        if [ -n "$out" ] && ! printf '%s\n' "$out" | grep -q "Vault not found" \
           && ! printf '%s\n' "$out" | grep -q "No matches found"; then
            printf '%s\n' "$out" | while read -r rel; do
                [ -n "$rel" ] || continue
                printf '%s/%s\n' "$vault" "$rel"
            done
            return 0
        fi
    fi

    for w in "$@"; do
        grep -rliF -e "$w" --exclude-dir=.obsidian --exclude-dir=.trash "$vault" 2>/dev/null
    done | awk -v v="$vault/" '{ p=substr($0, length(v)+1); n=split(p, a, "/"); for (i=1;i<=n;i++) if (substr(a[i],1,1)==".") next; print }' | sort -u
    return 0
}

cmd=${1:-}
[ $# -gt 0 ] && shift
case $cmd in
    locate) do_locate ;;
    search) do_search "$@" ;;
    *) echo "usage: vault.sh locate | search <vault> <word...>" >&2; exit 1 ;;
esac
exit 0
