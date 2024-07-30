import socket
import random
from utils import modinv
import json

P = 1000000007  # large prime number


def ot_Alice(m0, m1, conn):

    key_s = random.randint(1000, P-1)
    g = random.randint(1000, P-1)
    gs = pow(g, key_s, P)
    key_r0 = random.randint(1000, P-1)
    key_r1 = random.randint(1000, P-1)

    message1 = json.dumps({"g": g, "gs": gs})
    conn.send(message1.encode())
    # print(f"I sent g={g} and gs={gs} to Bob, my key_s={key_s}")

    L_choice = int(conn.recv(1024).decode())
    # print(f"I received L_choice={L_choice} from Bob")

    C00 = pow(g, key_r0, P)
    C01 = pow(L_choice, key_r0, P) ^ m0
    C10 = pow(g, key_r1, P)
    C11 = pow(gs * modinv(L_choice, P) % P, key_r1, P) ^ m1
    message2 = json.dumps({"C00": C00, "C01": C01, "C10": C10, "C11": C11})
    conn.send(message2.encode())

    # print(f"OT finishes, I sent C00={C00}, C01={C01}, C10={C10}, C11={C11} to Bob")


if __name__ == "__main__":
    alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alice_socket.bind(('127.0.0.1', 12345))
    alice_socket.listen(1)
    print("I'm listening on port 12345")
    conn, addr = alice_socket.accept()
    print("I'm connected to Bob")

    ot_Alice(7893213, 11130010, conn)

    conn.close()
    alice_socket.close()

