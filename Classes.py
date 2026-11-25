import pygame
from Constantes import cores


class CriarPersonagemLabirinto():
    def __init__(self,cor,largura,tamanho,posicaox, posicaoy):
        
        self.cor = cor
       
        self.rect = pygame.Rect(posicaox,posicaoy,largura,tamanho)


    def DesenharNaTela(self,tela):
        pygame.draw.rect(tela, self.cor, self.rect)





####Classe apenas para criar o "Retangulo / Personagem que vai andar pelo labirinto"