TH Wildau | INW | Telematik | Internetprogrammierung

---

Client-/Server-Anwendung mit WebSockets und XML
===============================================


Im Rahmen des [Open-Data-Ansatzes](https://de.wikipedia.org/wiki/Open_Data) stellen verschiedene Bundes- und Landesinstitutionen ausgewählte Daten zur öffentlichen Verwendung zur Verfügung, z.B. [Berlin Open Data](https://daten.berlin.de/).

Im Rahmen dieser Aufgabenstellung sollen die Daten der [Kurse der Berliner Volkshochschulen](https://daten.berlin.de/datensaetze/kurse-der-berliner-volkshochschulen) verwendet werden. Diese Daten stehen als [XML-Dokument](https://vhsit.berlin.de/VHSKURSE/OpenData/Kurse.xml) zur Verfügung. Auf Grundlage dieser Daten ist folgendes Szenario zu bearbeiten.


Szenario
--------

Ein Server verwaltet die Kurse. Clients können diese Daten abrufen und bearbeiten. Die Kommunikation zwischen Client und Server erfolgt mittels WebSockets.

Hinweise:  

- In <Klammern> angegebene Informationen beziehen sich auf die entspr. Elemente im XML-Dokument.
- Die im Folgenden verwendete Bezeichnung "Funktion" beschreibt eine fachliche Funktion und impliziert nicht, dass dies technisch zwingend als Python-Funktion umzusetzen ist. Über die Form der Umsetzung entscheiden Sie.


Funktion "Daten abrufen":

1. Ein Client ruft vom Server eine Liste der verfügbaren Kurse ab. Zu den Daten gehören <tag>name</tag> und "<untertitel>" und (relevant für den nächsten Schritt) die Beschreibung des gesamten Schema sowie "<guid>" oder "<nummer>".  
2. Ein Client ruft anhand der im Schema hinterlegten Elemente bzw. Attribute konkrete (ausgewählte) Daten (Elemente bzw. Attribute) ab ("<guid>" bzw. "<nummer>" sind zur eindeutigen Kursreferenz erforderlich).  
   Hinweis: Je nach angegebenen Daten kann dies einen konkreten Kurs oder mehrere Kurse betreffen.  
3. Der Server liefert die ausgewählten Daten im gewünschten Format (siehe weitere Anforderungen im Abschnitt Aufgabenstellung) an den Client.  
4. Ein Client gibt die abgerufenen Daten (auf der Konsole in lesbarem Format) aus.

Funktion "Kurs buchen":

1. Ein Client ruft vom Server den Kurskatalog ab.  
   Hinweis: Hier kann die Lösung zu obiger Funktion "Daten abrufen" (wieder)verwendet werden. Es sind aber alle Daten zum gesuchten Kurs zu liefern.  
2. Ein Client erfasst die Daten zur Kursbuchung mittels Nutzereingaben.  
   Als Daten sind Informationen über die Kursinteressenten (Name, Adresse, Telefonnummer oder E-Mail-Adresse) und die zu buchenden Kurse (<guid> bzw. <nummer>) zu erfassen.  
   Hinweis: Die Angabe von im Schema hinterlegten Pflichtdaten ist auf Client-Seite zu prüfen.  
3. Ein Client sendet die erfassten Daten an den Server.  
   Hinweis: Es steht Ihnen frei, jeweils nur einen Kurs oder mehrere Kurse gleichzeitig buchen zu lassen. Im letzten Fall müssen unter Punkt 1 die Daten mehrerer Kurse geliefert werden.  
4. Der Server prüft die Daten auf Schema-Konformität und inhaltliche Korrektheit (d.h. ob es die <guid> bzw. <nummer> auch gibt), speichert sie (im Erfolgsfall) und sendet dem Client (je nach Fall) eine Bestätigungsmeldung.  
   Hinweis: Fachliche Prüfungen, z.B. ob die max. Teilnehmerzahl überschritten wird, sind nicht erforderlich.

Funktion "Buchungen anzeigen":

1. Ein Client ruft vom Server eine Übersicht der von ihm gebuchten Kurse ab.  
   Hinweis: Eine Authentifizierung ist optional.
2. Der Server liefert die Daten im gewünschten Format (siehe weitere Anforderungen im Abschnitt Aufgabenstellung) an den Client.  
   Hinweis: Zu jedem Kurs sind folgende Daten zu liefern: <name>, <untertitel>, <beginn_datum>, <minimale_teilnehmerzahl>, <maximale_teilnehmerzahl> sowie die Anzahl der Buchungen
3. Ein Client gibt die abgerufenen Daten (auf der Konsole in lesbarem Format) aus.


Aufgabenstellung
----------------

Erstellen Sie eine Client-/Server-Anwendung mittels Python, mit der das beschriebene Szenario bearbeitet werden kann. Es wird folgendes Vorgehen empfohlen:

1. Erzeugen Sie ein XML-Schema für das XML-Dokument. Als Hilfestellung bei der Untersuchung der Struktur steht Ihnen das formatierte Dokument `Kurse_snippet.xml` zur Verfügung.

Hinweise:  

- Sie können hierzu geeignete externe Dienste verwenden. Ein entspr. generiertes XML-Schema ist zu prüfen und ggf. zu ergänzen.  
- Erweiterte Regeln, z.B. <minimale_teilnehmerzahl> <= <maximale_teilnehmerzahl>, sind optional. Die Möglichkeit steht ab [XML Schema 1.1](https://www.w3.org/TR/xmlschema11-1/#cAssertions) zur Verfügung. Im Fall einer Anwendung wäre zu prüfen, ob diese Erweiterung von den verwendeten Modulen zum Validieren der XML-Dokumente gegen ein XML Schema unterstützt wird.  
- Auf der o.a. Webseite "Kurse der Berliner Volkshochschulen" ist notiert, dass die Daten z.Zt. wöchentlich aktualisiert werden. Je nachdem, wann Sie das XML-Dokument laden, könnten Bearbeiter und Bewerter mit unterschiedlichen Dokumenten arbeiten. Bei korrektem XML Schema sollte das kein Problem darstellen sein.

2. Erstellen Sie ein XML-Schema für das Speichern von Kundenprofilen. Mit Hilfe dieses Schemas sind die entspr. XML-Dokumente zu erstellen und zu prüfen.

Hinweis: Für das Erzeugen von XML-Dokumenten auf Grundlage von XML-Schema-Dokumenten können externe Werkzeuge wie [PyXB](http://pyxb.sourceforge.net/) verwendet werden. In dem Fall werden bspw. basierend auf einem XML-Schema entspr. Python-Klassen erzeugt, mit denen XML-Dokumente erstellt werden können (siehe hierzu auch [Generating Binding Classes](http://pyxb.sourceforge.net/userref_pyxbgen.html#pyxbgen)).

Die obigen Punkte können Sie teamübergreifend bearbeiten. Kooperationen sind anzugeben.

Zum Speichern von gebuchten Kursen ist das XML-Dokument unter Punkt 1 zu erweitern. Betroffene Kurse sind an geeigneter Stelle um folgende Elemente zu ergänzen (Beispiel):

        <buchung>
            <kunde>12345</kunde>
            <kunde>67890</kunde>
        </buchung>

Für jeden buchenden Kunden ist ein Eintrag vorzusehen. Die Werte zu <kunde> müssen einen Bezug zum unter Punkt 2 erstellten XML-Dokument haben. Die angegebenen Elemente sind ebenfalls im XML-Schema vorzusehen.


Weitere Anforderungen:  

- Jede XML-Datei muss valides XML enthalten. Das ist durch Abgleich mit dem jeweiligen XML-Schema sicherzustellen. Das Schema wird vom Server verwaltet.  
- Ein Client sendet Daten immer als XML-Dokument an den Server. Das Dokument soll ebenfalls dem jeweiligen XML-Schema entsprechen. Der Server soll zusätzlich prüfen, ob das vom Client gesendete XML-Dokument dem entspr. XML-Schema entspricht. Im Fehlerfall ist der Client geeignet zu benachrichtigen.  
- Das Format der an den Client zu liefernden Daten legt der Client im Rahmen des Abrufs fest. Das Format der übertragenen Daten kann XML, CSV oder (optional) JSON sein. Das zu verwendende Format ist auf Client-Seite in einer Konfigurationsdatei zu speichern. Änderungen am Abrufformat in der Konfigurationsdatei sollen möglich sein, ohne die Client-Anwendung neu starten zu müssen.  
- Achten Sie auf eine sinnvolle Ausnahme- und Fehlerbehandlung.  
- Client und Server sollen jeweils in einer Endlosschleife laufen. Das Beenden kann entweder über geeignete Nutzereingaben oder allgemeinen Programmabbruch (Ctrl-C) erfolgen.  
- (optional) Die Anwendung soll auch mit mehreren (parallel arbeitenden) Instanzen der Client-Anwendung funktionieren.


---

Die Aufgabe ist Teil der Leistungsbewertung (siehe Prüfungsschema). Sie können die Aufgabe in 2er-Teams bearbeiten.  
Laden Sie Ihre Lösungen bis zum 09.11.2020 23.59 Uhr als ZIP-Datei im entspr. Abgabebereich im Moodle-Kurs hoch.  

Die ZIP-Datei soll enthalten:  

- erstellte Python-Skripte (Dateiendung .py)  
- erstellte XML-Dokumente (Dateiendung .xml) und XML Schema-Dokumente (Dateiendung .xsd)  
- Namen der Teammitglieder und Angabe von Kooperationen (Dateiendung .txt oder .md); Geben Sie bitte zusätzlich Ihren Arbeitsaufwand für die o.a. Funktionen bzw. die in der Aufgabenstellung genannten Punkte an.

Sollten Python-Module zu installieren sein, ist dies in den Python-Skripten bzw. als separate Datei requirements.txt anzugeben. Es wird davon ausgegangen, dass die Lösung in einer [virtuellen Python-Umgebung](https://docs.python.org/3/tutorial/venv.html) ausgeführt wird.

Hinweis: Die von o.a. Quelle geladene Datei `Kurse.xml` ist NICHT abzugeben.

---

Letzte Änderung: 27.10.2020


