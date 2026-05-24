"""
Laborator 6 - Sistem de Optimizare a Investitiilor
folosind Programare Dinamica (0/1 Knapsack)

Fiecare investitie poate fi aleasa cel mult o singura data.
Problema este modelata ca un knapsack 0/1:
  - "greutate" = costul investitiei
  - "valoare"  = profitul estimat
  - "capacitate" = bugetul disponibil

Relatia de recurenta:
  dp[i][b] = profitul maxim folosind primele i investitii cu buget b
  dp[i][b] = dp[i-1][b]                                    daca cost[i] > b
  dp[i][b] = max(dp[i-1][b], dp[i-1][b-cost[i]] + profit[i])  altfel
"""

import json
import os
import sys


# ─────────────────────────────────────────────────────────────
# 1. INCARCARE SI VALIDARE DATE
# ─────────────────────────────────────────────────────────────

CAMPURI_OBLIGATORII = {"nume", "cost", "profit", "categorie", "risc"}


def incarca_investitii(cale_fisier: str) -> list[dict]:
    """Incarca si valideaza investitiile din fisierul JSON."""
    if not os.path.exists(cale_fisier):
        sys.exit(f"[EROARE] Fisierul '{cale_fisier}' nu a fost gasit.")

    with open(cale_fisier, "r", encoding="utf-8") as f:
        try:
            date = json.load(f)
        except json.JSONDecodeError as e:
            sys.exit(f"[EROARE] Fisierul JSON este corupt: {e}")

    if not isinstance(date, list) or len(date) == 0:
        sys.exit("[EROARE] Fisierul JSON este gol sau nu contine o lista.")

    investitii_valide = []
    for idx, inv in enumerate(date):
        campuri_lipsa = CAMPURI_OBLIGATORII - set(inv.keys())
        if campuri_lipsa:
            print(f"[AVERTISMENT] Investitia #{idx+1} este incompleta "
                  f"(lipsesc: {campuri_lipsa}). Va fi ignorata.")
            continue
        if not isinstance(inv["cost"], (int, float)) or inv["cost"] <= 0:
            print(f"[AVERTISMENT] Investitia '{inv['nume']}' are cost invalid. Va fi ignorata.")
            continue
        if not isinstance(inv["profit"], (int, float)) or inv["profit"] <= 0:
            print(f"[AVERTISMENT] Investitia '{inv['nume']}' are profit invalid. Va fi ignorata.")
            continue
        investitii_valide.append(inv)

    if not investitii_valide:
        sys.exit("[EROARE] Nu exista investitii valide in fisier.")

    return investitii_valide


# ─────────────────────────────────────────────────────────────
# 2. AFISARE LISTA INVESTITII
# ─────────────────────────────────────────────────────────────

def afiseaza_investitii(investitii: list[dict]) -> None:
    """Afiseaza tabelul complet al investitiilor disponibile."""
    print("\n" + "=" * 72)
    print(" INVESTITII DISPONIBILE ".center(72))
    print("=" * 72)
    header = f"{'Nr':>3}  {'Nume':<18} {'Cost':>8} {'Profit':>8}  {'Categorie':<14} {'Risc':<10}"
    print(header)
    print("-" * 72)
    for i, inv in enumerate(investitii, 1):
        linie = (f"{i:>3}  {inv['nume']:<18} {inv['cost']:>8,.0f} "
                 f"{inv['profit']:>8,.0f}  {inv['categorie']:<14} {inv['risc']:<10}")
        print(linie)
    print("=" * 72)


# ─────────────────────────────────────────────────────────────
# 3. ANALIZA DESCRIPTIVA
# ─────────────────────────────────────────────────────────────

def analiza_descriptiva(investitii: list[dict]) -> None:
    """Statistici sumare asupra setului de investitii."""
    print("\n" + "=" * 55)
    print(" ANALIZA DESCRIPTIVA ".center(55))
    print("=" * 55)

    print(f"  Numar total de investitii : {len(investitii)}")

    inv_cost_min = min(investitii, key=lambda x: x["cost"])
    inv_cost_max = max(investitii, key=lambda x: x["cost"])
    inv_profit_max = max(investitii, key=lambda x: x["profit"])
    inv_raport_max = max(investitii, key=lambda x: x["profit"] / x["cost"])

    print(f"  Cost minim      : {inv_cost_min['cost']:>8,.0f}  ({inv_cost_min['nume']})")
    print(f"  Cost maxim      : {inv_cost_max['cost']:>8,.0f}  ({inv_cost_max['nume']})")
    print(f"  Profit maxim    : {inv_profit_max['profit']:>8,.0f}  ({inv_profit_max['nume']})")
    print(f"  Raport max P/C  : {inv_raport_max['profit']/inv_raport_max['cost']:>8.4f}  ({inv_raport_max['nume']})")

    # Distributie pe categorii
    categorii: dict[str, int] = {}
    for inv in investitii:
        categorii[inv["categorie"]] = categorii.get(inv["categorie"], 0) + 1
    print("\n  Distributie pe categorii:")
    for cat, nr in sorted(categorii.items()):
        print(f"    {cat:<15} : {nr}")

    # Distributie pe risc
    riscuri: dict[str, int] = {}
    for inv in investitii:
        riscuri[inv["risc"]] = riscuri.get(inv["risc"], 0) + 1
    print("\n  Distributie pe nivel de risc:")
    for risc, nr in sorted(riscuri.items()):
        print(f"    {risc:<15} : {nr}")

    print("=" * 55)


# ─────────────────────────────────────────────────────────────
# 4. FILTRARE SI ORDONARE
# ─────────────────────────────────────────────────────────────

def filtreaza_dupa_categorie(investitii: list[dict], categorie: str) -> list[dict]:
    return [inv for inv in investitii if inv["categorie"].lower() == categorie.lower()]


def filtreaza_dupa_risc(investitii: list[dict], risc: str) -> list[dict]:
    return [inv for inv in investitii if inv["risc"].lower() == risc.lower()]


def sorteaza_investitii(investitii: list[dict], criteriu: str) -> list[dict]:
    """
    criteriu poate fi: 'cost', 'profit', 'raport'
    """
    if criteriu == "cost":
        return sorted(investitii, key=lambda x: x["cost"])
    elif criteriu == "profit":
        return sorted(investitii, key=lambda x: x["profit"], reverse=True)
    elif criteriu == "raport":
        return sorted(investitii, key=lambda x: x["profit"] / x["cost"], reverse=True)
    else:
        return investitii


def meniu_filtrare(investitii: list[dict]) -> None:
    """Sub-meniu interactiv de filtrare si ordonare."""
    print("\n  [F] Filtrare / Ordonare investitii")
    print("    1. Dupa categorie")
    print("    2. Dupa nivel de risc")
    print("    3. Sortare dupa cost")
    print("    4. Sortare dupa profit")
    print("    5. Sortare dupa raport profit/cost")
    print("    0. Inapoi")
    opt = input("  Alegeti optiunea: ").strip()

    if opt == "1":
        cat = input("  Introduceti categoria: ").strip()
        rezultat = filtreaza_dupa_categorie(investitii, cat)
        if rezultat:
            afiseaza_investitii(rezultat)
        else:
            print(f"  Nu exista investitii in categoria '{cat}'.")
    elif opt == "2":
        risc = input("  Introduceti nivelul de risc (scazut/mediu/ridicat): ").strip()
        rezultat = filtreaza_dupa_risc(investitii, risc)
        if rezultat:
            afiseaza_investitii(rezultat)
        else:
            print(f"  Nu exista investitii cu risc '{risc}'.")
    elif opt in ("3", "4", "5"):
        criteriu = {"3": "cost", "4": "profit", "5": "raport"}[opt]
        afiseaza_investitii(sorteaza_investitii(investitii, criteriu))
    elif opt == "0":
        return
    else:
        print("  Optiune invalida.")


# ─────────────────────────────────────────────────────────────
# 5. INTRODUCEREA SI VALIDAREA BUGETULUI
# ─────────────────────────────────────────────────────────────

def citeste_buget() -> int:
    """Citeste un buget intreg pozitiv de la utilizator."""
    while True:
        raw = input("\n  Introduceti bugetul disponibil (RON): ").strip()
        try:
            buget = int(raw)
            if buget <= 0:
                print("  [!] Bugetul trebuie sa fie un numar pozitiv.")
            else:
                return buget
        except ValueError:
            print("  [!] Valoare invalida. Introduceti un numar intreg.")


# ─────────────────────────────────────────────────────────────
# 6 & 7. PROGRAMARE DINAMICA (tabelul DP)
# ─────────────────────────────────────────────────────────────

def construieste_tabel_dp(investitii: list[dict], buget: int) -> list[list[int]]:
    """
    Construieste tabelul DP pentru problema 0/1 Knapsack.

    dp[i][b] = profitul maxim selectand din primele i investitii
               cu un buget de b unitati.

    Dimensiune: (n+1) x (buget+1), initializat cu 0.

    Relatia de recurenta:
      - daca cost[i-1] > b:
            dp[i][b] = dp[i-1][b]
      - altfel:
            dp[i][b] = max(dp[i-1][b],
                           dp[i-1][b - cost[i-1]] + profit[i-1])
    """
    n = len(investitii)
    # Initializam tabelul cu zeros
    dp = [[0] * (buget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost_i = int(investitii[i - 1]["cost"])
        profit_i = int(investitii[i - 1]["profit"])
        for b in range(buget + 1):
            # Varianta fara investitia i
            dp[i][b] = dp[i - 1][b]
            # Varianta cu investitia i (daca incape in buget)
            if cost_i <= b:
                cu_investitie = dp[i - 1][b - cost_i] + profit_i
                if cu_investitie > dp[i][b]:
                    dp[i][b] = cu_investitie

    return dp


def afiseaza_tabel_dp_partial(dp: list[list[int]], investitii: list[dict],
                               buget: int, max_coloane: int = 15) -> None:
    """Afiseaza primele max_coloane coloane din tabelul DP (pentru verificare)."""
    pas = max(1, buget // max_coloane)
    coloane = list(range(0, buget + 1, pas))
    if buget not in coloane:
        coloane.append(buget)

    print("\n  Tabel DP (extras, primele coloane relevante):")
    header_cols = "".join(f"{c:>7}" for c in coloane)
    print(f"  {'Investitie':<18} {header_cols}")
    print("  " + "-" * (18 + 7 * len(coloane) + 1))

    print(f"  {'(baza)': <18} " + "".join(f"{dp[0][c]:>7}" for c in coloane))
    for i, inv in enumerate(investitii, 1):
        print(f"  {inv['nume']:<18} " + "".join(f"{dp[i][c]:>7}" for c in coloane))


# ─────────────────────────────────────────────────────────────
# 8. PROFIT OPTIM
# ─────────────────────────────────────────────────────────────

def profit_optim(dp: list[list[int]], buget: int) -> int:
    """Returneaza profitul maxim pentru bugetul dat."""
    return dp[len(dp) - 1][buget]


# ─────────────────────────────────────────────────────────────
# 9. RECONSTRUCTIA SOLUTIEI
# ─────────────────────────────────────────────────────────────

def reconstruieste_solutia(dp: list[list[int]], investitii: list[dict],
                            buget: int) -> list[dict]:
    """
    Parcurge tabelul DP in sens invers pentru a determina
    care investitii au fost incluse in solutia optima.
    """
    alese = []
    b = buget
    for i in range(len(investitii), 0, -1):
        # Daca valoarea difera fata de randul anterior, investitia i a fost aleasa
        if dp[i][b] != dp[i - 1][b]:
            alese.append(investitii[i - 1])
            b -= int(investitii[i - 1]["cost"])
    return alese


# ─────────────────────────────────────────────────────────────
# 10. AFISARE REZULTAT FINAL
# ─────────────────────────────────────────────────────────────

def afiseaza_rezultat(investitii_alese: list[dict], buget: int) -> None:
    """Afiseaza rezultatul complet al optimizarii."""
    cost_total = sum(int(inv["cost"]) for inv in investitii_alese)
    profit_total = sum(int(inv["profit"]) for inv in investitii_alese)
    buget_ramas = buget - cost_total

    print("\n" + "=" * 55)
    print(" REZULTAT FINAL - OPTIMIZARE DP ".center(55))
    print("=" * 55)
    print(f"  Buget disponibil      : {buget:>10,.0f} RON")
    print(f"  Profit optim          : {profit_total:>10,.0f} RON")
    print(f"  Cost total utilizat   : {cost_total:>10,.0f} RON")
    print(f"  Buget ramas           : {buget_ramas:>10,.0f} RON")
    print(f"  Numar investitii alese: {len(investitii_alese):>10}")
    print("\n  Investitii selectate:")
    if investitii_alese:
        for inv in investitii_alese:
            print(f"    - {inv['nume']:<18}  cost={inv['cost']:>7,.0f}  "
                  f"profit={inv['profit']:>7,.0f}  risc={inv['risc']}")
    else:
        print("    (nicio investitie selectata)")
    print("=" * 55)


# ─────────────────────────────────────────────────────────────
# RESTRICTIE SUPLIMENTARA: excluderea investitiilor cu risc ridicat
# + compararea solutiei pentru doua bugete diferite
# ─────────────────────────────────────────────────────────────

def optimizeaza(investitii: list[dict], buget: int,
                fara_risc_ridicat: bool = False,
                max_investitii: int | None = None) -> tuple[list[dict], list[list[int]]]:
    """
    Ruleaza algoritmul DP si returneaza (investitii_alese, tabel_dp).

    Parametri optionali:
      fara_risc_ridicat : exclude automat investitiile cu risc='ridicat'
      max_investitii    : limiteaza numarul maxim de investitii alese
                          (implementat prin DP 3D: dp[i][b][k])
    """
    subset = investitii
    if fara_risc_ridicat:
        subset = [inv for inv in investitii if inv["risc"] != "ridicat"]
        print(f"\n  [INFO] Mod fara risc ridicat: {len(subset)} investitii eligibile.")

    if max_investitii is None:
        # DP standard 0/1 knapsack
        dp = construieste_tabel_dp(subset, buget)
        alese = reconstruieste_solutia(dp, subset, buget)
        return alese, dp
    else:
        # DP 3D: dp[i][b][k] = profit maxim din primele i investitii,
        #        buget b, cu cel mult k investitii alese
        n = len(subset)
        k_max = max_investitii
        # dp3[i][b][k]
        dp3 = [[[0] * (k_max + 1) for _ in range(buget + 1)]
               for _ in range(n + 1)]

        for i in range(1, n + 1):
            cost_i = int(subset[i - 1]["cost"])
            profit_i = int(subset[i - 1]["profit"])
            for b in range(buget + 1):
                for k in range(k_max + 1):
                    dp3[i][b][k] = dp3[i - 1][b][k]
                    if cost_i <= b and k >= 1:
                        cu = dp3[i - 1][b - cost_i][k - 1] + profit_i
                        if cu > dp3[i][b][k]:
                            dp3[i][b][k] = cu

        # Reconstructie din dp3
        alese = []
        b, k = buget, k_max
        for i in range(n, 0, -1):
            if dp3[i][b][k] != dp3[i - 1][b][k]:
                alese.append(subset[i - 1])
                b -= int(subset[i - 1]["cost"])
                k -= 1

        # Convertim dp3 la dp2 standard (pentru afisare)
        dp2 = [[dp3[i][b2][k_max] for b2 in range(buget + 1)] for i in range(n + 1)]
        return alese, dp2


def compara_doua_bugete(investitii: list[dict],
                        buget1: int, buget2: int,
                        fara_risc_ridicat: bool = False) -> None:
    """Compara solutia optima pentru doua bugete diferite."""
    print("\n" + "=" * 65)
    print(f" COMPARATIE: buget {buget1:,} RON  vs  {buget2:,} RON ".center(65))
    print("=" * 65)
    for buget in (buget1, buget2):
        alese, _ = optimizeaza(investitii, buget, fara_risc_ridicat)
        cost_t = sum(int(x["cost"]) for x in alese)
        profit_t = sum(int(x["profit"]) for x in alese)
        print(f"\n  Buget: {buget:>10,} RON")
        print(f"  Profit optim: {profit_t:>8,} RON  |  "
              f"Cost utilizat: {cost_t:>8,} RON  |  "
              f"Ramas: {buget - cost_t:>8,} RON")
        print(f"  Investitii: {', '.join(x['nume'] for x in alese) or '(niciuna)'}")
    print("=" * 65)


# ─────────────────────────────────────────────────────────────
# MENIU PRINCIPAL
# ─────────────────────────────────────────────────────────────

def meniu_principal(investitii: list[dict]) -> None:
    while True:
        print("\n" + "=" * 55)
        print(" MENIU PRINCIPAL ".center(55))
        print("=" * 55)
        print("  1. Afiseaza investitiile disponibile")
        print("  2. Analiza descriptiva")
        print("  3. Filtrare / Ordonare investitii")
        print("  4. Optimizare pentru un buget (varianta standard)")
        print("  5. Optimizare fara investitii cu risc ridicat")
        print("  6. Optimizare cu numar maxim de investitii")
        print("  7. Comparatie doua bugete")
        print("  0. Iesire")
        print("=" * 55)
        opt = input("  Alegeti optiunea: ").strip()

        if opt == "0":
            print("\n  La revedere!\n")
            break

        elif opt == "1":
            afiseaza_investitii(investitii)

        elif opt == "2":
            analiza_descriptiva(investitii)

        elif opt == "3":
            meniu_filtrare(investitii)

        elif opt == "4":
            buget = citeste_buget()
            alese, dp = optimizeaza(investitii, buget)
            print(f"\n  Profit optim calculat: {profit_optim(dp, buget):,} RON")
            afis = input("  Doriti sa vedeti tabelul DP? (d/n): ").strip().lower()
            if afis == "d":
                afiseaza_tabel_dp_partial(dp, investitii, buget)
            afiseaza_rezultat(alese, buget)

        elif opt == "5":
            buget = citeste_buget()
            alese, dp = optimizeaza(investitii, buget, fara_risc_ridicat=True)
            subset_fara_risc = [inv for inv in investitii if inv["risc"] != "ridicat"]
            print(f"\n  Profit optim (fara risc ridicat): {profit_optim(dp, buget):,} RON")
            afis = input("  Doriti sa vedeti tabelul DP? (d/n): ").strip().lower()
            if afis == "d":
                afiseaza_tabel_dp_partial(dp, subset_fara_risc, buget)
            afiseaza_rezultat(alese, buget)

        elif opt == "6":
            buget = citeste_buget()
            while True:
                raw = input("  Numar maxim de investitii permise: ").strip()
                try:
                    k = int(raw)
                    if k <= 0:
                        print("  [!] Trebuie sa fie cel putin 1.")
                    else:
                        break
                except ValueError:
                    print("  [!] Introduceti un numar intreg.")
            alese, dp = optimizeaza(investitii, buget, max_investitii=k)
            profit_t = sum(int(x["profit"]) for x in alese)
            print(f"\n  Profit optim (max {k} investitii): {profit_t:,} RON")
            afiseaza_rezultat(alese, buget)

        elif opt == "7":
            print("\n  Introduceti primul buget:")
            buget1 = citeste_buget()
            print("  Introduceti al doilea buget:")
            buget2 = citeste_buget()
            risc_opt = input("  Excludeti riscul ridicat? (d/n): ").strip().lower()
            fara_risc = risc_opt == "d"
            compara_doua_bugete(investitii, buget1, buget2, fara_risc)

        else:
            print("  [!] Optiune invalida. Incercati din nou.")


# ─────────────────────────────────────────────────────────────
# PUNCT DE INTRARE
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    FISIER_JSON = "investitii.json"

    print("\n" + "=" * 55)
    print(" SISTEM DE OPTIMIZARE A INVESTITIILOR ".center(55))
    print("    (Programare Dinamica - 0/1 Knapsack)   ".center(55))
    print("=" * 55)

    investitii = incarca_investitii(FISIER_JSON)
    print(f"\n  [OK] {len(investitii)} investitii incarcate din '{FISIER_JSON}'.")

    meniu_principal(investitii)