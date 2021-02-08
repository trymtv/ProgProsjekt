from random import randint
import crypto_utils


class Cipher():
    def __init__(self, start=32, end=126):
        self.start = start
        self.end = end
        self.length = self.end - self.start + 1

    def encode(self, message, key):
        pass

    def decode(self, message, key):
        pass

    def verify(self, message, key_pair):
        pass

    def generate_keys(self):
        pass

    def shift_message_down(self, message):
        return [ord(elem) - self.start for elem in message]

    def shift_message_up(self, message):
        return "".join([chr(elem + self.start) for elem in message])

    def shifted_coding(self, message, func):
        shifted = self.shift_message_down(message)
        coded = [func(elem) for elem in shifted]
        return self.shift_message_up(coded)

    def __str__(self):
        return str(self.__class__.__name__) + f" start: {self.start}, end: {self.end}"


class CesarCipher(Cipher):

    def encode_decode(self, message, key):
        return self.shifted_coding(message, lambda char: (char + key) % self.length)

    def encode(self, message, key):
        return self.encode_decode(message, key)

    def decode(self, message, key):
        return self.encode_decode(message, key)

    def generate_keys(self):
        first_key = randint(1, self.length)
        return (first_key, self.length - first_key)

    def verify(self, message, key_pair):
        return message == self.decode(self.encode(message, key_pair[0]), key_pair[1])


class MulCipher(Cipher):

    def encode_decode(self, message, key):
        return self.shifted_coding(message, lambda char: (char * key) % self.length)

    def encode(self, message, key):
        return self.encode_decode(message, key)

    def decode(self, message, key):
        return self.encode_decode(message, key)

    def generate_keys(self):
        key1 = randint(1, self.length)
        while not (key2 := crypto_utils.modular_inverse(key1, self.length)):
            key1 = randint(1, self.length)
        return key1, key2

    def verify(self, message, key_pair):
        return message == self.decode(self.encode(message, key_pair[0]), key_pair[1])


class AffineCipher(Cipher):

    def __init__(self, start=32, end=126):
        super().__init__(start, end)
        self.cesar = CesarCipher(start, end)
        self.mul = MulCipher(start, end)

    def encode(self, message, key_pair):
        return self.mul.encode(self.cesar.encode(message, key_pair[1]), key_pair[0])

    def decode(self, message, key_pair):
        return self.cesar.decode(self.mul.decode(message, key_pair[0]), key_pair[1])

    def generate_keys(self):
        cesar_keys = self.cesar.generate_keys()
        mul_keys = self.mul.generate_keys()
        return ((mul_keys[0], cesar_keys[0]), (mul_keys[1], cesar_keys[1]))

    def verify(self, message, key_pair1, key_pair2):
        return message == self.decode(self.encode(message, key_pair1), key_pair2)


class UnbreakableCipher(Cipher):

    def encode_decode(self, message, key):
        shifted_message = self.shift_message_down(message)
        long_key = key * (len(message) // len(key) + 1)
        shifted_long_key = self.shift_message_down(long_key)
        for i in enumerate(shifted_message):
            shifted_message[i] = (shifted_message[i] +
                                  shifted_long_key[i]) % self.length
        return "".join(self.shift_message_up(shifted_message))

    def encode(self, message, key):
        return self.encode_decode(message, key)

    def decode(self, message, key):
        return self.encode_decode(message, key)

    def generate_keys(self, first_key):
        shifted_fist_key = self.shift_message_down(first_key)
        shifted_second_key = [self.length - char for char in shifted_fist_key]
        return "".join(self.shift_message_up(shifted_second_key))

    def verify(self, message, key_pair):
        return message == self.decode(self.encode(message, key_pair[0]), key_pair[1])


class RSA(Cipher):

    def encode_decode(self, message, key_pair):
        return [pow(number, key_pair[1], key_pair[0]) for number in message]

    def encode(self, message, key_pair):
        return self.encode_decode(crypto_utils.blocks_from_text(message, 1), key_pair)

    def decode(self, message, key_pair):
        return crypto_utils.text_from_blocks(self.encode_decode(message, key_pair), 8)

    def generate_keys(self):
        first_random_prime = crypto_utils.generate_random_prime(8)
        while (second_random_prime := crypto_utils.generate_random_prime(8)) == first_random_prime:
            pass
        modulus = first_random_prime * second_random_prime
        phi = (first_random_prime - 1) * (second_random_prime - 1)

        public_key = randint(3, phi - 1)
        while not (private_key := crypto_utils.modular_inverse(public_key, phi)):
            public_key = randint(3, phi - 1)

        return (modulus, public_key), (modulus, private_key)

    def verify(self, message, key_pair1, key_pair2):
        return message == self.decode(self.encode(message, key_pair1), key_pair2)


class Person():
    def __init__(self, key=0):
        self.key = key

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def operate_cypher(self):
        pass


class Sender(Person):
    def __init__(self, cipher, key=0):
        super().__init__(key)
        self.cipher = cipher


def main():
    test = RSA()
    keys = test.generate_keys()
    coded = test.encode("testting faen", keys[0])
    print(test.decode(coded, keys[1]))


if __name__ == "__main__":
    main()
