import pygame, random, ctypes
pygame.init()

frstr = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
pygame.display.set_caption("Tile")

ceas = pygame.time.Clock()

ompng = pygame.image.load("Img/om.png")
steagpng = pygame.image.load("Img/steag.png")

mov = (255, 0, 255)
galben = (255, 255, 0)
rosu = (255, 0, 0)
albastru = (0, 0, 255)
verde = (0, 255, 0)
portocaliu = (255, 125, 60)


varx = 0
vary = -10

culoare = verde

toate = pygame.sprite.Group()
ply = pygame.sprite.Group()
steag = pygame.sprite.Group()
tile = pygame.sprite.Group()

plc_albstr = False
plc_galb = False
plc_port = False
plc_rosie = False
reincepere = False

class pixel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.culoare = random.randrange(1, 7)
        
        if self.culoare == 1:
            culoare = mov
        elif self.culoare == 2:
            culoare = galben
        elif self.culoare == 3:
            culoare = rosu
        elif self.culoare == 4:
            culoare = albastru
        elif self.culoare == 5:
            culoare = verde
        elif self.culoare == 6:
            culoare = portocaliu

        self.image = pygame.Surface((50, 50))
        self.image.fill(culoare)
            
        self.rect = self.image.get_rect()
        self.rect.x = varx
        self.rect.y = vary
    def update(self):
        global plc_albstr, plc_galb, plc_port, plc_rosie, reincepere
        self.taste = pygame.key.get_pressed()
        self.atingere = pygame.sprite.spritecollide(self, ply, False)
        
        if self.taste[pygame.K_SPACE] or reincepere:
            self.kill()
        if self.atingere and self.culoare == 2 and plc_galb:
            reincepere = True
        if self.atingere and self.culoare == 3 and plc_rosie:
            reincepere = True
        if self.atingere and self.culoare == 6 and plc_port:
            reincepere = True
        if self.atingere and self.culoare == 4 and plc_albstr:
            reincepere = True

        if self.atingere and self.culoare == 1:
            plc_galb = True
        if self.atingere and self.culoare == 5:
            plc_albstr = True
        if self.atingere and self.culoare == 2:
            plc_rosie = True
        if self.atingere and self.culoare == 4:
            plc_port = True

            

class jucator(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(ompng, (23, 39))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.vit = 3
    def update(self):
        self.taste = pygame.key.get_pressed()
        if self.taste[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.vit
        if self.taste[pygame.K_DOWN] and self.rect.y < 800 - 39:
            self.rect.y += self.vit
        if self.taste[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.vit
        if self.taste[pygame.K_RIGHT] and self.rect.x < 800 - 23:
            self.rect.x += self.vit
        if self.taste[pygame.K_SPACE] or reincepere:
            self.kill()

class final(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(steagpng, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 800 - 50
        self.rect.y = 800 - 50
    def update(self):
        if reincepere:
            self.kill()

def generare():
    global vary
    global varx
    varx = 0
    vary = -50
    for i in range(300):
        if vary < 801:
            vary += 50
        else:
            vary = 0
            varx += 50
        pix = pixel()
        toate.add(pix)
        tile.add(pix)

rulare = True
generare()
om = jucator()
toate.add(om)
ply.add(om)
fin = final()
toate.add(fin)
steag.add(fin)
while rulare:
    ceas.tick(120)
    taste = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rulare = False
        elif taste[pygame.K_SPACE] or reincepere:
            generare()
            om = jucator()
            toate.add(om)
            ply.add(om)
            fin = final()
            toate.add(fin)
            steag.add(fin)
            plc_albstr = False
            plc_galb = False
            plc_port = False
            plc_rosie = False
            reincepere = False
        elif taste[pygame.K_F4]:
            frstr = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        elif taste[pygame.K_F3]:
            frstr = pygame.display.set_mode((800, 800), pygame.RESIZABLE)

    castig = pygame.sprite.groupcollide(ply, steag, False, True)

    if castig:
        ctypes.windll.user32.MessageBoxW(0, "Ti-ai pierdut timpul!", "Bravo", 1)
        rulare = False

    toate.update()
    toate.draw(frstr)
    pygame.display.flip()

pygame.quit()
