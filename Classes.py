import pygame


class CriarPersonagemLabirinto():
    def __init__(self, cor, largura, tamanho, posicaox, posicaoy):
        self.cor = cor
        self.rect = pygame.Rect(posicaox, posicaoy, largura, tamanho)

    def DesenharNaTela(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)


# Classe para criar o retângulo / personagem que vai andar pelo labirinto
