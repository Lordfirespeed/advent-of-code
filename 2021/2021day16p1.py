class Packet:
    def __init__(self, packetBinary):
        self.potentialPacketBinary = packetBinary

        self.version = None
        self.typeID = None
        self.value = None
        self.subPackets = None
        self.length = None

    @staticmethod
    def parse_value_binary(binary):
        currentPositionInBinary = 0
        valueBits = ""
        foundTerminatingGroup = False
        while not foundTerminatingGroup:
            packetIsNotTerminatorBit = int(binary[currentPositionInBinary], 2)
            if not packetIsNotTerminatorBit:
                foundTerminatingGroup = True

            currentPositionInBinary += 1
            valueBits += binary[currentPositionInBinary:currentPositionInBinary + 4]
            currentPositionInBinary += 4

        return int(valueBits, 2), currentPositionInBinary

    @staticmethod
    def parse_number_of_packets(binary, numberOfPackets):
        currentPositionInBinary = 0
        packets = []
        # print(f"Looking for {numberOfPackets} packets...")
        for packetIndex in range(numberOfPackets):
            newPacket = Packet(binary[currentPositionInBinary:])
            newPacket.parse()
            currentPositionInBinary += newPacket.length
            # print(f"new packet length was {newPacket.length}, current search length {currentPositionInBinary}")
            packets.append(newPacket)
        return packets, currentPositionInBinary

    @staticmethod
    def parse_packets_to_length(binary, lengthOfPackets):
        currentPositionInBinary = 0
        packets = []
        # print(f"Looking for packets of length {lengthOfPackets}")
        while currentPositionInBinary < lengthOfPackets:
            newPacket = Packet(binary[currentPositionInBinary:])
            newPacket.parse()
            currentPositionInBinary += newPacket.length
            # print(f"new packet length was {newPacket.length}, current search length {currentPositionInBinary}/{lengthOfPackets}")
            packets.append(newPacket)
        return packets, currentPositionInBinary

    def parse(self):
        # print(f"Parsing packet with binary {self.potentialPacketBinary}")

        versionBinary = self.potentialPacketBinary[0:3]
        typeIDBinary = self.potentialPacketBinary[3:6]
        self.version, self.typeID = int(versionBinary, 2), int(typeIDBinary, 2)

        if self.typeID == 4:  # literal value
            value, lengthOfValue = self.parse_value_binary(self.potentialPacketBinary[6:])
            self.value = value
            self.length = lengthOfValue + 6

        else:  # contains more packets
            lengthTypeID = int(self.potentialPacketBinary[6], 2)

            if lengthTypeID:  # grab packets until number of packets = the length value
                lengthValueBinary = self.potentialPacketBinary[7:18]
                lengthValue = int(lengthValueBinary, 2)
                potentialSubPacketBinary = self.potentialPacketBinary[18:]
                subPackets, lengthOfSubPackets = self.parse_number_of_packets(potentialSubPacketBinary, lengthValue)
                packetLength = 18 + lengthOfSubPackets
            else:  # grab packets until total packet length = the length value
                lengthValueBinary = self.potentialPacketBinary[7:22]
                lengthValue = int(lengthValueBinary, 2)
                potentialSubPacketBinary = self.potentialPacketBinary[22:]
                subPackets, lengthOfSubPackets = self.parse_packets_to_length(potentialSubPacketBinary, lengthValue)
                packetLength = 22 + lengthOfSubPackets

            self.subPackets = subPackets
            self.length = packetLength


class Solution:
    def __init__(self, hexPacket):
        self.enclosingPacketHex = hexPacket
        self.enclosingPacketBinary = self.process_hex_packet_to_binary(self.enclosingPacketHex)
        self.enclosingPacket = Packet(self.enclosingPacketBinary)

    @staticmethod
    def integer_to_binary(integer):
        return bin(integer)[2:]

    @staticmethod
    def integer_to_four_length_binary(integer):
        binary = Solution.integer_to_binary(integer)
        while len(binary) < 4:
            binary = "0" + binary
        return binary

    @staticmethod
    def hex_to_four_length_binary(hexString):
        return Solution.integer_to_four_length_binary(int(hexString, 16))

    @staticmethod
    def process_hex_packet_to_binary(hexPacket):
        return "".join([Solution.hex_to_four_length_binary(character) for character in hexPacket])

    @staticmethod
    def get_packet_version_numbers_sum(packet):
        sumOfSubPacketVersionSums = 0
        if packet.subPackets:
            sumOfSubPacketVersionSums = sum([Solution.get_packet_version_numbers_sum(subPacket) for subPacket in packet.subPackets])

        return packet.version + sumOfSubPacketVersionSums

    def parse_enclosing_packet(self):
        self.enclosingPacket.parse()

    def get_enclosing_packet_version_numbers_sum(self):
        return self.get_packet_version_numbers_sum(self.enclosingPacket)


if __name__ == "__main__":
    with open(r"Input\2021day16.txt") as inputFile:
        inputLines = [line.strip() for line in inputFile.readlines()]

    solver = Solution(inputLines[0])
    solver.parse_enclosing_packet()
    result = solver.get_enclosing_packet_version_numbers_sum()
    print(f"Sum of packet version numbers: {result}")
