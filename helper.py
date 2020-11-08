from configupdater import ConfigUpdater

def create_config(config, config_path):
  # create config file
  with open(config_path, 'w') as configfile:
    start_cfg = """
[misc]
format = xml
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
name: 4) Nach Stichwort filtern.
attribute: 5) Stich innerhalb eines Attributes suchen
back: 6) Zurueck.
choice: Ihre Wahl: 

[calltype]
show_some_elems: sse
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
