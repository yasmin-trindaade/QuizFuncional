import pygame
import json

# Inicialização
pygame.init()
tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Quiz Educacional")
clock = pygame.time.Clock()

# Configurações iniciais
font = pygame.font.Font(None, 36)
nome_jogador = ""
pontos = 0
fase_atual = 1  # A fase inicial agora começa em 1

# Perguntas do quiz (30 perguntas divididas em 3 fases)
perguntas_fases = {
    1: [
        {"pergunta": "Qual é a capital do Brasil?", "opcoes": ["Brasília", "Rio", "SP", "BH"], "correta": "Brasília"},
        {"pergunta": "2 + 2 é igual a?", "opcoes": ["4", "22", "5", "3"], "correta": "4"},
        {"pergunta": "Quem descobriu o Brasil?", "opcoes": ["Cabral", "Colombo", "Napoleão", "Nero"], "correta": "Cabral"},
        {"pergunta": "Qual é a capital da França?", "opcoes": ["Paris", "Londres", "Berlim", "Madrid"], "correta": "Paris"},
        {"pergunta": "Qual é o maior continente?","opcoes": ["África", "América", "Ásia", "Europa"], "correta": "Ásia"},
        {"pergunta": "Quantos estados tem o Brasil?", "opcoes": ["25", "27", "30", "32"], "correta": "27"}
    ],
    2: [
        {"pergunta": "Qual é o maior planeta do sistema solar?", "opcoes": ["Marte", "Terra", "Júpiter", "Saturno"], "correta": "Júpiter"},
        {"pergunta": "Qual é o elemento químico do símbolo H2O?", "opcoes": ["Oxigênio", "Água", "Hidrogênio", "Helio"], "correta": "Água"},
        {"pergunta": "Quem pintou a Mona Lisa?", "opcoes": ["Van Gogh", "Da Vinci", "Picasso", "Michelangelo"], "correta": "Da Vinci"},
        {"pergunta": "Em que ano o Brasil se tornou independente?", "opcoes": ["1800", "1822", "1850", "1900"],"correta": "1822"},
        {"pergunta": "Quem inventou a lâmpada elétrica?", "opcoes": ["Nikola Tesla", "Thomas Edison", "Albert Einstein", "Galileu Galilei"], "correta": "Thomas Edison"},
        {"pergunta": "Qual é o maior deserto do mundo?", "opcoes": ["Sahara", "Gobi", "Antártico", "Kalahari"], "correta": "Antártico"}

    ],
    3: [
        {"pergunta": "Qual é o maior oceano do mundo?", "opcoes": ["Atlântico", "Pacífico", "Índico", "Ártico"], "correta": "Pacífico"},
        {"pergunta": "Quem escreveu 'Dom Quixote'?", "opcoes": ["Shakespeare", "Cervantes", "Hemingway", "Dickens"], "correta": "Cervantes"},
        {"pergunta": "Qual é o maior animal terrestre?", "opcoes": ["Elefante", "Girafa", "Hipopótamo", "Baleia"], "correta": "Elefante"},
        {"pergunta": "Quem foi o primeiro homem a pisar na Lua?", "opcoes": ["Yuri Gagarin", "Neil Armstrong", "Buzz Aldrin", "John Glenn"], "correta": "Neil Armstrong"},
        {"pergunta": "Em que ano ocorreu a Revolução Francesa?", "opcoes": ["1789", "1799", "1600", "1812"], "correta": "1789"},
        {"pergunta": "Qual é a fórmula química da glicose?", "opcoes": ["C6H12O6", "CO2", "H2O", "NaCl"], "correta": "C6H12O6"}

    ]
}

# Função para exibir texto
def exibir_texto(texto, x, y, cor=(255, 255, 255)):
    render = font.render(texto, True, cor)
    tela.blit(render, (x, y))

# Função para salvar o ranking em um arquivo
def salvar_ranking(nome, pontuacao):
    try:
        with open("ranking.json", "r") as arquivo:
            ranking = json.load(arquivo)
    except FileNotFoundError:
        ranking = []
    
    ranking.append({"nome": nome, "pontos": pontuacao})
    ranking = sorted(ranking, key=lambda x: x["pontos"], reverse=True)[:5]  # Top 5
    with open("ranking.json", "w") as arquivo:
        json.dump(ranking, arquivo)

# Função para exibir o ranking
def exibir_ranking():
    try:
        with open("ranking.json", "r") as arquivo:
            ranking = json.load(arquivo)
    except FileNotFoundError:
        ranking = []

    tela.fill((0, 0, 0))
    exibir_texto("Ranking - Top 5 Jogadores", 250, 50, (255, 255, 0))
    for i, entrada in enumerate(ranking):
        texto = f"{i+1}. {entrada['nome']} - {entrada['pontos']} pontos"
        exibir_texto(texto, 200, 120 + i * 40)
    pygame.display.flip()
    pygame.time.wait(5000)

# Função para pedir o nome do jogador
def pedir_nome():
    global nome_jogador
    input_box = pygame.Rect(300, 250, 200, 50)
    texto_input = ''
    active = False
    font = pygame.font.Font(None, 36)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return texto_input
                    elif event.key == pygame.K_BACKSPACE:
                        texto_input = texto_input[:-1]
                    else:
                        texto_input += event.unicode
        
        tela.fill((0, 0, 0))
        txt_surface = font.render(texto_input, True, (255, 255, 255))
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        tela.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(tela, (255, 255, 255), input_box, 2)
        exibir_texto("Digite seu nome:", 270, 200)
        pygame.display.flip()
        clock.tick(30)

# Função para mostrar fase atual e perguntas
def jogar(fase_atual, pergunta_atual):
    global pontos
    tela.fill((0, 0, 0))  # Limpar tela

    # Exibir a fase
    exibir_texto(f"Fase {fase_atual}", 350, 20, (255, 255, 0))

    # Exibe a pergunta
    exibir_texto(pergunta_atual["pergunta"], 100, 100)

    botoes = []
    mouse_pos = pygame.mouse.get_pos()

    # Exibe as opções com botões
    for i, opcao in enumerate(pergunta_atual["opcoes"]):
        botao = pygame.Rect(100, 200 + i * 60, 600, 40)
        botoes.append(botao)
        pygame.draw.rect(tela, (100, 100, 255), botao)
        exibir_texto(opcao, 120, 210 + i * 60)

    pygame.display.flip()

    return botoes

# Função para processar respostas e avançar as fases
def processar_resposta(resposta, fase_atual, pergunta_atual):
    global pontos
    resposta_correta = pergunta_atual["correta"]

    if resposta.lower() == resposta_correta.lower():
        pontos += 1

    return pontos

# Loop principal do jogo
def main():
    global fase_atual, pontos, nome_jogador

    nome_jogador = pedir_nome()

    while fase_atual <= 3:  # Alterado para 3 fases
        perguntas = perguntas_fases[fase_atual]

        for idx, pergunta_atual in enumerate(perguntas):
            botoes = jogar(fase_atual, pergunta_atual)  # Exibe uma pergunta por vez
            
            resposta = None
            rodando = True
            while rodando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for i, botao in enumerate(botoes):
                            if botao.collidepoint(pygame.mouse.get_pos()):
                                resposta = pergunta_atual["opcoes"][i]
                                rodando = False

            # Processa a resposta do jogador
            pontos = processar_resposta(resposta, fase_atual, pergunta_atual)

        fase_atual += 1

    salvar_ranking(nome_jogador, pontos)
    print(f"Você acertou {pontos} de {len(perguntas_fases[3]) * 3} perguntas!")  # Ajuste no cálculo da pontuação total
    exibir_ranking()

# Iniciar o jogo
if __name__ == "__main__":
    main()
    pygame.quit()
