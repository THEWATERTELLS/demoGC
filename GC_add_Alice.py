from Encrypted_gates import EncGate, Circuit
import Encrypted_function as ef
import utils as ut
import socket
import json
import time

if __name__ == "__main__":

    # define my input
    input0 = 596
    # define mod number, n means mod 2^n+1
    mod = 9
    input_list = ut.num_to_list(input0, mod)
    input_list.reverse()

    # initialize a circuit
    ef.flush("table_add.txt")
    circuit_list = []
    json_list = []

    for i in range(mod):
        circuit = ef.add_circuit_initialize("table_add.txt")
        circuit_list.append(circuit)
        circuit_json = circuit.to_dict()
        json_list.append(circuit_json)

    # establish a connection and send the circuit to Bob
    alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alice_socket.bind(('127.0.0.1', 12346))
    alice_socket.listen(1)
    print("I'm listening on port 12345")
    conn, addr = alice_socket.accept()
    print("I'm connected to Bob")

    # send the circuit to bob
    message = json.dumps(json_list)
    conn.send(message.encode())
    cin0 = ut.adder_fetch("table_add.txt", 0)["cin0"]
    conn.send(str(cin0).encode())
    time.sleep(1)
    # if u don't sleep the sequence will be messed up

    for i in range(mod):
        ef.adder_send_input_to_bob(i, input_list[i], conn)
        time.sleep(1.5)

    result = json.loads(conn.recv(65536).decode())

    result_bin = []
    with open("table_add.txt", "r") as file:
        lines = file.readlines()
        for i in range(mod):
            js = json.loads(lines[i])
            if result[i] == js["so1"]:
                result_bin.append(1)
            else:
                result_bin.append(0)

    result_bin.reverse()
    result_int = ut.list_to_num(result_bin)
    print(f"result={result_int}")

    conn.send(str(result_int).encode())

    conn.close()
    alice_socket.close()
