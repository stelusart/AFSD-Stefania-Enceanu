"""
Proiect 2 — Las Vegas
Căutarea unui element într-un vector folosind ordine aleatoare

Algoritmul Las Vegas returnează ÎNTOTDEAUNA răspunsul corect,
dar numărul de pași variază aleatoriu de la o rulare la alta.
"""

import random
import matplotlib.pyplot as plt
import numpy as np

# 1. Generarea datelor de intrare


def genereaza_vector(n):
    """
    Generează un vector cu n valori distincte (permutare a lui 1..n).

    Parametri:
        n: dimensiunea vectorului

    Returnează:
        lista cu n valori distincte
    """
    vector = list(range(1, n + 1))
    random.shuffle(vector)
    return vector


def alege_tinta(vector):
    """Alege aleatoriu un element din vector ca valoare căutată."""
    return random.choice(vector)



# 2. Implementarea cautarii randomizate (Las Vegas)


def cauta_las_vegas(vector, tinta):
    """
    Caută 'tinta' în 'vector' verificând pozițiile într-o ordine aleatoare.

    Aceasta este esența algoritmului Las Vegas:
    - Răspunsul este ÎNTOTDEAUNA corect (dacă tinta există, o găsim sigur).
    - Numărul de pași VARIAZĂ aleatoriu la fiecare rulare.

    Parametri:
        vector: lista în care căutăm
        tinta:  valoarea căutată (garantat existentă în vector)

    Returnează:
        (pozitie_gasita, numar_pasi)
    """
    n = len(vector)
    indici_aleatori = list(range(n))
    random.shuffle(indici_aleatori)  # ordinea aleatoare de verificare

    for pas, idx in enumerate(indici_aleatori, start=1):
        if vector[idx] == tinta:
            return idx, pas  # găsit! returnăm poziția și numărul de pași

    # Nu ajungem niciodată aici dacă tinta există în vector
    raise ValueError("Tinta nu a fost găsită — eroare în date!")



# 3. Rulari multiple pentru acelasi input — variatia pașilor


print("=" * 55)
print("PROIECT 2 — LAS VEGAS: Căutare cu ordine aleatoare")
print("=" * 55)

N_TEST = 1000
NUM_RULARI = 30
vector_test = genereaza_vector(N_TEST)
tinta_test = alege_tinta(vector_test)

print(f"\nVector de dimensiune n={N_TEST}, căutăm valoarea: {tinta_test}")
print(f"Rulăm algoritmul de {NUM_RULARI} ori:\n")

pasi_rulari = []
for i in range(NUM_RULARI):
    pozitie, pasi = cauta_las_vegas(vector_test, tinta_test)
    pasi_rulari.append(pasi)

print(f"  Minim pași:  {min(pasi_rulari)}")
print(f"  Maxim pași:  {max(pasi_rulari)}")
print(f"  Medie pași:  {np.mean(pasi_rulari):.2f}")
print(f"  Teoretic (n+1)/2 = {(N_TEST + 1) / 2:.2f}")
print()
print("  Observație: Algoritmul Las Vegas produce MEREU răspunsul")
print("  corect, dar numărul de pași variază semnificativ.")

# 4. Experimente pentru dimensiuni diferite


dimensiuni = [100, 500, 1_000, 5_000, 10_000]
NUM_RULARI_EXP = 50

print(f"\nAnaliză pentru dimensiuni diferite ({NUM_RULARI_EXP} rulări/dimensiune):")
print(f"{'n':>8} | {'Min':>8} | {'Medie':>8} | {'Max':>8} | {'(n+1)/2':>8}")
print("-" * 50)

rezultate_dim = {}
for n in dimensiuni:
    vec = genereaza_vector(n)
    tinta = alege_tinta(vec)
    pasi_list = [cauta_las_vegas(vec, tinta)[1] for _ in range(NUM_RULARI_EXP)]
    rezultate_dim[n] = pasi_list
    print(f"{n:>8,} | {min(pasi_list):>8} | {np.mean(pasi_list):>8.1f} | "
          f"{max(pasi_list):>8} | {(n + 1) / 2:>8.1f}")


# 5. Grafice cu matplotlib

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Las Vegas — Căutare randomizată într-un vector",
             fontsize=14, fontweight="bold")

# Grafic 1: Pasii celor 30 de rulari pentru n=1000
ax1 = axes[0]
ax1.bar(range(1, NUM_RULARI + 1), pasi_rulari,
        color="#42A5F5", alpha=0.8, edgecolor="white", linewidth=0.5)
ax1.axhline(y=np.mean(pasi_rulari), color="#EF5350", linewidth=2,
            linestyle="--", label=f"Medie = {np.mean(pasi_rulari):.1f}")
ax1.axhline(y=(N_TEST + 1) / 2, color="#66BB6A", linewidth=2,
            linestyle=":", label=f"Teoretic (n+1)/2 = {(N_TEST + 1) / 2:.1f}")
ax1.set_xlabel("Numărul rulării")
ax1.set_ylabel("Număr de pași")
ax1.set_title(f"Variația pașilor la {NUM_RULARI} rulări (n={N_TEST:,})")
ax1.legend()
ax1.grid(True, alpha=0.3, axis="y")

#  Grafic 2: Min / Medie / Max în functie de dimensiunea vectorului
ax2 = axes[1]
medii = [np.mean(rezultate_dim[n]) for n in dimensiuni]
minime = [min(rezultate_dim[n]) for n in dimensiuni]
maxime = [max(rezultate_dim[n]) for n in dimensiuni]
teoretic = [(n + 1) / 2 for n in dimensiuni]

ax2.plot(dimensiuni, medii, "o-", color="#42A5F5", linewidth=2,
         markersize=7, label="Medie pași")
ax2.plot(dimensiuni, minime, "v--", color="#66BB6A", linewidth=1.5,
         markersize=6, label="Minim pași")
ax2.plot(dimensiuni, maxime, "^--", color="#EF5350", linewidth=1.5,
         markersize=6, label="Maxim pași")
ax2.plot(dimensiuni, teoretic, "s:", color="#AB47BC", linewidth=2,
         markersize=6, label="Teoretic (n+1)/2")
ax2.set_xlabel("Dimensiunea vectorului n")
ax2.set_ylabel("Număr de pași")
ax2.set_title("Min / Medie / Max pași vs. dimensiunea vectorului")
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/lab7/proiect2_las_vegas.png",
            dpi=150, bbox_inches="tight")
plt.close()
print("\n✓ Grafic salvat: proiect2_las_vegas.png")