import pygame
import sys
import random

# 1. Instellingen
pygame.init()
BREEDTE, HOOGTE = 800, 600
scherm = pygame.display.set_mode((BREEDTE, HOOGTE))
pygame.display.set_caption("Piranha - Prototype 2")

# Kleuren (voor tekst en achtergrond)
DONKERBLAUW = (10, 30, 60)  # Water
WIT = (255, 255, 255)       # Tekstkleur
GEEL = (255, 220, 0)        # Winsttekst

# --- GRAPHICS INLADEN MET VEILIGHEIDSCHECK ---
images_geladen = False

try:
    speler_img = pygame.image.load("piranha.png")
    kleine_vis_img = pygame.image.load("kleine_vis.png")
    grote_vis_img = pygame.image.load("grote_vis.png")
    
    # Pas de afbeeldingen direct aan naar de juiste groottes
    speler_img = pygame.transform.scale(speler_img, (40, 40))
    kleine_vis_img = pygame.transform.scale(kleine_vis_img, (20, 20))
    grote_vis_img = pygame.transform.scale(grote_vis_img, (60, 60))
    
    images_geladen = True
    print("Succes: Alle afbeeldingen zijn correct geladen!")
except Exception as e:
    print("Opmerking: Afbeeldingen niet gevonden. We spelen met gekleurde blokjes!")
    images_geladen = False

# Piranha (Speler) eigenschappen
speler_x = 400
speler_y = 300
speler_grootte = 40
speler_snelheid = 6

# Piranha (Speler) eigenschappen
speler_x = 400
speler_y = 300
speler_grootte = 40
speler_snelheid = 6

# Lettertypen voor de tekst
font_ui = pygame.font.SysFont("Helvetica", 30)
font_winst = pygame.font.SysFont("Helvetica", 80)

# Timers en Status
start_tijd = pygame.time.get_ticks()
straf_tijd = 0
onkwetsbaar_timer = 0
eind_tijd = 0
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
                   vissen.remove(vis) # Vis verdwijnt in stilte
               elif vis["type"] == "groot" and onkwetsbaar_timer == 0:
                   straf_tijd += 2
                   onkwetsbaar_timer = 60

       if onkwetsbaar_timer > 0:
           onkwetsbaar_timer -= 1

       # WINST CHECK
       aantal_kleine_vissen = len([v for v in vissen if v["type"] == "klein"])
       if aantal_kleine_vissen == 0:
           game_gewonnen = True
           eind_tijd = huidige_tijd

   # 4. Tekenen
   scherm.fill(DONKERBLAUW)
  
   # Teken de AI-vissen
   for vis in vissen:
       if images_geladen:
           afbeelding = kleine_vis_img if vis["type"] == "klein" else grote_vis_img
           scherm.blit(afbeelding, (vis["x"], vis["y"]))
       else:
           kleur = (0, 255, 100) if vis["type"] == "klein" else (255, 50, 50)
           pygame.draw.rect(scherm, kleur, (vis["x"], vis["y"], vis["grootte"], vis["grootte"]))

   # De Piranha tekenen
   if onkwetsbaar_timer > 0 and onkwetsbaar_timer % 10 < 5:
       pass
   else:
       if images_geladen:
           scherm.blit(speler_img, (speler_x, speler_y))
       else:
           kleur_speler = (255, 50, 50) if onkwetsbaar_timer > 50 else (0, 100, 255)
           pygame.draw.rect(scherm, kleur_speler, (speler_x, speler_y, speler_grootte, speler_grootte))

   # UI BOVENIN HET SCHERM TEKENEN
   if not game_gewonnen:
       tekst_timer = font_ui.render(f"Tijd: {huidige_tijd:.1f} sec", True, WIT)
       scherm.blit(tekst_timer, (20, 20))
   
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