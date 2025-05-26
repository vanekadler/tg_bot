file_path = r"C:\Users\Notebook23\Downloads\tg_bot\tg_bot\price.pdf"

try:
    with open(file_path, "rb") as f:
        print("Файл найден и открыт успешно!")
except FileNotFoundError:
    print("Файл НЕ найден. Проверь путь.")
except Exception as e:
    print(f"Ошибка при открытии файла: {e}")