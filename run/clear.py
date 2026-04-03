import ctypes
import platform

def windows_clear():
    # 1. Получаем дескриптор стандартного вывода (STDOUT)
    # -11 — это константа STD_OUTPUT_HANDLE
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    
    # 2. Получаем информацию о буфере консоли (размер, положение курсора)
    csbi = ctypes.create_string_buffer(22)
    res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
    
    if res:
        import struct
        # Распаковываем данные о ширине и высоте консоли
        _, _, _, _, _, left, top, right, bottom, _, _ = struct.unpack("hhhhHhhhhhh", csbi.raw)
        width = right - left + 1
        height = bottom - top + 1
        size = width * height
        
        # 3. Заполняем консоль пробелами (очистка текста)
        written = ctypes.c_ulong()
        coords = ctypes.c_ulong(0) # Координаты (0,0)
        ctypes.windll.kernel32.FillConsoleOutputCharacterW(handle, ord(' '), size, coords, ctypes.byref(written))
        
        # 4. Сбрасываем атрибуты (цвета) и возвращаем курсор в (0,0)
        ctypes.windll.kernel32.FillConsoleOutputAttribute(handle, 0x0007, size, coords, ctypes.byref(written))
        ctypes.windll.kernel32.SetConsoleCursorPosition(handle, coords)
    return 0

if list(platform.platform())[1] == 'Windows':
    windows_clear()
else:
    print('\033c')