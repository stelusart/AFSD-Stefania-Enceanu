#20. sunt_anagrame(a: str, b: str) -> str

#Verifică dacă a și b sunt anagrame, ignorând spațiile și literele mari/mici.
#Returnează mesaj: "'a' și 'b' sunt anagrame." sau "'a' și 'b' nu sunt anagrame.".
def sunt_anagrame(a: str, b: str) -> str:
    normalizat_a = a.lower().replace(' ', '')
    normalizat_b = b.lower().replace(' ', '')

    sortat_a = ''.join(sorted(normalizat_a))
    sortat_b = ''.join(sorted(normalizat_b))

    if sortat_a == sortat_b:
        return f"'{a}' si '{b}' sunt anagrame."
    else:
        return f"'{a}' si '{b}' nu sunt anagrame."


print(sunt_anagrame("mere", "erme"))