import pygame
import sys
import random

# 1. Instellingen
pygame.init()
BREEDTE, HOOGTE = 800, 600
scherm = pygame.display.set_mode((BREEDTE, HOOGTE))
pygame.display.set_caption("Piranha - Unieke Timers per Level")

# Kleuren
DONKERBLAUW = (10, 30, 60)
WIT = (255, 255, 255)
GEEL = (255, 220, 0)
GROEN_KNOP = (34, 177, 76)
LICHT_GROEN = (50, 220, 100)

# --- AFMETINGEN ---
speler_grootte = 60           
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
level_klaar_wacht_op_knop = False  
game_compleet = False

# NIEUW: Lijst om de tijden van elk level apart in op te slaan
level_tijden = {1: 0.0, 2: 0.0, 3: 0.0}

vissen = []

def start_nieuw_level(huidig_level):
    vissen.clear()
    
    if huidig_level == 1:
        aantal_klein, aantal_groot = 3, 2
        snelheid_klein, snelheid_groot = 4, 3
    elif huidig_level == 2:
        aantal_klein, aantal_groot = 5, 3
        snelheid_klein, snelheid_groot = 6, 5
    elif huidig_level == 3:
        aantal_klein, aantal_groot = 30, 4
        snelheid_klein, snelheid_groot = 6, 6  

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
start_knop_rect = pygame.Rect(300, 440, 200, 50)   
next_knop_rect = pygame.Rect(300, 380, 200, 50)   
opnieuw_knop_rect = pygame.Rect(300, 460, 200, 50) # Iets naar beneden geplaatst voor het eindoverzicht

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
           if not game_gestart:
               if start_knop_rect.collidepoint(muis_pos):
                   game_gestart = True
                   start_tijd = pygame.time.get_ticks() 
                   straf_tijd = 0 # Reset straftijd bij de start
           
           elif level_klaar_wacht_op_knop:
               if next_knop_rect.collidepoint(muis_pos):
                   level += 1
                   level_klaar_wacht_op_knop = False
                   speler_x, speler_y = 400, 300
                   start_nieuw_level(level)
                   start_tijd = pygame.time.get_ticks() # NIEUW: Reset de timer voor het volgende level!
                   straf_tijd = 0                       # NIEUW: Reset de straftijd voor het volgende level!
           
           elif game_compleet:
               if opnieuw_knop_rect.collidepoint(muis_pos):
                   level = 1
                   straf_tijd = 0
                   onkwetsbaar_timer = 0
                   game_compleet = False
                   level_klaar_wacht_op_knop = False
                   level_tijden = {1: 0.0, 2: 0.0, 3: 0.0} # Reset de opgeslagen tijden
                   speler_x, speler_y = 400, 300
                   start_nieuw_level(level)
                   start_tijd = pygame.time.get_ticks()

   # --- LOGICA VOOR DE GAMEPLAY ---
   if game_gestart and not level_klaar_wacht_op_knop and not game_compleet:
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
           level_tijden[level] = huidige_tijd # Sla de tijd van dit specifieke level op!
           
           if level < 3:
               level_klaar_wacht_op_knop = True 
           else:
               game_compleet = True

   # 4. TEKENEN
   scherm.fill(DONKERBLAUW)
  
   # MENU SCHERM
   if not game_gestart:
       tekst_titel = font_titel.render("PIRANHA", True, GEEL)
       scherm.blit(tekst_titel, (260, 80))
       
       uitleg_1 = font_ui.render("Hoe speel je het spel:", True, GEEL)
       uitleg_2 = font_ui.render("- Bestuur de piranha met de pijltjestoetsen.", True, WIT)
       uitleg_3 = font_ui.render("- Eet alle kleine vissen op om het level te halen.", True, WIT)
       uitleg_4 = font_ui.render("- Ontwijk de grote vissen.", True, WIT)
       uitleg_5 = font_ui.render("- Raak je een grote vis? Dan krijg je +2 seconden straftijd!", True, WIT)
       uitleg_6 = font_ui.render("Probeer de 3 levels zo snel mogelijk uit te spelen!", True, GEEL)
       
       scherm.blit(uitleg_1, (80, 180))
       scherm.blit(uitleg_2, (80, 220))
       scherm.blit(uitleg_3, (80, 250))
       scherm.blit(uitleg_4, (80, 280))
       scherm.blit(uitleg_5, (80, 310))
       scherm.blit(uitleg_6, (80, 360))
       
       kleur_knop = LICHT_GROEN if start_knop_rect.collidepoint(muis_pos) else GROEN_KNOP
       pygame.draw.rect(scherm, kleur_knop, start_knop_rect, border_radius=10)
       tekst_knop = font_ui.render("START GAME", True, WIT)
       scherm.blit(tekst_knop, (335, 452))

   # TUSSENSCHERM (Laat de tijd van het zojuist gespeelde level zien)
   elif level_klaar_wacht_op_knop:
       tekst_lvl = font_winst.render(f"Level {level} Gewonnen!", True, GEEL)
       tekst_tijd_status = font_ui.render(f"Tijd voor dit level: {level_tijden[level]:.1f} seconden", True, WIT)
       tekst_sub = font_ui.render("Klaar voor het volgende level?", True, GEEL) 
       
       scherm.blit(tekst_lvl, (160, 150))
       scherm.blit(tekst_tijd_status, (250, 240))
       scherm.blit(tekst_sub, (245, 290))
       
       kleur_next = LICHT_GROEN if next_knop_rect.collidepoint(muis_pos) else GROEN_KNOP
       pygame.draw.rect(scherm, kleur_next, next_knop_rect, border_radius=10)
       
       tekst_knop_next = f"START LEVEL {level + 1}"
       tekst_next = font_ui.render(tekst_knop_next, True, WIT)
       scherm.blit(tekst_next, (315, 392))

   # GAMEPLAY & EINDSCHERM
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

       # Lopende UI (Timer voor het HUIDIGE level)
       if not game_compleet:
           tekst_timer = font_ui.render(f"Tijd Level {level}: {huidige_tijd:.1f} sec", True, WIT)
           tekst_level = font_ui.render(f"Level: {level}", True, GEEL)
           scherm.blit(tekst_timer, (20, 20))
           scherm.blit(tekst_level, (BREEDTE - 100, 20))
       
       # Eindscherm (Nu met een compleet overzicht van alle levels!)
       if game_compleet:
           tekst_winst = font_winst.render("Spel Uitgespeeld!", True, GEEL)
           scherm.blit(tekst_winst, (170, 100))
           
           # Scores per level renderen
           score_l1 = font_ui.render(f"Tijd Level 1: {level_tijden[1]:.1f} sec", True, WIT)
           score_l2 = font_ui.render(f"Tijd Level 2: {level_tijden[2]:.1f} sec", True, WIT)
           score_l3 = font_ui.render(f"Tijd Level 3: {level_tijden[3]:.1f} sec", True, WIT)
           
           totale_tijd = level_tijden[1] + level_tijden[2] + level_tijden[3]
           score_totaal = font_ui.render(f"Totale Eindscore: {totale_tijd:.1f} seconden", True, GEEL)
           
           scherm.blit(score_l1, (280, 220))
           scherm.blit(score_l2, (280, 260))
           scherm.blit(score_l3, (280, 300))
           scherm.blit(score_totaal, (240, 370))
           
           kleur_opnieuw = LICHT_GROEN if opnieuw_knop_rect.collidepoint(muis_pos) else GROEN_KNOP
           pygame.draw.rect(scherm, kleur_opnieuw, opnieuw_knop_rect, border_radius=10)
           tekst_opnieuw = font_ui.render("AGAIN?", True, WIT)
           scherm.blit(tekst_opnieuw, (360, 472))

   pygame.display.flip()
   klok.tick(60)

pygame.quit()
sys.exit()