import pygame
from Constantes import cores,Tamanho,Fps,Velocidade,MAPA
from Classes import CriarPersonagemLabirinto


pygame.init()
tela = pygame.display.set_mode((len(MAPA[0]) * Tamanho, len(MAPA) * Tamanho)) # AQUI ELE VAI CRIAR A TELA DEPENDENDO DO TAMANHO DO MAPA QUE TU FIZER NAS CONSTANTES
pygame.display.set_caption("TimeStreaks") #### AQUI SERVE PRA BOTAR O NOME QUE TU QUISER NA PARTE DE CIMA DA TELA
Relogio = pygame.time.Clock() #AQUI VAI SERVIR PRA BOTAR O FPS DEPOIS




paredes = []###3 essa lista aqui vai servir pra guardar as paredes do labirinto


for y, linha in enumerate(MAPA): ##### o enumerate vai me devolver qual linha e oq tem nessa linha
    for x, letra in enumerate(linha):##### mesma coisa só que agora pra coluna
        if letra == "#":#se o item da coluna  "letra" for igual a "#" ele entra no iff
            paredes.append(pygame.Rect(x * Tamanho, y* Tamanho, Tamanho, Tamanho)) ### e adiciona em paredes um retangulo no pixel, e o tamanho do retângulo
        elif letra == "P": ######### aqui o "P" serve pra indicar onde o personagem vai começar
            inicio = (x,y) #variável que seta o começo do personagem


margem = 5
lado = Tamanho - 2 * margem
personagem = CriarPersonagemLabirinto(cores["Vermelho"],lado,lado, inicio[0] * Tamanho + margem, inicio[1] * Tamanho + margem) ####cria o personagem menor do que o caminho 



def mover(rect,dx,dy): #####função para mover
    rect.x += dx   ####quando o retângulo andar o X vai ser = a dx
    for p in paredes: #####laço para rodar tudo que tiver na lista paredes
        if rect.colliderect(p): ###serve pra ver se dois retângulos estão colidindo
            if dx > 0: ## se dx for maior que zero ou seja, estiver andando pra direita
                rect.right = p.left ##### quando colidir, a gente seta a direita do retângulo como a esquerda da parede
            if dx < 0: ## se dx for menor que zero, significa que ta andando pra esquerda
                rect.left = p.right # dai a esquerda do retangulo vira a esquerda da parede


    rect.y += dy ###################### a mesma coisa que rect.x só que serve pro eixo Y
    for p in paredes:
        if rect.colliderect(p):
            if dy > 0:
                rect.bottom = p.top
            if dy < 0:
                rect.top = p.bottom

















pygame.init()

fim_jogo = False

while fim_jogo == False:
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            fim_jogo = True            #ACABA O LOOP PRINCIPAL

    teclas = pygame.key.get_pressed() #####esse comando serve pra ver qual tecla esta sendo pressionada
    dx = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * Velocidade ## direção que ele vai andar vai * pela velocidade (Direção - outra direção pra caso ele apertar as duas, se anularem)
    dy = (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * Velocidade ## mesma coisa só que de cima pra baixo
    mover(personagem.rect,dx,dy) #chama a função de move

    tela.fill(cores["Preto"]) ###pinta o "fundo" da tela de preto
    for p in paredes: ###pinta as "paredes de azul claro"
        pygame.draw.rect(tela,cores["Azul Claro"], p)
    personagem.DesenharNaTela(tela) #desenhar o personagem na tela usando o método DesenharNaTela da função CriarPersonagemDoLabirinto

    pygame.display.flip() 
    Relogio.tick(Fps) #seta o fps do game 
pygame.quit() #### quando acabar o while, ele fecha o pygame