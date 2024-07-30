from Encrypted_gates import EncGate, Circuit
import utils as ut
from OT_Bob import ot_Bob
import json


def dec_bit_compare(afor1, afor3, bfor2, c, true, built_circuit, c1=None, c2=None):
    # a
    built_circuit.input_gate0.input_gate1.self_gate.input1 = afor1
    built_circuit.input_gate1.self_gate.input0 = afor3
    # b
    built_circuit.input_gate0.input_gate0.self_gate.input1 = bfor2
    # c
    if c1 is not None and c2 is not None:
        built_circuit.input_gate0.input_gate0.self_gate.input0 = c2
        built_circuit.input_gate0.input_gate1.self_gate.input0 = c1
    else:
        built_circuit.input_gate0.input_gate0.self_gate.input0 = c
        built_circuit.input_gate0.input_gate1.self_gate.input0 = c
    # true
    built_circuit.input_gate1.self_gate.input1 = true

    return built_circuit.calc()

def get_add_input_from_alice(round, mybit, bob_socket):
    # receive the input from Alice
    alice_input = json.loads(bob_socket.recv(65536).decode())
    print("Received input from Alice. Now OT starts.")
    # mybit must be 0 or 1
    my_input = ot_Bob(mybit, bob_socket)
    alice_bit = alice_input["input"]
    if round != alice_input["round"]:
        raise Exception("Round mismatch")

    return my_input, alice_bit

def get_input_from_alice(round, mybit, bob_socket):
    # receive the input from Alice
    message = json.loads(bob_socket.recv(65536).decode())
    print("Received input from Alice. Now OT starts.")
    # mybit must be 0 or 1
    bfor2 = ot_Bob(mybit, bob_socket)
    afor1 = message["a_for_1"]
    afor3 = message["a_for_3"]
    true = message["true"]
    if round != message["round"]:
        raise Exception("Round mismatch")

    return afor1, afor3, bfor2, true
