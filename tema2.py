elevi=["Ana", "Bogdan", "Carmen", "Darius", "Elena"]
note=[9, 7, 10, 4, 8]

elev_nou="Felix"
nota_elev_nou= 6
elev_de_sters="Darius"
interogari_nume=["Ana","Mara","Elena", "stop"]
absente=[1, 0, 2, 3, 0]
nota_minima=min(note)
nota_maxima=max(note)

#1.A1. listeaza elevii cu notele lor - afiseaza Ana are nota 9 etc.
for i in range(len(elevi)):
    print(f"{elevi[i]} are nota {note[i]}")

#2.A2 nota maxima si minima
for i in range(len(elevi)):
    if note[i] == nota_minima:
        print(f"nota minima {nota_minima}-{elevi[i]}")

for i in range(len(elevi)):
    if note[i] == nota_maxima:
        print(f"nota maxima {nota_maxima}-{elevi[i]}")

 # 3. A3 media clasei - media aritmetica
media=sum(note) / len(note)
print(f"media clasei este:{media:.2f}")

#4.A4 Promovati
for i in range(len(elevi)):
     if note[i] >=5:
         print(elevi[i])

 #PARTEA A DOUA B: 5 B5. +1 punct feicarei note max 10
for i in range(len(note)):
      if note[i] < 10:
         note[i] +1
         print(note[i])
 #6 B6. adauga elevul predefinit
elevi.append(elev_nou)
note.append(nota_elev_nou)
print(elev_nou)
print(nota_elev_nou)

#7 B7 sterge elevul predefinit

pozitie=elevi.index("Darius")
elevi.pop(pozitie)
note.pop(pozitie)
print(elevi)

#8 B8 afiseaza din nou lista
for i in range(len(elevi)):
    print(f"{elevi[i]} are nota {note[i]}")

#9 C9. cautari de nume cu while
i=0

print(elevi)
print(note)
print(interogari_nume)

while interogari_nume[i]!="stop":
    if interogari_nume[i] in elevi:
        j = elevi.index(interogari_nume[i])
        print(note[j])
    else:
        print("nu exista")
    i=1+i

#10 C10. numar promovati/respinsi

respinsi= 0
promovati= 0
for index in range(len(note)) :
     if note[i]>= 5:
            promovati=promovati+1
     else:
            respinsi=respinsi+1
            print(f"{respinsi} elevi respinsi si {promovati} elevi promovati" )

#11 C11 media promovatilor

lista2=[]
for nota in note :
    if nota >= 5:
        lista2.append(nota)



print(note)
if len(lista2)> 0:
    print(sum(lista2) / len(lista2))

