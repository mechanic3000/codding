"""
== Лото ==
Правила игры в лото.
Игра ведется с помощью специальных карточек, на которых отмечены числа,
и фишек (бочонков) с цифрами.
Количество бочонков — 90 штук (с цифрами от 1 до 90).
Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр,
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:
--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86
--------------------------
В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается
случайная карточка.
Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.
Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.

Побеждает тот, кто первый закроет все числа на своей карточке.
Пример одного хода:
Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71
--------------------------
-- Карточка компьютера ---
 7 11     - 14    87
      16 49    55 77    88
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)
Подсказка: каждый следующий случайный бочонок из мешка удобно получать
с помощью функции-генератора.
Подсказка: для работы с псевдослучайными числами удобно использовать
модуль random: http://docs.python.org/3/library/random.html
"""

import random


class WhoseNumber:
    @staticmethod
    def _whose(number):  # узнаем к какому десятку относится число
        rank = number // 10
        if number == 90:
            rank = 8
        return rank


class Numbers(WhoseNumber):
    def __init__(self, count, max_three=0):
        WhoseNumber.__init__(self)
        self._count = count  # количество чисел
        self._numbers = []
        self._i = -1
        self._max_three = max_three  # параметр максимум три числа в каждом десятке  1 - вкл , 0 - выкл
        self._rank_counter_dict = dict()
        self._make_numbers()

    def __iter__(self):
        return self

    def __next__(self):
        self._i += 1
        if self._i < len(self._numbers):
            return self._numbers[self._i]
        else:
            raise StopIteration

    def _make_numbers(self):  # создаем список уникальных чисел в заданном количестве
        while len(self._numbers) < self._count:
            rnd_number = random.randint(1, 90)
            self._rank_counter()

            if self._numbers.count(rnd_number) < 1 and self._max_three == 0:
                self._numbers.append(rnd_number)
            elif self._numbers.count(rnd_number) < 1 and self._max_three == 1:
                if self._rank_counter_dict.get(self._whose(rnd_number), 0) < 3:
                    self._numbers.append(rnd_number)
                else:
                    continue
            else:
                continue

    def _rank_counter(self):  # считаем сколько чисел в каждом десятке ( для карточек в каждом десятке д/б не более 3-х)
        self._rank_counter_dict.clear()
        for num in self._numbers:
            if self._rank_counter_dict.get(self._whose(num)):
                self._rank_counter_dict[self._whose(num)] += 1
            else:
                self._rank_counter_dict[self._whose(num)] = 1

    @property
    def get_numbers_list(self):
        return self._numbers

    def rm_number_fr_list(self, number):
        try:
            self._numbers.remove(number)
        except ValueError:
            pass

    def how_many_nums(self):
        return len(self._numbers)


class Card(WhoseNumber):
    def __init__(self, whose_card):
        WhoseNumber.__init__(self)
        self._numbers = Numbers(15, 1)
        self.whose_card = whose_card  # карта 1 - игрока, карта 2 - компьютера
        self._lines = dict()
        self._make_lines()

    def rm_number_fr_list(self, number):
        self._numbers.rm_number_fr_list(number)

    @property
    def how_many_nums(self):
        return self._numbers.how_many_nums()

    @property
    def get_lines(self):
        return self._lines

    def cross_out_number(self, number):
        try:
            self._lines[self._whose(number)][self._lines[self._whose(number)].index(number)] = "X"
        except ValueError:
            pass
        return True

    @property
    def get_card_numbers(self):
        return self._numbers.get_numbers_list

    def print_card(self):
        if self.whose_card == 1:
            print("---------- Ваша карточка ---------")
        elif self.whose_card == 2:
            print("------ Карточка компьютера -------")
        else:
            print("------------- Карточка -----------")
        for row in range(0, 3):
            current_line = str()
            for col in range(0, 9):
                current = self._lines.setdefault(col, [' ', ' ', ' '])
                current_line = current_line + str(current[row]) + '\t'
            print(current_line)
        print("----------------------------------")

    def _make_lines(self):
        for num in self._numbers:  # бежим по списку чисел, формируем сетку билета || ДЕСЯТОК : [числа] (см. коммент ниже)
            if isinstance(self._lines.get(self._whose(num)), list):
                self._lines[self._whose(num)].append(num)
            else:
                self._lines.setdefault(self._whose(num), [num])

        for num in self._lines:
            for i in range(1, 3):
                if len(self._lines[num]) < 3:
                    self._lines[num].insert(random.randint(0, 4), ' ')  # спасибо Олегу, подглядел в его скрипте!
        print(self._lines)  # раскоментить, если не поняно, что за список


class Game(WhoseNumber):
    def __init__(self):
        self._player_card = Card(1)
        self._cpu_card = Card(2)
        self._barrel = Numbers(90)
        self._passed_barrel = 0

    def start(self):
        self._prelude()
        for number in self._barrel:
            print("\n" * 25)
            print("Выпал боченок с номером - {}\t Осталось - {}".format(number, self._how_many_else_barrels()))
            self._player_card.print_card()
            self._cpu_card.print_card()
            answer = input("Зачеркнуть цифру? (y/n):")
            answer = answer.lower()  # вдруг кто-то БЛОНДИНКА!
            say_stop = False
            if answer == "y" and self._test_number(number, self._player_card.get_card_numbers):  # ответ ДА и номер ЕСТЬ
                self._player_card.rm_number_fr_list(number)
                self._player_card.cross_out_number(number)
            elif answer == "y" and not self._test_number(number,
                                                         self._player_card.get_card_numbers):  # ответ ДА, а номера НЕТ:
                print('(；⌣̀_⌣́)    -   Такого номер нет в Ваше карточке! Вы  П Р О И Г Р А Л И !!!')
                say_stop = True
            elif answer == "n" and self._test_number(number,
                                                     self._player_card.get_card_numbers):  # ответ НЕТ, а номер ЕСТЬ:
                print('(；⌣̀_⌣́)    -   Такой номер есть в карте! Вы  П Р О И Г Р А Л И !!!')
                say_stop = True
            else:
                pass

            self._cpu_card.rm_number_fr_list(number)
            self._cpu_card.cross_out_number(number)
            self._passed_barrel += 1

            if self._player_card.how_many_nums == 0 and self._cpu_card.how_many_nums != 0:
                print("\n")
                print("╰(▔∀▔)╯   П О О О О Б Е Д А А А !!!")
                say_stop = True
            elif self._cpu_card.how_many_nums == 0:
                print("\n")
                print("(；⌣̀_⌣́)   -    CPU Победил!  Вы П Р О И Г Р А Л И !!!")
                say_stop = True
            elif self._cpu_card.how_many_nums == 0 and self._player_card.how_many_nums == 0:
                print("\n")
                print("(；⌣̀_⌣́)   -    ╰(▔∀▔)╯     Н И Ч Ь Я !")
                say_stop = True

            if say_stop:
                print("\n")
                print("--== G A M E    O V E R ==--")
                break

    @staticmethod
    def _test_number(number, numbers_list):
        if numbers_list.count(number) > 0:
            return True
        else:
            return False

    @staticmethod
    def _prelude():
        print("\n")
        print("\"Р У С С К О Е    Л О Т Т О\"")
        print("""
        (；⌣̀_⌣́)
        Правила игры:
            Выпадает боченок с номером, Вам нужно нажать "y",
            если такой номер есть в Вашей карточке, или - "n",
            если такого номер в карточке нет.

            Побеждает тот, кто первый закроет все числа в карточке.
            Удачи!
        """)
        input("Нажмити ENTER для продолжения...")

    def _how_many_else_barrels(self):
        return len(self._barrel.get_numbers_list) - self._passed_barrel


game = Game()
game.start()
