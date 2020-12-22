from configupdater import ConfigUpdater
# for xml requests (Nikolai's advice)
from lxml.builder import E
from lxml import etree
import os
import sys
import xmlschema
import xml.etree.ElementTree as ET
 

#create xml kunden file
def create_kundenxml(client_id, username, vorname, nachname, strasse, plz, ort, land, mail, kennwort):
  xml_kunde = os.path.join(sys.path[0], 'data/kunden.xml') 
  tree = etree.parse(xml_kunde)
  root = tree.getroot()
  print('creating')
  new = E.kunde(
      E.id(client_id),
      E.username(username),
      E.vorname(vorname),
      E.nachname(nachname),
      E.adresse (
        E.strasse(strasse),
        E.plz(plz),
        E.ort(ort),
        E.land(land)
      ),
      E.mail(mail),
      E.kennwort(kennwort)
    )

  root.insert(1, new)
  tree.write(os.path.join(sys.path[0], 'data/kunden.xml'), encoding="utf-8", xml_declaration=True)


#add kunde to course with guid
def add_kunde_to_course(guid, client_id):
  xml_kunde = os.path.join(sys.path[0], 'data/kurse.xml') 
  tree = ET.parse(xml_kunde)
  root = tree.getroot()
  find = root.find("./veranstaltung[guid='{}']" .format(guid))
  addbuchung = ET.SubElement(find, 'buchungid')
  addbuchung.text = client_id
  tree.write(os.path.join(sys.path[0], 'data/kurse.xml'), encoding="utf-8", xml_declaration=True)

# 'Guid', 'Nummer', 'Name', 'Untertitel'
def xml_trimmer(tree):
  filters = ['dvv_kategorie', 'minimale_teilnehmerzahl', 'maximale_teilnehmerzahl', 'anzahl_termine',
            'beginn_datum', 'ende_datum', 'zielgruppe', 'schlagwort', 'text', 'veranstaltungsort', 'preis',
            'webadresse']
  for fltr in filters:
    for elem in tree.xpath('//veranstaltung/%s' % fltr):
        elem.getparent().remove(elem)

  return tree

# 'Name', 'Untertitel', 'beginn_datum', 'minimale_teilnehmerzahl', 'maximale_teilnehmerzahl'
def xml_trimmer_mybooks(tree):
  filters = ['dvv_kategorie', 'anzahl_termine', 'ende_datum', 'zielgruppe', 'schlagwort', 'text', 
  'veranstaltungsort', 'preis', 'guid', 'nummer', 'webadresse']
  for fltr in filters:
    for elem in tree.xpath('//veranstaltung/%s' % fltr):
        elem.getparent().remove(elem)  

  return tree
  
# path for all booked coursed
def path_constructor_book(val):
  return "//veranstaltung[buchungid='{}']" .format(val)

# path for specific attribute
def path_constructor_elem(attribute, val):
  return "//veranstaltung[{}='{}']" .format(attribute, val)

# path for string in text
def path_constructor_divers(val):
  return "//*[contains(text(), '{}')]" .format(val)

# path for string in text in specific attribute
def path_constructor_onlyname(attribute, val):
  return "//veranstaltung/{}[contains(text(), '{}')]" .format(attribute, val)  

def path_constructor_parentnode(client_id):
  return "//kunde[id='{}']" .format(client_id)

def path_constructor_client_username(client_username):
  print("//kunde[username='{}']" .format(client_username))
  return "//kunde[username='{}']" .format(client_username)

