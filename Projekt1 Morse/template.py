""" Template for Project 1: Morse code """

import time

from GPIOSimulator_v1 import *
GPIO = GPIOSimulator()

MORSE_CODE = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g',
              '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n',
              '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u',
              '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z', '.----': '1',
              '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
              '---..': '8', '----.': '9', '-----': '0'}


class SignalFilter():
    def __init__(self):
        pass


class MorseDecoder():
    """ Morse code class """

    def __init__(self, signal_width=15, polling_delay=0.00005):
        GPIO.setup(PIN_BTN, GPIO.IN, GPIO.PUD_DOWN)
        self.word = ""
        self.symbol_code = ""
        self.polling_delay = polling_delay
        self.signal_width = signal_width

    def reset(self):
        self.word = self.symbol_code = ""

    def read_one_signal(self):
        return GPIO.input(PIN_BTN)

    def decoding_loop(self):
        current_signal = 0
        signal_count = 0
        next_count = 0
        while True:
            if GPIO.input(PIN_BTN) == current_signal:
                signal_count += 1
                next_count = 0
            else:
                next_count += 1
                if next_count >= 5:
                    current_signal = not current_signal
                    signal_count = next_count
                    next_count = 0
            time.sleep(0.0001)
            print(current_signal)

    def process_signal(self, signal):
        """ handle the signals using corresponding functions """

    def update_current_symbol(self, signal):
        self.symbol_code += signal

    def handle_symbol_end(self):
        self.word += MORSE_CODE[self.symbol_code]
        self.symbol_code = ""

    def handle_word_end(self):
        print(self.word, end="")
        self.reset()

    def handle_reset(self):
        """ process when a reset signal received """


def main():
    decode = MorseDecoder()
    decode.decoding_loop()


if __name__ == "__main__":
    main()
