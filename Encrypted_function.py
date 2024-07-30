from Encrypted_gates import EncGate, Circuit, EncAdder, adder_from_dict
from utils import enc, fetch, adder_fetch
from OT_Alice import ot_Alice
import random
import json

MIN_RANDOM_NUM = 0x10000000
MAX_RANDOM_NUM = 10000000000037

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
#  holy shit this graph is a masterpiece

gate_id = 1


def randomize_gate_io(gate_id_, gate_type_, table_file, input_gate1_id=None, input_gate2_id=None):
    # gate_id_ is a number, gate_type_ is a string, table_file is a string
    # if input_gate1_id is None or input_gate2_id is None:
    if input_gate1_id is None:
        ix0 = random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM)
        ix1 = random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM)

    if input_gate2_id is None:
        iy0 = random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM)
        iy1 = random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM)

    with open(table_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            gate = json.loads(line)
            if input_gate1_id is not None and gate["gate_id"] == input_gate1_id:
                ix0 = gate["o0"]
                ix1 = gate["o1"]
            if input_gate2_id is not None and gate["gate_id"] == input_gate2_id:
                iy0 = gate["o0"]
                iy1 = gate["o1"]

    if ix0 is None or ix1 is None or iy0 is None or iy1 is None:
        raise Exception("No input gate found")


    o0 = (random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM) // 0x1000) * 0x1000
    o1 = (random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM) // 0x1000) * 0x1000

    table = {
        "gate_id": gate_id_,
        "gate_type": gate_type_,
        "ix0": ix0,
        "ix1": ix1,
        "iy0": iy0,
        "iy1": iy1,
        "o0": o0,
        "o1": o1
    }

    with open(table_file, "a", encoding="utf-8") as file:
        file.write(json.dumps(table) + "\n")

    if gate_type_ == "AND":
        o00 = enc(ix0, enc(iy0, o0))
        o01 = enc(ix0, enc(iy1, o0))
        o10 = enc(ix1, enc(iy0, o0))
        o11 = enc(ix1, enc(iy1, o1))

        gate = EncGate(gate_id_, o00, o01, o10, o11)
        return gate

    elif gate_type_ == "OR":
        o00 = enc(ix0, enc(iy0, o0))
        o01 = enc(ix0, enc(iy1, o1))
        o10 = enc(ix1, enc(iy0, o1))
        o11 = enc(ix1, enc(iy1, o1))

        gate = EncGate(gate_id_, o00, o01, o10, o11)
        return gate

    elif gate_type_ == "XOR":
        o00 = enc(ix0, enc(iy0, o0))
        o01 = enc(ix0, enc(iy1, o1))
        o10 = enc(ix1, enc(iy0, o1))
        o11 = enc(ix1, enc(iy1, o0))

        gate = EncGate(gate_id_, o00, o01, o10, o11)
        return gate

    else:
        raise Exception("Invalid gate type")


def define_gate_i(gate_id_, gate_type_, tablefile, ix0, ix1, iy0, iy1):
    o0 = (random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM) // 0x1000) * 0x1000
    o1 = (random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM) // 0x1000) * 0x1000

    table = {
        "gate_id": gate_id_,
        "gate_type": gate_type_,
        "ix0": ix0,
        "ix1": ix1,
        "iy0": iy0,
        "iy1": iy1,
        "o0": o0,
        "o1": o1
    }

    with open(tablefile, "a", encoding="utf-8") as file:
        file.write(json.dumps(table) + "\n")

    if gate_type_ == "AND":
        o00 = enc(ix0, enc(iy0, o0))
        o01 = enc(ix0, enc(iy1, o0))
        o10 = enc(ix1, enc(iy0, o0))
        o11 = enc(ix1, enc(iy1, o1))

        gate = EncGate(gate_id_, o00, o01, o10, o11)
        return gate

    elif gate_type_ == "OR":
        o00 = enc(ix0, enc(iy0, o0))
        o01 = enc(ix0, enc(iy1, o1))
        o10 = enc(ix1, enc(iy0, o1))
        o11 = enc(ix1, enc(iy1, o1))

        gate = EncGate(gate_id_, o00, o01, o10, o11)
        return gate

    elif gate_type_ == "XOR":
        o00 = enc(ix0, enc(iy0, o0))
        o01 = enc(ix0, enc(iy1, o1))
        o10 = enc(ix1, enc(iy0, o1))
        o11 = enc(ix1, enc(iy1, o0))

        gate = EncGate(gate_id_, o00, o01, o10, o11)
        return gate

    else:
        raise Exception("Invalid gate type")


def randomize_adder_io(gate_id_, table_file, input_gate_id=None):

    a0 = random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM)
    a1 = random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM)
    b0 = random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM)
    b1 = random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM)

    if input_gate_id is None:
        cin0 = random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM)
        cin1 = random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM)
    else:
        with open(table_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            line = lines[input_gate_id-1]
            gate = json.loads(line)
            cin0 = gate["co0"]
            cin1 = gate["co1"]

    so0 = (random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM) // 0x1000) * 0x1000
    so1 = (random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM) // 0x1000) * 0x1000
    co0 = (random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM) // 0x1000) * 0x1000
    co1 = (random.randint(MIN_RANDOM_NUM, MAX_RANDOM_NUM) // 0x1000) * 0x1000

    table = {
        "gate_id": gate_id_,
        "a0": a0,
        "a1": a1,
        "b0": b0,
        "b1": b1,
        "cin0": cin0,
        "cin1": cin1,
        "so0": so0,
        "so1": so1,
        "co0": co0,
        "co1": co1
    }

    with open(table_file, "a", encoding="utf-8") as file:
        file.write(json.dumps(table) + "\n")

    pso = []
    pco = []

    # these sentences may look crazy, but they are the truth table of a full adder

    pso.append(enc(a0, enc(b0, enc(cin0, so0))))
    pso.append(enc(a0, enc(b0, enc(cin1, so1))))
    pso.append(enc(a0, enc(b1, enc(cin0, so1))))
    pso.append(enc(a0, enc(b1, enc(cin1, so0))))
    pso.append(enc(a1, enc(b0, enc(cin0, so1))))
    pso.append(enc(a1, enc(b0, enc(cin1, so0))))
    pso.append(enc(a1, enc(b1, enc(cin0, so0))))
    pso.append(enc(a1, enc(b1, enc(cin1, so1))))

    pco.append(enc(a0, enc(b0, enc(cin0, co0))))
    pco.append(enc(a0, enc(b0, enc(cin1, co0))))
    pco.append(enc(a0, enc(b1, enc(cin0, co0))))
    pco.append(enc(a0, enc(b1, enc(cin1, co1))))
    pco.append(enc(a1, enc(b0, enc(cin0, co0))))
    pco.append(enc(a1, enc(b0, enc(cin1, co1))))
    pco.append(enc(a1, enc(b1, enc(cin0, co1))))
    pco.append(enc(a1, enc(b1, enc(cin1, co1))))

    gate = EncAdder(gate_id_, pso, pco)
    return gate


def add_circuit_initialize(file):
    global gate_id
    if gate_id == 1:
        gate1 = randomize_adder_io(gate_id, file)
        gate_id += 1
    else:
        gate1 = randomize_adder_io(gate_id, file, input_gate_id=gate_id-1)
        gate_id += 1

    return gate1


def circuit_initialize(file):
    global gate_id
    if gate_id < 5:
        gate1 = randomize_gate_io(gate_id, "XOR", file)
        gate_id += 1
        gate2 = randomize_gate_io(gate_id, "XOR", file)
        gate_id += 1
    else:
        gate1 = randomize_gate_io(gate_id, "XOR", file, input_gate1_id=gate_id-1)
        gate_id += 1
        gate2 = randomize_gate_io(gate_id, "XOR", file, input_gate1_id=gate_id-2)
        gate_id += 1
    gate3 = randomize_gate_io(gate_id, "AND", file)
    gate_id += 1
    gate4 = randomize_gate_io(gate_id, "AND", file, gate_id-2, gate_id-3)  # sequence matters!
    gate_id += 1
    gate5 = randomize_gate_io(gate_id, "XOR", file, gate_id-1, gate_id-2)  # sequence matters!
    gate_id += 1
    circuit = Circuit(gate5,
                      Circuit(gate4,
                              Circuit(gate2, None, None),
                              Circuit(gate1, None, None)),
                      Circuit(gate3, None, None))
    return circuit

def flush(file):
    with open(file, "w", encoding="utf-8") as file:
        file.write("")


def enc_bit_compare(a, b, c, built_circuit, table_file):
    with open(table_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            gate = json.loads(line)
            if gate["gate_id"] == 1:
                c_0_for_gate1 = gate["ix0"]
                c_1_for_gate1 = gate["ix1"]
                a_0_for_gate1 = gate["iy0"]
                a_1_for_gate1 = gate["iy1"]
            elif gate["gate_id"] == 2:
                c_0_for_gate2 = gate["ix0"]
                c_1_for_gate2 = gate["ix1"]
                b_0_for_gate2 = gate["iy0"]
                b_1_for_gate2 = gate["iy1"]
            elif gate["gate_id"] == 3:
                a_0_for_gate3 = gate["ix0"]
                a_1_for_gate3 = gate["ix1"]
                true_for_gate3 = gate["iy1"]

    if a == 1:
        built_circuit.input_gate0.input_gate1.self_gate.input1 = a_1_for_gate1
        built_circuit.input_gate1.self_gate.input0 = a_1_for_gate3
    else:
        built_circuit.input_gate0.input_gate1.self_gate.input1 = a_0_for_gate1
        built_circuit.input_gate1.self_gate.input0 = a_0_for_gate3

    if b == 1:
        built_circuit.input_gate0.input_gate0.self_gate.input1 = b_1_for_gate2
    else:
        built_circuit.input_gate0.input_gate0.self_gate.input1 = b_0_for_gate2

    if c == 1:
        built_circuit.input_gate0.input_gate0.self_gate.input0 = c_1_for_gate2
        built_circuit.input_gate0.input_gate1.self_gate.input0 = c_1_for_gate1
    else:
        built_circuit.input_gate0.input_gate0.self_gate.input0 = c_0_for_gate2
        built_circuit.input_gate0.input_gate1.self_gate.input0 = c_0_for_gate1

    built_circuit.input_gate1.self_gate.input1 = true_for_gate3

    return built_circuit.calc()


def send_input_to_bob(round, mybit, conn):
    round_info = fetch("table.txt", round)
    if mybit == 0:
        my_input_for_1 = round_info["gate1"]["a_0"]
        my_input_for_3 = round_info["gate3"]["a_0"]
    else:
        my_input_for_1 = round_info["gate1"]["a_1"]
        my_input_for_3 = round_info["gate3"]["a_1"]
    true = round_info["gate3"]["true"]
    # send Bob my input:
    my_message = {
        "round": round,
        "a_for_1": my_input_for_1,
        "a_for_3": my_input_for_3,
        "true": true
    }
    conn.send(json.dumps(my_message).encode())
    print("Sent my input to Bob. Now OT starts.")
    # starting OT
    ot_Alice(round_info["gate2"]["b_0"], round_info["gate2"]["b_1"], conn)


def adder_send_input_to_bob(round, mybit, conn):
    round_info = adder_fetch("table_add.txt", round)
    if mybit == 0:
        alice_input = round_info["a0"]
    else:
        alice_input = round_info["a1"]

    my_message = {
        "round": round,
        "input": alice_input
    }
    conn.send(json.dumps(my_message).encode())
    print("Sent my input to Bob. Now OT starts.")
    ot_Alice(round_info["b0"], round_info["b1"], conn)
# for test
#
# flush("table_add.txt")
# gate_list = []
# json_list = []
# for i in range(8):
#     circuit = add_circuit_initialize("table_add.txt")
#     gate_list.append(circuit)
#     dict = circuit.to_dict()
#     json_list.append(dict)
#
#     adder = adder_from_dict(dict)
#     print(adder.to_dict() == dict)
#
#     a = adder_fetch("table_add.txt", i)["a1"]
#     b = adder_fetch("table_add.txt", i)["b1"]
#     c = adder_fetch("table_add.txt", i)["cin0"]
#     print(circuit.calc(a, b, c))
#
# print(json_list)
# #
