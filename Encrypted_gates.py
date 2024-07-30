import json
import Normal_gates
from utils import enc, dec

def gate_from_dict(gate_json):
    # recursively load a gate from a json object.
    generated_gate = EncGate(0, 0, 0, 0, 0)
    generated_gate.gate_id = gate_json["gate_id"]
    generated_gate.po00 = gate_json["po00"]
    generated_gate.po01 = gate_json["po01"]
    generated_gate.po10 = gate_json["po10"]
    generated_gate.po11 = gate_json["po11"]
    return generated_gate


def circuit_from_dict(circuit_json):
    # recursively load a circuit from a json object.
    generated_circuit = Circuit(None, None, None)

    generated_circuit.self_gate = gate_from_dict(circuit_json["self_gate"])
    if circuit_json["input_gate0"] is not None:
        generated_circuit.input_gate0 = circuit_from_dict(circuit_json["input_gate0"])
    else:
        generated_circuit.input_gate0 = None

    if circuit_json["input_gate1"] is not None:
        generated_circuit.input_gate1 = circuit_from_dict(circuit_json["input_gate1"])
    else:
        generated_circuit.input_gate1 = None

    return generated_circuit

def adder_from_dict(adder_json):
    generated_adder = EncAdder(0, [], [])
    generated_adder.gate_id = adder_json["gate_id"]
    generated_adder.pso = adder_json["pso"]
    generated_adder.pco = adder_json["pco"]
    return generated_adder

class EncGate:
    def __init__(self, gate_id, po00, po01, po10, po11, input0=None, input1=None):
        # po stands for possible output
        self.gate_id = gate_id
        self.input0 = input0
        self.input1 = input1
        self.po00 = po00
        self.po01 = po01
        self.po10 = po10
        self.po11 = po11

    def calc(self, input0=None, input1=None):

        if input0 is None:
            if self.input0 is None:
                raise Exception("input0 is None at some gate")
            input0 = self.input0
        if input1 is None:
            if self.input1 is None:
                raise Exception("input1 is None at some gate")
            input1 = self.input1

        o00 = dec(input1, dec(input0, self.po00))
        o01 = dec(input1, dec(input0, self.po01))
        o10 = dec(input1, dec(input0, self.po10))
        o11 = dec(input1, dec(input0, self.po11))

        # using a postfix of 12 bits of '0's to mark the valid output
        # if more than 1 output is valid, raise an exception

        result = 0
        if o00 % 0x1000 == 0:
            result += 1

        if o01 % 0x1000 == 0:
            result += 2

        if o10 % 0x1000 == 0:
            result += 4

        if o11 % 0x1000 == 0:
            result += 8

        if result == 1:
            return o00
        elif result == 2:
            return o01
        elif result == 4:
            return o10
        elif result == 8:
            return o11
        else:
            raise Exception("no or more than 1 possible output is valid")

    def to_dict(self):
        return {
            "gate_id": self.gate_id,
            "po00": self.po00,
            "po01": self.po01,
            "po10": self.po10,
            "po11": self.po11
        }


class Circuit:

    def __init__(self, self_gate, input_gate0, input_gate1):

        self.self_gate = self_gate  # must be class EncGate

        # input_gate0 and input_gate1 must be class Circuit.
        if isinstance(input_gate0, Circuit):
            self.input_gate0 = input_gate0
        elif isinstance(input_gate0, EncGate):
            self.input_gate0 = Circuit(input_gate0, None, None)
        elif input_gate0 is None:
            self.input_gate0 = None

        if isinstance(input_gate1, Circuit):
            self.input_gate1 = input_gate1
        elif isinstance(input_gate1, EncGate):
            self.input_gate1 = Circuit(input_gate1, None, None)
        elif input_gate1 is None:
            self.input_gate1 = None

    def to_dict(self):
        return {
            "self_gate": self.self_gate.to_dict(),
            "input_gate0": self.input_gate0.to_dict() if self.input_gate0 else None,
            "input_gate1": self.input_gate1.to_dict() if self.input_gate1 else None
        }

    def calc(self):
        # in practise, the 2 input_gate should both be None or both be class Circuit
        if self.input_gate0 is None and self.input_gate1 is None:
            return self.self_gate.calc()
        elif isinstance(self.input_gate0, Circuit) and isinstance(self.input_gate1, Circuit):
            return self.self_gate.calc(self.input_gate0.calc(), self.input_gate1.calc())
        else:
            raise Exception("inputs are not both None or both Circuit")


class EncAdder:

    def __init__(self, gate_id, pso, pco):
        self.gate_id = gate_id
        #p stand for possible, s stands for sum, c stands for carry, pso and pco are lists
        self.pso = pso
        self.pco = pco

    def calc(self, a, b, cin):
        so = []
        flags = 0
        real_so = None
        for i in self.pso:
            ans = dec(cin, dec(b, dec(a, i)))
            so.append(ans)
            if ans % 0x1000 == 0:
                flags += 1
                real_so = ans

        co = []
        flagc = 0
        real_co = None
        for i in self.pco:
            ans = dec(cin, dec(b, dec(a, i)))
            co.append(ans)
            if ans % 0x1000 == 0:
                flagc += 1
                real_co = ans

        if flags != 1 or flagc != 1:
            raise Exception("no or more than 1 possible output is valid")
        else:
            return real_so, real_co

    def to_dict(self):
        return {
            "gate_id": self.gate_id,
            "pso": self.pso,
            "pco": self.pco
        }
