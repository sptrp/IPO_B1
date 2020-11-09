from configupdater import ConfigUpdater
# for xml requests (Nikolai's advice)
from lxml.builder import E
from lxml import etree
import os
import sys
import xml.etree.ElementTree as ET

def create_config(config, config_path):
  # create config file
  with open(config_path, 'w') as configfile:
    start_cfg = """
[misc]
format: xml
all_courses: All courses:
my_courses: My courses:
path_client: kunde
searched: Found courses:

[menu]
format_chosen: Format gewaehlt? j/n : 
greet: Bitte waehlen Sie einen Befehl : 
data: 1) Daten abrufen
book: 2) Kurs buchen
my_books: 3) Buchungen anzeigen
menu_choose_format: 4) Format aendern
choose_format: Bitte waehlen Sie ein Format 1) xml 2) csv :  
end: 9) Beenden
choice: Wahl eingeben : 
bye: Bye bye
repeat: Bitte wiederholen Sie die Eingabe.

[submenu2]
title: Bitte waehlen Sie, nach welchen Elementen Sie suchen wollen:
alle: 1) Alle Kurse abrufen.
guid: 2) Nach GU-ID filtern.
nummer: 3) Nach Nummer filtern.
name: 4) Nach Name filtern.
attribute: 5) Überall suchen
back: 6) Zurueck.
choice: Ihre Wahl: 
choice_guid: Bitte GUID angeben :
choice_nummer: Bitte Nummer angeben : 
choice_name: Bitte Name angeben :
choice_divers: Bitte Value angeben :  

[calltype]
show_some_elems: sse
show_my_courses: mcs
show_all_courses: acs
show_all_info: asa
"""
    config.read_string(start_cfg)
    config.write(configfile)


def config_switcher(config, configfile):
  # Call after format  
  choice_format = input (config['menu']['choose_format'].value)  
  if choice_format == '1':
    config.read(configfile)
    config['misc']['format'].value = 'xml'
    config.update_file()
  elif choice_format == '2':
    config.read(configfile)
    config['misc']['format'].value = 'csv'
    config.update_file()


# create request 
def create_request(config, calltype, client_id): 
  return E.request(
            E.course_request(
                E.format(config['misc']['format'].value),
                E.calltype(str(calltype)),
                E.element(""),
                E.value(""),
                E.client(str(client_id))
            )
        )

# create request for single element 
def create_elem_request(config, elem, calltype, value, client_id): 
  return E.request(
            E.course_request(
                E.format(config['misc']['format'].value),
                E.calltype(str(calltype)),
                E.element(elem),
                E.value(value),
                E.client(str(client_id))
            )
        )        

#validate xml with schema (aus den Skripten zur Vorlesung entnommen)
def xml_validator(input, schema):

    xml = et.parse(input)
    xsd = xmlschema.XMLSchema(schema)

    result = xsd.is_valid(xml)

    print(result)
    return result

#create xml kunden file
def create_kundenxml(client_id,vorname,nachname,strasse,plz,ort,land,nummer,mail):
  xml_kunde = os.path.join(sys.path[0], 'kunden.xml') 
  tree = ET.parse(xml_kunde)
  root = tree.getroot()
  
  new = ET.Element('kunde')
  newsub1 = ET.SubElement(new,'id')
  newsub1.text = 'Kundennummer'
  newsub2 = ET.SubElement(new,'vorname')
  newsub2.text = 'vorn'
  newsub3 = ET.SubElement(new,'nachname')
  newsub3.text = 'nn'
  newsub4 = ET.SubElement(new,'adresse')
  newsub4.text = ''
  newsub_ad = ET.SubElement(newsub4, 'strasse')
  newsub_ad.text = 'Asdasstr. 34'
  newsub_ad = ET.SubElement(newsub4, 'plz')
  newsub_ad.text = '12345'
  newsub_ad = ET.SubElement(newsub4, 'ort')
  newsub_ad.text = 'Asdasstr. 34'
  newsub_ad = ET.SubElement(newsub4, 'land')
  newsub_ad.text = 'Asdasstr. 34'
  newsub5 = ET.SubElement(new,'nummer')
  newsub5.text = '123'
  newsub6 = ET.SubElement(new,'mail')
  newsub6.text = 'as@da.de'
  newsub7 = ET.SubElement(new,'kurse')

  root.append(new)
  tree.write(os.path.join(sys.path[0], 'kunden.xml'))

#client_id = os.getpid()
#create_kundenxml(client_id,"HEROLD","HUNTER","HRASTR. 4", "12311", "BERLIN", "GER", "12314142","ab@ce.df")

# path for all booked coursed
def path_constructor(kunde, val):
  return "//veranstaltung/buchung[{}={}]" .format(kunde, val)

# path for specific attribute
def path_constructor_elem(attribute, val):
  return "//veranstaltung[{}='{}']" .format(attribute, val)

# path for string in text
def path_constructor_divers(val):
  return "//veranstaltung/*[contains(text(), '{}')]" .format(val)

# path for string in text in specific attribute
def path_constructor_onlyname(attribute, val):
  return "//veranstaltung/{}[contains(text(), '{}')]" .format(attribute, val)  