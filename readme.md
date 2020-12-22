Readme zur Aufgabe B2

---

Eine Ausarbeitung von Ivan und Stefan
===============================================

Einleitung
--------
Die Aufgabe wurde wieder größtenteils gemeinsam entwickelt, dafür genutzt wurden Discord und Github. Die Gesamtzeit beträgt für das Team ca. 40h.
Wir haben uns auch mit anderen Gruppen ausgetauscht, um Einblicke in deren Problemlösung zu bekommen, bzw. sich auszutauschen, aber ohne die Kopierung von Code.

Zu den Programmen
--------
- Der Server wird mittels der server_v2.py gestartet.
- In der helper_v2.py sind viele Funktionen abgelegt, das File selbst fuehrt aber nichts aus.
- Beim Start des Server kann der User entscheiden, ob die Kurse.xml neu geladen werden soll. Wählt der User nein, dann wird die verkürzte mitgelieferte Version benutzt.
- Die Kurse.xml liegt im data/ Unterordner
- Die Programme wurden jeweils auf Mac mit mit Python 3.7.3 und Windows mit 3.9 getestet und liefen erfolgreich.
- Bei kopierten Sachen aus dem Internet steht eine Quelle als Kommentar dahinter.
- Die Startseite des Server ist unter http://localhost:5000/index erreichbar.
- Über den 'Einloggen'-Button kommt man auch zum Registrieren, falls man noch keine Logindaten hat.
- Die Swagger-Dokumentation lässt sich aufrufen unter http://localhost:5000/api/ sobald der Server gestartet und die Kurse.xml-Anfrage beantwortet wurde
- Es wurde Flask-RESTX für die Infrastruktur benutzt, damit die Anwendung die http-Anfragen beantworten und die Swagger-Dokumentation im Code stattfinden kann.
- Die http Requests werden in der index.js mit JQuery AJAX hergestellt.
- Es liegt eine Server_comparison.txt Datei bei, in der nur die neu hinzugekommen Zeiles des Server im Vergleich zur Abgabe B2 hinterlegt sind.
- Als CSS Bibliothek wurde Bootstrap benutzt.
- DataTables wurde als Bibliothek für die Tabellenfunktionen genutzt.
- Die Tabellenfunktionen beinhalten neben der Pagination, die Anzahl der Anzeige, der Header bleibt immer im Sichtfeld auch ein echtzeit Filterfeld (rechtsseitig).
- Den alten Code aus B1 findet man im Ordner "legacy"

---
Letzte Änderung: 22.12.2020
