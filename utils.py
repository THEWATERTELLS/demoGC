import json

MOD = 10000000000037

def gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = gcd(b % a, a)
        return g, y - (b // a) * x, x

def modinv(a, m):
    g, x, y = gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def enc(key, value):
    global MOD
    return (key * value + 97 * key) % MOD

def dec(key, cipher):
    global MOD
    return ((cipher - 97 * key) % MOD) * modinv(key, MOD) % MOD

def num_to_list(num, maxlen=None):
    if maxlen == None:
        maxlen = 32
    bin_str = bin(num)[2:]
    bin_str = bin_str.zfill(maxlen)
    bin_list = [int(bit) for bit in bin_str]
    return bin_list

def list_to_num(bin_list):
    bin_str = ''.join([str(bit) for bit in bin_list])
    return int(bin_str, 2)

def fetch(file, round):
    # rounds start from 0
    with open(file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        gate1_info = json.loads(lines[round * 5])
        gate2_info = json.loads(lines[round * 5 + 1])
        gate3_info = json.loads(lines[round * 5 + 2])

        c_0_for_gate1 = gate1_info["ix0"]
        c_1_for_gate1 = gate1_info["ix1"]
        a_0_for_gate1 = gate1_info["iy0"]
        a_1_for_gate1 = gate1_info["iy1"]

        c_0_for_gate2 = gate2_info["ix0"]
        c_1_for_gate2 = gate2_info["ix1"]
        b_0_for_gate2 = gate2_info["iy0"]
        b_1_for_gate2 = gate2_info["iy1"]

        a_0_for_gate3 = gate3_info["ix0"]
        a_1_for_gate3 = gate3_info["ix1"]
        true_for_gate3 = gate3_info["iy1"]

    return {
        "gate1": {
            "c_0": c_0_for_gate1,
            "c_1": c_1_for_gate1,
            "a_0": a_0_for_gate1,
            "a_1": a_1_for_gate1
        },
        "gate2": {
            "c_0": c_0_for_gate2,
            "c_1": c_1_for_gate2,
            "b_0": b_0_for_gate2,
            "b_1": b_1_for_gate2
        },
        "gate3": {
            "a_0": a_0_for_gate3,
            "a_1": a_1_for_gate3,
            "true": true_for_gate3
        }
    }

def adder_fetch(file, round):
    # round starts from 0
    with open(file, "r", encoding="utf-8") as file:
        lines = file.readlines()
        gate_info = json.loads(lines[round])

    return {
        "gate_id": gate_info["gate_id"],
        "a0": gate_info["a0"],
        "a1": gate_info["a1"],
        "b0": gate_info["b0"],
        "b1": gate_info["b1"],
        "cin0": gate_info["cin0"],
        "cin1": gate_info["cin1"]
    }

