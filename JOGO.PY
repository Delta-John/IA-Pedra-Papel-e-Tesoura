import time
import random
from sklearn.tree import DecisionTreeClassifier

# ============================================================
#  Pedra, Papel e Tesoura com IA
#  Utiliza Decision Tree para prever padrões cognitivos humanos.
# ============================================================

NOMES = ["Pedra", "Papel", "Tesoura"]
ICON_JOGADOR = ["✊ Pedra", "✋ Papel", "✌️  Tesoura"]
ICON_IA = ["✊", "✋", "✌️"]

# Histórico para treinamento online da IA
# Features: [ultima_jogada_humano, ultima_jogada_ia, ultimo_resultado]
X = []
y = []

modelo = DecisionTreeClassifier(max_depth=4)

# Métricas de partida
vitorias_ia = 0
vitorias_humano = 0
empates = 0
streak_ia = 0
maior_streak = 0

ultima_jogador = None
ultima_ia = None
ultimo_resultado = None

def exibir_cabecalho():
    print("\n" + "=" * 62)
    print("   [0] ✊ Pedra   |   [1] ✋ Papel   |   [2] ✌️  Tesoura")
    print("   [9] Encerrar e ver relatório final")
    print("=" * 62)

def exibir_placar():
    total = vitorias_ia + vitorias_humano + empates
    taxa_ia = (vitorias_ia / total * 100) if total > 0 else 0.0
    
    c1 = f"  IA: {vitorias_ia}".ljust(15)
    c2 = f"Humano: {vitorias_humano}".ljust(15)
    c3 = f"Empates: {empates}".ljust(15)
    c4 = f"Rodadas: {total}".ljust(15)
    linha1 = f"{c1}{c2}{c3}{c4}"
    
    linha2 = f"  Taxa da IA: {taxa_ia:.1f}%".ljust(60)
    
    print("\n┌" + "─" * 60 + "┐")
    print(f"│{linha1}│")
    print("├" + "─" * 60 + "┤")
    print(f"│{linha2}│")
    print("└" + "─" * 60 + "┘")

exibir_cabecalho()

while True:
    try:
        entrada = input("\nSua escolha [0=Pedra, 1=Papel, 2=Tesoura, 9=Sair]: ").strip()
        if not entrada:
            continue
        jogador = int(entrada)
    except ValueError:
        print("Comando inválido! Digite 0, 1, 2 ou 9.")
        continue

    if jogador == 9:
        break

    if jogador not in [0, 1, 2]:
        print("Opção inválida! Escolha 0, 1 ou 2.")
        continue

    # --- NÚCLEO DE PREVISÃO DA IA ---
    tempo_ms = round(random.uniform(0.7, 1.9), 2)
    print(f"[Telemetria Neural] Analisando micro-padrões em {tempo_ms}ms...")
    time.sleep(0.3)

    # Se já temos histórico e variância nas jogadas
    if len(X) >= 4 and len(set(y)) > 1:
        entrada_atual = [[ultima_jogador, ultima_ia, ultimo_resultado]]
        previsao = modelo.predict(entrada_atual)[0]
        # Contra-jogada perfeita: pedra(0)->papel(1), papel(1)->tesoura(2), tesoura(2)->pedra(0)
        ia = (previsao + 1) % 3
        status_ia = f"Previu seu lance ({NOMES[previsao]})"
    elif len(y) >= 3 and len(set(y)) == 1:
        # Detecção de repetição contínua humana
        previsao = y[-1]
        ia = (previsao + 1) % 3
        status_ia = f"Detectou repetição ({NOMES[previsao]})"
    else:
        # Fase de calibração inicial
        ia = random.randint(0, 2)
        status_ia = "Fase de calibração / Leitura de dados"

    # --- CONFRONTO VISUAL ---
    print("\n─── RESULTADO ───")
    print(f"Você: {ICON_JOGADOR[jogador]}")
    print(f"IA:   {ICON_IA[ia]} ({NOMES[ia]})")
    print(f"Diagnóstico: {status_ia}")

    # --- RESULTADO DA RODADA ---
    # 1: Humano venceu | 0: Empate | -1: IA venceu
    if jogador == ia:
        print("\nEMPATE! As duas mentes convergiram.")
        empates += 1
        streak_ia = 0
        resultado_rodada = 0
    elif (jogador - ia) % 3 == 1:
        print("\nVOCÊ VENCEU! Você conseguiu quebrar o padrão algorítmico!")
        vitorias_humano += 1
        streak_ia = 0
        resultado_rodada = 1
    else:
        print("\nPONTO DA IA! Padrão antecipado com sucesso!")
        vitorias_ia += 1
        streak_ia += 1
        if streak_ia > maior_streak:
            maior_streak = streak_ia
        resultado_rodada = -1

    # --- APRENDIZADO ONLINE (FIT EM TEMPO REAL) ---
    if ultima_jogador is not None:
        X.append([ultima_jogador, ultima_ia, ultimo_resultado])
        y.append(jogador)

        if len(set(y)) > 1:
            modelo.fit(X, y)

    ultima_jogador = jogador
    ultima_ia = ia
    ultimo_resultado = resultado_rodada

    exibir_placar()

# --- RELATÓRIO FINAL AO SAIR ---
total_partidas = vitorias_ia + vitorias_humano + empates
print("\n" + "=" * 62)
print("               RELATÓRIO FINAL DA SESSÃO")
print("=" * 62)
if total_partidas > 0:
    taxa_final = (vitorias_ia / total_partidas) * 100
    print(f" Total de Rodadas Disputadas: {total_partidas}")
    print(f" Vitórias da IA:              {vitorias_ia} ({taxa_final:.1f}%)")
    print(f" Suas Vitórias:               {vitorias_humano} ({(vitorias_humano/total_partidas)*100:.1f}%)")
    print(f" Empates:                     {empates}")
    print(f" Maior Sequência da IA:       {maior_streak} vitórias consecutivas")
    print("-" * 62)
    if taxa_final >= 60:
        print(" Conclusão: A IA dominou a partida antecipando seus padrões!")
    else:
        print(" Conclusão: Você conseguiu ser imprevisível.")
else:
    print(" Nenhuma rodada foi jogada.")
print("=" * 62 + "\n")
