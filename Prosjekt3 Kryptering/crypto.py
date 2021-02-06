class Cipher():
    def __init__(self, start=32, end=126):
        self.start = start
        self.end = end
        self.length = self.end - self.start + 1

    def encode(self, message, key):
        pass

    def decode(self):
        pass

    def verify(self):
        pass

    def shift_message_down(self, message):
        return [ord(elem) - self.start for elem in message]

    def shift_message_up(self, message):
        return "".join([chr(elem + self.start) for elem in message])

    def __str__(self):
        return str(self.__class__.__name__) + f" start: {self.start}, end: {self.end}"


class CesarCipher(Cipher):

    def encode(self, message, key):
        pass


class Person():
    def __init__(self, key=0):
        self.key = key

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def operate_cypher(self):
        pass


def main():
    test = CesarCipher()
    test.encode("aaaaaazzzazazaz       ~~~~", 10)


if __name__ == "__main__":
    main()
