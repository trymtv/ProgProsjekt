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


class MorseDecoder():
    """ Morse code class """

    def __init__(self, signal_width=15, polling_delay=0.0001):
        GPIO.setup(PIN_BTN, GPIO.IN, GPIO.PUD_DOWN)
        self.word = ""
        self.symbol_code = ""
        self.polling_delay = polling_delay
        self.signal_width = signal_width

    # Resets all buffer variables
    def reset(self):
        self.word = self.symbol_code = ""

    # Reads and returns a signal from the morse stream
    def read_one_signal(self):
        return GPIO.input(PIN_BTN)

    """
    Loop for generating and checking signal.
    Solves signal instability by checking for a stable
    signal before determening a signal change.
    """

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
                if next_count >= 3:
                    self.decode_signal(current_signal, signal_count)
                    current_signal = not current_signal
                    signal_count = next_count
                    next_count = 0
            time.sleep(self.polling_delay)

    """
    Decode the given signal by type and length,
    then call subrutines.
    """

    def decode_signal(self, signal, length):
        if signal == 1:
            if length < self.signal_width:
                self.update_current_symbol(".")
            else:
                self.update_current_symbol("-")
        else:
            if length < self.signal_width:
                pass
            elif length < self.signal_width * 4:
                self.handle_symbol_end()
            else:
                self.handle_word_end()

    # Adds the deterimed signal to the current morse code.
    def update_current_symbol(self, signal):
        self.symbol_code += signal

    # Adds the current morse code to the current word.
    def handle_symbol_end(self):
        if self.symbol_code != "" and self.symbol_code in MORSE_CODE:
            self.word += MORSE_CODE[self.symbol_code]
        else:
            print("not symbol")
        self.symbol_code = ""

    # Adds the last symbol to the word and print it, then reset.
    def handle_word_end(self):
        self.handle_symbol_end()
        print(self.word)
        self.reset()


def main():
    decode = MorseDecoder()
    decode.decoding_loop()


if __name__ == "__main__":
    main()
