from Encrypted_gates import EncGate, Circuit, circuit_from_dict
import Decrypt_function as df
import utils as ut
import socket
import json
import time


if __name__ == "__main__":

    # define my input
    input0 = 0b10101010101010101010101010101000
    input_list = ut.num_to_list(input0)

    # establish connection with Alice
    bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bob_socket.connect(('127.0.0.1', 12345))
    print("I'm connected to Alice")

    # receive the circuit from Alice
    message = bob_socket.recv(65536).decode()
    json_list = json.loads(message)
    circuit_list = []
    for i in range(32):
        circuit_json = json_list[i]
        circuit = circuit_from_dict(circuit_json)
        circuit_list.append(circuit)
        # print(circuit.to_dict())

    # evaluate the circuit
    # get c for round 0 from alice
    round_0_c_json = json.loads(bob_socket.recv(1024).decode())
    c_for_gate1 = round_0_c_json["c_0_for_gate1"]
    c_for_gate2 = round_0_c_json["c_0_for_gate2"]
    c = 0
    time.sleep(1)

    for i in range(32):
        unit_circuit = circuit_list[i]
        afor1, afor3, bfor2, true = df.get_input_from_alice(i, input_list[i], bob_socket)
        print(f"Round {i}: afor1={afor1}, afor3={afor3}, bfor2={bfor2}, true={true}, c_for_gate1={c_for_gate1}, c_for_gate2={c_for_gate2}")
        if i == 0:
            pass
            c = df.dec_bit_compare(afor1, afor3, bfor2, 0, true, unit_circuit, c_for_gate1, c_for_gate2)
        else:
            pass
            c = df.dec_bit_compare(afor1, afor3, bfor2, c, true, unit_circuit)

        time.sleep(0.5)

    print(f"final result c={c}")
    bob_socket.send(str(c).encode())
    m = bob_socket.recv(1024).decode()
    print(m)

    bob_socket.close()