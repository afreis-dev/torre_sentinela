import os

def torre_sentinela():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        coordenada_valida = lambda coluna, linha: 0 <= coluna < 8 and 0 <= linha < 8
        posicao_para_coordenada = lambda posicao: (ord(posicao[0]) - 97, int(posicao[1]) - 1)
        coordenada_para_posicao = lambda coluna, linha: chr(coluna + 97) + str(linha + 1)

        def ler_posicao(mensagem):
            while True:
                entrada_usuario = input(mensagem).strip().lower()
                if len(entrada_usuario) == 2 and 'a' <= entrada_usuario[0] <= 'h' and '1' <= entrada_usuario[1] <= '8':
                    return posicao_para_coordenada(entrada_usuario)
                entrada_normalizada = entrada_usuario.replace(',', ' ').split()
                if len(entrada_normalizada) == 2 and all(valor.isdigit() for valor in entrada_normalizada):
                    coluna, linha = int(entrada_normalizada[0]) - 1, int(entrada_normalizada[1]) - 1
                    if coordenada_valida(coluna, linha):
                        return (coluna, linha)
                print(">> posição inválida. Use d5 ou '4 5'.")

        print()
        coluna_torre, linha_torre = ler_posicao("Posição da torre (ex.: d5 ou '4 5'): ")
        while True:
            quantidade_inimigos = input("Quantas peças inimigas? (0..63): ").strip()
            if quantidade_inimigos.isdigit() and 0 <= int(quantidade_inimigos) <= 63:
                quantidade_inimigos = int(quantidade_inimigos)
                break
            print(">> número inválido.")

        posicoes_ocupadas, posicoes_inimigas = {(coluna_torre, linha_torre)}, []
        for indice_peca in range(1, quantidade_inimigos + 1):
            while True:
                coluna_inimiga, linha_inimiga = ler_posicao(f"Peça #{indice_peca}: ")
                if (coluna_inimiga, linha_inimiga) in posicoes_ocupadas:
                    print(">> já ocupada.")
                else:
                    posicoes_ocupadas.add((coluna_inimiga, linha_inimiga))
                    posicoes_inimigas.append((coluna_inimiga, linha_inimiga))
                    break

        direcoes_torre = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        posicoes_inimigas_set = set(posicoes_inimigas)
        posicoes_capturaveis = []
        for delta_coluna, delta_linha in direcoes_torre:
            coluna_atual, linha_atual = coluna_torre, linha_torre
            while True:
                coluna_atual += delta_coluna
                linha_atual += delta_linha
                if not coordenada_valida(coluna_atual, linha_atual):
                    break
                if (coluna_atual, linha_atual) in posicoes_inimigas_set:
                    posicoes_capturaveis.append((coluna_atual, linha_atual))
                    break

        modo_decorativo = True
        largura_celula = 2
        separador_celula = " "

        if modo_decorativo:
            celula_clara, celula_escura = "░░", "▓▓"
            simbolo_torre, simbolo_captura, simbolo_inimigo = "♜", "×", "●"
        else:
            celula_clara, celula_escura = "..", "::"
            simbolo_torre, simbolo_captura, simbolo_inimigo = "T", "x", "o"

        formatar_celula = lambda texto: (texto + " " * largura_celula)[:largura_celula]

        tabuleiro = [[None] * 8 for _ in range(8)]
        for linha in range(8):
            for coluna in range(8):
                tabuleiro[7 - linha][coluna] = formatar_celula(
                    celula_clara if (coluna + linha) % 2 == 0 else celula_escura
                )

        for coluna_inimiga, linha_inimiga in posicoes_inimigas:
            tabuleiro[7 - linha_inimiga][coluna_inimiga] = formatar_celula(simbolo_inimigo)
        for coluna_captura, linha_captura in posicoes_capturaveis:
            tabuleiro[7 - linha_captura][coluna_captura] = formatar_celula(simbolo_captura)
        tabuleiro[7 - linha_torre][coluna_torre] = formatar_celula(simbolo_torre)

        print()
        for indice_linha in range(8):
            linha_formatada = separador_celula.join(tabuleiro[indice_linha])
            print(f"{8 - indice_linha:>2}  {linha_formatada}")

        cabecalho_colunas = separador_celula.join(
            f"{chr(97 + coluna):^{largura_celula}}" for coluna in range(8)
        )
        print("    " + cabecalho_colunas)
        print(f"   {simbolo_torre} torre   {simbolo_captura} capturável   {simbolo_inimigo} inimiga\n")

        posicoes_capturaveis.sort(key=lambda coordenada: (coordenada[0], coordenada[1]))
        posicoes_captura_texto = [coordenada_para_posicao(coluna, linha) for coluna, linha in posicoes_capturaveis]
        quantidade_capturas = len(posicoes_captura_texto)

        if quantidade_capturas == 0:
            print("0\nNenhuma peça pode ser capturada desta vez. ")
        else:
            print(quantidade_capturas)
            print(" ".join(posicoes_captura_texto))
            sufixo_peca = "peça" if quantidade_capturas == 1 else "peças"
            print(f"\n♜ A torre consegue capturar {quantidade_capturas} {sufixo_peca} nesta jogada! ")

        if input("\nOutra rodada? (s/n): ").strip().lower() != 's':
            print("\nQue mazela...")
            break

torre_sentinela()
