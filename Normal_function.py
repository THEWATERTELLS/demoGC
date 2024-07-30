from Normal_gates import NormalGate, AndGate, OrGate, XorGate, NormalCircuit

# ai  bi  ci   true---|/////|   (this gate is to ensure the input of a Circuit is always
# |   |   |          3| AND |--------------+           a Circuit or Gate, not raw number)
# o---+---+-----------|\\\\\|              |
# |   |   |                                +---->|/////|
# o---+---+--->|/////|                          5| XOR |---->c(i+1)
# |   |   |   1| XOR |-----+               +---->|\\\\\|
# |   |   o--->|\\\\\|     +---->|/////|   |
# |   |   |                     4| AND |---+
# |   o---+--->|/////|     +---->|\\\\\|
# |   |   |   2| XOR |-----+
# |   |   o--->|\\\\\|
#


def bit_compare(a, b, c):
    gate1 = XorGate(a, c)
    gate2 = XorGate(b, c)
    gate3 = AndGate(a, 1)
    gate4 = AndGate()
    gate5 = XorGate()

    circuit = NormalCircuit(gate5,
                            NormalCircuit(gate3, None, None),
                            NormalCircuit(gate4,
                                          NormalCircuit(gate2, None, None),
                                          NormalCircuit(gate1, None, None)))

    output = circuit.calc()
    return output


byte_array1 = [1, 1, 1, 1]
byte_array2 = [1, 0, 1, 0]
c = 0

print(bit_compare(1, 1, 0))

for _ in range(len(byte_array1)):
    a = byte_array1[_]
    b = byte_array2[_]
    c = bit_compare(a, b, c)

if c:
    print("a is greater than b")
else:
    print("a is less than or equal to b")


