Прежде чем начать пользоваться программой:
1. Установите браузер хром
https://www.google.com/intl/ru/chrome/safety/

2. Установить Хром драйвер
https://github.com/dreamshao/chromedriver
просто выберите натболее новую версию для вашей системы

3. скачайте компилятор VS code
https://code.visualstudio.com/download

4. Настройка VS code
зайдите в приложения
в верхнем левом углу нажмите file -> open folder
выберите папку в которой хотите хранить программу

затем сверху немного правее от file нажмите на terminal -> new terminal
в открывшевмся окне снизу наберите 

cd путь/к/вашей/папке

python -m venv venv

venv/Scripts/activate

pip install selenium

git clone https://github.com/ptrRUSSIAN/mangabuff_macro.git

должна скачаться библиотека

5. запустите программу
либо сверху на кнопку запуска либо прописав команду в терминале
python manga_macro.py

выберите 1 для первого входа, затем войдите в ваш аккаунт
после этого не закрывайте окно браузера а просто нажмите ENTER в терминале VS code

6. Настройте config.py по вашему жеданию
7. запустите файл повторно и наблюдайте за работой программы