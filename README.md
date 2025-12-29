Прежде чем начать пользоваться программой:

1. Установите браузер Chrome
https://www.google.com/intl/ru/chrome/safety/

2. Установите ChromeDriver
https://github.com/dreamshao/chromedriver
Просто выберите наиболее новую версию для вашей системы. После скачивания распакуйте архив в удобную папку. На Windows достаточно распаковать и запустить chromedriver.exe, чтобы все работало.

3. Скачайте и установите VS Code
https://code.visualstudio.com/download

4. Настройка VS Code
Зайдите в приложение.
В верхнем левом углу нажмите File -> Open Folder.
Выберите папку, в которой хотите хранить программу.

Затем сверху, немного правее от File, нажмите Terminal -> New Terminal.
В открывшемся окне снизу наберите следующие команды:

cd путь/к/вашей/папке

python -m venv venv

# Активация виртуального окружения (зависит от ОС):
# Для Windows:
venv\Scripts\activate
# Для Linux/Mac:
venv/bin/activate

pip install selenium

git clone https://github.com/ptrRUSSIAN/mangabuff_macro.git

Должна скачаться библиотека.

5. Запустите программу
Либо сверху на кнопку запуска, либо прописав команду в терминале:
python manga_macro.py

Выберите 1 для первого входа, затем войдите в ваш аккаунт.
После этого не закрывайте окно браузера, а просто нажмите ENTER в терминале VS Code.

6. Настройте config.py по вашему желанию
7. Запустите файл повторно и наблюдайте за работой программы.