import sqlite3
from datetime import date

conexiune = sqlite3.connect("biblioteca.db")
cursor = conexiune.cursor()

def creeaza_tabele():
    cursor.execute("""CREATE TABLE IF NOT EXISTS carti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titlu TEXT NOT NULL,
        autor TEXT NOT NULL,
        disponibila INTEGER DEFAULT 1
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS imprumuturi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        carte_id INTEGER,
        persoana TEXT NOT NULL,
        data_imprumut TEXT,
        FOREIGN KEY (carte_id) REFERENCES carti(id)
    )""")
    conexiune.commit()

def adauga_carte(titlu, autor):
    cursor.execute("INSERT INTO carti (titlu, autor) VALUES (?, ?)", (titlu, autor))
    conexiune.commit()
    print(f"Cartea '{titlu}' a fost adăugată.")

def vezi_carti_disponibile():
    cursor.execute("SELECT id, titlu, autor FROM carti WHERE disponibila = 1")
    rezultate = cursor.fetchall()
    if not rezultate:
        print("Nu există cărți disponibile.")
        return
    print("\n--- Cărți disponibile ---")
    for r in rezultate:
        print(f"ID: {r[0]} | {r[1]} — {r[2]}")

def vezi_toate_cartile():
    cursor.execute("SELECT id, titlu, autor, disponibila FROM carti")
    rezultate = cursor.fetchall()
    print("\n--- Toate cărțile ---")
    for r in rezultate:
        stare = "Disponibilă" if r[3] == 1 else "Împrumutată"
        print(f"ID: {r[0]} | {r[1]} — {r[2]} | {stare}")

def imprumuta_carte(carte_id, persoana):
    cursor.execute("SELECT disponibila FROM carti WHERE id = ?", (carte_id,))
    rezultat = cursor.fetchone()
    if rezultat is None:
        print("Nu există o carte cu acest ID.")
        return
    if rezultat[0] == 1:
        cursor.execute("UPDATE carti SET disponibila = 0 WHERE id = ?", (carte_id,))
        cursor.execute("INSERT INTO imprumuturi (carte_id, persoana, data_imprumut) VALUES (?, ?, ?)",
                        (carte_id, persoana, str(date.today())))
        conexiune.commit()
        print("Carte împrumutată cu succes.")
    else:
        print("Cartea nu este disponibilă momentan.")

def returneaza_carte(carte_id):
    cursor.execute("SELECT disponibila FROM carti WHERE id = ?", (carte_id,))
    rezultat = cursor.fetchone()
    if rezultat is None:
        print("Nu există o carte cu acest ID.")
        return
    cursor.execute("UPDATE carti SET disponibila = 1 WHERE id = ?", (carte_id,))
    conexiune.commit()
    print("Carte returnată cu succes.")

def vezi_istoric_imprumuturi():
    cursor.execute("""
        SELECT imprumuturi.id, carti.titlu, imprumuturi.persoana, imprumuturi.data_imprumut
        FROM imprumuturi
        JOIN carti ON imprumuturi.carte_id = carti.id
        ORDER BY imprumuturi.id DESC
    """)
    rezultate = cursor.fetchall()
    if not rezultate:
        print("Nu există împrumuturi înregistrate.")
        return
    print("\n--- Istoric împrumuturi ---")
    for r in rezultate:
        print(f"#{r[0]} | Carte: {r[1]} | Persoană: {r[2]} | Data: {r[3]}")

def meniu():
    creeaza_tabele()
    while True:
        print("\n===== BIBLIOTECA =====")
        print("1. Adaugă carte")
        print("2. Vezi cărți disponibile")
        print("3. Vezi toate cărțile")
        print("4. Împrumută o carte")
        print("5. Returnează o carte")
        print("6. Vezi istoric împrumuturi")
        print("0. Ieșire")

        optiune = input("Alege o opțiune: ").strip()

        if optiune == "1":
            titlu = input("Titlu: ").strip()
            autor = input("Autor: ").strip()
            adauga_carte(titlu, autor)

        elif optiune == "2":
            vezi_carti_disponibile()

        elif optiune == "3":
            vezi_toate_cartile()

        elif optiune == "4":
            try:
                carte_id = int(input("ID carte: "))
            except ValueError:
                print("ID invalid.")
                continue
            persoana = input("Numele persoanei: ").strip()
            imprumuta_carte(carte_id, persoana)

        elif optiune == "5":
            try:
                carte_id = int(input("ID carte: "))
            except ValueError:
                print("ID invalid.")
                continue
            returneaza_carte(carte_id)

        elif optiune == "6":
            vezi_istoric_imprumuturi()

        elif optiune == "0":
            print("La revedere!")
            conexiune.close()
            break

        else:
            print("Opțiune invalidă, încearcă din nou.")

if __name__ == "__main__":
    meniu()