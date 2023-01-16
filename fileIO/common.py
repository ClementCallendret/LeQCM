from pathlib import Path

sep = "\n\n\n==========\n\n\n"

if not(Path("./static/save.txt").is_file()):
    print("init save file")
    with open('./static/save.txt', 'w') as out:
        #replace by some gibberish stuffè
        print(""+sep+"[]", file=out)


def load():
    with open('./static/save.txt', 'r') as file:
        file = file.read().split(sep)
        file[0]=file[0].split("\n=b=\n")
        for i in range(len(file[0])):
            file[0][i] = file[0][i].split("\n=a=\n")
        file[0][-1][1] = file[0][-1][1].replace("\n", '')
        return file

def save(data):
    with open('./static/save.txt', 'w') as file:
        out = ""
        for couple in data[0]:
            for item in couple:
                out+= item + "\n=a=\n"
            out=out[:-4]
            out+="=b=\n"
        out = out[:-4]
        out+= sep + str(data[1])
        print(out, file=file)