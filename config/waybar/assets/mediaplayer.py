#!/usr/bin/env python3

# ==========================================================
# Waybar + Spotify + Dunst Integration
# ----------------------------------------------------------
# - Exibe música atual na Waybar
# - Envia notificação ao trocar de faixa
# - Evita spam de notificações
# - Cache de capas (não baixa repetidamente)
# - Estrutura limpa e resiliente
# ==========================================================

import gi
gi.require_version("Playerctl", "2.0")

from gi.repository import Playerctl, GLib
from gi.repository.Playerctl import Player

import argparse
import logging
import sys
import signal
import json
import os
import subprocess
import urllib.request
import hashlib

logger = logging.getLogger(__name__)

# Diretório de cache de capas
CACHE_DIR = os.path.expanduser("~/.cache/waybar-covers")

# ==========================================================
# Inicialização do cache
# ==========================================================
def ensure_cache():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

# ==========================================================
# Handler para encerramento seguro
# ==========================================================
def signal_handler(sig, frame):
    logger.info("Encerrando script...")
    sys.stdout.write("\n")
    sys.stdout.flush()
    sys.exit(0)

# ==========================================================
# Gerenciador de players
# ==========================================================
class PlayerManager:
    def __init__(self, selected_player=None, excluded_player=[]):
        self.manager = Playerctl.PlayerManager()
        self.loop = GLib.MainLoop()

        self.last_track = ""

        self.manager.connect("name-appeared", self.on_player_appeared)
        self.manager.connect("player-vanished", self.on_player_vanished)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        self.selected_player = selected_player
        self.excluded_player = excluded_player.split(',') if excluded_player else []

        ensure_cache()
        self.init_players()

    # ======================================================
    # Inicializa players existentes
    # ======================================================
    def init_players(self):
        for player in self.manager.props.player_names:
            if player.name in self.excluded_player:
                continue
            if self.selected_player and self.selected_player != player.name:
                continue
            self.init_player(player)

    def run(self):
        self.loop.run()

    # ======================================================
    # Inicializa player individual
    # ======================================================
    def init_player(self, player):
        player = Playerctl.Player.new_from_name(player)

        player.connect("playback-status", self.on_playback_status_changed)
        player.connect("metadata", self.on_metadata_changed)

        self.manager.manage_player(player)

        self.on_metadata_changed(player, player.props.metadata)

    # ======================================================
    # Saída formatada para Waybar
    # ======================================================
    def write_output(self, text, player):
        if len(text) > 40:
            text = text[:40]

        text = text.replace("&", "&amp;")

        output = {
            "text": text,
            "class": "custom-" + player.props.player_name,
            "alt": player.props.player_name
        }

        sys.stdout.write(json.dumps(output) + "\n")
        sys.stdout.flush()

    def clear_output(self):
        sys.stdout.write("\n")
        sys.stdout.flush()

    # ======================================================
    # Cache inteligente da capa
    # ======================================================
    def get_cached_cover(self, url):
        try:
            # cria hash da URL (único por música)
            filename = hashlib.md5(url.encode()).hexdigest() + ".jpg"
            path = os.path.join(CACHE_DIR, filename)

            # se já existe, usa cache
            if os.path.exists(path):
                return path

            # baixa e salva
            urllib.request.urlretrieve(url, path)
            return path

        except Exception as e:
            logger.debug(f"Erro ao cachear capa: {e}")
            return None

    # ======================================================
    # Evento: play/pause alterado
    # ======================================================
    def on_playback_status_changed(self, player, status):
        self.on_metadata_changed(player, player.props.metadata)

    # ======================================================
    # Retorna player ativo
    # ======================================================
    def get_first_playing_player(self):
        players = self.manager.props.players

        for player in players[::-1]:
            if player.props.status == "Playing":
                return player

        return players[0] if players else None

    # ======================================================
    # Evento: metadata alterado (nova música)
    # ======================================================
    def on_metadata_changed(self, player, metadata):

        artist = player.get_artist()
        title = player.get_title()

        if not title:
            return

        track = f"{artist} - {title}" if artist else title

        # ==================================================
        # NOTIFICAÇÃO
        # ==================================================
        if player.props.status == "Playing":

            if track != self.last_track:

                # leitura segura do metadata
                cover_url = None
                try:
                    cover_url = metadata["mpris:artUrl"]
                    cover_url = str(cover_url)
                except Exception:
                    pass

                icon_path = "spotify"

                if cover_url:
                    cached = self.get_cached_cover(cover_url)
                    if cached:
                        icon_path = cached

                # notificação mais estruturada
                subprocess.run([
                    "notify-send",
                    "-r", "9999",
                    "-i", icon_path,
                    title,
                    artist if artist else ""
                ])

                self.last_track = track

            display = " " + track
        else:
            display = " " + track

        # ==================================================
        # ATUALIZA WAYBAR
        # ==================================================
        current = self.get_first_playing_player()

        if current and current.props.player_name == player.props.player_name:
            self.write_output(display, player)

    # ======================================================
    # Eventos do Player
    # ======================================================
    def on_player_appeared(self, _, player):
        if player.name in self.excluded_player:
            return
        if not self.selected_player or player.name == self.selected_player:
            self.init_player(player)

    def on_player_vanished(self, _, player):
        self.clear_output()

# ==========================================================
# Argumentos CLI
# ==========================================================
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player")
    parser.add_argument("--exclude")
    return parser.parse_args()

# ==========================================================
# MAIN
# ==========================================================
def main():
    args = parse_arguments()

    output = {
        "text": "Spotify",
        "class": "custom-spotify",
        "alt": "spotify"
    }

    sys.stdout.write(json.dumps(output) + "\n")
    sys.stdout.flush()

    player = PlayerManager(args.player, args.exclude)
    player.run()

if __name__ == "__main__":
    main()