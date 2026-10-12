#!/usr/bin/env bash
printf '%b\n' "$(
    cat << 'CHEAT'
\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m
\033[1;97m  Herdr × tmux Quick Reference\033[0m                             \033[2mPress 'q' to close\033[0m
\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m

\033[1;33m  Window / Tab & Pane Muscle Memory\033[0m
   \033[1;32mCtrl+b c\033[0m            New window (tab)                   \033[2m(same as tmux)\033[0m
   \033[1;32mCtrl+b l\033[0m            Jump to last active pane/window    \033[2m(mapped to last_pane)\033[0m
   \033[1;32mCtrl+b n / p\033[0m        Next / Previous tab                \033[2m(or Ctrl+b 1..9)\033[0m
   \033[1;32mCtrl+b |\033[0m  \033[2mor\033[0m  \033[1;32mv\033[0m       Split vertical (side-by-side)      \033[2m(|, v, % all active)\033[0m
   \033[1;32mCtrl+b -\033[0m  \033[2mor\033[0m  \033[1;32m"\033[0m       Split horizontal (stacked)         \033[2m(- and " both active)\033[0m
   \033[1;32mCtrl+b Space\033[0m        Rotate split layout (| <-> -)      \033[2m(side-by-side <-> stacked)\033[0m
   \033[1;32mCtrl+b Arrows\033[0m       Focus pane left/down/up/right      \033[2m(or h/j/k, Ctrl+b Tab)\033[0m
   \033[1;32mCtrl+b H/J/K/L\033[0m      Swap pane left/down/up/right       \033[2m(Shift + h/j/k/l)\033[0m
   \033[1;32mCtrl+b z\033[0m            Zoom / unzoom focused pane         \033[2m(same as tmux)\033[0m
   \033[1;32mCtrl+b r\033[0m            Resize mode                        \033[2m(then h/j/k/l, Esc)\033[0m
   \033[1;32mCtrl+b x / X\033[0m        Close pane (x) / Close tab (X)
   \033[1;32mCtrl+b ,\033[0m  \033[2mor\033[0m  \033[1;32mT\033[0m       Rename active tab                  \033[2m(Shift+p = pane)\033[0m
   \033[1;32mCtrl+b d\033[0m  \033[2mor\033[0m  \033[1;32mq\033[0m       Detach client                      \033[2m(agents keep running)\033[0m

\033[1;33m  Copy Mode & Scrollback Search\033[0m
   \033[1;32mCtrl+b [\033[0m            Enter vi copy mode                 \033[2m(q or Esc to exit)\033[0m
   \033[1;32m/\033[0m  \033[2mor\033[0m  \033[1;32m?\033[0m              Search forward / backward          \033[2m(n / N for next/prev)\033[0m
   \033[1;32mCtrl+b e\033[0m            Open scrollback in $EDITOR         \033[2m(full Vim regex /)\033[0m
   \033[1;32mSpace / v -> y\033[0m      Select & Yank to clipboard         \033[2m(V for full lines)\033[0m

\033[1;33m  Herdr Agent & Workspace Controls\033[0m
   \033[1;32mCtrl+b o\033[0m            Jump to blocked / notifying agent  \033[2m(red sidebar badge)\033[0m
   \033[1;32mCtrl+b g\033[0m            Session / Agent navigator (goto)   \033[2m(fuzzy jump anywhere)\033[0m
   \033[1;32mCtrl+b w\033[0m            Workspace picker                   \033[2m(h/j/k/l, Enter, 1..9)\033[0m
   \033[1;32mCtrl+b b\033[0m            Toggle left sidebar                \033[2m(Workspaces & Agents)\033[0m
   \033[1;32mCtrl+b ?\033[0m            Built-in searchable keybind list   \033[2m(type to filter, Esc)\033[0m
   \033[1;32mCtrl+b /\033[0m            Open this popup cheatsheet         \033[2m(q to dismiss)\033[0m
   \033[1;32mCtrl+b R\033[0m            Reload ~/.config/herdr/config.toml
CHEAT
)" | less -R
