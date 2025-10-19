import string
#articol despre analizarea modificarii Codului Penal cu privire la femicid
articol=" Ministerul Justiției a lansat, luni, o consultare privind necesitatea modificării legislației pentru introducerea femicidul în Codul penal care să fie pedepsit cu închisoare pe viață ori între 15 și 25 de ani. Aceeași pedeapsă este propusă și pentru uciderea unei persoane pe motive referitoare la rasă, etnie, religie, orientare sexuală, naționalitate, apartenență politică, avere, origine socială, vârstă, dizabilitate, boală cronică necontagioasă sau infecție HIV/SIDA ori pentru alte împrejurări de același fel"

#PE PRIMA PARTE
#imparte sirul in doua

half=len(articol)//2

first_half=(articol[:half])
second_half=(articol[half:])

#Transformă toate literele în majuscule

first_half=first_half.upper()

#Elimina toate spațiile goale de la începutul și finalul șirului

first_half=first_half.strip()

#PE A DOUA PARTE

#Inversează ordinea caracterelor

second_half=second_half[::-1]

#Transformă prima literă în majusculă

second_half=second_half.capitalize()

#Elimină toate caracterele de punctuație (., ,, !, ?) din această parte

chars_to_remove = ".,!?"
translation_table = str.maketrans("", "", chars_to_remove)
second_half = second_half.translate(translation_table)

#Combină cele două părți și afișează rezultatul

combined_text = first_half + second_half
print(combined_text)