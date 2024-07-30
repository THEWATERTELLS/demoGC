from Encrypted_gates import EncGate, Circuit
import Encrypted_function as ef
import utils as ut
import socket
import json
import time

if __name__ == "__main__":

    # define my input
    input0 = 0b10101010101010101010101010101010
    input_list = ut.num_to_list(input0)

    # initialize a circuit
    ef.flush("table.txt")
    circuit_list = []
    json_list = []

    for i in range(32):
        circuit = ef.circuit_initialize("table.txt")
        circuit_list.append(circuit)
        circuit_json = circuit.to_dict()
        json_list.append(circuit_json)

    # establish a connection and send the circuit to Bob
    alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alice_socket.bind(('127.0.0.1', 12345))
    alice_socket.listen(1)
    print("I'm listening on port 12345")
    conn, addr = alice_socket.accept()
    print("I'm connected to Bob")

    # send the circuit to bob
    message = json.dumps(json_list)
    conn.send(message.encode())

    # starting rounds
    # before starting send initial c0 to bob
    c_0_for_gate1 = ut.fetch("table.txt", 0)["gate1"]["c_0"]
    c_0_for_gate2 = ut.fetch("table.txt", 0)["gate2"]["c_0"]
    conn.send(json.dumps({"c_0_for_gate1": c_0_for_gate1, "c_0_for_gate2": c_0_for_gate2}).encode())
    time.sleep(1)
    # if u don't sleep the sequence will be messed up

    for i in range(32):
        ef.send_input_to_bob(i, input_list[i], conn)
        time.sleep(1)

    result = int(conn.recv(1024).decode())

    with open("table.txt", "r") as file:
        lines = file.readlines()
        js = json.loads(lines[159])
        o0 = js["o0"]
        o1 = js["o1"]

    print(f"result={result}, o0={o0}, o1={o1}")
    if result == o1:
        print("Alice is greater than Bob!")
        conn.send("Alice is greater than Bob!".encode())
    elif result == o0:
        print("Alice is less than or equal to Bob!")
        conn.send("Alice is less than or equal to Bob!".encode())

    conn.close()
    alice_socket.close()