import pygame

pygame.init()

fim_jogo = False

while fim_jogo == False:
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            fim_jogo = True            #ACABA O LOOP PRINCIPAL
