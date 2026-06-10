import os
import sys

try:
    def get_me():
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        return script_dir

    root_dir = os.path.dirname(get_me())
    data_file = os.path.join(root_dir, 'current_user_data.txt')

    # Читаем данные из файла
    with open(data_file, 'r', encoding='utf-8') as file:
        other = [line.rstrip('\n') for line in file.readlines()]

    # Получаем целевой путь: из аргумента или из файла
    target = sys.argv[1] if len(sys.argv) > 1 else other[1]

    # Обрабатываем специальные случаи
    if target == "-":
        target = other[2]  # предыдущий каталог
    elif target.startswith("/"):
        # Абсолютный путь — оставляем как есть
        pass
    elif target.startswith("~"):
        # Домашняя директория — расширяем ~
        target = os.path.expanduser(target)
    else:
        target = os.path.join(other[0], target)  # относительный путь от текущего каталога

    # Преобразуем в абсолютный путь
    target = os.path.abspath(target)

    # Проверяем существование директории
    if not os.path.exists(target):
        print(f"[False, Директория не существует: {target}]")
        sys.exit(1)

    if not os.path.isdir(target):
        print(f"[False, Это не директория: {target}]")
        sys.exit(1)

    # Обновляем файл данных
    with open(data_file, 'w', encoding='utf-8') as file:
        file.write(f"{target}\n{other[1]}\n{other[0]}")

    # Выводим новый путь для использования в оболочке
    print(target)

except Exception as err:
    print([False, err])
    sys.exit(1)
