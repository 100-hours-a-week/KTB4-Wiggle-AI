import os
import argparse
import json
from jamo import h2j, j2hcj

SHORTCUTS_FILENAME = "mac_shortcuts.json"
SIMILARITY_THRESHOLD = 0.7
def load_shortcuts() -> list:
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, SHORTCUTS_FILENAME)

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def calc_levenshtein_distance(a: str, b: str) -> int:
    a = j2hcj(h2j(a))
    b = j2hcj(h2j(b))
    na, nb = len(a), len(b)
    d = list([0 for _ in range(nb+1)] for _ in range(na+1))
    for i in range(na+1):
        d[i][0] = i
    for j in range(nb+1):
        d[0][j] = j
    
    for i in range(1, na+1):
        for j in range(1, nb+1):
            if a[i-1] == b[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min((d[i-1][j], d[i][j-1], d[i-1][j-1])) + 1
    return 1 - d[-1][-1] / max(na, nb)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('desc', nargs='*')
    args = parser.parse_args()

    shortcuts = load_shortcuts()

    if args.desc:
        query = ' '.join(args.desc)
    else:
        query = input("원하는 단축키 기능을 입력하세요: ")

    shortcut_found = False
    for shortcut in shortcuts:
        for word in shortcut['desc'].split(' '):
            calc_levenshtein_distance(query, word)
            if calc_levenshtein_distance(query, word) > SIMILARITY_THRESHOLD:
                print(shortcut['key'], ':', shortcut['desc'])
                shortcut_found = True
                break

    if not shortcut_found:
        print('단축키가 검색되지 않았습니다.')


if __name__ == '__main__':
    main()
