from graphics import *
#from pygame import *
from random import *
from time import *
from functions import *

sprites_pontos = []
sprites_pontos_2 = []  
for i in range (10):
    sprites_pontos.append(Image(Point(20, 20), f"sprites/{i}.png"))
    sprites_pontos_2.append(Image(Point(45, 20), f"sprites/{i}.png"))


largura = 244
altura  = 350
rodando = True
win = GraphWin("Flappy Bird", largura, altura, autoflush = False)
    
def desenhar():
    fundo = Image(Point(100, 100),"sprites/fundo.png")  
    Image.draw(fundo, win)
    base = Image(Point(150, 336), "sprites/chao.png")
    base.draw(win)
    mensagem = Image(Point(125, 150),"sprites/message.png")
    mensagem.draw(win)

    if win.getKey():
        base.undraw()
        mensagem.undraw()
        return True 

def criarCano():
    inicio = 265
    cano_y = randint(35, 160)
    cano_cima = Rectangle(Point(inicio, -5), Point(inicio + 46, cano_y))
    cano_baixo = Rectangle(Point(inicio, cano_y + 100), Point(inicio + 46, 355))

    sprite_cima = Image(Point(inicio + 23, cano_y - 159), "sprites/pipe-top.png")
    sprite_baixo = Image(Point(inicio + 23, 175 + cano_y + 100 - 15), "sprites/pipe-bottom.png")

    sprite_cima.draw(win)
    sprite_baixo.draw(win)

    return [sprite_cima, sprite_baixo, cano_cima, cano_baixo]

def main():
    hitbox_passaro = Circle(Point(125, 190), 15)
    passaro = Image(Point(125, 190), "sprites/yellowbird-midflap.png")
    passaro.draw(win)
    linha_chao = Line(Point(0, 281), Point(350, 281))
    linha_teto = Line(Point(0, -1), Point(350, -1))
    base = Image(Point(150, 336), "sprites/chao.png")

    gravidade = 1.75
    vel_y = 0
    vel_x = -3
    colisao_cano = False

    pontos = 0
    dezenas = 0
    scores = [0, 0]
    sprites_pontos[scores[0]].draw(win)

    canos = [criarCano()]
    base.draw(win)

    while True:
        vel_y += gravidade

        if win.checkKey():
            vel_y = -11
        
        for cano in canos:
            cano[0].move(vel_x, 0)
            cano[1].move(vel_x, 0)
            cano[2].move(vel_x, 0)
            cano[3].move(vel_x, 0)
        
        if canos[-1][2].getP2().getX() <= 130:
            canos.append(criarCano()) 
            base.undraw()
            base.draw(win)

        if canos[0][2].getP2().getX() < 0:
            canos[0][0].undraw()
            canos[0][1].undraw()
            canos.pop(0)
        
        if canos[0][2].getP2().getX() == 125:
            pontos += 1
            if dezenas == 0:
                scores[0] += 1
            
            if scores[0] > 9 or scores[1] > 9:
                sprites_pontos[scores[0] - 1].undraw()
                dezenas += 1
                scores[0] = dezenas
                scores[1] = 0

            if dezenas == 0:
                sprites_pontos[scores[0]].draw(win)
                sprites_pontos[scores[0] - 1].undraw()
            else:
                sprites_pontos[scores[0]].undraw()
                sprites_pontos[scores[0]].draw(win)

            if dezenas > 0:
                sprites_pontos_2[scores[1]].draw(win)
                sprites_pontos_2[scores[1] - 1].undraw()
                scores[1] += 1

        for cano in canos:
            if verify_colision_circle_rectangle2(hitbox_passaro, cano[2]) or verify_colision_circle_rectangle2(hitbox_passaro, cano[3]):
                colisao_cano = True

        if verify_colision_circle_line(hitbox_passaro, linha_chao) or verify_colision_circle_line(hitbox_passaro, linha_teto) or colisao_cano:
            break
            
        else:
            passaro.move(0, vel_y)
            hitbox_passaro.move(0, vel_y)
        update(24)
    
    passaro.undraw()
    passaro = Image(Point(125, hitbox_passaro.getCenter().getY()) , "sprites/dead.png")
    passaro.draw(win)
    msg_morte = Image(Point(125, 125), "sprites/gameover.png")
    msg_morte.draw(win)
    """restart = Image(Point(125, 180), "sprites/restart.png")
    restart.draw(win)"""
    pontuacao_sombra = Text(Point(125, 165),f"você fez {pontos} pontos!")
    pontuacao_sombra.setFace("courier")
    pontuacao_sombra.setSize(15)
    pontuacao_sombra.setTextColor("black")
    pontuacao_sombra.setStyle("bold")
    pontuacao_sombra.draw(win)

    pontuacao = Text(Point(123, 163),f"você fez {pontos} pontos!")
    pontuacao.setFace("courier")
    pontuacao.setSize(15)
    pontuacao.setTextColor("white")
    pontuacao.setStyle("bold")
    pontuacao.draw(win)

    sprites_pontos[scores[0]].undraw()
    sprites_pontos_2[scores[0]].undraw()

    win.getKey()
    win.clear()
    
while True:
    desenhar()
    main()

#testmain
