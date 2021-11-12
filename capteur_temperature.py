import radio
from ssd1306 import initialize, clear_oled
from microbit import button_a, display, temperature,sleep, pin0

from ssd1306_text import add_text


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

        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)

"""
Programme pour le capteur de temperature
"""


radio.config(channel=47, address=0x75626969)
radio.on()

if __name__ == "__main__":
    # Step 1 : Connexion à la passerelle
    # A FAIRE

    initialize(pinReset = pin0)
    clear_oled()

    add_text(1, 1, "Init...")


    sleep(1000)


    temp="null"
    choix=""
    key = "keyfoifefeoijfe"
    while True:

        if button_a.was_pressed():
            print(str(temperature()))
            radio.send(SimpleEncryption.encode(key,str(temperature())))
            print("msg send")

        incoming = radio.receive()

        if incoming:
            choix=SimpleEncryption.decode(key, incoming)
            print("incoming", SimpleEncryption.decode(key, incoming))

        if choix == "TL":
                temp = str(temperature()) + " C  " + str(display.read_light_level())
        elif choix == "LT":
                temp =  str(display.read_light_level())+ "    "+ str(temperature()) + " C  "


        add_text(1, 1, temp)


