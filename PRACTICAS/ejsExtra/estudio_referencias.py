##comprobar si ha cambiado la referencia o no al sumar 1

def number(number):
    number += 1

number2 = int(input("Introduce un numero: "))

print(id(number2))
number(number2)
print(id(number2))

number2 += 1

print(id(number2))
