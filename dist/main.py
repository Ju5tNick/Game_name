# -*- coding: utf-8 -*-

import sys
import math
import pygame

from random import choice, randrange

# import pymorphy2
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton, QInputDialog

from PyQt5 import QtCore, QtWidgets

FIELD_WIDTH = 20  # ширина (y)
FIELD_LENGHT = 30  # длина (x)
HERO_NOUNS = ['Артур', 'Лев', 'Ричард', 'Эль']
HERO_ADJECTIVES = ['Бесстрашный', 'Львиное Сердце', 'Непоколебимый']
SPIDERS_NAMES = ['Люцифер', 'Тони', 'Мистер Пушистые Штанишки', 'Граф']


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(191, 136)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 191, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.play_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.play_button.setObjectName("play_button")
        self.verticalLayout.addWidget(self.play_button)
        self.exit_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.exit_button.setObjectName("exit_button")
        self.verticalLayout.addWidget(self.exit_button)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.play_button.setText(_translate("Form", "Играть"))
        self.exit_button.setText(_translate("Form", "Выход"))


class Ui_QWidget(object):
    def setupUi(self, QWidget):
        QWidget.setObjectName("QWidget")
        QWidget.resize(972, 589)
        self.verticalLayoutWidget = QtWidgets.QWidget(QWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(800, 40, 161, 211))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.move_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.move_button.setObjectName("move_button")
        self.verticalLayout_2.addWidget(self.move_button)
        self.day_end_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.day_end_button.setObjectName("day_end_button")
        self.verticalLayout_2.addWidget(self.day_end_button)
        self.info_screen = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.info_screen.setObjectName("info_screen")
        self.verticalLayout_2.addWidget(self.info_screen)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.exit_button = QtWidgets.QPushButton(QWidget)
        self.exit_button.setGeometry(QtCore.QRect(800, 515, 157, 23))
        self.exit_button.setObjectName("exit_button")
        self.change_weapon_btn = QtWidgets.QPushButton(QWidget)
        self.change_weapon_btn.setGeometry(QtCore.QRect(800, 290, 158, 23))
        self.change_weapon_btn.setObjectName("change_weapon_btn")
        self.pick_up_button = QtWidgets.QPushButton(QWidget)
        self.pick_up_button.setGeometry(QtCore.QRect(800, 260, 158, 23))
        self.pick_up_button.setObjectName("pick_up_button")
        self.attack_button = QtWidgets.QPushButton(QWidget)
        self.attack_button.setGeometry(QtCore.QRect(800, 260, 158, 23))
        self.attack_button.setObjectName("attack_button")
        self.show_range_button = QtWidgets.QPushButton(QWidget)
        self.show_range_button.setGeometry(QtCore.QRect(800, 260, 158, 23))
        self.show_range_button.setObjectName("show_range_button")

        self.retranslateUi(QWidget)
        QtCore.QMetaObject.connectSlotsByName(QWidget)

    def retranslateUi(self, QWidget):
        _translate = QtCore.QCoreApplication.translate
        QWidget.setWindowTitle(_translate("QWidget", "Form"))
        self.label.setText(_translate("QWidget", "День"))
        self.label_2.setText(_translate("QWidget", "Осталось действий: "))
        self.move_button.setText(_translate("QWidget", "В путь"))
        self.day_end_button.setText(_translate("QWidget", "Закончить день"))
        self.exit_button.setText(_translate("QWidget", "Выход"))
        self.change_weapon_btn.setText(_translate("QWidget", "Сменить оружие на след."))
        self.pick_up_button.setText(_translate("QWidget", "Подобрать"))
        self.attack_button.setText(_translate("QWidget", "Атаковать"))
        self.show_range_button.setText(_translate("QWidget", "Показать диапазон"))


class Weapon:
    def __init__(self, name, damage, range, need_energy_per_shoot, coords=[]):
        self.name, self.damage, self.range, self.n_e_p_s, self.coords = name, damage, range, need_energy_per_shoot, coords

    def hit(self, actor, target, counter):
        if target.is_alive():
            if counter < actor.get_weapon().get_e_p_s():
                return (False, 'Не хватает сил')
            pos_x_actor, pos_y_actor = actor.get_coords()[0], actor.get_coords()[1]
            pos_x_target, pos_y_target = target.get_coords()[0], target.get_coords()[1]
            cathet1 = pos_x_actor - pos_x_target
            cathet2 = pos_y_actor - pos_y_target
            distance = math.sqrt((cathet1 ** 2) + (cathet2 ** 2))
            if actor.get_weapon().get_range() < int(distance) - 1:
                return (False, f'Враг слишком далеко для оружия {self.name}')
            else:
                target.get_damage(actor.get_weapon().get_damage())
                return (True,
                        f'Врагу нанесен урон оружием {actor.get_weapon().get_name()} в размере {actor.get_weapon().get_damage()}')
        return (False, 'Враг уже повержен')

    def get_name(self):
        return self.name

    def get_damage(self):
        return self.damage

    def get_range(self):
        return self.range

    def get_e_p_s(self):
        return self.n_e_p_s

    def get_coords(self):
        return self.coords

    def get_info(self):
        return f'{self.name.capitalize()}, Урон: {self.damage} hp, Диапазон: {self.range} кл, Тратит энергии за атаку: {self.n_e_p_s}'


class Enemy:
    def __init__(self, name, hp, base_coord, damage):
        self.name, self.hp, self.alive, self.base_coord = name, hp, True, base_coord
        self.flag, self.damage, self.d_day = True, damage, 0
        x, y = choice([-1, 1, 0]), choice([-1, 1, 0])
        while base_coord[0] + y >= FIELD_WIDTH and base_coord[1] + x >= FIELD_LENGHT:
            x, y = choice([-1, 1, 0]), choice([-1, 1, 0])
        self.coords = (base_coord[0] + choice([-1, 1]), base_coord[1] + choice([-1, 1]))

    def get_name(self):
        return self.name

    def get_flag(self):
        return self.flag

    def get_self_damage(self):
        return self.damage

    def set_flag(self):
        self.flag = False

    def get_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp, self.alive = 0, False

    def is_alive(self):
        return self.alive

    def get_coords(self):
        return self.coords


class Spider(Enemy):
    def __init__(self, name, hp, base_coord, damage):
        super().__init__(name, hp, base_coord, damage)

    def can_attack(self, MH_coords):
        if ((abs(MH_coords[0] - self.coords[0]) == 1 and MH_coords[1] == self.coords[1]) or
                (abs(MH_coords[1] - self.coords[1]) == 1 and MH_coords[0] == self.coords[0])):
            return True
        return False

    def attack(self, MH):
        MH.get_damage(self.damage)

    def get_info(self):
        if self.alive:
            return f'{self.name}\nЖив, {self.hp} hp\nУрон: {self.damage} hp\nАтакует только вплотную'
        return f'{self.name}, мертв'

    def make_move(self, hero_coords, field):
        if self.is_alive():

            move, moves = [1, 0, -1], []
            for _ in range(2):
                diff_y, diff_x = hero_coords[0] - self.coords[0], hero_coords[1] - self.coords[1]
                del_x, del_y = 0, 0

                if abs(hero_coords[0]) - abs(self.coords[0]) != 0:
                    for elem in move:
                        if abs(hero_coords[0] - (self.coords[0] + elem)) < abs(diff_y):
                            if field[self.coords[0] + elem][self.coords[1]] == None:
                                del_y = elem
                                break

                if abs(hero_coords[1]) - abs(self.coords[1]) != 0:
                    for elem in move:
                        if abs(hero_coords[1] - (self.coords[1] + elem)) < abs(diff_x):
                            if field[self.coords[0] + del_y][self.coords[1] + elem] == None:
                                del_x = elem
                                break

                moves.append((self.coords[0] + del_y, self.coords[1] + del_x))
                self.coords = moves[-1]

            return moves
        return self.coords

    def set_dead_day(self):
        self.d_day += 1

    def get_d_day(self):
        return self.d_day

    def get_image(self):
        if self.hp > 0:
            return 'images/spider/spider.png'
        return 'images/spider/dead_spider.png'


class MainHero:
    def __init__(self, coords, name, hp):
        self.coords, self.hp, self.name, self.weapons, self.weapon = coords, hp, name, [], None

    def is_alive(self):
        if self.hp > 0:
            return True
        return False

    def get_damage(self, amount):
        self.hp -= amount

    def get_coords(self):
        return self.coords

    def get_weapons(self):
        return self.weapons

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_info(self):
        weapons = ', '.join([weapon.get_name().capitalize() for weapon in self.weapons])
        return f'{self.name}\nЗдоровья: {self.hp} hp\nОружие:\n{weapons}\n\nТекущее оружие: {self.get_weapon().get_info()}'

    def get_weapon(self):
        if self.weapon == None:
            return self.weapons[0]
        return self.weapon

    def make_move(self, new_coords):
        self.coords = new_coords

    def add_weapon(self, weapon):
        if type(weapon) is Weapon:
            self.weapons.append(weapon)
            self.weapon = weapon
            return f'Подобрал {weapon.get_name().lower()}'
        else:
            return 'Это не оружие'

    def next_weapon(self):
        if self.get_weapon() == None:
            return 'Я безоружен'
        elif len(self.weapons) == 1:
            return 'У меня только одно оружие'
        else:
            a = self.weapons.index(self.weapon)
            if a + 1 == len(self.weapons):
                self.weapon = self.weapons[0]
            else:
                self.weapon = self.weapons[a + 1]
            return f'Сменил оружие на {self.weapon.get_name()}'

    def heal(self, amount):
        if self.hp + amount > 200:
            self.hp = 200
        else:
            self.hp += amount
        return f'Полечился, теперь здоровья {self.hp}'

    def get_image(self):
        if self.get_weapon().get_name().lower() == 'кинжал':
            return 'images/knights/knightWithDagger.png'
        elif self.get_weapon().get_name().lower() == 'меч':
            return 'images/knights/knightWithSword.png'
        elif self.get_weapon().get_name().lower() == 'лук':
            return 'images/knights/knightWithBow.png'
        return 'images/knights/knight.png'


class Cave:
    def __init__(self):
        self.coords = (choice([randrange(1, 4), randrange(16, FIELD_WIDTH - 1)]),
                       choice([randrange(1, 4), randrange(26, FIELD_LENGHT - 1)]))

    def get_coords(self):
        return self.coords

    def get_info(self):
        return 'Просто пещера'


class MainMenu(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        # self.initUI()
        self.setupUi(self)

        # def initUI(self):
        # uic.loadUi('main_window.ui', self)
        self.setWindowTitle('Menu')
        self.setWindowIcon(QIcon("images/icon.png"))

        self.play_button.clicked.connect(self.open_game_window)
        self.exit_button.clicked.connect(self.exit)

    def open_game_window(self):
        self.game_form = Game(self, "Game_name")
        self.game_form.show()

    def exit(self):
        self.close()


class Game(QWidget, Ui_QWidget):
    def __init__(self, *args):
        super().__init__()
        # self.initUI(args)

        # def initUI(self, args):
        # super().__init__()
        self.setupUi(self)
        # uic.loadUi('game_window.ui', self)
        self.setWindowTitle('Game_name')
        self.setWindowIcon(QIcon("images/icon.png"))
        pygame.init()

        self.moves, self.day, self.field, self.enemies, self.s_field = [], 1, [], [], []
        self.action_counter, counter2, self.flag, self.show_green, self.painted = 10, 40, True, True, []
        self.object1, self.enemy_a_counter, self.dead_enemies, self.flag2 = None, 10, [], False

        self.old_coords, self.new_coords = (0, 0), (0, 0)

        # self.morph = pymorphy2.MorphAnalyzer()

        self.move_button.setEnabled(False)
        self.day_end_button.setEnabled(False)
        self.show_range_button.setEnabled(False)

        self.info_screen.setReadOnly(True)

        self.attack_button.hide()
        self.change_weapon_btn.hide()
        self.show_range_button.hide()
        self.pick_up_button.hide()

        self.attack_button.clicked.connect(self.attack)
        self.move_button.clicked.connect(self.make_move)
        self.day_end_button.clicked.connect(self.day_end)
        self.show_range_button.clicked.connect(self.show_range)
        self.exit_button.clicked.connect(self.exit)
        self.change_weapon_btn.clicked.connect(self.change_weapon)
        self.pick_up_button.clicked.connect(self.pick_up)

        for i in range(FIELD_WIDTH):
            counter1, row = 40, []
            for j in range(FIELD_LENGHT):
                self.btn = QPushButton('', self)
                self.btn.resize(25, 25)
                self.btn.move(counter1, counter2)
                self.btn.clicked.connect(self.main_run)
                counter1 += 25
                row.append(self.btn)
            counter2 += 25
            self.s_field.append([None for i in range(FIELD_LENGHT)])
            self.field.append(row)

    def main_run(self):
        self.new_coords = self.get_coords(self.sender())
        self.sound('sounds/action.wav')

        if self.flag:
            self.e_base = Cave()
            self.set_image('images/cave.png', coords=[self.e_base.get_coords()[0], self.e_base.get_coords()[1]])
            self.s_field[self.e_base.get_coords()[0]][self.e_base.get_coords()[1]] = self.e_base
            self.knight = MainHero(self.new_coords, f'{choice(HERO_NOUNS)} {choice(HERO_ADJECTIVES)}', 200)
            self.knight.add_weapon(Weapon('кулаки', 25, 1, 1))
            self.s_field[self.new_coords[0]][self.new_coords[1]] = self.knight
            self.set_image(self.knight.get_image(), object1=self.sender())
            self.old_coords = self.new_coords
            self.label_2.setText(f'Осталось действий: {self.action_counter}')
            self.label_2.setStyleSheet("color: rgb(0, 0, 0);")
            self.label.setText(f'День {self.day}')
            self.move_button.setEnabled(True)
            self.day_end_button.setEnabled(True)
            self.show_range_button.setEnabled(True)
            self.flag = False

        if self.knight.is_alive() == False:
            self.info_screen.setPlainText('Самоубийца :D')
            self.exit()

        if self.sender() in self.moves:
            [elem.setStyleSheet("background-color: rgb(235, 235, 235);") for elem in
             self.moves[self.moves.index(self.sender()):]]
            if self.moves[:self.moves.index(self.sender())] == []:
                self.old_coords, self.new_coords = self.knight.get_coords(), self.knight.get_coords()
            else:
                self.new_coords = self.get_coords(self.moves[self.moves.index(self.sender())])
                self.old_coords = self.get_coords(self.moves[self.moves.index(self.sender()) - 1])
            self.action_counter += len(self.moves[self.moves.index(self.sender()):])
            self.label_2.setText(f'Осталось действий: {self.action_counter}')
            self.label_2.setStyleSheet("color: rgb(0, 0, 0);")
            self.moves = self.moves[:self.moves.index(self.sender())]

        if self.check_coord(self.old_coords, self.new_coords, self.knight.get_coords()) and self.flag == False:
            self.sender().setStyleSheet("background-color: grey;")
            self.old_coords = self.new_coords

            self.moves.append(self.field[self.new_coords[0]][self.new_coords[1]])
            self.action_counter -= 1
            self.label_2.setText(f'Осталось действий: {self.action_counter}')
            self.label_2.setStyleSheet("color: rgb(0, 0, 0);")

        if self.s_field[self.new_coords[0]][self.new_coords[1]] != None:
            if self.object1 != None:
                self.field[self.object_coords[0]][self.object_coords[1]].setStyleSheet(
                    "background-color: rgb(235, 235, 235);")
            self.object1 = self.s_field[self.new_coords[0]][self.new_coords[1]]
            self.object_coords = self.new_coords

            if type(self.object1) is Spider:
                self.attack_button.show()
                self.change_weapon_btn.hide()
                self.show_range_button.hide()
                self.pick_up_button.hide()
            if type(self.object1) is MainHero:
                self.change_weapon_btn.show()
                self.show_range_button.show()
                self.pick_up_button.hide()
                self.attack_button.hide()
            if type(self.object1) is Weapon:
                self.pick_up_button.show()
                self.attack_button.hide()
                self.change_weapon_btn.hide()
                self.show_range_button.hide()

            self.field[self.object_coords[0]][self.object_coords[1]].setStyleSheet("background-color: rgb(0, 187, 13);")
            self.info_screen.setPlainText(self.object1.get_info())
        else:
            self.field[self.object_coords[0]][self.object_coords[1]].setStyleSheet(
                "background-color: rgb(235, 235, 235);")
            self.attack_button.hide()
            self.change_weapon_btn.hide()
            self.show_range_button.hide()
            self.pick_up_button.hide()
            self.info_screen.setPlainText('')

    def pick_up(self):
        self.attack_button.hide()
        self.change_weapon_btn.hide()
        self.show_range_button.hide()
        if ((abs(self.knight.get_coords()[0] - self.object_coords[0]) == 1 and self.knight.get_coords()[1] ==
             self.object_coords[1]) or
                (abs(self.knight.get_coords()[1] - self.object_coords[1]) == 1 and self.knight.get_coords()[0] ==
                 self.object_coords[0]) or
                (abs(self.knight.get_coords()[1] - self.object_coords[1]) == 1 and abs(
                    self.knight.get_coords()[0] - self.object_coords[0]) == 1)):
            self.sound("sounds/get_coin.wav")
            self.info_screen.setPlainText(self.knight.add_weapon(self.object1))
            self.field[self.object_coords[0]][self.object_coords[1]].setIcon(QIcon())
            self.field[self.object_coords[0]][self.object_coords[1]].setStyleSheet(
                "background-color: rgb(235, 235, 235);")
            self.s_field[self.object_coords[0]][self.object_coords[1]] = None
            self.set_image(self.knight.get_image(), coords=self.knight.get_coords())
        else:
            self.info_screen.setPlainText('Предмет слишком далеко')

    def change_weapon(self):
        self.info_screen.setPlainText(self.knight.next_weapon())
        self.set_image(self.knight.get_image(), coords=self.knight.get_coords())
        self.show_green = False
        self.show_range()

    def set_image(self, image, coords=[], object1=None):
        if object1 != None:
            object1.setIcon(QIcon(image))
            object1.setIconSize(QSize(20, 20))
        else:
            self.field[coords[0]][coords[1]].setIcon(QIcon(image))
            self.field[coords[0]][coords[1]].setIconSize(QSize(20, 20))

    def sound(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    def attack(self):
        result = self.knight.get_weapon().hit(self.knight, self.object1, self.action_counter)
        if self.action_counter - self.knight.get_weapon().get_e_p_s() >= 0 and result[0]:
            self.action_counter -= self.knight.get_weapon().get_e_p_s()
            self.enemy_a_counter -= self.knight.get_weapon().get_e_p_s()
            self.label_2.setText(f'Осталось действий: {self.action_counter}')
            self.label_2.setStyleSheet("color: rgb(0, 0, 0);")
            self.set_image(self.object1.get_image(), coords=[self.object_coords[0], self.object_coords[1]])
            self.sound("sounds/destroy.wav")
            self.info_screen.setPlainText(f'{result[1]}, потратил энергии: {self.knight.get_weapon().get_e_p_s()}')
        else:
            self.label_2.setText(f'Осталось действий: {self.action_counter}')
            self.label_2.setStyleSheet("color: rgb(255, 0, 0);")
            self.info_screen.setPlainText(result[1])

    def show_range(self):
        if self.knight.get_weapons() != []:
            rang = self.knight.get_weapon().get_range() + 1
            coords = self.knight.get_coords()
            if self.show_green:
                for i in range(int(coords[0]) - rang + 1, int(coords[0]) + rang):
                    if i >= 0 and i < FIELD_WIDTH and coords[1] + rang >= 0 and coords[1] + rang < FIELD_LENGHT:
                        self.field[i][coords[1] + rang].setStyleSheet("background-color: rgb(135, 255, 0);")
                        self.painted.append((i, coords[1] + rang))

                for i in range(int(coords[0]) - rang + 1, int(coords[0]) + rang):
                    if i >= 0 and i < FIELD_WIDTH and coords[1] - rang >= 0 and coords[1] - rang < FIELD_LENGHT:
                        self.field[i][coords[1] - rang].setStyleSheet("background-color: rgb(135, 255, 0);")
                        self.painted.append((i, coords[1] - rang))

                for i in range(int(coords[1]) - rang + 1, int(coords[1]) + rang):
                    if i >= 0 and i < FIELD_LENGHT and coords[0] + rang >= 0 and coords[0] + rang < FIELD_WIDTH:
                        self.field[coords[0] + rang][i].setStyleSheet("background-color: rgb(135, 255, 0);")
                        self.painted.append((coords[0] + rang, i))

                for i in range(int(coords[1]) - rang + 1, int(coords[1]) + rang):
                    if i >= 0 and i < FIELD_LENGHT and coords[0] - rang >= 0 and coords[0] - rang < FIELD_WIDTH:
                        self.field[coords[0] - rang][i].setStyleSheet("background-color: rgb(135, 255, 0);")
                        self.painted.append((coords[0] - rang, i))

                self.show_range_button.setText('Скрыть диапазон')
                self.show_green = False
            else:
                [self.field[elem[0]][elem[1]].setStyleSheet("background-color: rgb(235, 235, 235);") for elem in
                 self.painted]
                self.painted = []
                self.show_range_button.setText('Показать диапазон')
                self.show_green = True

    def spawn_enemies(self):
        if self.day % 2 == 0:
            while len(self.enemies) != self.day // 2:
                spider = Spider(choice(SPIDERS_NAMES), 50, self.e_base.get_coords(), 20)
                self.enemies.append(spider)
                self.s_field[spider.get_coords()[0]][spider.get_coords()[1]] = spider

    def enemy_actions(self):
        damage, count = 0, 0
        while self.enemy_a_counter != self.action_counter:
            if self.enemies != []:
                for enemy in self.enemies:
                    if enemy.is_alive():
                        if enemy.get_flag():
                            self.set_image(enemy.get_image(), coords=[enemy.get_coords()[0], enemy.get_coords()[1]])
                            self.s_field[enemy.get_coords()[0]][enemy.get_coords()[1]] = enemy
                            enemy.set_flag()
                        else:
                            self.field[enemy.get_coords()[0]][enemy.get_coords()[1]].setIcon(QIcon())
                            self.s_field[enemy.get_coords()[0]][enemy.get_coords()[1]] = None
                            moves = enemy.make_move(self.knight.get_coords(), self.s_field)
                            self.set_image(enemy.get_image(), coords=[moves[-1][0], moves[-1][1]])
                            self.s_field[moves[-1][0]][moves[-1][1]] = enemy
                            if enemy.can_attack(self.knight.get_coords()):
                                enemy.attack(self.knight)
                                damage += enemy.get_self_damage()
                                count += 1

                            if self.knight.is_alive() == False:
                                self.info_screen.setPlainText('Вы погибли')
                                self.exit()

                    else:
                        del self.enemies[self.enemies.index(enemy)]
                        self.dead_enemies.append(enemy)

            self.enemy_a_counter -= 1

        if damage != 0:
            self.info_screen.setPlainText(
                f'Вас атаковали и нанесли урон в размере {damage}\nЗдоровья теперь {self.knight.get_hp()}')

    def dead_enemy_action(self):
        for d_enemy in self.dead_enemies:
            d_enemy.set_dead_day()
            if d_enemy.get_d_day() >= 8:
                self.field[d_enemy.get_coords()[0]][d_enemy.get_coords()[1]].setIcon(QIcon())
                self.s_field[d_enemy.get_coords()[0]][d_enemy.get_coords()[1]] = None
                del self.dead_enemies[self.dead_enemies.index(d_enemy)]
            elif d_enemy.get_d_day() >= 4:
                self.set_image('images/spider/spider_skeleton.png',
                               coords=[d_enemy.get_coords()[0], d_enemy.get_coords()[1]])

    def day_end(self):
        answer = ''

        if self.action_counter > 5:
            self.info_screen.setPlainText('Вы не можете завершить день, пока не совершите хотя бы 5 действий.')
            return 0

        if self.action_counter != 0:
            while answer.lower() != 'да':
                answer, ok_pressed = QInputDialog.getItem(
                    self, "Вы уверены?",
                    "Если вы закончите день сейчас,\nто все свободные действия сгорят.\nВы уверены (да/нет)? ",
                    ("да", "нет"), 1, False)
                if ok_pressed == False or answer.lower() == 'нет':
                    return 0

        self.day += 1
        self.enemy_actions()
        self.make_move()
        self.dead_enemy_action()
        self.spawn_enemies()

        # word1 = self.morph.parse('день')[0]
        if self.day == 1:
            d='день'
        elif 2<=self.day <5:
            d='дня'
        else:
            d = 'дней'
        if self.day < 5:
            l_d_u_spawn_weapon = f'Осталось {5 - self.day} {d} до получения нового оружия'  # Left_Days_Until_spawn_weapon
        elif self.day < 10 and self.day >= 5:
            l_d_u_spawn_weapon = f'Осталось {5 - (self.day - 5)} {d} до получения нового оружия'
        elif self.day < 15 and self.day >= 10:
            l_d_u_spawn_weapon = f'Осталось {5 - (self.day - 10)} {d} до получения нового оружия'
        else:
            l_d_u_spawn_weapon = ''

        if self.knight.get_hp() < 200:
            self.info_screen.setPlainText(self.knight.heal(20) + '\n' + l_d_u_spawn_weapon)
        else:
            self.info_screen.setPlainText(l_d_u_spawn_weapon)

        if self.day % 5 != 0:
            self.flag2 = True

        coords = (randrange(0, FIELD_WIDTH), randrange(0, FIELD_LENGHT))
        if self.day == 5 and self.flag2:
            while self.s_field[coords[0]][coords[1]] != None:
                coords = (randrange(0, FIELD_WIDTH), randrange(0, FIELD_LENGHT))
            dagger = Weapon('кинжал', 50, 1, 1, coords=coords)
            self.s_field[coords[0]][coords[1]], self.flag2 = dagger, False
            self.set_image('images/weapons/dagger.png', coords=coords)

        elif self.day == 10 and self.flag2:
            while self.s_field[coords[0]][coords[1]] != None:
                coords = (randrange(0, FIELD_WIDTH), randrange(0, FIELD_LENGHT))
            sword = Weapon('меч', 50, 2, 2, coords=coords)
            self.s_field[coords[0]][coords[1]], self.flag2 = sword, False
            self.set_image('images/weapons/sword.png', coords=coords)

        elif self.day == 15 and self.flag2:
            while self.s_field[coords[0]][coords[1]] != None:
                coords = (randrange(0, FIELD_WIDTH), randrange(0, FIELD_LENGHT))
            bow = Weapon('лук', 50, 5, 2, coords=coords)
            self.s_field[coords[0]][coords[1]], self.flag2 = bow, False
            self.set_image('images/weapons/bow.png', coords=coords)

        self.action_counter, self.enemy_a_counter = 10, 10
        self.label.setText(f'День {self.day}')
        self.label_2.setText(f'Осталось действий: {self.action_counter}')
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);")

    def make_move(self):
        if self.moves != []:
            if self.object1 != None:
                self.field[self.object_coords[0]][self.object_coords[1]].setStyleSheet(
                    "background-color: rgb(235, 235, 235);")
                self.attack_button.hide()
                self.info_screen.setPlainText('')
            self.show_green = False
            self.show_range()
            self.field[self.knight.get_coords()[0]][self.knight.get_coords()[1]].setIcon(QIcon())
            self.s_field[self.knight.get_coords()[0]][self.knight.get_coords()[1]] = None
            self.set_image(self.knight.get_image(), object1=self.moves[-1])

            self.knight.make_move(self.get_coords(self.moves[-1]))
            self.s_field[self.knight.get_coords()[0]][self.knight.get_coords()[1]] = self.knight
            [elem.setStyleSheet("background-color: rgb(235, 235, 235);") for elem in self.moves]
            self.moves = []
            self.sound('sounds/jump.wav')

        self.enemy_actions()

    def check_coord(self, c1, c2, kc):
        if self.action_counter == 0:
            self.label_2.setStyleSheet("color: rgb(255, 0, 0);")
            return False
        if (c1 == c2 or c2 == kc or
                self.s_field[c2[0]][c2[1]] != None):
            return False
        if ((c1[0] == c2[0] + 1 and c1[1] == c2[1]) or
                (c1[0] == c2[0] - 1 and c1[1] == c2[1]) or
                (c1[0] == c2[0] and c1[1] == c2[1] + 1) or
                (c1[0] == c2[0] and c1[1] == c2[1] - 1)):
            return True
        return False

    def get_coords(self, object):
        for i in range(len(self.field)):
            if object in self.field[i]:
                j = self.field[i].index(object)
                return (i, j)

    def exit(self):
        # word1 = self.morph.parse('день')[0]
        if self.day == 1:
            d='день'
        elif 2<=self.day <5:
            d='дня'
        else:
            d = 'дней'
        answer, ok_pressed = QInputDialog.getItem(
            self, "Конец", f"Вы продержались {self.day} {d}", ["ok"], 1,
            False)

        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainMenu()
    app.setStyle('Fusion')
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
