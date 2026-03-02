from lab1lvl1var2func import find_paris

try:
    V = int(input(f"об'єм операції: "))
    donations = [int(x) for x in input(f"список об'ємів: ").split()]
    result = find_paris(donations, V)
    if result == -1:
        print("нема донорів")
    else:
        print(f"можливі донори: {result}")
except Exception:
    print(f"помилка колєга")
