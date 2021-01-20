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

    def reset(self):
        """ Resets all buffer variables"""
        self.word = self.symbol_code = ""

    def read_one_signal(self):
        """Reads and returns a signal from the morse stream"""
        return GPIO.input(PIN_BTN)

    def print_led_status(self, symbol):
        """Prints the correct led status"""
        if symbol == "-":
            GPIO.output(PIN_BLUE_LED, GPIO.LOW)
            GPIO.output(PIN_RED_LED_0, GPIO.HIGH)
            GPIO.output(PIN_RED_LED_1, GPIO.HIGH)
            GPIO.output(PIN_RED_LED_2, GPIO.HIGH)
        else:
            GPIO.output(PIN_RED_LED_0, GPIO.LOW)
            GPIO.output(PIN_RED_LED_1, GPIO.LOW)
            GPIO.output(PIN_RED_LED_2, GPIO.LOW)
            GPIO.output(PIN_BLUE_LED, GPIO.HIGH)

    def reset_leds(self):
        """Sets all led to low"""
        GPIO.output(PIN_BLUE_LED, GPIO.LOW)
        GPIO.output(PIN_RED_LED_0, GPIO.LOW)
        GPIO.output(PIN_RED_LED_1, GPIO.LOW)
        GPIO.output(PIN_RED_LED_2, GPIO.LOW)

    def decoding_loop(self):
        """
        Loop for generating and checking signal.
        Solves signal instability by checking for a stable
        signal before determening a signal change.
        """
        current_signal = 0
        signal_count = 0
        next_count = 0
        while True:
            if self.read_one_signal() == current_signal:
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

    def decode_signal(self, signal, length):
        """
        Decode the given signal by type and length,
        then call subrutines.
        """
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

    def update_current_symbol(self, signal):
        """Adds the deterimed signal to the current morse code."""
        self.print_led_status(signal)
        self.symbol_code += signal

    def handle_symbol_end(self):
        """Adds the current morse code to the current word."""
        self.reset_leds()
        if self.symbol_code != "" and self.symbol_code in MORSE_CODE:
            self.word += MORSE_CODE[self.symbol_code]
        else:
            print("not symbol")
        self.symbol_code = ""

    def handle_word_end(self):
        """Adds the last symbol to the word and print it, then reset."""
        self.handle_symbol_end()
        print(self.word)
        self.reset()


def main():
    decode = MorseDecoder()
    decode.decoding_loop()


if __name__ == "__main__":
    main()
