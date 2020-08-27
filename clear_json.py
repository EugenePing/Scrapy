import io

def clean_json(file):
    f1 = io.open(file, 'r', errors='ignore')
    f2 = io.open('result.json', 'w', errors='ignore')
    f2.write('[')
    for line in f1:
        f2.write(line.replace('}{', '},{'))
    f2.write(']')
    f1.close()
    f2.close()

clean_json("IT-blok.json")
