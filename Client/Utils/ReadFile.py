import os


def readLineFromLast(path, n):
    try:
        filesize = os.path.getsize(path)
        file = open(path, 'rb')
        if filesize == 0:
            return None
        elif filesize < n:
            return file.readlines()
        else:
            offset = -n
            while -offset < filesize:
                file.seek(offset, 2)
                lines = file.readlines()
                length = len(lines)
                if length > n:
                    return lines[-n]
                elif length * 2 < n:
                    offset *= 2
                else:
                    offset += int(offset / length)
            file.seek(0)
            lines = file.readlines()
            if len(lines) < n:
                return None
            return lines[-n]
    except FileNotFoundError:
        print(path + ' not found!')
        return None



