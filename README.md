# Бот для кино

Устанавливаем `virtualenv` и активируем виртуальное окружение: 
```
pip install virtualenv
virtualenv venv
source venv/Scripts/activate
```

Скачиваем нужные библиотеки: 
```
pip install -r requirements.txt
```

Так же нужно определить `BOT_TOKEN` и `ADMINS`
```
export BOT_TOKEN=Ваш токен
export ADMINS=id1
```

Запускаем
```
python app.py
```