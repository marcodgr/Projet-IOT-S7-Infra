import radio
from microbit import button_a, display, uart, temperature, sleep
import random

"""
SimpleEncryption (c) v1shwa
Vigenere Cipher
https://gist.github.com/v1shwa/148ec11d0a75be0e5b2af1c449558ba4
"""


class SimpleEncryption:
    @staticmethod
    def encode(key, clear):
        enc = []
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return "".join(enc)

    @staticmethod
    def decode(key, enc):
        dec = []
        enc = enc
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)


"""
Programme pour le concentrateur
"""


radio.config(channel=47, address=0x75686979)
radio.on()

if __name__ == "__main__":

    key = "1a1c994a-013e-48b8-b451-eed000554f05"
    while True:
        if uart.any():
            data = str(uart.read(), "UTF-8")
            if data == "LT" or data == "TL":
                radio.send(SimpleEncryption.encode(key, data))

        if button_a.was_pressed():  # pour tester
            radio.send(SimpleEncryption.encode(key, "TL"))

        incoming = radio.receive()

        if incoming:
            result =  SimpleEncryption.decode(key, incoming)
            if result[0] == "I":
                print(result)
        if False:
            no_capteur = ""
            for _ in range(2):
                no_capteur += random.choice(["A", "B", "C", "D", "E", "F"])
            print("I", str(temperature()) + ";" + str(display.read_light_level()) + ";" + no_capteur)
            sleep(1000)