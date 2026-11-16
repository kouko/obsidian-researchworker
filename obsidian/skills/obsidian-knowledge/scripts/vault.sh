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

# Read one registry value without lossy capture. Exit 2 when the key is absent,
# exit 1 when the value spans lines: plutil raw output always ends in exactly
# one newline, so a value that itself contains one shows up as a leftover line,
# which command substitution would strip silently and accept as the value.
plutil_raw() {
    plutil -extract "$1" raw -o - "$2" 2>/dev/null | {
        IFS= read -r v || exit 2
        IFS= read -r extra && exit 1
        printf '%s\n' "$v"
    }
}

# Emit each registry candidate, newest ts first.
plutil_vaults() {
    file=$1
    ids=$(plutil -extract vaults json -o - "$file" 2>/dev/null \
        | grep -oE '"[^"]+":\{' | sed 's/"//g;s/:{$//')
    [ -n "$ids" ] || return 0
    for id in $ids; do
        path=$(plutil_raw "vaults.$id.path" "$file") || continue
        ts=$(plutil_raw "vaults.$id.ts" "$file")
        # A ts that itself spanned lines is a malformed entry, not a missing
        # one: drop it rather than fall back to 0 and keep the entry.
        [ $? -eq 1 ] && continue
        [ -n "$ts" ] || ts=0
        # One entry prints as one `ts path` line; a control character in either
        # field can split it into extra lines that would become vault paths the
        # registry never named. Drop the whole entry before it is printed.
        case "$path $ts" in
            *[[:cntrl:]]*) continue ;;
        esac
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
        p = v.get("path")
        if isinstance(p, str) and not any(c < " " or c == "\x7f" for c in p + str(v.get("ts") or "")):
            print(p)
except Exception:
    pass
EOF
}

# Best-effort open-vault read on platforms without plutil. UNVERIFIED.
python_registry_open_vault() {
    python3 - "$1" 2>/dev/null <<'EOF' || return 0
import json, sys
try:
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    for v in data.get("vaults", {}).values():
        if isinstance(v, dict) and v.get("open") is True:
            p = v.get("path")
            if isinstance(p, str) and not any(c < " " or c == "\x7f" for c in p):
                print(p)
            break
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

    # Keep only query words with at least one non-blank character.
    n=0
    for w in "$@"; do
        case $w in
            *[![:space:]]*)
                if [ "$n" -eq 0 ]; then set -- "$w"; else set -- "$@" "$w"; fi
                n=$((n + 1))
                ;;
        esac
    done
    [ "$n" -gt 0 ] || exit 0

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
    if [ -n "$cli" ] && [ -r "$reg" ]; then
        if command -v plutil >/dev/null 2>&1; then
            for id in $(plutil -extract vaults json -o - "$reg" 2>/dev/null \
                    | grep -oE '"[^"]+":\{' | sed 's/"//g;s/:{$//'); do
                [ "$(plutil_raw "vaults.$id.open" "$reg")" = "true" ] || continue
                open_vault=$(plutil_raw "vaults.$id.path" "$reg")
                break
            done
        else
            open_vault=$(python_registry_open_vault "$reg")
        fi
    fi
    if [ -n "$cli" ] && [ "$open_vault" = "$vault" ]; then
        query=""
        for w in "$@"; do
            # Quote each word so the CLI reads it as a literal phrase. A bare
            # word with a space is AND-of-terms and a `file:`/`path:` prefix is
            # an operator; the grep fallback below matches fixed strings only,
            # so quoting is what makes both engines read the same words alike.
            # A `"` inside a word ends the phrase and the rest is parsed as
            # operator syntax (measured), and the CLI accepts no backslash
            # escape -- so that query is unencodable and the grep engine answers.
            case $w in
                *\"*) query=""; break ;;
            esac
            [ -z "$query" ] && query="\"$w\"" || query="$query OR \"$w\""
        done
        if [ -n "$query" ]; then
            out=$("$cli" search "query=$query" "vault=$vault" 2>/dev/null) || out=""
            if [ -n "$out" ] && ! printf '%s\n' "$out" | grep -q "Vault not found" \
               && ! printf '%s\n' "$out" | grep -q "No matches found"; then
                printf '%s\n' "$out" | while read -r rel; do
                    case $rel in
                        Error:*|*": "*) continue ;;
                        [!/]*) ;;
                        *) continue ;;
                    esac
                    [ -n "$rel" ] || continue
                    # Same dot-component filter as the grep fallback: drop any
                    # relative path with a dot-prefixed component (.., .obsidian,
                    # .claudian, .trash) so both engines return the same hit set
                    # and no traversal line can become a printed note path.
                    printf '%s\n' "$rel" | awk '{ n=split($0, a, "/"); for (i=1;i<=n;i++) if (substr(a[i],1,1)==".") next; print }' \
                        | while read -r safe; do
                            printf '%s/%s\n' "$vault" "$safe"
                        done
                done
                return 0
            fi
        fi
    fi

    # Fixed-string match per word, notes only: the CLI indexes `.md` files, so
    # a non-note file grep could return would make the hit set depend on which
    # engine ran.
    for w in "$@"; do
        grep -rliF -e "$w" --include='*.md' --exclude-dir=.obsidian --exclude-dir=.trash "$vault" 2>/dev/null
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
