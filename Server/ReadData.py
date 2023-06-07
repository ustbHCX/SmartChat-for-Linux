def getData(path: str):
    info = {}
    try:
        file = open(path, 'r', encoding="utf8")
        data = file.readlines()
        for line in data:
            if line.find(':') > 0:
                tmp = line.replace('\n', '').split(':')
                key = tmp[0]
                value = tmp[1].rstrip().split(" ")
                if value == ['']:
                    info[key] = []
                else:
                    info[key] = value
    except Exception as e:
        raise e
    else:
        file.close()
        return info


def setData(path: str, info: dict):
    try:
        file = open(path, 'w', encoding="utf8")
        for i in zip(info.keys(), info.values()):
            line = i[0] + ":" + " ".join(i[1]) + "\n"
            file.write(line)
    except Exception as e:
        raise e
    else:
        file.close()
