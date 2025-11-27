import argparse
import csv
import struct
import os

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

def create_instruction(opcode, b, c):
    instruction_int = 0
    if opcode == OP_LOAD_CONST:
        # A: 0-2(3 бита), B: 3-14 (12 бит), C: 15-32 (18 бит)
        instruction_int = (opcode & 0x7) | ((b & 0xFFF) << 3) | ((c & 0x3FFFF) << 15)
    else:
        # A: 0-2(3 бита), B: 3-20 (18 бит), C: 21-38 (18 бит)
        instruction_int = (opcode & 0x7) | ((b & 0x3FFFF) << 3) | ((c & 0x3FFFF) << 21)

    # Возвращаем словарь с исходными данными и собранным числом
    return {
        "A": opcode,
        "B": b,
        "C": c,
        "int_val": instruction_int
    }

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

            # Выбираем код операции в зависоимости от имени команды
            if cmd == "LOAD_CONST":
                instructions.append(create_instruction(OP_LOAD_CONST, op1, op2))
            elif cmd == "READ_MEM":
                instructions.append(create_instruction(OP_READ_MEM, op1, op2))
            elif cmd == "WRITE_MEM":
                instructions.append(create_instruction(OP_WRITE_MEM, op1, op2))
            elif cmd == "ABS":
                instructions.append(create_instruction(OP_ABS, op1, op2))
            else:
                print(f"Unknown command: {cmd}")

    return instructions

def write_binary(instructions, output_path):
    with open(output_path, "wb") as f:
        for instr in instructions:
            val = instr["int_val"]
            # Записываем 5 байт
            bytes_val = struct.pack("<Q", val)[:5]
            f.write(bytes_val)

def print_test_mode(instructions):
    print("Test Mode:")
    for idx, instr in enumerate(instructions):
        # Форматируем вывод байтов для проверки
        val = instr["int_val"]
        bytes_val = struct.pack('<Q', val)[:5]
        hex_str = ", ".join(f"0x{b:02X}" for b in bytes_val)
        print(f" {idx}: A={instr['A']}, B={instr['B']}, C={instr['C']}")
        print(f"    {hex_str}")

def main():
    args = parse_args()
    ir = assemble(args.input_file)
    if args.test:
        print_test_mode(ir)

    write_binary(ir, args.output_file)

    size = os.path.getsize(args.output_file)
    print(f"Размер двоичного файла: {size} байт")

if __name__ == "__main__":
    main()
