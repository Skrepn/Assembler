import argparse
import csv

# Коды операций
OP_LOAD_CONST = 5
OP_READ_MEM = 3
OP_WRITE_MEM = 7
OP_ABS = 4

def parse_args():
    # Парсим аргументы командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument("--test", action="store_true")
    return parser.parse_args()

def assemble(input_path):
    instructions = []

    with open(input_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            # Пропускаем пустые строки
            if not row:
                continue

            # Получаем имя команды
            cmd = row[0].strip().upper()
            try:
                # Получаем операнды
                op1 = int(row[1])
                op2 = int(row[2])
            except ValueError:
                print(f"Error parsing operands in row: {row}")
                continue

            instr = {"A": 0, "B": op1, "C": op2}

            if cmd == "LOAD_CONST":
                instr["A"] = OP_LOAD_CONST
            elif cmd == "READ_MEM":
                instr["A"] = OP_READ_MEM
            elif cmd == "WRITE_MEM":
                instr["A"] = OP_WRITE_MEM
            elif cmd == "ABS":
                instr["A"] = OP_ABS
            else:
                print(f"Unknown command: {cmd}")
                continue

            instructions.append(instr)

    return instructions

def print_test_mode(instructions):
    print("Test Mode:")
    for idx, instr in enumerate(instructions):
        print(f" {idx}: A={instr['A']}, B={instr['B']}, C={instr['C']}")

def main():
    args = parse_args()
    ir = assemble(args.input_file)
    if args.test:
        print_test_mode(ir)

if __name__ == "__main__":
    main()
