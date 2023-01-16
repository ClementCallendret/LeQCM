from pathlib import Path



if not(Path("./static/login.txt").is_file()):
    print("init save file")
    with open('./static/login.txt', 'w') as out:
        print("", file=out)

#add encrypt later for login


def load():
    with open('./static/login.txt', 'r') as file:
        file = file.read()[:-1].split("\n\n\n")
        if file != ['']:
            for i in range(len(file)):
                file[i] = file[i].split("\n\n")
            file[-1][1] = file[-1][1].replace("\n", '')
        else:
            file = []
        return file

def save(data):
    with open('./static/login.txt', 'w') as file:
        out = ""
        for couple in data:
            for item in couple:
                out+= item + "\n\n"
            out=out[:-2]
            out+="\n\n\n"
        out = out[:-3]
        print(out, file=file)