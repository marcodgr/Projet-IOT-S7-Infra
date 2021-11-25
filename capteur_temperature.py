import radio
from ssd1306 import initialize, clear_oled
from microbit import button_a, display, temperature, sleep, pin0

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

    initialize(pinReset=pin0)
    clear_oled()

    add_text(1, 1, "Init...")

    sleep(1000)

    key = "1a1c994a-013e-48b8-b451-eed990554f05"
    while True:

        sleep(1000)

        temp = str(temperature()) + " C       "
        lum = str(display.read_light_level()) + "    "

        if button_a.was_pressed():
            radio.send(SimpleEncryption.encode(key, str(temperature())))
            print("msg send")

        incoming = radio.receive()

        if incoming:
            choix = SimpleEncryption.decode(key, incoming)
            print("incoming", SimpleEncryption.decode(key, incoming))

        if choix == "TL":
            add_text(1, 1, temp)
            add_text(1, 2, lum)
        elif choix == "LT":
            add_text(1, 1, lum)
            add_text(1, 2, temp)

        sending = str(temperature()) + ";" + str(display.read_light_level() + ";AA")  # Ajout du code du capteur
        radio.send(SimpleEncryption.encode(key, sending))
