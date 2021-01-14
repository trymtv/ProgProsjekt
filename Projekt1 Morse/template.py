""" Template for Project 1: Morse code """

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

    def __init__(self):
        """ initialize your class """

    def reset(self):
        """ reset the variable for a new run """

    def read_one_signal(self):
        """ read a signal from Raspberry Pi """

    def decoding_loop(self):
        """ the main decoding loop """

    def process_signal(self, signal):
        """ handle the signals using corresponding functions """

    def update_current_symbol(self, signal):
        """ append the signal to current symbol code """

    def handle_symbol_end(self):
        """ process when a symbol ending appears """

    def handle_word_end(self):
        """ process when a word ending appears """

    def handle_reset(self):
        """ process when a reset signal received """

    def show_message(self):
        """ print the decoded message """


def main():
    """ the main function """

if __name__ == "__main__":
    main()
