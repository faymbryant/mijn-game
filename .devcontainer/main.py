import pygame
import sys


# 1. Instellingen
pygame.init()
# Verander deze getallen:
BREEDTE, HOOGTE = 1000, 700
scherm = pygame.display.set_mode((BREEDTE, HOOGTE))
pygame.display.set_caption("Mijn Eerste Game - Hello World")


# Kleuren
ZWART = (20, 20, 20)
GROEN = (0, 255, 0)
WIT = (255, 255, 255)


# Cirkel eigenschappen
x, y = 300, 200
stap_x, stap_y = 4, 4
straal = 20


# Lettertype voor de tekst
font = pygame.font.SysFont("Arial", 32)


# 2. Game Loop
klok = pygame.time.Clock()


while True:
   # Events checken (zoals het kruisje klikken)
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()


   # 3. Logica (berekeningen)
   x += stap_x
   y += stap_y


   # Botsing met de randen
   if x + straal > BREEDTE or x - straal < 0:
       stap_x *= -1
   if y + straal > HOOGTE or y - straal < 0:
       stap_y *= -1


   # 4. Tekenen
   scherm.fill(ZWART)
  
   # Tekst op het scherm
   tekst = font.render("Hello World! De game draait.", True, WIT)
   scherm.blit(tekst, (150, 50))
  
   # De stuiterende cirkel
   pygame.draw.circle(scherm, GROEN, (x, y), straal)


   # Scherm verversen
   pygame.display.flip()
  
   # Snelheid begrenzen op 60 frames per seconde
   klok.tick(60)