from tkinter import *
from tkinter import messagebox
from random import randint

def pressKey(event):
    # print(f'Клавиша: {event.keycode}, символ {event.char.upper()}')
    if (event.keycode == 17):  # Чит на CTRL
        wordLabel['text'] = wordComp
    ch = event.char.upper()  # Получаем символ с клавиши
    if (len(ch) == 0):
        return 0
    codeBtn = ord(ch) - st
    if (codeBtn >= 0 and codeBtn <= 32):  # Определяем порядковый номер нажатой буквы в рус алфавите
        pressLetter(codeBtn)

def updateInfo():  # Обновляем инфу об очках и тд
    scoreLabel['text'] = f"Ваши очки: {score}"
    topScoreLabel['text'] = f'Лучший результат: {topScore}'
    userTryLabel['text'] = f'Осталось попыток: {userTry}'

def getWordsFromFile():  # Загружаем слова их файла в список
    ret = []  # Список для возвращаемого результата
    try:  # Блок проверки ошибок
        f = open('words.txt', 'r', encoding='utf-8')  # Дескриптор
        for l in f.readlines():  # Читаем построчно
            l = l.upper()
            l = l.replace("\n", '')  # Убираем символ переноса строки аля ENTER
            ret.append(l)
        f.close()
    except:
        print('Файл не найден или поврежден/переименован')
        quit(0)
    return ret

def startNewRound():  # Начинает новый раунд с новым словом и выводит его на экран
    global wordStar, wordComp, userTry  # При помощи global мы можем изменять глобальные переменные
    wordComp = dictionary[randint(0, len(dictionary) - 1)]
    wordStar = '-' * len(wordComp)
    wordLabel['text'] = wordStar
    wordLabel.place(x=WIDTH // 2 - wordLabel.winfo_reqwidth() // 2, y=50)
    for i in range(32):
        btn[i]['text'] = chr(st + i)
        btn[i]['state'] = 'normal'
    userTry = 10
    updateInfo()

def saveTopScore():  # Сохраняет рекорд в файл
    global topScore
    topScore = score
    try:
        f = open('topchik.txt', 'w', encoding='utf-8')
        f.write(str(topScore))
        f.close()
    except:
        messagebox.showinfo('Ошибка', 'Возникла проблема с сохранением очков')

def getTopScore():  # Возвращает макс значение очков из файла
    try:
        f = open('topchik.txt', 'r', encoding='utf-8')
        m = int(f.readline())
        f.close()
    except:
        m = 0
    return m

def compareWord(s1,s2):  # Сравниваем строки и считаем различия в них
    res = 0  # Возвращемый результат
    for i in range(len(s1)):  # Сравниваем строки посимвольно
        if (s1[i] != s2[i]):
            res += 1  # Если символы разные, то увеличиваем рез
    print(f"Совпадений найдено: {res}")
    return res

def getWordStar(ch):  # Изменяет строку, когда ползователь угадал букву
    ret = ''
    for i in range(len(wordComp)):
        # Сравниваем символы
        if (wordComp[i] == ch):
            ret += ch
        else:
            ret += wordStar[i]
    return ret

def pressLetter(n):
    '''Считывает нажатие кнопки и выключает её, выводя в другие ф-ции значения нажатой кнопки
Также начисление очков за победу, проверка победы, начисление очков по ходу игры, отнимание кол-ва попыток'''
    global wordStar, score, userTry
    if (btn[n]['text'] == '.'):  # Если кнопка нажата (вместо нее точка), то прерываем метод
        return 0
    btn[n]['text'] = '.'
    btn[n]['state'] = 'disabled'  # Выключаем кнопку, больше нельзя нажать
    oldWordStar = wordStar  # Временная переменная
    wordStar = getWordStar(chr(st + n))  # Получаем строку с открытыми символами
    count = compareWord(wordStar, oldWordStar)  # Находим различие между старой и новой строкой
    wordLabel['text'] = wordStar
    # Считаем очки
    if (count > 0):
        score += count * 10
    else:
        score -= 20
        if (score < 0):
            score = 0
        userTry -= 1
    # Сравниваем загадонное слово с содержимым wordStar
    if (wordStar == wordComp):
        score += score // 2  # Добавляем 50% очков
        updateInfo()  # Обнова инфы
        if (score > topScore):
            messagebox.showinfo("Красава!", f'Слово угадано: {wordComp}! Набрали рекорд!')
            saveTopScore()
        else:
            messagebox.showinfo("Угадали!", f'Слово угадано: {wordComp}')
        startNewRound()
    elif (userTry <= 0):
        messagebox.showinfo('Проебали!!', 'Все попытки просрали, но ничего, в следующий раз залетит!')
        quit(0)

    updateInfo()




# Создание окна
root = Tk()  # ссылка на окно в памяти, всегда обозначать///Начало блока окна
root.bind('<Key>', pressKey)  # обработчик клавиш
root['bg'] = 'pink'
root.resizable(False, False)  # запрещаем изменение размеров окна
root.title('Угадай слово by Vano')  # заголовок

# Настройка геометрии окна
WIDTH = 810
HEIGHT = 320

# Получаем ширину и высоту экрана пользователя
SCR_WIDTH = root.winfo_screenwidth()
SCR_HEIGHT = root.winfo_screenheight()

# Вычисление точки расположения окна игры на экране пользователя
POS_X = SCR_WIDTH // 2 - WIDTH // 2
POS_Y = SCR_HEIGHT // 2 - HEIGHT // 2

# Устанавливаем нужные параметры окна
root.geometry(f'{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}')

# root.geometry(f'{810}x{320}+{root.winfo_screenwidth() // 2 - 810 // 2}+{root.winfo_screenheight() // 2 - 320 // 2}')

# Метки для вывода слова, которое человек угадывает в текущем раунде, очков, рекорда и попыток
wordLabel = Label(font='consolas 35')
scoreLabel = Label(font=', 12')
topScoreLabel = Label(font=', 12')
userTryLabel = Label(font=', 12')

# Устанавливаем на места метки
scoreLabel.place(x=10, y=165)
topScoreLabel.place(x=10, y=190)
userTryLabel.place(x=10, y=215)

# Хранение значений
score = 0
topScore = getTopScore()  # Рекорд игры
userTry = 10

# Создание и размещение кнопок алфавита
st = ord('А')  # Код символа
btn = []
for i in range(32):
    btn.append(Button(text=chr(st + i), width=2, font='consolas 15'))  # Добавление кнопок в список по индексам
    btn[i].place(x=215 + (i % 11) * 35, y=150 + i // 11 * 50)  # Размещение кнопок
    btn[i]['command'] = lambda x=i: pressLetter(x)  # Анонимная функция, можно записать лишь одно значение или выражение

wordComp = ''  # Загадонное слово
wordStar = ''  # Слово со звездочками

#Словарь
dictionary = getWordsFromFile()

# Начало игры
startNewRound()

root.mainloop()  # Конец блока окна
