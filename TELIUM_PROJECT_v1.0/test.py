import time

def typeLine(line):
    for letter in line:
        print(letter, end="", flush=True)
        time.sleep(0.0005)
    


with open("MAP.txt", "r", encoding="utf-8") as map:
    for line in range(60):
        typeLine(map.readline())
        


queen = "👾"
worker = "👽"
player = "🧑"
vent = "▦"
infomation_panle = "⌬"

print(queen, worker, player, vent, infomation_panle)