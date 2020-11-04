dvv_kategorie = elem.find('dvv_kategorie').text
minimale_teilnehmerzahl = elem.find('minimale_teilnehmerzahl').text
maximale_teilnehmerzahl = elem.find('maximale_teilnehmerzahl').text
anzahl_termine = elem.find('anzahl_termine').text
beginn_datum = elem.find('beginn_datum').text
ende_datum = elem.find('ende_datum').text
zielgruppe = elem.find('zielgruppe').text
schlagwoerter = elem.find('schlagwort').text
veranstaltungsort_name = elem.find('veranstaltungsort/name').text
veranstaltungsort_adresse_land = elem.find('veranstaltungsort/adresse/land').text
veranstaltungsort_adresse_plz = elem.find('veranstaltungsort/adresse/plz').text
veranstaltungsort_adresse_ort = elem.find('veranstaltungsort/adresse/ort').text
cols = ['guid', 'nummer', 'name', 'untertitel', 'dvv_kategorie', 
  'minimale_teilnehmerzahl', 'maximale_teilnehmerzahl', 'anzahl_termine', 
  'beginn_datum', 'ende_datum', 'zielgruppe', 'schlagwoerter', 'veranstaltungsort', 
  'veranstaltungsort_land', 'veranstaltungsort_plz', 'veranstaltungsort_ort', 
  'veranstaltungsort_barrierefrei', 'preis_betrag', 'preis_rabatt_moeglich', 
  'preis_zusatz', 'webadresse']

veranstaltungsort_adresse_strasse = elem.find('veranstaltungsort/adresse/strasse').text
veranstaltungsort_barrierefrei = elem.find('veranstaltungsort/barrierefrei').text
preis_betrag = elem.find('preis/betrag').text
preis_rabatt_moeglich = elem.find('preis/rabatt_moeglich').text
preis_zusatz = elem.find('preis/zusatz').text
webadresse = elem.find('webadresse').text

rows.append({"guid": guid, "nummer": nummer, "name": name, "untertitel": untertitel, 
                  "dvv_kategorie": dvv_kategorie, "minimale_teilnehmerzahl": minimale_teilnehmerzahl, 
                  "maximale_teilnehmerzahl": maximale_teilnehmerzahl, "anzahl_termine": anzahl_termine, 
                  "beginn_datum": beginn_datum, "ende_datum": ende_datum, "zielgruppe": zielgruppe, 
                  "schlagwort": schlagwoerter, "veranstaltungsort": veranstaltungsort_name,
                  "veranstaltungsort_land": veranstaltungsort_adresse_land, 
                  "veranstaltungsort_plz": veranstaltungsort_adresse_plz, 
                  "veranstaltungsort_ort": veranstaltungsort_adresse_ort, 
                  "veranstaltungsort_barrierefrei": veranstaltungsort_barrierefrei,
                  "preis_betrag": preis_betrag, "preis_rabatt_moeglich": preis_rabatt_moeglich, 
                  "preis_zusatz": preis_zusatz, 
                  "webadresse": webadresse})