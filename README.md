## demoGC

### Introduction

一个基于姚氏混淆电路的MPC实现。可以进行 [1, 2^32] 整数的秘密比较，可以进行模任意2的整数次方加法

### Environment

python = 3.10.4

### Usage

- secure comparison:

  在 `GC_Alice.py` 文件中设置 `input0` 为 Alice 的输入，在 `GC_Bob.py` 文件中设置 `input0` 为 Bob 的输入，先运行 Alice，再运行 Bob，即可进行比较。程序运行将占用12345端口。为避免套接字乱序，程序中设置有 `sleep` 语句，程序运行将持续30s左右.

- modular addition:

  在 `GC_add_Alice.py` 文件中设置 `input0` 为 Alice 的输入，在 `GC_add_Bob.py` 文件中设置 `input0` 为 Bob 的输入；分别设置两个文件中的 `mod` 为模数（ mod = n 表示模 2^(n+1) 加法）先运行 Alice，再运行 Bob，即可进行模加法。

### Structure

部分文件和重要方法介绍如下：

- `GC_Alice.py` 、`GC_Bob.py` 、`GC_add_Alice.py` 、`GC_add_Bob.py`:

  分别是 Alice、Bob 进行 secure comparison 和 modular addition 的主函数。

- `Encrypted_gates.py`

  定义了混淆电路中电路的类。包括：

  - `EncGate`: 加密布尔门。内部存储四个可能的加密输出，在 Alice 对其初始化过后会连同可能输出发送给 Bob
  - `Circuit`: 电路结构。因为安全比较需要重复的布尔逻辑单元，将加密布尔门组合成为电路封装，方便后续将电路的发送和计算。电路的计算仅接受加密布尔门作为输入，单独的数字输入将被转化为一个 `& 1` 的加密与门。
  - `EncAdder`: 加密全加器，实现安全模加法的单元。因为安全比较已经尝试过布尔门的组合，全加器如果布尔门的组合来表示，可能要封装成两个电路（因为每次计算有2个输出，即 `sum` 和 `carry` ），可能会使电路很复杂。于是将整个加法逻辑单元封装成3个输入、2个输出的算数逻辑门，简化电路结构。

- `Encrypted_function.py`:

  定义了 Alice 在加密电路可能用到的方法。

  - `randomize_gate_io` 和 `define_gate_i`: 初始化加密布尔门。随机化布尔门的输入和输出，并将真值表转化为 json 对象储存在 `table.txt` 中。前者是随机化输入，后者是指定门的输入，二者都会随机生成后缀为12bit 的 `0` 的输出。如果在参数中指定 `input_gate0_id` 和 `input_gate1_id` ，将会取这些id对应的门的输出作为自己的输入，方便Bob的解密。
  - `randomize_adder_io`: 初始化加密全加器。支持指定全加器的输出作为自己的输入。将全加器真值表转化为 json 对象储存在 `table_add.txt` 中。
  - `circuit_initialize`、`add_circuit_initialize`: 加法电路和比较电路的初始化，包括初始化电路循环单元中的各个门、将部分门的输入输出联系起来。
  -  `send_input_to_bob`、 `adder_send_input_to_bob`: 在安全比价和安全模加法中和 Bob 交换数据，其中包括发送自己的输入、和 Bob 进行 OT 协议使 Bob 拿到自己输入对应的随机数。

- `Decrypt_function.py`:

  定义了 Bob 在解密的时候可能用到的方法。

  - `dec_bit_compare`: 在安全比较中用于计算 `Circuit` 的输出
  - `get_input_from_alice` 、`get_add_input_from_alice`: 分别在安全比较和安全模加法中拿到 Alice 的输入、用 OT 协议拿到自己输入对应的随机数。

- `OT_Alice.py` 、`OT_Bob.py`: 

  分别是 Alice 和 Bob 进行 OT 协议的方法。

- `utils.py`:

  定义了一系列方便操作的方法。

### Notes

项目仅为学习测试，未在效率和稳定性上做任何优化。仅用于了解 GC 基本实现。