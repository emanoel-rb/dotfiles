#!/bin/bash

echo "Instalando dotfiles..."

# Criar diretórios
mkdir -p ~/.config

# Backup configs antigas
echo "Criando backup..."
mv ~/.config/hypr ~/.config/hypr.bak 2>/dev/null
mv ~/.config/waybar ~/.config/waybar.bak 2>/dev/null
mv ~/.config/kitty ~/.config/kitty.bak 2>/dev/null
mv ~/.config/rofi ~/.config/rofi.bak 2>/dev/null
mv ~/.config/dunst ~/.config/dunst.bak 2>/dev/null
mv ~/.zshrc ~/.zshrc.bak 2>/dev/null

# Copiar configs
echo "Copiando configs..."

cp -r config/hypr ~/.config/
cp -r config/waybar ~/.config/
cp -r config/kitty ~/.config/
cp -r config/rofi ~/.config/
cp -r config/dunst ~/.config/

cp zsh/.zshrc ~/

echo "Instalação concluída."
echo "Reinicie o sistema ou o Hyprland."
