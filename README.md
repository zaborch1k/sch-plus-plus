<picture>
 <source media="(prefers-color-scheme: dark)" srcset="sch1++.png">
 <source media="(prefers-color-scheme: light)" srcset="sch1++.png">
 <img alt="sch1++" src="sch1++.png">
</picture>

# SCH1++ (SCHool educational 1nterpreter)

***Прилагаются ссылки на файл с документацией и видеоролик, демонстрирующий работу программы (см. [url.md](https://github.com/zaborch1k/sch-plus-plus/blob/main/url.md))***

## Руководство для пользователей
### Установка
1. Скачайте файл по [ссылке](https://disk.yandex.ru/d/MFuoQeEjXR8Npw). ***Примечание: к сожалению, язык находиться в стадии разработки, поэтому не все устройства поддерживаются.***
2. Кликните дважды на установленный файл формата `.exe` (если Вы видите что-то вроде "браузер заблокировал этот файл как небезопасный", заставьте браузер его разблокировать. Обычно для этого достаточно выбрать "все равно скачать"/"файл безопасный"). Когда файл начнет запускаться, ОС будет этим недовольна и предупредит Вас о возмоной опасности и подозрительности этого файла, но мы-то знаем, что это не так, верно? В случае с windows, нажмите "подробнее", затем "все равно запустить файл" (в остальных системах аналогично).
3. Браво, Вы это сделали! Теперь Вы, если все прошло успешно, видите некрасивое окно терминала. НЕ ЗАКРЫВАЙТЕ ЕГО, НИКТО НЕ ИДЕАЛЕН! Если оно очень сильно смущает Вас - просто сверните. Дождитесь появления окна с интерпретатором (наверху будет наша эмблема).
### Пользование
Перед Вами главное окно - 4 кнопки и поле для ввода снизу. 
* Кнопка RUN отвечает за запуск кода. Когда Вы ввели код в поле для ввода/открыли уже имеющийся файл - можете ее нажать и проверить работу Вашего кода.
* Кнопка STOP - за остановку выполнения кода и возвращения исполнителся на исходную точку
* Кнопка SAVE позволяет сохранить Ваш код на любое место на Вашем компьютере
* Кнопка OPEN открывает любой файл (формата `.txt`!) из Вашего компьютера
### Синтаксис
Ниже представлен синтаксис языка, все команды и их использование (N - любое натуральное число от 1 до 1000; переменная, имеющая значение числа в данном интервале; выражение (с операторами +-*/ и ()), выполнив которое получится число, принадлежащее данному интервалу (например `x+3`)):
1. Команды, изменяющие положение исполнителя в данном направлении
- RIGHT/LEFT/UP/DOWN N
- Пример: `RIGHT 4`
2. Условные блоки
- IFBLOCK DIR -> проверить наличие края сетки в направлении DIR (RIGHT/UP/LEFT/DOWN). В случае наличия - выполнить следующий блок команд до ENDIF.
- Обязательно наличие ENDIF и отступов в 4 пробела!
- Пример:
```
IFBLOCK RIGHT
   LEFT 3
   RIGHT 4
ENDIF
```
3. Циклы
- REPEAT N -> повторяет блок до ENDREPEAT N раз
- Обязательно наличие ENDREPEAT и отступов в 4 пробела!
- Пример:
```
REPEAT 4
   LEFT 3
ENDREPEAT
```
4. Объявление переменных
- SET <имя переменной> = N -> задает значение переменной равное N
- Пример: `SET x = 2`
5. Процедуры
  
    a) Объявление
    - PROCEDURE <имя процедуры> -> начать определение процедуры с данным именем
    - Обязательно наличие ENDPROC и отступов в 4 пробела!
    - Пример:
   ```
   PROCEDURE x
    RIGHT 4
   ENDPROC
   ```
    b) Вызов
    - СALL <имя процедуры> -> выполняет блок процедуры
    - Пример: `CALL d`
  

## Руководство для разработчиков
### Описание строения программных файлов
Для фунцкциональной схемы можете посмортеть [*документацию*](). Краткое описание будет тут.
Наша программа состоит из нескольких файлов. 
1. Главный - `gui.py`. Именно он запускается первым, а затем вызывает остальных. Основные функции и детали:
* `resource_path(path)` -> возвращает полный путь к файлу по его короткому пути. Нужна, чтобы находить файлы (например, с иконкой) на компьютерах пользователей
* `prog_space` -> главное окно, создается с помощью Tkinter
* `create_polygon()` -> создает полигон, если окно запущено в первый раз
* `run_polygon()` -> создает полигон при нажатии RUN, один раз вызывает `create_polygon()`. Обрабатывает введенные данные, отправляет `interp.py` (`get_data()`), получает их и отрисовывает полигон (`window.performer.update`)
*  `kill_polygon()` -> останавливает исполнение, возвращает в начальную точку исполнителя
*  `save_file()` -> записывает файлы в БД (если SAVE)
*  `open_file()` -> открывает файлы из БД (если OPEN)
*  `error_msg(txt)` -> вызывает сообщения об ошибках
*  `class Performer` -> наследник `arcade.Sprite`, "исполнитель". Точка, движущаяся по экрану -> метод `update(dir, num)` для обновленной отрисовки
*  `class Polygon` -> наследник `arcade.Window`, полигон -> метод `on_draw()` для отрисовки самого себя
2. `interp.py` - интерпретатор. Основные функции и детали:
 *  `get_data(data)` -> получает данные из `gui.py`. Возвращает результат `do_interp(data)`
 *  `do_interp(data)` ->  создает экземпляр `i` класса `Interp` и передает ему результат `parse(data)` из `lexparse.py`. Возвращает результат `i.run()`
 *  `class Interp` -> исполняет полученные (уже пропарсенные) данные; главный метод -> `run()`, возвращает результат формата `(self.qmove, self.error, self.qpos)`, где `self.qmove` - список передвижений (формат `[[dir, num],])`/`None`), `self.error` - тстрока-сообщение об ошибке/`None`, `self.qpos` - список позиций исполнителя (формата `[[x, y],]`/`None`).
3. `lexparse.py` - файл лексер+парсер. Набор грамматических правил и токенов, создан на PLY (Python Lex Yacc). Основные функции и детали:
 *  `class IndentLex` ->  доп. лексер для обработки отступов (кроме этого ничего не делает)
 *  `parse(data)` -> парсит данные, создает лексер, парсер PLY и `IndentLex`
### БОНУС 
Вы думали, мы оставили консоль, потому что ленивые? О нет, это скорее фича и пасхалочка. В исходном коде есть одна не влияющая на работу программы ошибка. Мы сделали своего рода квест для тебя, *разработчик!*
