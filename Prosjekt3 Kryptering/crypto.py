from random import randint
import crypto_utils

with open("english_words.txt", "r") as file:
    word_list = [elem.strip() for elem in file]
word_lookup_list = set(word_list)


class Cipher():
    def __init__(self, start=32, end=126):
        self.start = start
        self.end = end
        self.length = self.end - self.start + 1
        self.key_range = range(0, self.length)

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
        private_key = randint(1, self.length)
        return (private_key, self.length - private_key)

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
        private_key = randint(1, self.length)
        while not (public_key := crypto_utils.modular_inverse(private_key, self.length)):
            private_key = randint(1, self.length)
        return private_key, public_key

    def verify(self, message, key_pair):
        return message == self.decode(self.encode(message, key_pair[0]), key_pair[1])


class AffineCipher(Cipher):

    def __init__(self, start=32, end=126):
        super().__init__(start, end)
        self.cesar = CesarCipher(start, end)
        self.mul = MulCipher(start, end)

    def encode(self, message, key):
        return self.mul.encode(self.cesar.encode(message, key[1]), key[0])

    def decode(self, message, key):
        return self.cesar.decode(self.mul.decode(message, key[0]), key[1])

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
        for i, _ in enumerate(shifted_message):
            shifted_message[i] = (shifted_message[i] +
                                  shifted_long_key[i]) % self.length
        return "".join(self.shift_message_up(shifted_message))

    def encode(self, message, key):
        return self.encode_decode(message, key)

    def decode(self, message, key):
        return self.encode_decode(message, key)

    def generate_keys(self):
        first_key = word_list[randint(0, len(word_list))]
        shifted_fist_key = self.shift_message_down(first_key)
        shifted_second_key = [self.length - char for char in shifted_fist_key]
        print(first_key)
        return "".join(self.shift_message_up(shifted_second_key)), first_key

    def verify(self, message, key_pair):
        return message == self.decode(self.encode(message, key_pair[0]), key_pair[1])


class RSA(Cipher):

    def encode_decode(self, message, key):
        return [pow(number, key[1], key[0]) for number in message]

    def encode(self, message, key):
        return self.encode_decode(crypto_utils.blocks_from_text(message, 1), key)

    def decode(self, message, key):
        return crypto_utils.text_from_blocks(self.encode_decode(message, key), 8)

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

    def verify(self, message, key_pair):
        return message == self.decode(self.encode(message, key_pair[0]), key_pair[1])


class Person():
    def __init__(self, cipher):
        self.keys = 0
        self.cipher = cipher

    def get_key(self):
        return self.keys

    def operate_cipher(self, message):
        pass


class Sender(Person):

    def operate_cipher(self, message):
        return self.cipher.encode(message, self.keys[0])

    def set_key(self):
        self.keys = self.cipher.generate_keys()

    def get_key(self):
        return self.keys[1]


class Reciever(Person):

    def set_key(self, keys):
        self.keys = keys

    def operate_cipher(self, message):
        return self.cipher.decode(message, self.keys)


class Hacker():
    def __init__(self, cipher):
        self.cipher = cipher
        self.word_chain_length = 3

    def check_words_in_list(self, words):
        return all(str.lower(word) in word_lookup_list for word in words[0:self.word_chain_length])

    def hack_single_key_cipher(self, message):
        for key in self.cipher.key_range:
            decoded_message = self.cipher.decode(message, key)
            split_decoded_message = decoded_message.split(" ")
            if self.check_words_in_list(split_decoded_message):
                return decoded_message
        return "No match found"

    def hack_double_key_cipher(self, message):
        for key1 in self.cipher.key_range:
            for key2 in self.cipher.key_range:
                decoded_message = self.cipher.decode(message, (key1, key2))
                split_decoded_message = decoded_message.split(" ")
                if self.check_words_in_list(split_decoded_message):
                    return decoded_message
        return "No match found"

    def hack_unbreakable_cipher(self, message):
        for word in word_list:
            decoded_message = self.cipher.decode(message, word)
            split_decoded_message = decoded_message.split(" ")
            if self.check_words_in_list(split_decoded_message):
                return decoded_message
        return "No match found"


def main():
    cipher = RSA()
    person1 = Sender(cipher)
    person2 = Reciever(cipher)
    person1.set_key()
    person2.set_key(person1.get_key())
    hacker = Hacker(cipher)
    coded_message = person1.operate_cipher("Another test test this ball cock")
    print(hacker.hack_unbreakable_cipher(coded_message))
    print(person2.operate_cipher(coded_message))


if __name__ == "__main__":
    main()
