def afiseaza_tabla(tabla):
    print("\n  0 1 2")
    for i, linie in enumerate(tabla):
        print(f"{i} {' '.join(linie)}")
    print()

def citeste_mutare(tabla, jucator):
    while True:
        try:
            print(f"Randul jucatorului {jucator}:")
            linie = int(input("Introdu linia (0, 1, 2): "))
            coloana = int(input("Introdu coloana (0, 1, 2): "))
            if 0 <= linie <= 2 and 0 <= coloana <= 2:
                if tabla[linie][coloana] == ".":
                    return linie, coloana
                else:
                    print("Eroare: Pozitia este deja ocupata")
            else:
                print("Eroare: Coordonate invalide (alege 0, 1 sau 2).")
        except ValueError:
            print("Eroare: Te rog introdu numere intregi.")


def stare_joc(tabla):

    for i in range(3):
        if tabla[i][0] == tabla[i][1] == tabla[i][2] != ".":
            return tabla[i][0]
        if tabla[0][i] == tabla[1][i] == tabla[2][i] != ".":
            return tabla[0][i]

    if tabla[0][0] == tabla[1][1] == tabla[2][2] != ".":
        return tabla[0][0]
    if tabla[0][2] == tabla[1][1] == tabla[2][0] != ".":
        return tabla[0][2]

    plina = True
    for linie in tabla:
        if "." in linie:
            plina = False
            break

    if plina:
        return "EGAL"
    else:
        return "CONTINUA"


def joaca_joc():
    tabla = [["." for _ in range(3)] for _ in range(3)]
    jucator_curent = "X"

    while True:
        afiseaza_tabla(tabla)

        l, c = citeste_mutare(tabla, jucator_curent)

        tabla[l][c] = jucator_curent

        status = stare_joc(tabla)

        if status != "CONTINUA":
            afiseaza_tabla(tabla)
            if status == "EGAL":
                print("Jocul s-a terminat la egalitate!")
            else:
                print(f"Felicitari! Jucătorul {status} a castigat!")
            break

        jucator_curent = "O" if jucator_curent == "X" else "X"


    #start joc
if __name__ == "__main__":
    joaca_joc()