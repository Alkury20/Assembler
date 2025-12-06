import argparse
import yaml


OPCODES = {
    "const": 14,
    "load": 0,
    "store": 3,
    "add": 8
}

def parse_yaml_to_ir(path):
    with open(path, 'r') as f:
        program = yaml.safe_load(f)

    ir_program = []

    for instr in program:
        mnemonic = list(instr.keys())[0]
        args = instr[mnemonic]

        if mnemonic not in OPCODES:
            raise ValueError(f"Неизвестная команда: {mnemonic}")

        A = OPCODES[mnemonic]

        # Общие поля
        B = args.get("B")
        C = args.get("C")
        D = args.get("D")

        entry = {"A": A}

        if B is not None:
            entry["B"] = B
        if C is not None:
            entry["C"] = C
        if D is not None:
            entry["D"] = D

        ir_program.append(entry)

    return ir_program

def print_ir(ir):
    for i, instr in enumerate(ir):
        print(f"\nПример {i + 1}:")
        for k, v in instr.items():
            print(f"  {k}: {v}")


def ir_to_machine_code(ir):
    machine_code = bytearray()
    
    for instr in ir:
        A = instr["A"]
        B = instr.get("B", 0)
        C = instr.get("C", 0)
        D = instr.get("D")

        byte0 = ((C & 1) << 7) | ((B & 0x7) << 4) | (A & 0xF)
        machine_code.append(byte0)
        
        if D is not None:
            byte1 = ((D & 0x7) << 6) | ((C >> 1) & 0x3F)
            machine_code.append(byte1)
            machine_code.extend([0x00, 0x00, 0x00])
        else:
            c_shifted = C >> 1
            machine_code.append((c_shifted >> 0) & 0xFF)
            machine_code.append((c_shifted >> 8) & 0xFF)
            machine_code.append((c_shifted >> 16) & 0xFF)
            machine_code.append((c_shifted >> 24) & 0xFF)
    return bytes(machine_code)


def print_machine_code(machine_code):
    for i in range(0, len(machine_code), 5):
        cmd_bytes = machine_code[i:i+5]
        hex_str = ", ".join([f"0x{b:02X}" for b in cmd_bytes])
        print(hex_str)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Путь к YAML файлу")
    parser.add_argument("output", help="Путь к двоичному файлу-результату")
    parser.add_argument("--test", action="store_true", help="Режим тестирования")

    args = parser.parse_args()

    ir = parse_yaml_to_ir(args.source)
    machine_code = ir_to_machine_code(ir)

    with open(args.output, 'wb') as f:
        f.write(machine_code)

    print(f"Размер двоичного файла: {len(machine_code)} байт")
    
    if args.test:
        print("\nПромежуточное представление:")
        print_ir(ir)
        print("\nМашинный код (байтовый формат):")
        print_machine_code(machine_code)


if __name__ == "__main__":
    main()