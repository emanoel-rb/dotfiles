# ==========================================================
# ZSH CONFIG - Clean + Cyberpunk Neon + Seta >
# ==========================================================

# ==========================================================
# KEYBINDS
# ==========================================================
bindkey "^[[H" beginning-of-line
bindkey "^[[F" end-of-line
bindkey "^[[3~" delete-char
bindkey "^H" backward-kill-word
bindkey "^[[3;5~" kill-word
bindkey "^[[1;5D" backward-word
bindkey "^[[1;5C" forward-word

# ==========================================================
# ALIASES
# ==========================================================
alias ls='ls --color=auto'
alias s='kitten ssh'

# ==========================================================
# ZINIT (PLUGIN MANAGER)
# ==========================================================
ZINIT_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/zinit/zinit.git"
if [ ! -d "$ZINIT_HOME" ]; then
    mkdir -p "$(dirname "$ZINIT_HOME")"
    git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
fi
source "$ZINIT_HOME/zinit.zsh"

# Plugins
zinit light zsh-users/zsh-autosuggestions
zinit light zsh-users/zsh-syntax-highlighting

# ==========================================================
# FZF
# ==========================================================
if command -v fzf >/dev/null 2>&1; then
    source <(fzf --zsh --style full --preview 'cat {}' --preview-window right:60%:wrap)
fi

# ==========================================================
# PROMPT MANUAL CYBERPUNK NEON - Força seta >
# ==========================================================
PROMPT='%B%F{cyan}>%f%b  '

# ==========================================================
# PROMPT CLEANUP / SAFETY
# ==========================================================
setopt no_beep
setopt autopushd
setopt hist_ignore_dups
setopt share_history