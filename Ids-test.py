

def old(url):
    old = open(url, 'r')
    lines = old.readlines()
    print(lines[2])

if __name__ == "__main__":
    old('old-ids.txt')
