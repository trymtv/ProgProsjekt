class Cipher():
    def __init__(self, start=32, end=126):
        self.start = start
        self.end = end
        self.length = self.end - self.start + 1

    def encode(self, message, key):
        pass

    def decode(self, message, key):
        pass

    def verify(self, message, key):
        pass

    def shift_message_down(self, message):
        return [ord(elem) - self.start for elem in message]

    def shift_message_up(self, message):
        return "".join([chr(elem + self.start) for elem in message])

    def __str__(self):
        return str(self.__class__.__name__) + f" start: {self.start}, end: {self.end}"


class CesarCipher(Cipher):

    def encode(self, message, key):
        shifted = self.shift_message_down(message)
        coded = [(elem + key) % self.length for elem in shifted]
        return self.shift_message_up(coded)

    def decode(self, message, key):
        shifted = self.shift_message_down(message)
        decoded = [(elem + self.length - key) % self.length for elem in shifted]
        return self.shift_message_up(decoded)

    def verify(self, message, key):
        coded = self.encode(message, key)
        return message == self.decode(coded, key)


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
    coded = test.encode("Johann e dumme!", 10)
    print(coded)
    print(test.decode(coded, 10))



if __name__ == "__main__":
    main()
