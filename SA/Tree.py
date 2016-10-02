import datetime


class Tree(object):
    """docstring for Tree."""

    def __init__(self, name, data):
        self.children = []
        self.name = name
        self.data = data
        self.creation = datetime.datetime.today()
        self.modification = datetime.datetime.today()
        self.version = 0
        self.tamanho = len(data)

    def deleteTree(self, name):
        self.children.remove(name)

    def printing(self):
            return("Versao : " + str(self.version) + "\n" + \
                   "Criacao : " + str(self.creation) + "\n" + \
                   "Modificacao : " + str(self.modification) + "\n" + \
                   "Tamanho : " + str(self.tamanho) + "\n\n" + \
                    self.data + "\n"
                   )

    def modificationTree(self, data):
        print(data)
        self.data = data
        self.version += 1
        self.modification = datetime.datetime.now()

    def snake_born(self, data, name):
        a = Tree(name, data)
        self.children.append(a)
        return a

    def exist_snake(self, name):
        for i in self.children:
            if(i.name == name):
                return False
        return True

    def search_snake(self, name):
        for i in self.children:
            if(i.name == name):
                return i
        return None
