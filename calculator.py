running = True

while running:
    firstdig = int(input())
    operator = input()
    secondig = int(input(""))
    equal_to = input()
    final = ""

    if equal_to != "=":
        final = "Come Again :)"
    else:
        if operator == "+":
            final = firstdig + secondig
        elif operator == "-":
            final = firstdig - secondig
        elif operator == "*":
            final = firstdig * secondig
        elif operator == "/":
            if secondig == 0:
                print("sorry, can't divide... :(")
            else:
                final = firstdig / secondig
        else:
            print("Unknown operator")


        print(f"result: {final}")

    users_choice = input("Do you wish to continue?(Yes/No): ")
    if users_choice is not ["yes", "y"]:
        print("Thanks for using dorcas's calculator")
        running = False