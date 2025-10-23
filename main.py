import os
def torre_sentinela():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        ok  = lambda c,l: 0 <= c < 8 and 0 <= l < 8
        p2c = lambda s: (ord(s[0]) - 97, int(s[1]) - 1)
        c2p = lambda c,l: chr(c + 97) + str(l + 1)

        def ler_pos(msg):
            while True:
                s = input(msg).strip().lower()
                if len(s) == 2 and 'a' <= s[0] <= 'h' and '1' <= s[1] <= '8':
                    return p2c(s)
                t = s.replace(',', ' ').split()
                if len(t) == 2 and all(x.isdigit() for x in t):
                    c, l = int(t[0]) - 1, int(t[1]) - 1
                    if ok(c, l): return (c, l)
                print(">> posição inválida. Use d5 ou '4 5'.")

        print()
        col_t, lin_t = ler_pos("Posição da torre (ex.: d5 ou '4 5'): ")
        while True:
            n = input("Quantas peças inimigas? (0..63): ").strip()
            if n.isdigit() and 0 <= int(n) <= 63:
                n = int(n); break
            print(">> número inválido.")

        usados, pecas = {(col_t, lin_t)}, []
        for i in range(1, n + 1):
            while True:
                c, l = ler_pos(f"Peça #{i}: ")
                if (c, l) in usados:
                    print(">> já ocupada.")
                else:
                    usados.add((c, l)); pecas.append((c, l)); break

        dirs = [(0,1),(0,-1),(-1,0),(1,0)]
        s = set(pecas); capt = []
        for dx, dy in dirs:
            x, y = col_t, lin_t
            while True:
                x += dx; y += dy
                if not ok(x, y): break
                if (x, y) in s: capt.append((x, y)); break

        FANCY = True
        CELL_W = 2
        SEP = " "

        if FANCY:
            bg_light, bg_dark = "░░", "▓▓"
            sym_t, sym_x, sym_i = "♜", "×", "●"
        else:
            bg_light, bg_dark = "..", "::"
            sym_t, sym_x, sym_i = "T", "x", "o"

        fix = lambda s: (s + " " * CELL_W)[:CELL_W]

        B = [[None]*8 for _ in range(8)]
        for l in range(8):
            for c in range(8):
                B[7-l][c] = fix(bg_light if (c + l) % 2 == 0 else bg_dark)

        for c, l in pecas: B[7-l][c] = fix(sym_i)
        for c, l in capt:  B[7-l][c] = fix(sym_x)
        B[7-lin_t][col_t] = fix(sym_t)

        print()
        for r in range(8):
            linha = SEP.join(B[r])
            print(f"{8 - r:>2}  {linha}")

        header = SEP.join(f"{chr(97+c):^{CELL_W}}" for c in range(8))
        print("    " + header)
        print(f"   {sym_t} torre   {sym_x} capturável   {sym_i} inimiga\n")

        capt.sort(key=lambda z: (z[0], z[1]))
        out = [c2p(c, l) for c, l in capt]
        k = len(out)

        if k == 0:
            print("0\nNenhuma peça pode ser capturada desta vez. ")
        else:
            print(k)
            print(" ".join(out))
            msg = "peça" if k == 1 else "peças"
            print(f"\n♜ A torre consegue capturar {k} {msg} nesta jogada! ")

        if input("\nOutra rodada? (s/n): ").strip().lower() != 's':
            print("\nEncerrando...")
            break

torre_sentinela()