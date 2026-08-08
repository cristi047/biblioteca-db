Aplicație CLI (linie de comandă) scrisă în Python, cu bază de date SQLite,
pentru gestionarea împrumuturilor de cărți într-o bibliotecă.
Funcționalități
-
Adăugare cărți noi în catalog
-
Vizualizare cărți disponibile pentru împrumut
-
Vizualizare toate cărțile (disponibile + împrumutate)
-
Împrumutarea unei cărți, cu înregistrarea persoanei și a datei
-
Returnarea unei cărți împrumutate
-
Istoric complet al împrumuturilor (folosind JOIN între tabele)
Tehnologii folosite
-
Python 3 — logica aplicației
-
SQLite3 — bază de date relațională, stocată local într-un fișier
Structura bazei de date
Două tabele legate printr-o relație de tip foreign key:
-
carti — id, titlu, autor, disponibilitate
-
imprumuturi — id, carteid (leagă de tabelul carti), persoana, dataimprumut
