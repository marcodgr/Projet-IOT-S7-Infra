## A téléverser sur le microcontroleur (tp3.py)
import radio
from microbit import button_a, display


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

radio.config(channel=47, address=0x75626969)
radio.on()

if __name__ == "__main__":
    # Step 1 : Connexion à la passerelle
    # A FAIRE
    key = "keyfoifefeoijfe"
    while True:

        if button_a.was_pressed():
            radio.send(SimpleEncryption.encode(key, "coucou"))
            print("msg send")

        incoming = radio.receive()

        if incoming:
            print("I", SimpleEncryption.decode(key, incoming))
