import pygame
import sys
import random

# 1. Instellingen
pygame.init()
BREEDTE, HOOGTE = 800, 600
scherm = pygame.display.set_mode((BREEDTE, HOOGTE))
pygame.display.set_caption("Piranha - Met Tussenscherm")

# Kleuren
DONKERBLAUW = (10, 30, 60)
WIT = (255, 255, 255)
GEEL = (255, 220, 0)
GROEN_KNOP = (34, 177, 76)
LICHT_GROEN = (50, 220, 100)

# --- AFMETINGEN ---
speler_grootte = 50           
kleine_vis_grootte = 35       
grote_vis_breedte = 100       
grote_vis_hoogte = 65         

# --- GRAPHICS INLADEN ---
images_geladen = False
try:
    speler_img = pygame.image.load("piranha.png")
    kleine_vis_img = pygame.image.load("kleine_vis.png")
    grote_vis_img = pygame.image.load("grote_vis.png")
    
    speler_img = pygame.transform.scale(speler_img, (speler_grootte, speler_grootte))
    kleine_vis_img = pygame.transform.scale(kleine_vis_img, (kleine_vis_grootte, kleine_vis_grootte))
    grote_vis_img = pygame.transform.scale(grote_vis_img, (grote_vis_breedte, grote_vis_hoogte))
    images_geladen = True
except Exception as e:
    images_geladen = False

# Speler eigenschappen
speler_x, speler_y = 400, 300
speler_snelheid = 6

# Lettertypen
font_titel = pygame.font.SysFont("Helvetica", 65)  
font_ui = pygame.font.SysFont("Helvetica", 24)     
font_winst = pygame.font.SysFont("Helvetica", 65)    

# Game Status & Progressie
game_gestart = False  
level = 1
start_tijd = 0
straf_tijd = 0
onkwetsbaar_timer = 0
eind_tijd = 0
level_1_klaar = False    # NIEUW: Houdt bij of we op het tussenscherm staan
game_compleet = False

vissen = []

def start_nieuw_level(huidig_level):
    vissen.clear()
    if huidig_level == 1:
        aantal_klein, aantal_groot = 3, 2
        snelheid_klein, snelheid_groot = 4, 3
    else:
        aantal_klein, aantal_groot = 5, 4
        snelheid_klein, snelheid_groot = 6, 5

    for i in range(aantal_klein):
        vissen.append({
            "x": random.randint(50, BREEDTE - 50),
            "y": random.randint(50, HOOGTE - 50),
            "stap_x": random.choice([-snelheid_klein, snelheid_klein]),
            "stap_y": random.choice([-snelheid_klein, snelheid_klein]),
            "b": kleine_vis_grootte, "h": kleine_vis_grootte, "type": "klein"
        })

    for i in range(aantal_groot):
        vissen.append({
            "x": random.randint(50, BREEDTE - 100),
            "y": random.randint(50, HOOGTE - 70),
            "stap_x": random.choice([-snelheid_groot, snelheid_groot]),
            "stap_y": random.choice([-snelheid_groot, snelheid_groot]),
            "b": grote_vis_breedte, "h": grote_vis_hoogte, "type": "groot"
        })

start_nieuw_level(level)

# Knoppen definiëren
start_knop_rect = pygame.Rect(300, 350, 200, 50)
next_knop_rect = pygame.Rect(300, 350, 200, 50)   # NIEUW: Knop voor Level 2
opnieuw_knop_rect = pygame.Rect(300, 420, 200, 50)

# 2. Game Loop
klok = pygame.time.Clock()
running = True

while running:
   pygame.event.pump()
   muis_pos = pygame.mouse.get_pos()
   
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
           
       if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
           # Startmenu klik
           if not game_gestart:
               if start_knop_rect.collidepoint(muis_pos):
                   game_gestart = True
                   start_tijd = pygame.time.get_ticks() 
           
           # NIEUW: Tussenscherm klik (Naar level 2)
           elif level_1_klaar:
               if next_knop_rect.collidepoint(muis_pos):
                   level = 2
                   level_1_klaar = False
                   speler_x, speler_y = 400, 300
                   start_nieuw_level(level)
           
           # Eindscherm klik (Opnieuw spelen)
           elif game_compleet:
               if opnieuw_knop_rect.collidepoint(muis_pos):
                   level = 1
                   straf_tijd = 0
                   onkwetsbaar_timer = 0
                   game_compleet = False
                   level_1_klaar = False
                   speler_x, speler_y = 400, 300
                   start_nieuw_level(level)
                   start_tijd = pygame.time.get_ticks()

   # --- LOGICA VOOR DE GAMEPLAY ---
   # De gameplay draait nu ALLEEN als het spel gestart is, Level 1 niet net klaar is, en het spel niet compleet is
   if game_gestart and not level_1_klaar and not game_compleet:
       huidige_tijd = (pygame.time.get_ticks() - start_tijd) / 1000 + straf_tijd

       # Besturing Speler
       toetsen = pygame.key.get_pressed()
       if toetsen[pygame.K_LEFT]:  speler_x -= speler_snelheid
       if toetsen[pygame.K_RIGHT]: speler_x += speler_snelheid
       if toetsen[pygame.K_UP]:    speler_y -= speler_snelheid
       if toetsen[pygame.K_DOWN]:  speler_y += speler_snelheid

       if speler_x < 0: speler_x = 0
       if speler_x > BREEDTE - speler_grootte: speler_x = BREEDTE - speler_grootte
       if speler_y < 0: speler_y = 0
       if speler_y > HOOGTE - speler_grootte: speler_y = HOOGTE - speler_grootte

       speler_rect = pygame.Rect(speler_x, speler_y, speler_grootte, speler_grootte)

       # AI Vissen Logica
       for vis in vissen[:]:
           vis["x"] += vis["stap_x"]
           vis["y"] += vis["stap_y"]

           if vis["x"] + vis["b"] > BREEDTE or vis["x"] < 0: vis["stap_x"] *= -1
           if vis["y"] + vis["h"] > HOOGTE or vis["y"] < 0: vis["stap_y"] *= -1

           vis_rect = pygame.Rect(vis["x"], vis["y"], vis["b"], vis["h"])

           if speler_rect.colliderect(vis_rect):
               if vis["type"] == "klein":
                   vissen.remove(vis)
               elif vis["type"] == "groot" and onkwetsbaar_timer == 0:
                   straf_tijd += 2
                   onkwetsbaar_timer = 60

       if onkwetsbaar_timer > 0:
           onkwetsbaar_timer -= 1

       # LEVEL & WINST CHECK
       aantal_kleine_vissen = len([v for v in vissen if v["type"] == "klein"])
       if aantal_kleine_vissen == 0:
           if level == 1:
               level_1_klaar = True # Activeer het tussenscherm!
           else:
               game_compleet = True
               eind_tijd = huidige_tijd

   # 4. TEKENEN
   scherm.fill(DONKERBLAUW)
  
   # MENU SCHERM
   if not game_gestart:
       tekst_titel = font_titel.render("PIRANHA", True, GEEL)
       tekst_uitleg = font_ui.render("Eet de groene vissen. Ontwijk de brede rode!", True, WIT)
       scherm.blit(tekst_titel, (260, 160))
       scherm.blit(tekst_uitleg, (200, 260))
       
       kleur_knop = LICHT_GROEN if start_knop_rect.collidepoint(muis_pos) else GROEN_KNOP
       pygame.draw.rect(scherm, kleur_knop, start_knop_rect, border_radius=10)
       tekst_knop = font_ui.render("START GAME", True, WIT)
       scherm.blit(tekst_knop, (335, 362))

   # TUSSENSCHERM (Level 1 Gewonnen)
   elif level_1_klaar:
       tekst_lvl1 = font_winst.render("Level 1 Gewonnen!", True, GEEL)
       tekst_sub = font_ui.render("Maak je klaar voor het zwaardere werk...", True, WIT)
       scherm.blit(tekst_lvl1, (160, 180))
       scherm.blit(tekst_sub, (210, 270))
       
       kleur_next = LICHT_GROEN if next_knop_rect.collidepoint(muis_pos) else GROEN_KNOP
       pygame.draw.rect(scherm, kleur_next, next_knop_rect, border_radius=10)
       tekst_next = font_ui.render("LEVEL 2 START", True, WIT)
       scherm.blit(tekst_next, (325, 362))

   # GAMEPLAY & EINDCHEFM
   else:
       # Teken vissen
       for vis in vissen:
           if images_geladen:
               scherm.blit(kleine_vis_img if vis["type"] == "klein" else grote_vis_img, (vis["x"], vis["y"]))
           else:
               kleur = (0, 255, 100) if vis["type"] == "klein" else (255, 50, 50)
               pygame.draw.rect(scherm, kleur, (vis["x"], vis["y"], vis["b"], vis["h"]))

       # Teken Piranha
       if not (onkwetsbaar_timer > 0 and onkwetsbaar_timer % 10 < 5):
           if images_geladen:
               scherm.blit(speler_img, (speler_x, speler_y))
           else:
               kleur_speler = (255, 50, 50) if onkwetsbaar_timer > 50 else (0, 100, 255)
               pygame.draw.rect(scherm, kleur_speler, (speler_x, speler_y, speler_grootte, speler_grootte))

       # Lopende UI
       if not game_compleet:
           tekst_timer = font_ui.render(f"Tijd: {huidige_tijd:.1f} sec", True, WIT)
           tekst_level = font_ui.render(f"Level: {level}", True, GEEL)
           scherm.blit(tekst_timer, (20, 20))
           scherm.blit(tekst_level, (BREEDTE - 100, 20))
       
       # Eindscherm
       if game_compleet:
           tekst_winst = font_winst.render("Spel Uitgespeeld!", True, GEEL)
           tekst_score = font_ui.render(f"Je totale eindtijd score: {eind_tijd:.1f} seconden", True, WIT)
           scherm.blit(tekst_winst, (170, 160))
           scherm.blit(tekst_score, (240, 260))
           
           kleur_opnieuw = LICHT_GROEN if opnieuw_knop_rect.collidepoint(muis_pos) else GROEN_KNOP
           pygame.draw.rect(scherm, kleur_opnieuw, opnieuw_knop_rect, border_radius=10)
           tekst_opnieuw = font_ui.render("AGAIN?", True, WIT)
           scherm.blit(tekst_opnieuw, (360, 432))

   pygame.display.flip()
   klok.tick(60)

pygame.quit()
sys.exit()