from Encrypted_gates import EncAdder, adder_from_dict
import Decrypt_function as df
import utils as ut
import socket
import json
import time

if __name__ == "__main__":

    #define my input
    input0 = 772
    # define mod number, n means mod 2^n
    mod = 9
    input_list = ut.num_to_list(input0, mod)
    input_list.reverse()

    # establish connection with Alice
    bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bob_socket.connect(('127.0.0.1', 12346))
    print("I'm connected to Alice")

    # receive the circuit from Alice
    message = bob_socket.recv(65536).decode()
    json_list = json.loads(message)
    adder_list = []
    for i in range(mod):
        adder_json = json_list[i]
        adder = adder_from_dict(adder_json)
        adder_list.append(adder)

    # evaluate the circuit
    # get cin for round 0 from alice
    cin0 = int(bob_socket.recv(1024).decode())
    c = cin0
    time.sleep(1)
    result = []

    for i in range(mod):
        unit_adder = adder_list[i]
        b, a = df.get_add_input_from_alice(i, input_list[i], bob_socket)
        print(f"Round {i}: a={a}, b={b}, c={c}")
        s, c = unit_adder.calc(a, b, c)
        result.append(s)
        time.sleep(0.7)

    time.sleep(1)
    print(f"s={result}")
    bob_socket.send(json.dumps(result).encode())
    m = int(bob_socket.recv(65536).decode())

    print(f"final result:{m}")

    bob_socket.close()

