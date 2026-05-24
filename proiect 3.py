"""
Proiect 3 - Algoritm Genetic
Alegerea unei echipe de proiect cu buget limitat

Problema: Selectam o echipa cu scor total maxim, fara a depasi bugetul.
Reprezentare: cromozom binar (1 = candidat selectat, 0 = candidat neales)
"""

import random
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------------
# 1. Definirea problemei - candidati si buget
# ------------------------------------------------------------------

# Fiecare candidat: nume, cost, scor_competenta
CANDIDATI = [
    {"id":  0, "nume": "Alice",    "cost": 50, "scor": 90},
    {"id":  1, "nume": "Bob",      "cost": 40, "scor": 70},
    {"id":  2, "nume": "Carol",    "cost": 60, "scor": 95},
    {"id":  3, "nume": "Dan",      "cost": 30, "scor": 55},
    {"id":  4, "nume": "Elena",    "cost": 70, "scor": 85},
    {"id":  5, "nume": "Florin",   "cost": 25, "scor": 60},
    {"id":  6, "nume": "Gabi",     "cost": 80, "scor": 100},
    {"id":  7, "nume": "Horia",    "cost": 45, "scor": 75},
    {"id":  8, "nume": "Ioana",    "cost": 35, "scor": 65},
    {"id":  9, "nume": "Mihai",    "cost": 55, "scor": 88},
    {"id": 10, "nume": "Nicoleta", "cost": 20, "scor": 45},
    {"id": 11, "nume": "Octavia",  "cost": 65, "scor": 92},
]

BUGET_MAX = 200
N_GENE = len(CANDIDATI)  # lungimea cromozomului = numarul de candidati

print("=" * 60)
print("PROIECT 3 - ALGORITM GENETIC: Selectie echipa optima")
print("=" * 60)
print(f"\nBuget maxim: {BUGET_MAX} unitati")
print(f"\n{'ID':>3} | {'Nume':>10} | {'Cost':>5} | {'Scor':>5}")
print("-" * 35)
for c in CANDIDATI:
    print(f"{c['id']:>3} | {c['nume']:>10} | {c['cost']:>5} | {c['scor']:>5}")

# ------------------------------------------------------------------
# 2. Reprezentarea unei solutii - cromozom binar
# ------------------------------------------------------------------
# Exemplu: [1,0,1,0,0,1,0,1,0,0,0,1]
# => selectati: Alice(0), Carol(2), Florin(5), Horia(7), Octavia(11)
# Gena = 1 => candidatul este ales
# Gena = 0 => candidatul nu este ales

def decodifica_cromozom(cromozom):
    """Returneaza lista candidatilor selectati (gena = 1)."""
    return [CANDIDATI[i] for i, gena in enumerate(cromozom) if gena == 1]

# ------------------------------------------------------------------
# 3. Functia de fitness
# ------------------------------------------------------------------

def calculeaza_fitness(cromozom):
    """
    Evalueaza un cromozom.

    Daca bugetul este depasit => fitness = 0 (penalizare totala).
    Altfel => fitness = scorul total al echipei.

    Penalizarea prin excludere completa (fitness=0) este simpla si
    eficienta: forteaza algoritmul sa evite solutiile invalide.
    """
    echipa = decodifica_cromozom(cromozom)
    cost_total = sum(c["cost"] for c in echipa)
    scor_total = sum(c["scor"] for c in echipa)

    if cost_total > BUGET_MAX:
        return 0  # solutie invalida - penalizare totala
    return scor_total

# ------------------------------------------------------------------
# 4. Populatia initiala
# ------------------------------------------------------------------

def genereaza_populatie(marime):
    """
    Genereaza 'marime' cromozomi aleatori.

    Diversitatea initiala este importanta: daca toti cromozomii sunt
    identici, algoritmul nu poate evolua (nu exista variatie de explorat).
    """
    return [[random.randint(0, 1) for _ in range(N_GENE)]
            for _ in range(marime)]

# ------------------------------------------------------------------
# 5. Operatorii genetici
# ------------------------------------------------------------------

def selectie_turneu(populatie, fitness_vals, k=3):
    """
    Selectie prin turneu: alegem k indivizi la intamplare si il returnam
    pe cel cu fitness-ul cel mai mare.

    Rol: favorizeaza indivizii buni, dar pastreaza diversitatea
    (indivizii slabi au o sansa mica, dar nu zero).
    """
    concurenti_idx = random.sample(range(len(populatie)), k)
    castigator_idx = max(concurenti_idx, key=lambda i: fitness_vals[i])
    return populatie[castigator_idx][:]

def crossover_un_punct(parinte1, parinte2):
    """
    Crossover cu un punct: alegem un punct de taiere aleatoriu si
    combinam cele doua jumatati.

    Rol: combina caracteristici ale ambilor parinti, explorand
    noi regiuni ale spatiului de solutii.
    """
    punct = random.randint(1, N_GENE - 1)
    copil1 = parinte1[:punct] + parinte2[punct:]
    copil2 = parinte2[:punct] + parinte1[punct:]
    return copil1, copil2

def mutatie(cromozom, rata_mutatie=0.05):
    """
    Mutatie bit-flip: fiecare gena are o probabilitate rata_mutatie
    de a fi schimbata (0->1 sau 1->0).

    Rol: introduce diversitate, ajuta algoritmul sa evite
    blocarea intr-un optim local.
    """
    return [1 - gena if random.random() < rata_mutatie else gena
            for gena in cromozom]

# ------------------------------------------------------------------
# 6. Rularea algoritmului genetic pe mai multe generatii
# ------------------------------------------------------------------

def algoritm_genetic(marime_pop=50, num_generatii=100,
                     rata_mutatie=0.05, rata_crossover=0.8):
    """
    Ruleaza algoritmul genetic si returneaza evolutia fitness-ului.

    Parametri:
        marime_pop      - numarul de cromozomi in populatie
        num_generatii   - cate generatii evoluam
        rata_mutatie    - probabilitatea mutatiei per gena
        rata_crossover  - probabilitatea aplicarii crossover-ului

    Returneaza:
        (cel_mai_bun_cromozom, istoric_best_fitness, istoric_avg_fitness)
    """
    populatie = genereaza_populatie(marime_pop)
    historic_best = []
    historic_avg  = []

    for _ in range(num_generatii):
        fitness_vals = [calculeaza_fitness(c) for c in populatie]

        # Elitism: pastram cel mai bun individ nemodificat
        idx_best = int(np.argmax(fitness_vals))
        elit = populatie[idx_best][:]

        historic_best.append(fitness_vals[idx_best])
        historic_avg.append(float(np.mean(fitness_vals)))

        # Construim noua generatie
        noua_populatie = [elit]
        while len(noua_populatie) < marime_pop:
            p1 = selectie_turneu(populatie, fitness_vals)
            p2 = selectie_turneu(populatie, fitness_vals)

            if random.random() < rata_crossover:
                c1, c2 = crossover_un_punct(p1, p2)
            else:
                c1, c2 = p1[:], p2[:]

            noua_populatie.append(mutatie(c1, rata_mutatie))
            if len(noua_populatie) < marime_pop:
                noua_populatie.append(mutatie(c2, rata_mutatie))

        populatie = noua_populatie

    # Evaluare finala
    fitness_final = [calculeaza_fitness(c) for c in populatie]
    idx_best_final = int(np.argmax(fitness_final))
    return populatie[idx_best_final], historic_best, historic_avg


# Rulare principala
print("\nRulam algoritmul genetic (50 indivizi, 150 generatii)...")
cromozom_final, best_hist, avg_hist = algoritm_genetic(
    marime_pop=50, num_generatii=150, rata_mutatie=0.05
)

echipa_finala = decodifica_cromozom(cromozom_final)
cost_final    = sum(c["cost"] for c in echipa_finala)
scor_final    = sum(c["scor"] for c in echipa_finala)

print(f"\nCea mai buna echipa gasita:")
for c in echipa_finala:
    print(f"  - {c['nume']:10} (cost={c['cost']}, scor={c['scor']})")
print(f"\nCost total:  {cost_final} / {BUGET_MAX}  "
      f"{'OK - in buget' if cost_final <= BUGET_MAX else 'DEPASIT'}")
print(f"Scor total:  {scor_final}")
print(f"Best fitness initial: {best_hist[0]}  ->  final: {best_hist[-1]}")

# ------------------------------------------------------------------
# 7. Grafice cu matplotlib.pyplot
# ------------------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Algoritm Genetic - Selectia echipei cu buget limitat",
             fontsize=14, fontweight="bold")

generatii = range(1, len(best_hist) + 1)

# Grafic 1: Best fitness vs Avg fitness pe generatii
ax1 = axes[0]
ax1.plot(generatii, best_hist, color="#EF5350", linewidth=2,
         label="Cel mai bun fitness")
ax1.plot(generatii, avg_hist, color="#42A5F5", linewidth=1.5,
         linestyle="--", alpha=0.8, label="Fitness mediu")
ax1.fill_between(generatii, avg_hist, best_hist,
                 alpha=0.15, color="#EF5350")
ax1.set_xlabel("Generatie")
ax1.set_ylabel("Fitness (scor total echipa)")
ax1.set_title("Evolutia fitness-ului pe generatii")
ax1.legend()
ax1.grid(True, alpha=0.3)

# Grafic 2: Comparatie rate de mutatie diferite
ax2 = axes[1]
rate_mutatie = [0.01, 0.05, 0.10, 0.20]
culori_rate  = ["#66BB6A", "#42A5F5", "#FF9800", "#EF5350"]

for rata, culoare in zip(rate_mutatie, culori_rate):
    _, best_h, _ = algoritm_genetic(
        marime_pop=50, num_generatii=150, rata_mutatie=rata
    )
    ax2.plot(range(1, len(best_h) + 1), best_h,
             color=culoare, linewidth=1.8,
             label=f"mutatie={rata * 100:.0f}%")

ax2.set_xlabel("Generatie")
ax2.set_ylabel("Cel mai bun fitness")
ax2.set_title("Comparatie: rate diferite de mutatie")
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("proiect3_algoritm_genetic.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nGrafic salvat: proiect3_algoritm_genetic.png")