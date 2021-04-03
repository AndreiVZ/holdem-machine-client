from PyQt5 import QtGui
import math

from Rooms.Poker888 import Parsing_888 as pars_888
from Strategy import Basic_Strategy as bs
from Tools import Mouse_Keyboard as mk


class Table:
    def __init__(self):
        # players in the game
        self.pl_inTG_areas = []
        self.pl_inTG_list = []
        self.pl_inTG_now = 0
        self.pl_inTG_last = 0
        # players bet & pot
        self.bet_pot_areas = []
        self.bet_pot_list = []
        # players positions
        self.positions_list = []
        # my cards
        self.my_cards_areas = []
        self.Im_inTG = False
        self.new_deal = True
        # board cards
        self.board_cards_areas = []
        self.board_cards_last = 0
        # my turn
        self.my_turn_areas = []
        self.my_turn = False
        # stack (BB)
        self.stack_areas = []
        self.stack_list = []

    def set_areas(self, x, y):
        self.pl_inTG_areas = [[1, 1],  # [width, height]
                              [70 + x, 276 + y],  # [player_01_X, player_01_Y]
                              [70 + x, 147 + y],  # [player_02_X, player_02_Y]
                              [344 + x, 95 + y],  # [player_03_X, player_03_Y]
                              [620 + x, 147 + y],  # [player_04_X, player_04_Y]
                              [620 + x, 276 + y]]  # [player_05_X, player_05_Y]
        self.bet_pot_areas = [[56, 12],  # [width, height]
                              [182 + x, 296 + y],  # [bet_01_X, bet_01_Y]
                              [182 + x, 180 + y],  # [bet_02_X, bet_02_Y]
                              [326 + x, 157 + y],  # [bet_03_X, bet_03_Y]
                              [428 + x, 180 + y],  # [bet_04_X, bet_04_Y]
                              [428 + x, 296 + y],  # [bet_05_X, bet_05_Y]
                              [282 + x, 318 + y],  # [bet_06_X, bet_06_Y]
                              [342 + x, 183 + y]]  # [pot_X, pot_Y]
        self.my_cards_areas = [[81, 18],  # [width, height]
                               [302 + x, 359 + y]]  # [area_X, area_Y]
        self.board_cards_areas = [[204, 18],  # [width, height]
                                  [238 + x, 204 + y]]  # [area_X, area_Y]
        self.my_turn_areas = [[1, 1],  # [width, height]
                              [360 + x, 430 + y]]  # [my_turn_X, my_turn_Y]
        self.stack_areas = [[40, 11],  # [width, height]
                            [32 + x, 304 + y],  # [stack_01_X, stack_01_Y]
                            [32 + x, 175 + y],  # [stack_02_X, stack_02_Y]
                            [312 + x, 123 + y],  # [stack_03_X, stack_03_Y]
                            [584 + x, 175 + y],  # [stack_04_X, stack_04_Y]
                            [584 + x, 304 + y],  # [stack_05_X, stack_05_Y]
                            [370 + x, 427 + y]]  # [stack_06_X, stack_06_Y]
        self.buttons_area = [[244 + x, 460 + y, 244 + 50 + x, 460 + 21 + y],  # 1 button
                             [310 + x, 460 + y, 310 + 65 + x, 460 + 21 + y],  # 2 button
                             [390 + x, 460 + y, 390 + 65 + x, 460 + 21 + y],  # 3 button
                             [367 + x, 493 + y, 367 + 29 + x, 493 + 7 + y],  # max
                             [425 + x, 500 + y, 435 + x, 505 + y]]  # input

    def clear_table(self, sti):
        """clear the table"""
        # sti refresh data
        for col in range(0, 6):
            for row in range(0, 7):
                item = QtGui.QStandardItem(str(''))
                sti.setItem(row, col, item)

    def pl_inTG(self, image, sti):
        """get all the players still in the game"""
        self.pl_inTG_list = []
        # crop area
        width = self.pl_inTG_areas[0][0]
        height = self.pl_inTG_areas[0][1]
        # player_01-05
        for i in range(1, 6):
            image_crop = image.crop((self.pl_inTG_areas[i][0],
                                     self.pl_inTG_areas[i][1],
                                     self.pl_inTG_areas[i][0] + width,
                                     self.pl_inTG_areas[i][1] + height))
            self.pl_inTG_list.append(pars_888.check_inTG(image_crop, f'pl_inTG_list_{i}'))
        # player_06 (me)
        self.pl_inTG_list.append(True)

        # sti refresh data
        self.pl_inTG_now = sum(self.pl_inTG_list)
        if self.pl_inTG_now != self.pl_inTG_last:
            col = 0
            for row in range(0, 6):
                item_str = str('    *') if self.pl_inTG_list[row] else str('')
                item = QtGui.QStandardItem(item_str)
                sti.setItem(row, col, item)

    def bet_pot(self, image, sti):
        """get all the bets & the pot"""
        self.bet_pot_list = []
        # crop area
        width = self.bet_pot_areas[0][0]
        height = self.bet_pot_areas[0][1]
        # player_01-06 bets + 1 pot
        for i in range(1, 8):
            image_crop = image.crop((self.bet_pot_areas[i][0],
                                     self.bet_pot_areas[i][1],
                                     self.bet_pot_areas[i][0] + width,
                                     self.bet_pot_areas[i][1] + height))
            self.bet_pot_list.append(pars_888.check_bet_pot(image_crop, f'bet_pot_list_{i}'))
        # округлим ставки вниз кроме '0.5'
        for i in range(len(self.bet_pot_list)):
            if self.bet_pot_list[i] >= 1:
                self.bet_pot_list[i] = math.floor(self.bet_pot_list[i])

        # sti refresh data
        col = 2
        for row in range(0, 7):
            item_str = str(self.bet_pot_list[row]) if self.bet_pot_list[row] > 0 else str('')
            item = QtGui.QStandardItem(item_str)
            sti.setItem(row, col, item)

    def stack(self, image, sti):
        """get all the stack (BB) for all the players still in the game"""
        self.stack_list = []
        # crop area
        width = self.stack_areas[0][0]
        height = self.stack_areas[0][1]
        # player_01-06
        for i in range(1, 7):
            if self.pl_inTG_list[i - 1]:
                image_crop = image.crop((self.stack_areas[i][0],
                                         self.stack_areas[i][1],
                                         self.stack_areas[i][0] + width,
                                         self.stack_areas[i][1] + height))
                self.stack_list.append(pars_888.check_stack(image_crop, f'stack_list{i}'))
            else:
                self.stack_list.append(0)
        # округлим стек вниз
        self.stack_list = [math.floor(x) for x in self.stack_list]

        # sti refresh data
        col = 1
        for row in range(0, 6):
            item_str = str(self.stack_list[row]) if self.pl_inTG_list[row] else str('')
            item = QtGui.QStandardItem(item_str)
            sti.setItem(row, col, item)

    def positions(self, sti):
        """get all the positions"""
        self.positions_list = [0, 0, 0, 0, 0, 0]
        try:
            start = self.bet_pot_list.index(0.5)
        except ValueError:
            return

        # заполним список self.positions_list
        position = 1
        for i in range(start, 6):
            if self.pl_inTG_list[i]:
                self.positions_list[i] = position
                position += 1
        for i in range(0, start):
            if self.pl_inTG_list[i]:
                self.positions_list[i] = position
                position += 1

        # sti refresh data
        col = 3
        for row in range(0, 6):
            item_str = str(self.positions_list[row]) if self.positions_list[row] > 0 else str('')
            item = QtGui.QStandardItem(item_str)
            sti.setItem(row, col, item)

    def my_cards(self, image, sti, label, table):
        """get my cards"""
        # suits
        # crop area
        width = self.my_cards_areas[0][0]
        height = self.my_cards_areas[0][1]
        image_crop = image.crop((self.my_cards_areas[1][0],
                                 self.my_cards_areas[1][1],
                                 self.my_cards_areas[1][0] + width,
                                 self.my_cards_areas[1][1] + height))
        my_suits = pars_888.check_my_suits(image_crop)
        self.Im_inTG = not bool(my_suits.count('-'))

        # ranks
        if self.Im_inTG:
            if self.new_deal:
                # обновим свои карты
                self.new_deal = False
                cards_to_find = 2
                my_ranks = pars_888.check_card_ranks(image_crop, 'my_ranks', cards_to_find)

                # sti refresh data
                col = 4
                for row in range(5, 7):
                    # rank
                    item_rank = QtGui.QStandardItem(my_ranks[row - 5])
                    sti.setItem(row, col, item_rank)
                    # suit
                    item_suit = QtGui.QStandardItem(my_suits[row - 5])
                    sti.setItem(row, col + 1, item_suit)
        else:
            if not self.new_deal:
                # сбросил свои карты, уже не мой ход
                label.setText(f'{table}) -')
                self.new_deal = True
                my_ranks = ['-', '-']

                # sti refresh data
                col = 4
                for row in range(5, 7):
                    # rank
                    item_rank = QtGui.QStandardItem(my_ranks[row - 5])
                    sti.setItem(row, col, item_rank)
                    # suit
                    item_suit = QtGui.QStandardItem(my_suits[row - 5])
                    sti.setItem(row, col + 1, item_suit)

    def board_cards(self, image, sti):
        """get board cards"""
        # suits
        # crop area
        width = self.board_cards_areas[0][0]
        height = self.board_cards_areas[0][1]
        image_crop = image.crop((self.board_cards_areas[1][0],
                                 self.board_cards_areas[1][1],
                                 self.board_cards_areas[1][0] + width,
                                 self.board_cards_areas[1][1] + height))
        board_suits = pars_888.check_board_suits(image_crop)
        cards_to_find = 5 - board_suits.count('-')

        # ranks
        if cards_to_find != self.board_cards_last:
            # обновим карты боарда
            if cards_to_find:
                board_ranks = pars_888.check_card_ranks(image_crop, 'board_ranks', cards_to_find)
            else:
                board_ranks = ['-', '-', '-', '-', '-']

            # sti refresh data
            col = 4
            for row in range(0, 5):
                # rank
                item_rank = QtGui.QStandardItem(board_ranks[row])
                sti.setItem(row, col, item_rank)
                # suit
                item_suit = QtGui.QStandardItem(board_suits[row])
                sti.setItem(row, col + 1, item_suit)
        self.board_cards_last = cards_to_find

    def if_my_turn(self, image):
        """check if my turn"""
        # crop area
        width = self.my_turn_areas[0][0]
        height = self.my_turn_areas[0][1]
        image_crop = image.crop((self.my_turn_areas[1][0],
                                 self.my_turn_areas[1][1],
                                 self.my_turn_areas[1][0] + width,
                                 self.my_turn_areas[1][1] + height))
        self.my_turn = pars_888.check_my_turn(image_crop)

    def my_move(self, sti, log_name):
        """get my_move from Basic_Strategy"""
        inTG = []
        stack = []
        bet = []
        position = []
        board = []
        my_cards = []

        # inTG, stack, bet, position
        for i in range(6):
            item = sti.data(sti.index(i, 0))
            inTG.append(False if item in ['', None] else bool(item))
            item = sti.data(sti.index(i, 1))
            stack.append(float(0) if item in ['', None] else float(item))
            item = sti.data(sti.index(i, 2))
            bet.append(float(0) if item in ['', None] else float(item))
            item = sti.data(sti.index(i, 3))
            position.append(int(0) if item in ['', None] else int(item))
        # board_cards
        for i in range(5):
            item = sti.data(sti.index(i, 4))
            board.append('-' if item in ['', '-', None] else int(item))
            item = sti.data(sti.index(i, 5))
            board.append('-' if item in ['', '-', None] else item)
        # my_cards
        for i in range(5, 7):
            item = sti.data(sti.index(i, 4))
            my_cards.append('-' if item in ['', '-', None] else int(item))
            item = sti.data(sti.index(i, 5))
            my_cards.append('-' if item in ['', '-', None] else item)
        # pot
        item = sti.data(sti.index(6, 2))
        pot = float(item)

        # log_file enabled
        # with open(f'{log_name}.log', mode='a', encoding="utf-8") as log_file:
        #     my_move = bs.MyMove(inTG, stack, bet, position, board, my_cards, pot, log_file)
        # log_file disabled
        log_file = 0
        my_move = bs.MyMove(inTG, stack, bet, position, board, my_cards, pot, log_file)
        return my_move

    def click_my_move(self, my_move, sti):
        """click the buttons accordingly my_move"""
        if my_move in ['Fold']:
            self.click_fold(sti)
        if my_move in ['Call']:
            self.click_call()
        if my_move in ['Check',
                       'Check, Call',
                       'Check || Call']:
            self.click_check()
        if my_move in ['Check, Fold', 'Check, Fold', 'Check || Fold']:
            bet = max(self.bet_pot_list[0:6])
            if bet > 0:
                self.click_fold(sti)
            else:
                self.click_check()
        if my_move in ['3Bet IP 3x']:
            self.click_bet_x(3)
        if my_move in ['3Bet OOP 4x']:
            self.click_bet_x(4)
        if my_move in ['4Bet 27 || AllIn',
                       '4Bet 27 || AllIn(30)',
                       '4Bet 27 || AllIn(50)']:
            self.click_allin()
        if my_move in ['CBet 4/5 Pot']:
            self.click_pot_x(4 / 5)
        if my_move in ['CBet 2/3 Pot',
                       'Float 2/3 Pot',
                       'Bet 2/3 Pot']:
            self.click_pot_x(2 / 3)
        if my_move in ['Bet 2/3 Pot || Fold']:
            bet = max(self.bet_pot_list[0:6])
            if bet > 0:
                self.click_fold(sti)
            else:
                self.click_pot_x(2 / 3)
        if my_move in ['Bet 2/3 Pot || Call']:
            bet = max(self.bet_pot_list[0:6])
            if bet > 0:
                self.click_call()
            else:
                self.click_pot_x(2 / 3)
        if my_move in ['Bet 2/3 Pot || AllIn(30)',
                       'Bet 2/3 Pot || AllIn',
                       'Bet 2/3 Pot || Raise 3.25x (AllIn)']:
            bet = max(self.bet_pot_list[0:6])
            if bet > 0:
                self.click_allin()
            else:
                self.click_pot_x(2 / 3)
        if my_move in ['Raise 3']:
            self.click_BB(3)
        if my_move in ['Raise 3+Limpers']:
            limpers = self.bet_pot_list.count(1) - 1
            self.click_BB(3 + limpers)
        if my_move in ['Raise 3.25x']:
            self.click_bet_x(3.25)
        if my_move in ['Check, Raise 3.25x']:
            bet = max(self.bet_pot_list[0:6])
            if bet > 0:
                self.click_bet_x(3.25)
            else:
                self.click_check()
        if my_move in ['Raise 3.25x || Fold']:
            bet = max(self.bet_pot_list[0:6])
            if bet > 0:
                self.click_fold(sti)
            else:
                self.click_bet_x(3.25)
        if my_move in ['Raise 3.25x || AllIn(50)',
                       'Raise 3.25x || AllIn']:
            bet = max(self.bet_pot_list[0:6])
            if bet > 0:
                self.click_allin()
            else:
                self.click_bet_x(3.25)
        if my_move in ['AllIn']:
            self.click_allin()

    def click_fold(self, sti):
        self.pl_inTG_last = 0
        mk.click_on_area(*self.buttons_area[0])
        self.clear_table(sti)

    def click_check(self):
        mk.click_on_area(*self.buttons_area[1])

    def click_call(self):
        mk.click_on_area(*self.buttons_area[1])

    def click_BB(self, x):
        mk.click_on_area(*self.buttons_area[4])
        mk.write_on_area(round(x))
        mk.click_on_area(*self.buttons_area[2])

    def click_bet_x(self, x):
        bet = max(self.bet_pot_list[0:6])
        mk.click_on_area(*self.buttons_area[4])
        mk.write_on_area(round(x * bet))
        mk.click_on_area(*self.buttons_area[2])

    def click_pot_x(self, x):
        pot = self.bet_pot_list[6]
        mk.click_on_area(*self.buttons_area[4])
        mk.write_on_area(round(x * pot))
        mk.click_on_area(*self.buttons_area[2])

    def click_allin(self):
        mk.click_on_area(*self.buttons_area[3])
        mk.click_on_area(*self.buttons_area[2])
