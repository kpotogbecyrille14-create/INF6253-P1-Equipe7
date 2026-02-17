import re

PART1_PATH = r"C:\Users\LevelinG\Downloads\UQO\Cours\Web_sémantique\Projet\INF6253-P1\part1_web1\resultats.txt"

def read_part1_results():
    temps = {}
    with open(PART1_PATH, "r", encoding="utf-8") as f:
        for line in f:
            # Format : R1 | 23.61 ms | Manchester United
            match = re.match(r"(R\d+)\s*\|\s*([\d\.]+)\s*ms", line)
            if match:
                req = match.group(1)
                ms = float(match.group(2))
                temps[req] = ms
    return temps

if __name__ == "__main__":
    print(read_part1_results())
