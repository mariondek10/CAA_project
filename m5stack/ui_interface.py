from m5stack import *
from m5stack_ui import *

# Initialisation de l'écran
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x000000)

# Création des éléments fixes
title = M5Label('BIKE DASHBOARD', x=70, y=20, color=0xFFFFFF, font=FONT_MONT_18)
label_vitesse = M5Label('0', x=110, y=90, color=0x00FF00, font=FONT_MONT_34)
unit = M5Label('km/h', x=135, y=150, color=0x00FF00, font=FONT_MONT_14)
status = M5Label('GPS: Waiting...', x=10, y=210, color=0xAAAAAA, font=FONT_MONT_14)

def update_display(vitesse, has_fix):
    """Mise à jour dynamique de l'écran"""
    label_vitesse.set_text(str(round(vitesse, 1)))
    if has_fix:
        status.set_text("GPS: Locked")
        status.set_color(0x00FF00)
    else:
        status.set_text("GPS: Searching...")
        status.set_color(0xFF0000)