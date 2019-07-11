from tkinter import *
import random

#переменные
# настройка окна

WIDTH = 1000
HEIGHT = 500
#настройка ракеток

PAD_W = 10
PAD_H = 100

# Настройка мяча

BALL_RADIUS = 30

# Устанвливаем окно

root = Tk()
root.title("PythonGameTable")

# animation

c = Canvas(root, width = WIDTH, height = HEIGHT, background = "#003300")
c.pack()

# Элементы поля

# Левая сторона

c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill = "white")

#правая сторона

c.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill = "white")

# Централбная линия

c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill = "white")

# Установка игровых объектов

BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2,
                     HEIGHT/2-BALL_RADIUS/2,
                     WIDTH/2+BALL_RADIUS/2,
                     HEIGHT/2+BALL_RADIUS/2, fill="white")

# создаем ракетки

LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width=PAD_W, fill="yellow")
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2,
                          PAD_H, width=PAD_W, fill="yellow")

#заставляем мяч двигаться

#по горизонтали

BALL_X_CHANGE = 10

#по вертикали

BALL_Y_CHANGE = 0


#переменные для ракеток

PAD_SPEED = 30
LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0

#функция движения ракеток

def move_pads():
    PADS = {LEFT_PAD: LEFT_PAD_SPEED,
            RIGHT_PAD: RIGHT_PAD_SPEED}
    #перебор ракеток

    for pad in PADS:
        #двигаем ракетку с заданной скоростью
        c.move(pad,0,PADS[pad])
        #если ракетка выйдет за зону вернуть в исходное положение
        if c.coords(pad)[1] < 0:
            c.move(pad,0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad,0, HEIGHT - c.coords(pad)[3])

def main():
    move_ball()
    move_pads()
    root.after(30,main)

#Установим фокус на Canvas чтобы он реагировал на нажатия
c.focus_set()

#Напищем функцию обрабатывания клавиш

def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "s":
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED

#Привяжем к Canvas эту функцию
c.bind("<KeyPress>", movement_handler)

#Создадим функцию реагирование на отпускание клавиш
def stop_pad(event):
    global LEFT_PAD_SPEED,RIGHT_PAD_SPEED
    if event.keysym in "ws":
        LEFT_PAD_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0

c.bind("<KeyRelease>", stop_pad)

#Добавляем переменнные
# на сколько будет увеличиваться скорость мяча с кадлым ударом мяча

BALL_SPEED_UP = 1.1
BALL_MAX_SPEED = 40
BALL_X_SPEED = 10
BALL_Y_SPEED = 10

#Добавляем глобальную переменную отвечающее за расстоняие
# до правого края игрового поля

right_line_distance = WIDTH - PAD_W

# Функция отскока мяча

def bounce(action):
    global BALL_X_SPEED,BALL_Y_SPEED
    if action == "strike":
        BALL_Y_SPEED = random.randrange(-10,10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED

def move_ball():
    #определяем координаты мяча и его центра
    ball_left, ball_top,ball_right,ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2

    # Отскоки
    #Если мяч далеко от вертикальных линий - мяч просто летит
    if ball_right + BALL_X_SPEED < right_line_distance and \
            ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    #Eсли мяч касаеться правой или левой стороны поля
    elif ball_right == right_line_distance or ball_left == PAD_W:
        #проверяем правой или левой стороны мы касаемся
        if ball_right > WIDTH / 2:
            #Если правой, то сравниваем позицию центра мяча
            #c позицией правой каретки
            #И если мяч в пределах каретки делаем отскок
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce("strike")
            else:
                update_score("left")
                respawn_ball()

        else:
            #тоже самое для левого игрока
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce("strike")
            else:
                update_score("right")
                respawn_ball()
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance-ball_right,BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)
        #горизорнтальный отскок
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")

#подсчет очков
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

#Текстоввые объекты
p_1_text = c.create_text(WIDTH-WIDTH/6, PAD_H/4,
                        text = PLAYER_1_SCORE,
                        fill = "white",
                        font = "Arial 20")
p_2_text = c.create_text(WIDTH/6, PAD_H/4,
                        text = PLAYER_2_SCORE,
                        fill = "white",
                        font = "Arial 20")
#Создадим функцию расчета и респауна мяча

INITIAL_SPEED = 10

def update_score(player):
    global PLAYER_1_SCORE,PLAYER_2_SCORE
    if player == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text = PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text = PLAYER_2_SCORE)

def respawn_ball():
    global BALL_X_SPEED
    # Выставляем мяч по центру
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2-BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)
    # Задаем мячу направление в сторону проигравшего игрока,
    # но снижаем скорость до изначальной
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED) / abs(BALL_X_SPEED)

main()
root.mainloop()
