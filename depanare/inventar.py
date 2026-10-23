# inventar.py - rezumatul tintelor dintr-un fisier JSON
# Unealta a fost scrisa in graba si nu mai merge. Reparati-o.
# Rulare:  python inventar.py tinte.json --prag 1000
import argparse
import json


def incarca(cale): #lipseau :(2 puncte) la declararea functiei
    """Citeste lista de tinte din fisierul JSON."""
    with open(cale) as f:
        return json.load(f)


def port_valid(text):
    """Intoarce portul ca int, sau None daca nu e un numar."""
    try:
        return int(text)
    except ValueError:
        return None #am corectat linia ca sa se afle in interiorul blocului except


def pe_servicii(tinte):
    """Dict: serviciu -> lista de porturi."""
    grupe = {}
    for t in tinte:
        serviciu = t.get("serviciu", "necunoscut") #am folosit functia get pentru a nu provoca erori
        port = port_valid(t["port"])
        if port is None:
            print("sar peste", t["gazda"], ": port invalid", t["port"])
            continue
        if serviciu not in grupe: #am adaugat un if fiindca list se reseta de fiecare data
            grupe[serviciu] = [] 
        grupe[serviciu].append(port)
    return grupe #functia nu returna dictionarul deci el nu putea fi utilizat in alte operatii

def peste_prag(tinte, prag):
    """Lista gazdelor cu un port mai mare decat pragul."""
    rezultat = []
    for t in tinte:
        port = port_valid(t["port"])
        if port is not None and port > int(prag): #exista deja o functie care trateza portul invalid
            rezultat.append(t["gazda"])
    return rezultat #nu trebuie sa se afle in interiorul buclei for


def main():
    p = argparse.ArgumentParser()
    p.add_argument("fisier")
    p.add_argument("--prag", default=1024)
    a = p.parse_args()

    tinte = incarca(a.fisier)
    print(f"Tinte citite: {len(tinte)}") #am folosit un f string pentru a afisa mesajul

    grupe = pe_servicii(tinte)
    for serviciu, porturi in grupe.items():
        print(f"{serviciu}: {porturi}")

    mari = peste_prag(tinte, a.prag)
    print(f"Peste {a.prag}: {mari}")

    with open("raport_inventar.json", "w") as f:
        json.dump({"servicii": grupe, "peste_prag": mari}, f, indent=2)
    print("Raport salvat in raport_inventar.json")


if __name__ == "__main__":
    main()
