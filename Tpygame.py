#pip install pygame-ce

import pygame
import random

from pygame.locals import ( 
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  KEYDOWN,
  QUIT,
  K_ESCAPE,
  K_SPACE,
)

pygame.init()

clock = pygame.time.Clock()

SC_WIDHT = 800
SC_HEIGHT = 600

half_w = int(SC_WIDHT/2)
half_h = int(SC_HEIGHT/2)




class Player(pygame.sprite.Sprite):
  def __init__(self):
    super(Player, self).__init__()
    self.surf = pygame.Surface((75,25))
    self.surf.fill((0,255,0)) # branco
    self.rect = self.surf.get_rect()

  def update(self, pressed):
    if pressed[pygame.K_UP]:
      self.rect.move_ip(0, -5)  
    if pressed[pygame.K_DOWN]:
      self.rect.move_ip(0, 5)  
    if pressed[pygame.K_LEFT]:
      self.rect.move_ip(-5, 0)  
    if pressed[pygame.K_RIGHT]:
      self.rect.move_ip(5, 0)  


    # verifica se saiu da tela
    if self.rect.bottom >= SC_HEIGHT:
      self.rect.bottom = SC_HEIGHT
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.left <= 0:
      self.rect.left = 0
    if self.rect.right >= SC_WIDHT:
      self.rect.right =SC_WIDHT



class Enemy(pygame.sprite.Sprite):
  def __init__(self):
    super(Enemy, self).__init__()
    self.surf = pygame.Surface((25,25))
    self.surf.fill((0,15,225)) # branco
    self.rect = self.surf.get_rect(
      center = (
        random.randint(0, SC_WIDHT),
        random.randint(-100, -20)
      )
    )
    self.speed = random.randint(5, 20)

  def update(self):
    self.rect.move_ip(0,  self.speed)  
    if self.rect.top > SC_HEIGHT:
      self.kill()

vidas = 3
# criar uma fonte7
fonte = pygame.font.SysFont('Arial', 30)
texto = fonte.render(f'Vidas {vidas}', True, (255, 0, 128))

fonte_ra = pygame.font.SysFont('Arial', 22, bold=True)
texto_ra = fonte_ra.render('RA: 26397', True, (0, 0, 0))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

screen = pygame.display.set_mode([SC_WIDHT,SC_HEIGHT])
pygame.display.set_caption("Primeiro jogo")

running = True
jogador = Player()

inimigos = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(jogador)
posico = jogador.rect

while running:
  
  posicao = jogador.rect
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE or \
         event.key == pygame.K_x:
        running = False   

    if event.type == pygame.QUIT:
      running = False
    elif event.type == ADDENEMY:
      novo = Enemy()
      inimigos.add(novo)
      all_sprites.add(novo)

  teclas = pygame.key.get_pressed()
  jogador.update(teclas)
  inimigos.update()
  
  achou = pygame.sprite.spritecollide(jogador, inimigos, True)
  if achou:
    vidas -= 1
    texto = fonte.render(f'Vidas {vidas}', True, (255, 0, 128))
    if vidas == 0:
        jogador.kill()
        running = False

  screen.fill((255,255,255))

  foto = pygame.image.load('eu ft.jpeg')
  foto = pygame.transform.scale(foto, (60, 70))

  foto_x = SC_WIDHT - 60 - 10
  screen.blit(foto, (foto_x, 5))

  ra_x = SC_WIDHT - texto_ra.get_width() - 10
  screen.blit(texto_ra, (ra_x, 70))

  for entidade in all_sprites:  
    screen.blit(jogador.surf, jogador.rect)      
    screen.blit(entidade.surf, entidade.rect)
  screen.blit(texto, (30,0))


  pygame.display.flip()
  clock.tick(30)

pygame.quit()