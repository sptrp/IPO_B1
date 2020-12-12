Readme zur Websocketaufgabe

---

Eine Ausarbeitung von Ivan und Stefan
===============================================

Einleitung
--------
Wir haben 95% der Arbeit gemeinsam im Discord und per Github erarbeitet. Jeder von uns hat Minimum 40h reine Zeit in die Ausarbeitung gesteckt.
Die genaue Aufteilung ist nicht wirklich nachvollziehbar und wir waren beide die ganze Zeit über im Video- und Voice-Chat.
Wir haben uns auch mit anderen Gruppen ausgetauscht, insb. mit Nikolai. So haben wir das funktionierende Kurs-Schema mit seiner Hilfe fertiggestellt.


Zu den Programmen
--------
- Der Server wird mittels der server.py gestartet.
- Der Client dann mit der client.py.
- Beim Starten des Client wird eine temporäre config Datei erstellt. Diese besitzt den Namen config'PIDNUMMER'.cfg. Diese Datei bestimmt ueber viele Ablaeufe bei der Kommunikation zwischen Server und Client.
- Die Requests, die zur Kommunikation zwischen Server und Client fungieren, werden mit dem Elementbuilder in XML-Form gebaut.
- In der helper.py sind viele Funktionen abgelegt, das File selbst fuehrt aber nichts aus.
- Die Schema und XML-Files sind selbsterklaerend: kunden.xsd, kunden.xml,kurse.xsd.
- Die Validierung der originalen Kurse.xml dauert relativ lange.
- Die Programme wurden jeweils auf Mac und Windows mit Python 3.7.3 bzw. 3.8.5 getestet und liefen erfolgreich.
- Bei kopierten Sachen aus dem Internet steht eine Quelle als Kommentar dahinter.
---

Letzte Änderung: 09.11.2020


