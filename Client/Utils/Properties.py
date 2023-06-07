# 读取Properties文件类


class Properties:
    def __init__(self, file_path):
        self.file_path = file_path

    def getProperties(self):
        try:
            pro_file = open(self.file_path, 'r', encoding='utf-8')
            properties = {}
            for line in pro_file:
                if line.find('=') > 0:
                    strs = line.replace('\n', '').split('=')
                    properties[strs[0]] = strs[1]
        except Exception as e:
            raise e
        else:
            pro_file.close()
        return properties




