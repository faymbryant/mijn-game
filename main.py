import pygame
import sys
import random

# 1. Instellingen
pygame.init()
BREEDTE, HOOGTE = 800, 600
scherm = pygame.display.set_mode((BREEDTE, HOOGTE))
pygame.display.set_caption("Piranha - Prototype 1: Voltooid!")

# Kleuren
BLAUW = (0, 100, 255)       # Piranha
DONKERBLAUW = (10, 30, 60)  # Water
GROEN = (0, 255, 100)       # Kleine vissen
ROOD = (255, 50, 50)        # Grote vissen
WIT = (255, 255, 255)       # Tekstkleur
GEEL = (255, 220, 0)        # Winsttekst

# Piranha (Speler) eigenschappen
speler_x = 400
speler_y = 300
speler_grootte = 40
speler_snelheid = 6

# Lettertypen voor de tekst
font_au = pygame.font.SysFont("Helvetica", 50)
font_winst = pygame.font.SysFont("Helvetica", 100)

toon_au_timer = 0  # Timer om de "AU!" tekst even in beeld te houden
game_gewonnen = False  # Houdt bij of de speler heeft gewonnen

# AI Vissen aanmaken
vissen = []

# 3 Kleine vissen toevoegen
for i in range(3):
    vissen.append({
        "x": random.randint(50, BREEDTE - 50),
        "y": random.randint(50, HOOGTE - 50),
        "stap_x": random.choice([-4, 4]),
        "stap_y": random.choice([-4, 4]),
        "grootte": 20,
        "kleur": GROEN,
        "type": "klein"
    })

# 2 Grote vissen toevoegen
for i in range(2):
    vissen.append({
        "x": random.randint(50, BREEDTE - 50),
        "y": random.randint(50, HOOGTE - 50),
        "stap_x": random.choice([-3, 3]),
        "stap_y": random.choice([-3, 3]),
        "grootte": 60,
        "kleur": ROOD,
        "type": "groot"
    })

# 2. Game Loop
klok = pygame.time.Clock()
running = True

while running:
   pygame.event.pump()
   
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False

   # ALLES HIERONDER GEBEURT ALLEEN ALS JE NOG NIET GEWONNEN HEBT
   if not game_gewonnen:
       # Knoppen uitlezen voor de besturing
       toetsen = pygame.key.get_pressed()
       if toetsen[pygame.K_LEFT]:  speler_x -= speler_snelheid
       if toetsen[pygame.K_RIGHT]: speler_x += speler_snelheid
       if toetsen[pygame.K_UP]:    speler_y -= speler_snelheid
       if toetsen[pygame.K_DOWN]:  speler_y += speler_snelheid

       # Zorgen dat de Piranha binnen het scherm blijft
       if speler_x < 0: speler_x = 0
       if speler_x > BREEDTE - speler_grootte: speler_x = BREEDTE - speler_grootte
       if speler_y < 0: speler_y = 0
       if speler_y > HOOGTE - speler_grootte: speler_y = HOOGTE - speler_grootte

       # Maak een Pygame Rect voor de speler
       speler_rect = pygame.Rect(speler_x, speler_y, speler_grootte, speler_grootte)

       # LOGICA VAN DE AI-VISSEN & BOTSINGEN
       for vis in vissen[:]:
           # Beweeg de vis
           vis["x"] += vis["stap_x"]
           vis["y"] += vis["stap_y"]

           # Stuiteren tegen de randen
           if vis["x"] + vis["grootte"] > BREEDTE or vis["x"] < 0:
               vis["stap_x"] *= -1
           if vis["y"] + vis["grootte"] > HOOGTE or vis["y"] < 0:
               vis["stap_y"] *= -1

           # Botsingsdetectie
           vis_rect = pygame.Rect(vis["x"], vis["y"], vis["grootte"], vis["grootte"])

           if speler_rect.colliderect(vis_rect):
               if vis["type"] == "klein":
                   vissen.remove(vis)
               elif vis["type"] == "groot":
                   toon_au_timer = 30

       # WINST CHECK: Tel hoeveel kleine vissen er nog zijn
       aantal_kleine_vissen = len([v for v in vissen if v["type"] == "klein"])
       if aantal_kleine_vissen == 0:
           game_gewonnen = True

   # 4. Tekenen (Dit blijft wel doorgaan zodat we het winstscherm zien)
   scherm.fill(DONKERBLAUW)
  
   # Teken de AI-vissen
   for vis in vissen:
       pygame.draw.rect(scherm, vis["kleur"], (vis["x"], vis["y"], vis["grootte"], vis["grootte"]))

   # De Piranha tekenen
   pygame.draw.rect(scherm, BLAUW, (speler_x, speler_y, speler_grootte, speler_grootte))

   # Als de AU!-timer loopt, teken de tekst
   if toon_au_timer > 0 and not game_gewonnen:
       tekst_au = font_au.render("AU!", True, WIT)
       scherm.blit(tekst_au, (20, 20))
       toon_au_timer -= 1

   # Als er gewonnen is, toon de grote tekst in het midden
   if game_gewonnen:
       tekst_winst = font_winst.render("Gewonnen!", True, GEEL)
       # Netjes in het midden van het scherm plaatsen
       scherm.blit(tekst_winst, (180, 250))

   # Scherm verversen
   pygame.display.flip()
   klok.tick(60)

pygame.quit()
sys.exit()