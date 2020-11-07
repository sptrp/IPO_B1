def main():

    choice = '0'

    while choice != '9':
        print("Bitte waehlen sie zwischen 1 bis 4:")
        print("1) Daten abrufen")
        print("2) Kurs buchen")
        print("3) Buchungen anzeigen")
        print("9) Beenden")
        
        choice = input ("Please make a choice: ")

        if choice == "5":
            print("Go to another menu")
            second_menu()
        elif choice == "4":
            print("Do Something 4")
        elif choice == "3":
            print("Do Something 3")
        elif choice == "2":
            print("Do Something 2")
        elif choice == "1":
            print("Do Something 1")
        elif choice == "9":
            print("Program closed.")
        else:
            print("I don't understand your choice.")

def second_menu():
    print("This is the second menu")

main()