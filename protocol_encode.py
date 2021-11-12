## A téléverser sur le microcontroleur (tp3.py)
import radio


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


class RadioProtocol:
    def __init__(self, address, secret_key):
        self.addr = address
        self.secret_key = secret_key

    def calculateChecksum(self, message):
        nleft = len(message)
        sum = 0
        pos = 0
        while nleft > 1:
            sum = ord(message[pos]) * 256 + (ord(message[pos + 1]) + sum)
            pos = pos + 2
            nleft = nleft - 2
        if nleft == 1:
            sum = sum + ord(message[pos]) * 256

        """sum = (sum >> 16) + (sum & 0xFFFF)
        sum += (sum >> 16)
        sum = (~sum & 0xFFFF)"""

        return sum

    def sendPacket(self, message, addrDest):
        encoded_message = SimpleEncryption.encode(self.secret_key, message)
        if len(encoded_message) < 251:
            packet = (
                ""
                + str(self.addr)
                + "|"
                + str(len(message))
                + "|"
                + str(addrDest)
                + "|"
                + encoded_message
                + "|"
                + str(self.calculateChecksum(encoded_message))
            )
            radio.send_bytes(packet)

    def receivePacket(self, packet):
        if packet is None:
            return 0
        else:
            tabRes = packet.format(1).split("|")
            stuff = dict()
            stuff["addrSrc"] = tabRes[0]
            stuff["lenMess"] = tabRes[1]
            stuff["addrDest"] = tabRes[2]
            stuff["encoded_message"] = tabRes[3]
            stuff["message"] = SimpleEncryption.decode(self.secret_key, stuff["encoded_message"])
            stuff["receivedCheckSum"] = tabRes[4]

            if self.verifyCheckSum(stuff["receivedCheckSum"], self.calculateChecksum(stuff["encoded_message"])):
                if self.addr == int(stuff["addrDest"]):
                    return stuff["message"]
                else:
                    return -1
            return "IT NO WORK"

    def verifyCheckSum(self, checkSum, receivedCheckSum):
        return int(checkSum) == receivedCheckSum
