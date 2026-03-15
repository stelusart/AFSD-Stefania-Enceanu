import csv
import os


class GlosarManager:
    def __init__(self, nume_fisier="glosar.csv"):
        # Initializam dictionarul gol pentru date si setam numele fisierului de salvare
        self.date={}
        self.nume_fisier=nume_fisier

    def adaugare(self):
        #Primeste input de la utilizator si adauga un cuvant nou in dictionar
        cuv = input("Cuvant nou: ").strip().lower()
        if cuv in self.date:
            print(f"'{cuv}' exista deja in baza de date.")
            return

        #Salvam detaliile sub forma de dictionar imbricat (nested dictionary)
        self.date[cuv] = {
            "def": input("Definitie: "),
            "cat": input("Categorie: "),
            "ex": input("Exemplu: ")
        }
        print("Salvat cu succes in memorie!")

    def cauta(self, mod="exact"):
        #Cauta un termen. Daca mod e 'exact', cauta cheia precisa.
        #Daca nu, cauta daca textul este continut in oricare dintre chei.
        text = input("Introdu textul cautat: ").strip().lower()

        if mod == "exact":
            if text in self.date:
                info = self.date[text]
                print(f"\n[{text.upper()}]\nDefinitie: {info['def']}\nCategorie: {info['cat']}\nExemplu: {info['ex']}")
            else:
                print("Nu a fost gasit.")
        else:
            #List comprehension pentru a gasi toate cheile care contin fragmentul cautat
            rezultate = [k for k in self.date if text in k]
            print(f"Potriviri gasite: {', '.join(rezultate) if rezultate else 'Niciuna'}")

    def editare(self):
        #Permite modificarea unei singure proprietati (def/cat/ex) pentru un cuvant existent
        cuv = input("Ce cuvant modificam? ").strip().lower()
        if cuv not in self.date:
            print("Cuvantul nu a fost gasit.")
            return

        camp = input("Ce modifici? (def/cat/ex): ").strip().lower()
        if camp in self.date[cuv]:
            self.date[cuv][camp] = input(f"Valoare noua pentru {camp}: ")
            print("Actualizat!")
        else:
            print("Camp invalid.")

    def eliminare(self):
        #Sterge o intrare din dictionar folosind metoda pop()
        cuv = input("Cuvant de sters: ").strip().lower()
        if self.date.pop(cuv, None):
            print(f"'{cuv}' a fost eliminat.")
        else:
            print("Nu am ce sterge.")

    def listare_totala(self):
        #Afiseaza toate cuvintele intr-un format tabelar simplu folosind f-strings pentru aliniere
        if not self.date:
            return print("Glosarul este gol.")

        print(f"\n{'TERMEN':<15} | {'CATEGORIE':<15} | {'DEFINITIE'}")
        print("-" * 55)
        for t, info in self.date.items():
            print(f"{t.upper():<15} | {info['cat']:<15} | {info['def']}")

    def raport_statistici(self):
        #Calculeaza numarul total de termeni si distributia lor pe categorii
        print(f"\nTotal termeni: {len(self.date)}")
        categorii = {}
        for info in self.date.values():
            c = info['cat']
            #Daca categoria nu exista, o initializeaza cu 0 si adauga 1
            categorii[c] = categorii.get(c, 0) + 1

        for c, v in categorii.items():
            print(f" - {c}: {v}")

    def export_csv(self):
        #Scrie datele din memorie intr-un fisier CSV folosind DictWriter
        try:
            with open(self.nume_fisier, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["termen", "def", "cat", "ex"])
                writer.writeheader()
                for t, info in self.date.items():
                    # Folosim unpack operator (**) pentru a combina cheia 'termen' cu restul info
                    writer.writerow({"termen": t, **info})
            print(f"Date salvate in {self.nume_fisier}")
        except Exception as e:
            print(f"Eroare la scriere: {e}")

    def import_csv(self):
        #Citeste datele din fisierul CSV si le incarca inapoi in dictionarul aplicatiei
        if not os.path.exists(self.nume_fisier):
            return print("Fisierul CSV nu exista.")

        with open(self.nume_fisier, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            #Reconstruim dictionarul folosind dictionary comprehension
            self.date = {row['termen']: {k: row[k] for k in ('def', 'cat', 'ex')} for row in reader}
        print("Date incarcate!")


def porneste_aplicatia():
    #Functia principala care gestioneaza bucla meniului (UI)
    app = GlosarManager()

    #Mapare intre input-ul de la tastatura si functiile clasei (folosind lambda pentru parametri)
    actiuni = {
        "1": app.adaugare,
        "2": lambda: app.cauta("exact"),
        "3": lambda: app.cauta("fragment"),
        "4": app.editare,
        "5": app.eliminare,
        "6": app.listare_totala,
        "7": app.raport_statistici,
        "8": app.export_csv,
        "9": app.import_csv
    }

    while True:
        print("\n--- PANOU CONTROL GLOSAR ---")
        print("1. Adauga | 2. Cautare | 3. Sugestii | 4. Edit | 5. Sterge")
        print("6. Lista  | 7. Stats    | 8. Export    | 9. Import | 0. Iesire")

        cmd = input("\nSelecteaza actiunea: ").strip()

        if cmd == "0":
            print("Inchidere aplicatie... La revedere!")
            break

        actiune = actiuni.get(cmd)
        if actiune:
            actiune()  #Executa functia asociata cheii din dictionar
        else:
            print("Optiune invalida.")


if __name__ == "__main__":
    porneste_aplicatia()
