import pygame
from constantes import cores, Tamanho, Fps, Velocidade, Margem, MAPA, SAIDA, PORTAIS, INICIO_HUB
from classes import CriarPersonagemLabirinto


pygame.init()
LARGURA, ALTURA = len(MAPA[0]) * Tamanho, len(MAPA) * Tamanho  # tela do tamanho do mapa
tela = pygame.display.set_mode((LARGURA, ALTURA)) #
pygame.display.set_caption("TimeStreaks") #Bota o nome na janela do jogo
relogio = pygame.time.Clock() #fps depois
fonte = pygame.font.SysFont("arial", 28, bold=True)
fonte_titulo = pygame.font.SysFont("arial", 80, bold=True)


#labirinto
paredes = []    #3 essa lista aqui vai servir pra guardar as paredes do labirinto
inicio = (1, 1)
for y, linha in enumerate(MAPA): ##### o enumerate vai me devolver qual linha e oq tem nessa linha
    for x, letra in enumerate(linha):##### mesma coisa só que agora pra coluna
        if letra == "#":#se o item da coluna  "letra" for igual a "#" ele entra no iff
            paredes.append(pygame.Rect(x * Tamanho, y* Tamanho, Tamanho, Tamanho)) ### e adiciona em paredes um retangulo no pixel, e o tamanho do retângulo
        elif letra == "P": ######### aqui o "P" serve pra indicar onde o personagem vai começar
            inicio = (x,y) #variável que seta o começo do personagem

saida = pygame.Rect(SAIDA[0] * Tamanho, SAIDA[1] * Tamanho, Tamanho, Tamanho)
portais = []
for nome, x, y, liberado in PORTAIS:
    area = pygame.Rect(x * Tamanho, y * Tamanho, Tamanho, Tamanho)
    portais.append((nome, area, liberado))

lado = Tamanho - 2 * Margem
personagem = CriarPersonagemLabirinto(cores["Vermelho"], lado, lado, 0, 0)


def posicionar(casa):
    personagem.rect.topleft = (casa[0] * Tamanho + Margem, casa[1] * Tamanho + Margem)



def mover(rect,dx,dy, obstaculos): #####função para mover
    rect.x += dx   ####quando o retângulo andar o X vai ser = a dx
    for p in obstaculos: #####laço para rodar tudo que tiver na lista paredes
        if rect.colliderect(p): ###serve pra ver se dois retângulos estão colidindo
            if dx > 0: ## se dx for maior que zero ou seja, estiver andando pra direita
                rect.right = p.left ##### quando colidir, a gente seta a direita do retângulo como a esquerda da parede
            if dx < 0: ## se dx for menor que zero, significa que ta andando pra esquerda
                rect.left = p.right # dai a esquerda do retangulo vira a esquerda da parede


    rect.y += dy ###################### a mesma coisa que rect.x só que serve pro eixo Y
    for p in obstaculos:
        if rect.colliderect(p):
            if dy > 0:
                rect.bottom = p.top
            if dy < 0:
                rect.top = p.bottom

    rect.clamp_ip(tela.get_rect())  # não deixa sair da tela


def escrever(texto, fonte_usada, cor, centro):
    imagem = fonte_usada.render(texto, True, cor)
    tela.blit(imagem, imagem.get_rect(center=centro))


#principal
OPCOES = ["Jogar", "Sair"]
opcao = 0
estado = "menu"  # "menu", "hub" ou "labirinto"
rodando = True

while rodando:
    # 1 Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False #ACABA O LOOP PRINCIPAL
        elif evento.type == pygame.KEYDOWN:
            if estado == "menu":
                if evento.key in (pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s):
                    opcao = 1 - opcao
                elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if OPCOES[opcao] == "Jogar":
                        estado = "hub"
                        posicionar(INICIO_HUB)
                    else:
                        rodando = False #ACABA O LOOP PRINCIPAL
            elif evento.key == pygame.K_ESCAPE:
                if estado == "labirinto":
                    estado = "hub"
                    posicionar(INICIO_HUB)
                else:
                    estado = "menu"

    # 2 Movimento (setas ou WASD)
    if estado != "menu":
        teclas = pygame.key.get_pressed() #####esse comando serve pra ver qual tecla esta sendo pressionada
        dx = ((teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - (teclas[pygame.K_LEFT] or teclas[pygame.K_a])) * Velocidade ## direção que ele vai andar vai * pela velocidade (Direção - outra direção pra caso ele apertar as duas, se anularem)
        dy = ((teclas[pygame.K_DOWN] or teclas[pygame.K_s]) - (teclas[pygame.K_UP] or teclas[pygame.K_w])) * Velocidade ## mesma coisa só que de cima pra baixo

        if estado == "hub":
            bloqueados = [area for nome, area, liberado in portais if not liberado]
            mover(personagem.rect, dx, dy, bloqueados)
            for nome, area, liberado in portais:
                if liberado and area.collidepoint(personagem.rect.center):
                    estado = "labirinto"
                    posicionar(inicio)
        else:
            mover(personagem.rect, dx, dy, paredes) #chama a função de move
            if saida.collidepoint(personagem.rect.center):
                estado = "hub"
                posicionar(INICIO_HUB)

    # 3 Desenhos das areas
    tela.fill(cores["Preto"])###pinta o "fundo" da tela de preto

    if estado == "menu": 
        escrever("TimeStreaks", fonte_titulo, cores["Branco"], (LARGURA // 2, 180))
        for i, texto in enumerate(OPCOES):
            cor = cores["Amarelo"] if i == opcao else cores["Branco"]
            escrever(texto, fonte, cor, (LARGURA // 2, 320 + i * 60))
    else:
        if estado == "hub":
            for nome, area, liberado in portais:
                cor = cores["Dourado"] if liberado else cores["Cinza"]
                pygame.draw.rect(tela, cor, area)
                escrever(nome, fonte, cor, (area.centerx, area.top - 25))
        else:
            for parede in paredes:
                pygame.draw.rect(tela, cores["Azul Claro"], parede) ###pinta as "paredes de azul claro"
            pygame.draw.rect(tela, cores["Verde"], saida)
        personagem.DesenharNaTela(tela) #desenhar o personagem na tela usando o método DesenharNaTela da função CriarPersonagemDoLabirinto

    pygame.display.flip()
    relogio.tick(Fps) #seta o fps do game 
pygame.quit() #### quando acabar o while, ele fecha o pygame
