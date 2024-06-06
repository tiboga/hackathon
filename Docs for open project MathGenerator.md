# 1. Скачивание всех необходимых библиотек.
Первое, что нужно знать, это то, что проект написан на Python. Убедимся, что он установлен. В противном случае скачаем по ссылке: https://www.python.org/getit/
![Pasted image 20240606215659.png](https://github.com/tiboga/hackathon/blob/Alexandro/Pasted%20image%2020240606215659.png)
После этого открываем консоль и скачиваем все нужные библиотеки:
```bash
pip install flask flask-login flask-wtf flask-restful sqlalchemy requests waitress matplotlib
```
# 2. Скачиваем проект с GitHub.
Прямая ссылка на репозиторий с проектом: https://github.com/tiboga/hackathon.git
Либо можно через консоль:
```bash
git clone https://github.com/tiboga/hackathon.git
```
# 3. Открываем проект в IDE.
Мы пользовались IDE **PyСharm Community Edition** и проект работал стабильно.
После открытия коренной папки советуем проверить наличие шага [[#1. Скачивание всех необходимых библиотек.]]
Открываем файл main.py
![Pasted image 20240606221536.png](https://github.com/tiboga/hackathon/blob/Alexandro/Pasted%20image%2020240606221536.png)
Видим это:
![Pasted image 20240606221657.png](https://github.com/tiboga/hackathon/blob/Alexandro/Pasted%20image%2020240606221657.png)
Запускаем его нажатием на кнопку.
![Pasted image 20240606221750.png](https://github.com/tiboga/hackathon/blob/Alexandro/Pasted%20image%2020240606221750.png)
В консоли появляется сообщение:
```bash
Подключение к базе данных по адресу sqlite:///db/main.db?check_same_thread=False
 * Serving Flask app 'main'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
http://127.0.0.1:5000 - ссылка на локальный сервер с запущенным проектом.
