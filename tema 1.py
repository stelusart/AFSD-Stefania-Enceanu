produse = ["espresso", "latte", "cappuccino", "ceai", "ciocolata calda", "croissant"]
preturi = [8.0, 12.0, 11.0, 7.0, 10.0, 9.0]
stoc = [20, 15, 18, 30, 12, 10]
cant_comanda = [0, 0, 0, 0, 0, 0]
reducere_curenta = 0.0
tip_reducere_activa = "fara"


def afisare_meniu_produse(produse, preturi, stoc):
    print("\n--- MENIU PRODUSE ---")
    for i in range(len(produse)):
        print(f"{i}. {produse[i]:<15} | Pret: {preturi[i]:>5.2f} lei | Stoc: {stoc[i]}")


def adaugare_produs(cant_comanda, stoc, index, cantitate):
    if 0 <= index < len(produse):
        if cantitate > 0:
            if cant_comanda[index] + cantitate <= stoc[index]:
                cant_comanda[index] += cantitate
                return True
            else:
                print(f"Stoc insuficient!")
                return False
    print("Date invalide.")
    return False


def scadere_produs(cant_comanda, index, cantitate):
    if 0 <= index < len(produse):
        if cantitate > 0 and cant_comanda[index] >= cantitate:
            cant_comanda[index] -= cantitate
            return True
    print("Operatiune invalida.")
    return False


def calcul_total(cant_comanda, preturi):
    total = 0.0
    for i in range(len(cant_comanda)):
        total += cant_comanda[i] * preturi[i]
    return total


def stabilire_reducere(total, tip):
    val = 0.0
    if tip == "student" and total >= 30.0:
        val = 0.10 * total
    elif tip == "happy" and total >= 50.0:
        val = 0.15 * total
    elif tip == "cupon" and total >= 25.0:
        val = 7.0

    if tip != "fara" and tip != "inapoi" and val == 0 and total > 0:
        print(f"Total insuficient pentru {tip}.")

    return min(val, total)


def afisare_bon(produse, cant_comanda, preturi, total, reducere):
    print("\n========= BON FISCAL =========")
    for i in range(len(produse)):
        if cant_comanda[i] > 0:
            print(f"{produse[i]:<15} x {cant_comanda[i]:>2} = {cant_comanda[i] * preturi[i]:>6.2f} lei")
    print("-" * 30)
    print(f"Subtotal:        {total:>9.2f} lei")
    print(f"Reducere:       -{reducere:>9.2f} lei")
    print(f"TOTAL FINAL:     {total - reducere:>9.2f} lei")
    print("==============================\n")


def finalizare_comanda(stoc, cant_comanda):
    for i in range(len(stoc)):
        stoc[i] -= cant_comanda[i]
        cant_comanda[i] = 0


def anulare_comanda(cant_comanda):
    for i in range(len(cant_comanda)):
        cant_comanda[i] = 0


while True:
    print("\n1. Meniu | 2. Adauga | 3. Scade | 4. Reducere | 5. Finalizeaza | 6. Anuleaza | 0. Iesire")
    opt = input("Optiune: ")

    if opt == "1":
        afisare_meniu_produse(produse, preturi, stoc)
    elif opt == "2":
        try:
            idx = int(input("Index: "))
            cant = int(input("Cantitate: "))
            adaugare_produs(cant_comanda, stoc, idx, cant)
        except ValueError:
            pass
    elif opt == "3":
        try:
            idx = int(input("Index: "))
            cant = int(input("Cantitate: "))
            scadere_produs(cant_comanda, idx, cant)
        except ValueError:
            pass
    elif opt == "4":
        t = calcul_total(cant_comanda, preturi)
        if t == 0:
            print("Comanda goala.")
        else:
            print("1. Student | 2. Happy | 3. Cupon | 4. Fara | 5. Inapoi")
            s_opt = input("Reducere: ")
            if s_opt == "1":
                tip_reducere_activa = "student"
            elif s_opt == "2":
                tip_reducere_activa = "happy"
            elif s_opt == "3":
                tip_reducere_activa = "cupon"
            elif s_opt == "4":
                tip_reducere_activa = "fara"

            if s_opt != "5":
                reducere_curenta = stabilire_reducere(t, tip_reducere_activa)
    elif opt == "5":
        t = calcul_total(cant_comanda, preturi)
        if t > 0:
            reducere_finala = stabilire_reducere(t, tip_reducere_activa)
            afisare_bon(produse, cant_comanda, preturi, t, reducere_finala)
            finalizare_comanda(stoc, cant_comanda)
            tip_reducere_activa = "fara"
            reducere_curenta = 0
        else:
            print("Comanda goala.")
    elif opt == "6":
        anulare_comanda(cant_comanda)
        tip_reducere_activa = "fara"
        reducere_curenta = 0
    elif opt == "0":
        break