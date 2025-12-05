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



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Путь к YAML файлу")
    parser.add_argument("output", help="пусто")
    parser.add_argument("--test", action="store_true", help="вывод(режим тестирования)")

    args = parser.parse_args()

    ir = parse_yaml_to_ir(args.source)

    if args.test:
        print_ir(ir)


if __name__ == "__main__":
    main()