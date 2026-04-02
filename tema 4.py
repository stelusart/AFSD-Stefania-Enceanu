import json
import os


#Structura de date si Functii de Incarcare
def incarca_date(nume_fisier="competitori.json"):
    """Incarca competitorii dintr-un fisier JSON."""
    if not os.path.exists(nume_fisier):
        #Daca fisierul nu exista returnam o lista goala
        return []

    try:
        with open(nume_fisier, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Eroare: Fisierul JSON este corupt!")
        return []


def salveaza_date(competitori, nume_fisier="competitori.json"):
    """Salveaza datele curente inapoi in fisierul JSON."""
    try:
        with open(nume_fisier, "w", encoding="utf-8") as f:
            json.dump(competitori, f, indent=4, ensure_ascii=False)
        print("Datele au fost salvate cu succes.")
    except Exception as e:
        print(f"Eroare la salvarea datelor: {e}")


# Implementare Quicksort
def trebuie_sa_fie_inainte(c1, c2):
    """Returneaza True daca competitorul c1 trebuie sa fie inaintea lui c2
    conform criteriilor de departajare stabilite.
    """
    # Criteriul 1: Punctaj descrescator
    if c1["punctaj"] > c2["punctaj"]:
        return True
    if c1["punctaj"] < c2["punctaj"]:
        return False

    # Criteriul2: Timp crescator (daca punctajele sunt egale)
    if c1["timp"] < c2["timp"]:
        return True
    if c1["timp"] > c2["timp"]:
        return False

    # Criteriul 3:Nume alfabetic (daca punctajul si timpul sunt egale)
    return c1["nume"].lower() < c2["nume"].lower()


def quicksort(lista):
    """Algoritmul Quicksort implementat manual."""
    if len(lista) <= 1:
        return lista

    pivot = lista[len(lista) // 2]

    #Impartim lista in functie de criteriile de departajare
    stanga = [x for x in lista if trebuie_sa_fie_inainte(x, pivot)]
    egal = [
        x
        for x in lista
        if not trebuie_sa_fie_inainte(x, pivot)
        and not trebuie_sa_fie_inainte(pivot, x)
    ]
    dreapta = [x for x in lista if trebuie_sa_fie_inainte(pivot, x)]

    return quicksort(stanga) + egal + quicksort(dreapta)


#  Operatiuni Competitori
def adauga_competitor(competitori):
    """Adauga un competitor nou in lista."""
    print("\n--- Adaugare Competitor Nou ---")
    nume = input("Introduceti numele competitorului: ").strip()

    if not nume:
        print("Eroare: Nu puteti introduce un competitor fara nume!")
        return

    try:
        punctaj = float(input("Introduceti punctajul: "))
        timp = float(input("Introduceti timpul (in secunde): "))
    except ValueError:
        print("Eroare: Punctajul si timpul trebuie sa fie numere!")
        return

    competitori.append({"nume": nume, "punctaj": punctaj, "timp": timp})
    print(f"Competitorul {nume} a fost adaugat cu succes.")


def actualizeaza_competitor(competitori):
    """Actualizeaza rezultatele unui competitor existent."""
    if not competitori:
        print("\nLista este goala. Nu aveti pe cine actualiza.")
        return

    print("\n--- Actualizare Rezultate ---")
    nume = input(
        "Introduceti numele competitorului pe care doriti sa il modificati: "
    ).strip()

    gasit = False
    for comp in competitori:
        if comp["nume"].lower() == nume.lower():
            gasit = True
            print(
                f"S-a gasit {comp['nume']}. Date curente: Punctaj: {comp['punctaj']}, Timp: {comp['timp']}"
            )
            try:
                comp["punctaj"] = float(input("Introduceti noul punctaj: "))
                comp["timp"] = float(input("Introduceti noul timp: "))
                print("Rezultatele au fost actualizate!")
            except ValueError:
                print("Eroare: Punctajul si timpul trebuie sa fie numere!")
            break

    if not gasit:
        print(f"Competitorul '{nume}' nu a fost gasit in lista.")


# Afisare, Clasament si Statistici
def afiseaza_competitori(competitori):
    """Afiseaza lista completa a competitorilor in starea actuala."""
    if not competitori:
        print("\nNu exista competitori inregistrati.")
        return

    print(f"\n{'Nume':<25} | {'Punctaj':<10} | {'Timp':<10}")
    print("-" * 51)
    for comp in competitori:
        print(f"{comp['nume']:<25} | {comp['punctaj']:<10} | {comp['timp']:<10}")


def afiseaza_clasament(competitori):
    """Genereaza clasamentul, trateaza egalitatile si afiseaza pozitia corecta."""
    if not competitori:
        print("\nNu exista competitori pentru a genera un clasament.")
        return

    # Sortam lista folosind algoritmul nostru Quicksort
    lista_sortata = quicksort(competitori)

    print(f"\n{'Loc':<5} {'Nume':<25} {'Punctaj':<10} {'Timp':<10}")
    print("-" * 55)

    pozitie_curenta = 1
    for i in range(len(lista_sortata)):
        curent = lista_sortata[i]

        #Tratarea egalitatilor pentru stabilirea locului
        if i > 0:
            precedent = lista_sortata[i - 1]
            # Sunt la egalitate daca au acelasi punctaj si acelasi timp
            if (
                curent["punctaj"] != precedent["punctaj"]
                or curent["timp"] != precedent["timp"]
            ):
                pozitie_curenta = i + 1

        print(
            f"{pozitie_curenta:<5} {curent['nume']:<25} {curent['punctaj']:<10} {curent['timp']:<10}"
        )


def afiseaza_statistici(competitori):
    """Calculeaza si afiseaza statistici sumare."""
    if not competitori:
        print("\nNu exista date pentru a calcula statistici.")
        return

    numar_total = len(competitori)
    punctaje = [c["punctaj"] for c in competitori]
    timpi = [c["timp"] for c in competitori]

    punctaj_maxim = max(punctaje)
    punctaj_minim = min(punctaje)
    media_punctajelor = sum(punctaje) / numar_total
    cel_mai_bun_timp = min(timpi)

    print("\n--- Statistici Competitie ---")
    print(f"Numar total de competitori: {numar_total}")
    print(f"Punctaj maxim:              {punctaj_maxim}")
    print(f"Punctaj minim:              {punctaj_minim}")
    print(f"Media punctajelor:          {media_punctajelor:.2f}")
    print(f"Cel mai bun timp:           {cel_mai_bun_timp}")


#Meniul Interactiv si Fluxul Aplicatiei
def meniu():
    competitori = incarca_date()

    while True:
        print("\n================ MENIU ================")
        print("1. Afiseaza lista curenta a competitorilor")
        print("2. Adauga un competitor nou")
        print("3. Actualizeaza rezultatul unui competitor")
        print("4. Genereaza si afiseaza clasamentul (Sortare)")
        print("5. Afiseaza statistici sumare")
        print("6. Salveaza si Iesi")
        print("=======================================")

        optiune = input("Alegeti o optiune (1-6): ").strip()

        if optiune == "1":
            afiseaza_competitori(competitori)
        elif optiune == "2":
            adauga_competitor(competitori)
        elif optiune == "3":
            actualizeaza_competitor(competitori)
        elif optiune == "4":
            afiseaza_clasament(competitori)
        elif optiune == "5":
            afiseaza_statistici(competitori)
        elif optiune == "6":
            salveaza_date(competitori)
            print("La revedere!")
            break
        else:
            print(
                "Optiune invalida! Va rugam sa introduceti o cifra de la 1 la 6."
            )


if __name__ == "__main__":
    meniu()