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
        final = firstdig / secondig
    else:
        print("Unknown operator")


print(final) 
