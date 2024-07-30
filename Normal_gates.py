
class NormalGate:
    def __init__(self, input0, input1):
        self.input0 = input0
        self.input1 = input1


class AndGate(NormalGate):
    def __init__(self, input0=None, input1=None):
        super().__init__(input0, input1)

    def calc(self, input0=None, input1=None):
        if input0 is None:
            input0 = self.input0
        if input1 is None:
            input1 = self.input1
        return input0 & input1


class OrGate(NormalGate):
    def __init__(self, input0=None, input1=None):
        super().__init__(input0, input1)

    def calc(self, input0=None, input1=None):
        if input0 is None:
            input0 = self.input0
        if input1 is None:
            input1 = self.input1
        return input0 | input1


class XorGate(NormalGate):
    def __init__(self, input0=None, input1=None):
        super().__init__(input0, input1)

    def calc(self, input0=None, input1=None):
        if input0 is None:
            input0 = self.input0
        if input1 is None:
            input1 = self.input1
        return input0 ^ input1



class NormalCircuit:
    def __init__(self, self_gate, input_gate0, input_gate1):
        self.self_gate = self_gate # must be class NormalGate

        if isinstance(input_gate0, NormalCircuit):
            self.input_gate0 = input_gate0
        elif isinstance(input_gate0, NormalGate):
            self.input_gate0 = NormalCircuit(input_gate0, None, None)
        elif input_gate0 is None:
            self.input_gate0 = None

        if isinstance(input_gate1, NormalCircuit):
            self.input_gate1 = input_gate1
        elif isinstance(input_gate1, NormalGate):
            self.input_gate1 = NormalCircuit(input_gate1, None, None)
        elif input_gate1 is None:
            self.input_gate1 = None

    def to_dict(self):
        return {
            "self_gate": self.self_gate.to_dict(),
            "input_gate0": self.input_gate0.to_dict() if self.input_gate0 else None,
            "input_gate1": self.input_gate1.to_dict() if self.input_gate1 else None
        }

    def calc(self):
        # if input0 and input1 are not None, then we are at the input layer
        if self.input_gate0 is None and self.input_gate1 is None:
            return self.self_gate.calc()
        else:
            return self.self_gate.calc(self.input_gate0.calc(), self.input_gate1.calc())


# gates whose inputs are from gates in the deeper layer should set null as input
#
# gate1 = AndGate(1, 1)
# gate2 = OrGate(1, 0)
# gate3 = XorGate(0, 0)
# gate4 = AndGate()
# gate5 = OrGate()
#
# circuit1 = NormalCircuit(gate5,
#                          NormalCircuit(gate4,
#                                        NormalCircuit(gate3, None, None),
#                                        NormalCircuit(gate2, None, None)),
#                          NormalCircuit(gate1, None, None))

# print(circuit1.calc())



