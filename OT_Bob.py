import socket
import random
from utils import modinv
import json

P = 1000000007  # large prime number


def ot_Bob(choice, bob_socket):

    message1 = json.loads(bob_socket.recv(1024).decode())
    g = message1["g"]
    gs = message1["gs"]
    # print(f"I received g={g} and gs={gs} from Alice")

    k = random.randint(1000, P-1)
    gk = pow(g, k, P)

    if choice == 0:
        L_choice = gk
    else:
        L_choice = gs * modinv(gk, P) % P

    bob_socket.send(str(L_choice).encode())
    # print(f"I sent L{choice}={L_choice} to Alice")

    message2 = json.loads(bob_socket.recv(1024).decode())
    C00 = message2["C00"]
    C01 = message2["C01"]
    C10 = message2["C10"]
    C11 = message2["C11"]
    # print(f"I received C00={C00}, C01={C01}, C10={C10}, C11={C11} from Alice")

    if choice == 0:
        m = C01 ^ pow(C00, k, P)
    else:
        m = C11 ^ pow(C10, k, P)

    print(f"OT finished, I received m={m} from Alice")
    return m


if __name__ == "__main__":
    bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bob_socket.connect(('127.0.0.1', 12345))
    print("I'm connected to Alice")

    ot_Bob(1, bob_socket)

    bob_socket.close()

