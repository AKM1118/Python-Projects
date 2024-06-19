# this file contains code snippets which are using the lambda functions

# using lambda function to map a new list with all values squared
x = [1, 2, 3, 4, 5]
print(list(map(lambda z: z ** 2, x)))

# using lambda function to filter a list with a key as lambda function
y = [1, 7, 32, 6, 89, 4, 2, 1, 6, 2, 7, 1, 0]
print(list(filter(lambda z: z - 1 != 0, y)))


# sorting object by attributes using lambda functions
class Citizen:
    def __init__(self, name, age):
        self.name = name
        self.age = age


Ciz_1 = Citizen("Arkadii", 69)
Ciz_2 = Citizen("Benjamin", 18)
Ciz_3 = Citizen("Carmen", 27)

L = [Ciz_1, Ciz_2, Ciz_3]
print(f"Before sorting: {[Ciz.name for Ciz in L]}")

L.sort(key=lambda x: x.age)
print(f"After sorting: {[Ciz.name for Ciz in L]}")


