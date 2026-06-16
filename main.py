import pygame
import sys
import random

# 1. Instellingen
pygame.init()
BREEDTE, HOOGTE = 800, 600
scherm = pygame.display.set_mode((BREEDTE, HOOGTE))
pygame.display.set_caption("Piranha - Prototype 2: Timer & Straf")

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
font_ui = pygame.font.SysFont("Helvetica", 30)
font_winst = pygame.font.SysFont("Helvetica", 80)

# Timers en Status
start_tijd = pygame.time.get_ticks() # Onthoud wanneer het spel begon
straf_tijd = 0                       # Extra seconden opgelopen door straf
onkwetsbaar_timer = 0                # Timer voor de "AU!"-status en onkwetsbaarheid
eind_tijd = 0                        # Slaat de eindscore op bij winst
game_gewonnen = False

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

   if not game_gewonnen:
       # Bereken de huidige tijd (in seconden) + de opgelopen straftijd
       huidige_tijd = (pygame.time.get_ticks() - start_tijd) / 1000 + straf_tijd

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

       speler_rect = pygame.Rect(speler_x, speler_y, speler_grootte, speler_grootte)

       # LOGICA VAN DE AI-VISSEN & BOTSINGEN
       for vis in vissen[:]:
           vis["x"] += vis["stap_x"]
           vis["y"] += vis["stap_y"]

           if vis["x"] + vis["grootte"] > BREEDTE or vis["x"] < 0:
               vis["stap_x"] *= -1
           if vis["y"] + vis["grootte"] > HOOGTE or vis["y"] < 0:
               vis["stap_y"] *= -1

           vis_rect = pygame.Rect(vis["x"], vis["y"], vis["grootte"], vis["grootte"])

           if speler_rect.colliderect(vis_rect):
               if vis["type"] == "klein":
                   vissen.remove(vis)
               elif vis["type"] == "groot" and onkwetsbaar_timer == 0:
                   straf_tijd += 2          # Direct 2 seconden straf erbij!
                   onkwetsbaar_timer = 60   # 1 seconde (60 frames) onkwetsbaar en rood flitsen

       # Verminder de onkwetsbaarheidstimer als deze actief is
       if onkwetsbaar_timer > 0:
           onkwetsbaar_timer -= 1

       # WINST CHECK
       aantal_kleine_vissen = len([v for v in vissen if v["type"] == "klein"])
       if aantal_kleine_vissen == 0:
           game_gewonnen = True
           eind_tijd = huidige_tijd # Sla de definitieve eindtijd op

   # 4. Tekenen
   scherm.fill(DONKERBLAUW)
  
   # Teken de AI-vissen
   for vis in vissen:
       pygame.draw.rect(scherm, vis["kleur"], (vis["x"], vis["y"], vis["grootte"], vis["grootte"]))

   # De Piranha tekenen (Flitst rood als je geraakt bent)
   if onkwetsbaar_timer > 0 and onkwetsbaar_timer % 10 < 5:
       # Sla het tekenen van de speler soms een frame over voor een knipper-effect
       pass
   else:
       # Als je net geraakt bent, kleur je even ROOD, anders BLAUW
       kleur_speler = ROOD if onkwetsbaar_timer > 50 else BLAUW
       pygame.draw.rect(scherm, kleur_speler, (speler_x, speler_y, speler_grootte, speler_grootte))

   # UI BOVENIN HET SCHERM TEKENEN
   if not game_gewonnen:
       tekst_timer = font_ui.render(f"Tijd: {huidige_tijd:.1f} sec", True, WIT)
       scherm.blit(tekst_timer, (20, 20))
   
   # Als er gewonnen is, toon het eindscherm met de score
   if game_gewonnen:
       tekst_winst = font_winst.render("Level Voltooid!", True, GEEL)
       tekst_score = font_ui.render(f"Je score (totale tijd): {eind_tijd:.1f} seconden", True, WIT)
       
       scherm.blit(tekst_winst, (160, 200))
       scherm.blit(tekst_score, (200, 320))

   # Scherm verversen
   pygame.display.flip()
   klok.tick(60)

pygame.quit()
sys.exit()