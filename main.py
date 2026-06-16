import pygame
import sys

# 1. Instellingen
pygame.init()
BREEDTE, HOOGTE = 800, 600
scherm = pygame.display.set_mode((BREEDTE, HOOGTE))
pygame.display.set_caption("Piranha - Prototype 1")

# Kleuren
BLAUW = (0, 100, 255)      # Kleur voor de Piranha speler
DONKERBLAUW = (10, 30, 60) # Een mooie 'water' achtergrondkleur

# Piranha (Speler) eigenschappen
speler_x = 400
speler_y = 300
speler_grootte = 40
speler_snelheid = 6

# 2. Game Loop
klok = pygame.time.Clock()

while True:
   # Events checken
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()

   # Knoppen uitlezen voor de besturing
   toetsen = pygame.key.get_pressed()
   
   if toetsen[pygame.K_LEFT]:
       speler_x -= speler_snelheid
   if toetsen[pygame.K_RIGHT]:
       speler_x += speler_snelheid
   if toetsen[pygame.K_UP]:
       speler_y -= speler_snelheid
   if toetsen[pygame.K_DOWN]:
       speler_y += speler_snelheid

   # Zorgen dat de Piranha niet buiten het scherm zwemt
   if speler_x < 0:
       speler_x = 0
   if speler_x > BREEDTE - speler_grootte:
       speler_x = BREEDTE - speler_grootte
   if speler_y < 0:
       speler_y = 0
   if speler_y > HOOGTE - speler_grootte:
       speler_y = HOOGTE - speler_grootte

   # 4. Tekenen
   scherm.fill(DONKERBLAUW) # Achtergrond vullen met waterkleur
  
   # De Piranha tekenen (voor nu een blauw vierkant)
   pygame.draw.rect(scherm, BLAUW, (speler_x, speler_y, speler_grootte, speler_grootte))

   # Scherm verversen
   pygame.display.flip()
  
   # Snelheid begrenzen op 60 frames per seconde voor soepele besturing
   klok.tick(60)