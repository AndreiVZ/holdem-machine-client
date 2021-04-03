import random
from datetime import datetime


def MyMove(InTG, Stack, Bet, Position0, Board0, MyCards0, Pot, log_file=0):
    # получение Position_i, Position_s, Board, MyCards
    Params_Preparing(Position0, Board0, MyCards0)

    # определение улицы
    if Board_01[0] == '-':
        MyMove = Preflop(InTG, Stack, Bet, Position_i_01, Position_s_01, Board_01, MyCards_01, Pot, log_file)
    elif Board_01[6] == '-':
        MyMove = Flop(InTG, Stack, Bet, Position_i_01, Position_s_01, Board_01, MyCards_01, Pot, log_file)
    elif Board_01[8] == '-':
        MyMove = Turn(InTG, Stack, Bet, Position_i_01, Position_s_01, Board_01, MyCards_01, Pot, log_file)
    else:
        MyMove = River(InTG, Stack, Bet, Position_i_01, Position_s_01, Board_01, MyCards_01, Pot, log_file)

    return MyMove


def Params_Preparing(Position0, Board0, MyCards0):
    global Position_i_01, Position_s_01, Board_01, MyCards_01

    Position_i_01 = Position0.copy()
    Position_s_01 = Position_name(Position0)
    Board_01 = Board_order(Board0)
    MyCards_01 = MyCards_order(MyCards0)


def Position_name(Position):
    # разметка позиций по названиям
    Position_list = ['SB', 'BB', 'EP', 'MP', 'CO', 'BTN']
    Position_max = max(Position)
    for i in range(0, max(Position) - 2):
        ind_max = Position.index(Position_max - i)
        Position[ind_max] = Position_list.pop()
    Position[Position.index(1)] = 'SB'
    Position[Position.index(2)] = 'BB'
    return Position


def Board_order(Board):
    # Preflop
    if Board[0] == '-':
        return Board

    # Flop (Turn, River)
    # отсортируем карты боарда по порядку
    CardsOrder = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    Board_order = []
    for i in CardsOrder:
        if Board[0] == i:
            Board_order.extend(Board[0:2])
        if Board[2] == i:
            Board_order.extend(Board[2:4])
        if Board[4] == i:
            Board_order.extend(Board[4:6])
    # восстановим карты Turn и River
    Board_order.extend(Board[6:10])
    return Board_order


def MyCards_order(MyCards):
    if MyCards[0] < MyCards[2]:
        MyCards_order = []
        MyCards_order.extend(MyCards[2:4])
        MyCards_order.extend(MyCards[0:2])
        return MyCards_order
    else:
        return MyCards


def MyHand(MyCards):
    # конвертация [12, 'h', 5, 's'] в '125o'
    if MyCards[0] == MyCards[2]:
        return str(MyCards[0]) + str(MyCards[2])
    elif MyCards[1] == MyCards[3]:
        return str(MyCards[0]) + str(MyCards[2]) + 's'
    elif MyCards[1] != MyCards[3]:
        return str(MyCards[0]) + str(MyCards[2]) + 'o'


def Preflop(InTG, Stack, Bet, Position_i, Position_s, Board, MyCards, Pot, log_file):
    # log_file.write('\n---Preflop--- ' + datetime.now().strftime('%Y%m%d_%H%M%S') + '\n')
    Round = 2 if Bet[5] > 1 else 1
    # определим MyPosition & max_bet
    MyPosition = Position_s[5]
    # log_file.write(f'MyPosition = {MyPosition}\n')
    # log_file.write(f'MyHand = {MyHand(MyCards)}\n')

    # actions_before_me in ['None', 'Limpers', 'Raise', 'Raise || Call', '3Bet', '4Bet || AllIn']
    max_bet = max(Bet)
    if max_bet == 1.0:  # банк не открыт
        Limpers_total = Bet.count(1.0) - 1
        Limpers_positions = []  # сколько было лимперов и т.д.
        # установим actions_before_me ---------------------------------------------------
        if Limpers_total == 0:
            actions_before_me = 'None'
        elif Limpers_total >= 1:
            actions_before_me = 'Limpers'
            # заполним Limpers_positions ------------------------------------------------
            if MyPosition != 'SB' and MyPosition != 'BB':
                range_end = Position_i[5]
            else:
                range_end = max(Position_i) + 1
            for i in range(3, range_end):
                # место игрока (строка) в Position_s ('SB'-'BTN')
                if Bet[Position_i.index(i)] == 1:
                    Limpers_positions.append([0, Position_s[Position_i.index(i)],
                                              1, Stack[Position_i.index(i)]])
            if MyPosition == 'BB':
                # проверка для SB
                if Bet[Position_i.index(1)] == 1:
                    Limpers_positions.append([0, Position_s[Position_i.index(1)],
                                              1, Stack[Position_i.index(1)]])
            # ---------------------------------------------------------------------------
        players_positions = Limpers_positions
        # -------------------------------------------------------------------------------
    else:  # банк открыт
        max_bet = 1.0
        Raises_total = 0
        Raisers_positions = []  # сколько было ставок больше 1BB и т.д.
        Raisers_positions_start = False
        # заполним Raisers_positions ----------------------------------------------------
        Position_i_FromMe = Position_i[0:5]
        Position_i_FromMe.insert(0, Position_i[5])
        for i in Position_i_FromMe:
            if Bet[Position_i.index(i)] > max_bet:
                max_bet = Bet[Position_i.index(i)]
                Raises_total += 1
                Raisers_positions_start = True
            if max_bet == Bet[Position_i.index(i)] and Raisers_positions_start:
                # место игрока (строка) в Position_s ('SB'-'BTN')
                Raisers_positions.append([Raises_total, Position_s[Position_i.index(i)],
                                          max_bet, Stack[Position_i.index(i)]])
        # -------------------------------------------------------------------------------
        players_positions = Raisers_positions
        # установим actions_before_me ---------------------------------------------------
        if Raises_total == 1:
            if len(Raisers_positions) == 1:
                actions_before_me = 'Raise'
            else:
                actions_before_me = 'Raise || Call'
        elif Raises_total == 2:
            actions_before_me = '3Bet'
        else:
            actions_before_me = '4Bet || AllIn'

    # actions_before_me с учетом max_bet ------------------------------------------------
    if actions_before_me in ['Raise', 'Raise || Call']:
        if max_bet >= 8:
            actions_before_me = '3Bet'
    if actions_before_me == '3Bet':
        if max_bet >= 27:
            actions_before_me = '4Bet || AllIn'

    # определим MyMove ----------------------------------------------------------------
    MyMove = PreflopMyMove(MyPosition, MyHand(MyCards), Round, actions_before_me, players_positions)

    # окончательное действие на PreFlop -------------------------------------------------------------------
    # log_file.write(f'MyMove = {MyMove}\n')
    return MyMove


def PlayersMoneyMoreXBB(PlayersPos, X, MyPosition):  # хотя бы у одного игрока больше XBB
    for i in range(len(PlayersPos)):
        if PlayersPos[i][1] != MyPosition and PlayersPos[i][2] + PlayersPos[i][3] >= X:
            return True
    return False


def PreflopMyMove(MyPosition, MyHand, Round, BeforeMe, PlayersPos):
    global ImIP_01, ImAgg_01, LimpPot_01
    ImAgg_01 = True    # по умолчанию
    ImIP_01 = True     # по умолчанию
    LimpPot_01 = False # по умолчанию
    Position_list = ['SB', 'BB', 'EP', 'MP', 'CO', 'BTN']
    for i in PlayersPos:
        # если хоть у кого-то есть позиция на меня
        if Position_list.index(i[1]) > Position_list.index(MyPosition):
            ImIP_01 = False
            break

    # premium ----------------------------------------------------------------- OK
    if MyHand in ['1414', '1313', '1212',
                  '1413s', '1413o']:
        if BeforeMe in ['None']:
            return 'Raise 3'
        if BeforeMe in ['Limpers']:
            return 'Raise 3+Limpers'
        if BeforeMe in ['Raise', 'Raise || Call']:
            return '3Bet IP 3x' if ImIP_01 else '3Bet OOP 4x'
        if BeforeMe in ['3Bet']:
            if MyHand in ['1212', '1413s', '1413o']:
                ImAgg_01 = False
                return 'Call'  # 4Bet (Round=2) может определить как 3Bet и сыграть Call
            else:
                return '4Bet 27 || AllIn'
        if BeforeMe in ['4Bet || AllIn']:
            if MyHand in ['1414', '1313']:
                return '4Bet 27 || AllIn'
            else:
                if PlayersMoneyMoreXBB(PlayersPos, 50, MyPosition):  # (если >= 50BB)
                    return 'Fold'
                else:
                    return '4Bet 27 || AllIn(50)'

    # strong broadway --------------------------------------------------------- OK
    elif MyHand in ['1412s', '1412o',
                    '1411s', '1411o',
                    '1312s', '1312o']:
        if BeforeMe in ['None']:
            return 'Raise 3'
        if BeforeMe in ['Limpers']:
            return 'Raise 3+Limpers'
        if BeforeMe in ['Raise', 'Raise || Call']:
            if PlayersMoneyMoreXBB(PlayersPos, 50, MyPosition):  # (если >= 50BB)
                ImAgg_01 = False
                return 'Call'
            else:
                if MyHand in ['1412s', '1412o']:
                    return '3Bet(50) IP 3x' if ImIP_01 else '3Bet(50) OOP 4x'
                else:
                    ImAgg_01 = False
                    return 'Call'
        if BeforeMe in ['3Bet']:
            if MyHand in ['1412s', '1412o']:
                ImAgg_01 = False
                return 'Call'  # 4Bet (Round=2) может определить как 3Bet и сыграть Call
            else:
                return 'Fold'
        if BeforeMe in ['4Bet || AllIn']:
            if Round == 1:
                return 'Fold'
            else:
                if PlayersMoneyMoreXBB(PlayersPos, 50, MyPosition):  # (если >= 50BB)
                    return 'Fold'
                else:
                    if MyHand in ['1412s', '1412o']:
                        return '4Bet 27 || AllIn(50)'
                    else:
                        return 'Fold'

    # weak broadway ----------------------------------------------------------- OK
    elif MyHand in ['1410s', '1410o',
                    '1311s', '1311o']:
        if BeforeMe in ['None']:
            if MyPosition in ['EP']:
                return 'Fold'
            else:
                return 'Raise 3'
        if BeforeMe in ['Limpers']:
            if MyPosition in ['EP']:
                return 'Fold'
            else:
                return 'Raise 3+Limpers'
        if BeforeMe in ['Raise', 'Raise || Call']:
            return 'Fold'
        if BeforeMe in ['3Bet', '4Bet || AllIn']:
            if Round == 1:
                return 'Fold'
            else:
                if PlayersMoneyMoreXBB(PlayersPos, 30, MyPosition):  # (если >= 30BB)
                    return 'Fold'
                else:
                    return '4Bet 27 || AllIn(30)'

    # strong pairs ------------------------------------------------------------ OK
    elif MyHand in ['1111', '1010', '99', '88']:
        if BeforeMe in ['None']:
            return 'Raise 3'
        if BeforeMe in ['Limpers']:
            return 'Raise 3+Limpers'
        if BeforeMe in ['Raise', 'Raise || Call']:
            if PlayersMoneyMoreXBB(PlayersPos, 50, MyPosition):  # (если >= 50BB)
                ImAgg_01 = False
                return 'Call'
            else:
                if MyHand in ['1111', '1010']:
                    return '3Bet(50) IP 3x' if ImIP_01 else '3Bet(50) OOP 4x'
                else:
                    ImAgg_01 = False
                    return 'Call'
        if BeforeMe in ['3Bet']:
            if MyHand in ['1111', '1010']:
                ImAgg_01 = False
                return 'Call'  # 4Bet (Round=2) может определить как 3Bet и сыграть Call
            else:
                return 'Fold'
        if BeforeMe in ['4Bet || AllIn']:
            if Round == 1:
                return 'Fold'
            else:
                if PlayersMoneyMoreXBB(PlayersPos, 50, MyPosition):  # (если >= 50BB)
                    return 'Fold'
                else:
                    if MyHand in ['1111', '1010']:
                        return '4Bet 27 || AllIn(50)'
                    else:
                        return 'Fold'

    # weak pairs -------------------------------------------------------------- OK
    elif MyHand in ['77', '66', '55', '44', '33', '22']:
        if BeforeMe in ['None']:
            return 'Raise 3'
        if BeforeMe in ['Limpers']:
            if MyPosition in ['MP', 'CO', 'BTN']:
                if PlayersMoneyMoreXBB(PlayersPos, 30, MyPosition):  # (если >= 30BB)
                    return 'Raise 3+Limpers'
                else:
                    return 'Fold'
            if MyPosition in ['SB']:
                LimpPot_01 = True
                ImAgg_01 = False
                return 'Call'
            if MyPosition in ['BB']:
                LimpPot_01 = True
                ImAgg_01 = False
                return 'Check'
        if BeforeMe in ['Raise', 'Raise || Call']:
            if PlayersMoneyMoreXBB(PlayersPos, 70, MyPosition):  # (если >= 70BB)
                ImAgg_01 = False
                return 'Call'
            else:
                return 'Fold'
        if BeforeMe in ['3Bet', '4Bet || AllIn']:
            return 'Fold'

    # major connectors -------------------------------------------------------- OK
    elif MyHand in ['1310s', '1310o',
                    '1211s', '1211o',
                    '1210s', '1210o',
                    '1110s', '1110o']:
        if BeforeMe in ['None']:
            if MyPosition in ['EP', 'MP']:
                return 'Fold'
            else:
                return 'Raise 3'
        if BeforeMe in ['Limpers']:
            if MyPosition in ['BB']:
                LimpPot_01 = True
                ImAgg_01 = False
                return 'Check'
            else:
                return 'Raise 3+Limpers'
        if BeforeMe in ['Raise', 'Raise || Call']:
            return 'Fold'
        if BeforeMe in ['3Bet', '4Bet || AllIn']:
            if Round == 1:
                return 'Fold'
            else:
                if PlayersMoneyMoreXBB(PlayersPos, 30, MyPosition):  # (если >= 30BB)
                    return 'Fold'
                else:
                    return '4Bet 27 || AllIn(30)'

    # 'CO', 'BTN' ------------------------------------------------------------- OK
    elif MyHand in ['149s', '148s', '147s', '146s', '145s', '144s', '143s', '142s',
                    '139s', '138s',
                    '129s',
                    '119s',
                    '109s',
                    '98s',
                    '87s',
                    '149o', '148o', '147o',
                    '139o', '138o',
                    '129o',
                    '119o']:
        if BeforeMe in ['None']:
            if MyPosition in ['EP', 'MP']:
                return 'Fold'
            else:
                return 'Raise 3'
        if BeforeMe in ['Limpers']:
            if MyPosition in ['CO', 'BTN']:
                if PlayersMoneyMoreXBB(PlayersPos, 30, MyPosition):  # (если >= 30BB)
                    return 'Raise 3+Limpers'
                else:
                    return 'Fold'
            elif MyPosition in ['SB']:
                LimpPot_01 = True
                ImAgg_01 = False
                return 'Call'
            elif MyPosition in ['BB']:
                LimpPot_01 = True
                ImAgg_01 = False
                return 'Check'
            else:
                return 'Fold'
        if BeforeMe in ['Raise', 'Raise || Call', '3Bet', '4Bet || AllIn']:
            return 'Fold'

    # 'BTN' ------------------------------------------------------------------- OK
    elif MyHand in ['137s', '136s', '135s', '134s', '133s', '132s',
                    '128s', '127s',
                    '118s',
                    '108s',
                    '97s',
                    '86s',
                    '76s', '75s',
                    '65s',
                    '146o', '145o', '144o', '143o', '142o',
                    '109o']:
        if BeforeMe in ['None']:
            if MyPosition in ['EP', 'MP', 'CO']:
                return 'Fold'
            else:
                return 'Raise 3'
        if BeforeMe in ['Limpers']:
            if MyPosition in ['BTN']:
                if PlayersMoneyMoreXBB(PlayersPos, 30, MyPosition):  # (если >= 30BB)
                    return 'Raise 3+Limpers'
                else:
                    return 'Fold'
            elif MyPosition in ['SB']:
                LimpPot_01 = True
                ImAgg_01 = False
                return 'Call'
            elif MyPosition in ['BB']:
                LimpPot_01 = True
                ImAgg_01 = False
                return 'Check'
            else:
                return 'Fold'
        if BeforeMe in ['Raise', 'Raise || Call', '3Bet', '4Bet || AllIn']:
            return 'Fold'

    # MyHand is not in any range ----------------------------------------------
    else:
        if BeforeMe in ['None', 'Limpers'] and MyPosition in ['BB']:
            LimpPot_01 = True
            ImAgg_01 = False
            return 'Check'
        else:
            return 'Fold'


def Flop(InTG, Stack, Bet, Position_i, Position_s, Board, MyCards, Pot, log_file):
    global ImIP_01, ImAgg_01, LimpPot_01
    # log_file.write('---Flop--- ' + datetime.now().strftime('%Y%m%d_%H%M%S') + '\n')
    # Good or Bad Flop is ---------------------------------------------------------------
    FlopIsGood = CheckFlopIsGood(Board, InTG, MyCards)
    # log_file.write(f'FlopIsGood = {FlopIsGood}\n')
    # Power of MyHand -------------------------------------------------------------------
    MyCards_Board = []
    MyCards_Board.extend(MyCards)
    try:
        MyCards_Board.extend(Board[0:int(Board.index('-'))])
    except ValueError:
        MyCards_Board.extend(Board[0:10])
    MyHandPower = FlopHandPower(MyCards_Board, FlopIsGood, log_file)
    # log_file.write(f'MyHandPower = {MyHandPower}\n')

    # определим MyMove ----------------------------------------------------------------
    # обновим все переменные:
    ImIP_01 = CheckImIP(InTG, Position_i)
    # убедимся, что я все еще агрессор (проверка на DonkBet)
    # ImAgg_01 = True  # здесь д.б. доступно global ImAgg_01 (с Preflop) !!!! ПОТОМ УДАЛИТЬ !!!!
    if ImAgg_01:
        ImAgg_01 = CheckImAgg(Bet, Position_i)
    # log_file.write(f'ImAgg = {ImAgg_01}\n')
    HUPot = True if sum(InTG) == 2 else False
    ImRaised = True if Bet[5] > 0 else False
    # log_file.write(f'ImRaised = {ImRaised}\n')
    if LimpPot_01:
        # log_file.write(f'LimpPot = {LimpPot_01}\n')
        MyMove = FlopMyMove_LimpPot_01(ImAgg_01, ImIP_01, ImRaised, HUPot, FlopIsGood, MyHandPower, InTG, Stack, Bet, Pot, MyCards_Board)
    else:
        MyMove = FlopMyMove(ImAgg_01, ImIP_01, ImRaised, HUPot, FlopIsGood, MyHandPower, InTG, Stack, Bet, Pot, MyCards_Board)

    # окончательное действие на Flop ----------------------------------------------------
    # log_file.write(f'MyMove = {MyMove}\n')
    return MyMove


def CheckImIP(InTG, Position_i):
    for i in range(0, 5):
        if InTG[i] and Position_i[i] > Position_i[5]:
            return False
    return True


def CheckImAgg(Bet, Position_i):
    for i in range(0, 5):  # был DonkBet - инициатива перехвачена
        if Position_i[i] < Position_i[5] and Bet[i] > 0 and Bet[5] == 0:
            return False
    return True


def FlopHandPower(Cards, FlopIsGood, log_file):
    # log_file.write(f'{Cards}\n')

    # правильный порядок для Rank & Suit ------------------------------------------------
    RankOrder = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    SuitOrder = ['h', 'c', 'd', 's']
    # массивы 15 * 4 и 4 * 15 из 0
    DeckBySuits = [[0] * 15 for i in range(4)]  # (+1: Ace is 1 or 14, +1: index 0 is useless)
    DeckByRank = [[0] * 4 for i in range(15)]  # (+1: Ace is 1 or 14, +1: index 0 is useless)
    for i in range(0, len(Cards), 2):
        r = RankOrder.index(int(Cards[i]))
        s = SuitOrder.index(Cards[i + 1])
        DeckByRank[r][s] = 1
        DeckBySuits[s][r] = 1
        if r == 14:  # '14' can be '1' in Straight
            DeckByRank[1][s] = 1
            DeckBySuits[s][1] = 1

    # классификация Hand_Rank ===========================================================
    # Hand_Rank in [0 - 'Air', 1 - '1Pair', 2 - '2Pairs', 3 - 'Set', 4 - 'Straight',
    #               5 - 'Flush', 6 - 'FullHouse', 7 - 'Four', 8 - 'StraightFlush']

    # 1. найдем совпадения --------------------------------------------------------------
    Hand1 = []
    Ranges = [0, 0, 0, 0, 0]
    for i in range(4, 0, -1):  # кол-во возможных совпадений от каре и ниже
        for j in range(14, 1, -1):
            if sum(DeckByRank[j]) == i:
                Ranges[i] += 1
                for z in range(0, i):
                    Hand1.append(j)
    if Ranges[2] == 3:
        Hand1_5 = Hand1[0:4]
        Hand1_5.append(max(Hand1[5], Hand1[-1]))
    else:
        Hand1_5 = Hand1[0:5]

    # подсчитаем Hand_Rank (изначально Hand_Rank = 0)
    Hand_Rank = 0
    if Ranges[2] == 1:
        Hand_Rank = 1
    if Ranges[2] >= 2:
        Hand_Rank = 2
    if Ranges[3] == 1:
        if Ranges[2] > 0:
            Hand_Rank = 6
        else:
            Hand_Rank = 3
    if Ranges[3] == 2:
        Hand_Rank = 6
    if Ranges[4] > 0:
        Hand_Rank = 7

    # 2. найдем стрит -------------------------------------------------------------------
    Hand2 = []
    for i in range(14, 0, -1):
        if sum(DeckByRank[i]) > 0:
            Hand2.append(i)

    for i in range(0, len(Hand2) - 4):
        if Hand2[i] - Hand2[i + 4] == 4 and Hand_Rank < 4:
            Hand_Rank = 4
            Hand2_5 = Hand2[i:i + 5]

    # 3. найдем флеш --------------------------------------------------------------------
    # сколько карт каждой масти
    Hand3 = []
    for i in DeckBySuits:
        if sum(i[2:]) >= 5 and Hand_Rank < 5:
            Hand_Rank = 5
            for j in range(14, 0, -1):
                if i[j]:
                    Hand3.append(j)
            Hand3_5 = Hand3[0:5]

            # 4. проверим флеш на стрит-флеш --------------------------------------------
            for x in range(0, len(Hand3) - 4):
                if Hand3[x] - Hand3[x + 4] == 4 and Hand_Rank < 8:
                    Hand_Rank = 8
                    Hand4_5 = Hand3[x:x + 5]

    # Hand_Final - выберем сильнейшую комбинацию ----------------------------------------
    if Hand_Rank in [8]:
        Hand_Final = Hand4_5
    elif Hand_Rank in [5]:
        Hand_Final = Hand3_5
    elif Hand_Rank in [4]:
        Hand_Final = Hand2_5
    else:
        Hand_Final = Hand1_5
    # log_file.write(f'Hand_Final = {Hand_Final}\n')

    # классификация Rank_Final (полная) =================================================
    # Rank_Final in ['Air',
    #                'DrawW', 'DrawM', 'DrawS',
    #                'ThirdPair', 'SecondPair',
    #                'TPWK', 'TPSK', 'TPTK',
    #                'OverPair', '2Pairs',
    #                'Set', 'Straight', 'Flush',
    #                'FullHouse', 'Four', 'StraightFlush']

    # подсчитаем Rank_Final (изначально Rank_Final = 'Air')
    Rank_Final = 'Air'
    if Hand_Rank == 0:  # ---------------------------------------------------------------
        # ситуация 01: DrawW (слабые дро) -----------------------------------------------
        # ситуация 01A: гатшот
        # ситуация 01B: любой гатшот на «плохом» флопе
        # 'дырявый' гатшот
        for i in range(0, len(Hand2) - 3):  # уже есть Hand2
            if Hand2[i] - Hand2[i + 3] == 4:
                Rank_Final = 'DrawW_Gutshot_01A'
        # гатшот с тузом
        if (Hand2[0] == 14 and Hand2[3] == 11) or (Hand2[-1] == 1 and Hand2[-4] == 4):
            Rank_Final = 'DrawW_Gutshot_01A14'
        # ситуация 01C: гатшот с одной оверкартой
        for i in range(0, len(Hand2) - 3):
            if Hand2[i] - Hand2[i + 3] == 4 and Cards[2] < Cards[4] < Cards[0]:
                Rank_Final = 'DrawW_Gutshot_01C'
        # ситуация 01D: открытое стрит-дро на монотонном флопе
        if Cards[5] == Cards[7] == Cards[9]:
            for i in range(0, len(Hand2) - 3):
                if Hand2[i] - Hand2[i + 3] == 3:
                    Rank_Final = 'DrawW_StrDraw_01D'
        # ситуация 01E: открытое стрит-дро на «плохом» флопе
        if not FlopIsGood:
            for i in range(0, len(Hand2) - 3):
                if Hand2[i] - Hand2[i + 3] == 3:
                    # исключим гатшот с тузом 'Gutshot_01A14'
                    if Hand2[i] != 14 and Hand2[i + 3] != 1:
                        Rank_Final = 'DrawW_StrDraw_01E'
        # ситуация 01F: флэш-дро с одной картой (до Q) на монотонном флопе
        if Cards[5] == Cards[7] == Cards[9]:
            if Cards[1] == Cards[5] and Cards[0] < 12:
                Rank_Final = 'DrawW_FlushDraw_01F'
            if Cards[3] == Cards[5] and Cards[2] < 12:
                Rank_Final = 'DrawW_FlushDraw_01F'

        # ситуация 02: DrawM (средние дро) -----------------------------------------------
        # ситуация 02A: среднее или слабое флэш-дро с 2мя картами (до 11 вкл.)
        if Cards[1] == Cards[3]:
            suits = Cards[4:10].count(Cards[1])
            if suits == 2 and Cards[0] <= 11:
                Rank_Final = 'DrawM_FlushDraw_02A'
        # ситуация 02D1: две оверкарты плюс гатшот (без 14)
        for i in range(0, len(Hand2) - 3):
            if Hand2[i] - Hand2[i + 3] == 4 and Cards[2] > Cards[4]:
                Rank_Final = 'DrawM_Gutshot_02D1'
        # ситуация 02D2: две оверкарты плюс гатшот (с 14)
        for i in range(0, len(Hand2) - 3):
            if Hand2[i] - Hand2[i + 3] == 3 and Cards[2] > Cards[4] and Cards[0] == 14:
                Rank_Final = 'DrawM_Gutshot_02D2'
        # ситуация 02E: открытое стрит-дро на «хорошем» флопе
        if FlopIsGood:
            for i in range(0, len(Hand2) - 3):
                if Hand2[i] - Hand2[i + 3] == 3:
                    # исключим гатшот с тузом 'Gutshot_01A14'
                    if Hand2[i] != 14 and Hand2[i + 3] != 1:
                        Rank_Final = 'DrawM_StrDraw_02E'
        # ситуация 02F: гатшот плюс флэш-дро на монотонном флопе
        if Cards[5] == Cards[7] == Cards[9]:
            if Cards[1] == Cards[5] or Cards[3] == Cards[5]:
                # 'дырявый' гатшот
                for i in range(0, len(Hand2) - 3):
                    if Hand2[i] - Hand2[i + 3] == 4:
                        Rank_Final = 'DrawM_Gut_FlushDraw_02F'
                # гатшот с тузом
                if (Hand2[0] == 14 and Hand2[3] == 11) or (Hand2[-1] == 1 and Hand2[-4] == 4):
                    Rank_Final = 'DrawM_Gut_FlushDraw_02F14'
        # ситуация 02G: натс флэш-дро без оверкарт
        if Cards[1] == Cards[3]:
            suits = Cards[4:10].count(Cards[1])
            if suits == 2 and Cards[0] < Cards[4]:  # без оверкарт
                # натс
                for i in range(14, 10, -1):
                    if i in [Cards[0]]:
                        Rank_Final = 'DrawM_Nuts_FlushDraw_02G'
                        break
                    elif i in Cards[4:8+1]:
                        continue
                    else:
                        break
        # ситуация 02J: натс флэш-дро с одной оверкартой на «хорошем» флопе
        if FlopIsGood and Cards[1] == Cards[3]:
            suits = Cards[4:10].count(Cards[1])
            if suits == 2 and Cards[2] < Cards[4] < Cards[0]:  # 1 оверкарта
                if Cards[0] == 14:  # натс
                    Rank_Final = 'DrawM_Nuts_FlushDraw_02J'
        # ситуация 02K: натс флэш-дро с двумя оверкартами на «плохом» флопе
        if not FlopIsGood and Cards[1] == Cards[3]:
            suits = Cards[4:10].count(Cards[1])
            if suits == 2 and Cards[2] > Cards[4]:  # 2 оверкарты
                # натс
                if Cards[0] == 14:
                    Rank_Final = 'DrawM_Nuts_FlushDraw_02K'
        # ситуация 02L: флэш-дро с одной картой A, K, Q, на монотонном флопе
        if Cards[5] == Cards[7] == Cards[9]:
            if Cards[1] == Cards[5] and Cards[0] >= 12:
                Rank_Final = 'DrawM_FlushDraw_02L'
            if Cards[3] == Cards[5] and Cards[2] >= 12:
                Rank_Final = 'DrawM_FlushDraw_02L'
        # ситуация 02N: стрит-флэш дро на монотонной доске
        if Cards[5] == Cards[7] == Cards[9]:
            Str_FlushDraw = []
            for i in DeckBySuits:
                if sum(i[2:]) == 4:
                    for j in range(14, 0, -1):
                        if i[j]:
                            Str_FlushDraw.append(j)
            if Cards[1] == Cards[5] or Cards[3] == Cards[5]:
                # 'дырявый' гатшот
                for i in range(0, len(Str_FlushDraw) - 3):
                    if Str_FlushDraw[i] - Str_FlushDraw[i + 3] == 4:
                        Rank_Final = 'DrawM_Str-FlushDraw_02N1'
                # открытое стрит-дро (вкл. гатшот с тузом)
                for i in range(0, len(Str_FlushDraw) - 3):
                    if Str_FlushDraw[i] - Str_FlushDraw[i + 3] == 3:
                        Rank_Final = 'DrawM_Str-FlushDraw_02N2'
        # описание в 'if Hand_Rank == 1'
            # ситуация 02B: пара плюс открытое стрит-дро
            # ситуация 02C: пара плюс гатшот
            # ситуация 02H: оверпара плюс флэш-дро на монотонной доске
            # ситуация 02I: оверпара плюс стрит-дро на «плохом» флопе
            # ситуация 02M: топ пара плюс натс флэш-дро на монотонном флопе

        # ситуация 03: DrawS (сильные дро) -----------------------------------------------
        # ситуация 03A: стрит-флэш дро
        if Cards[1] == Cards[3]:
            suits = Cards[4:10].count(Cards[1])
            if suits == 2:
                Str_FlushDraw = []
                for i in DeckBySuits:
                    if sum(i[2:]) == 4:
                        for j in range(14, 0, -1):
                            if i[j]:
                                Str_FlushDraw.append(j)
                # 'дырявый' гатшот
                for i in range(0, len(Str_FlushDraw) - 3):
                    if Str_FlushDraw[i] - Str_FlushDraw[i + 3] == 4:
                        Rank_Final = 'DrawS_Str-FlushDraw_03A1'
                # открытое стрит-дро (вкл. гатшот с тузом)
                for i in range(0, len(Str_FlushDraw) - 3):
                    if Str_FlushDraw[i] - Str_FlushDraw[i + 3] == 3:
                        Rank_Final = 'DrawS_Str-FlushDraw_03A2'
        # ситуация 03B: стрит-дро плюс флэш-дро
        if Cards[1] == Cards[3]:
            suits = Cards[4:10].count(Cards[1])
            if suits == 2:
                # 'дырявый' гатшот
                for i in range(0, len(Hand2) - 3):
                    if Hand2[i] - Hand2[i + 3] == 4:
                        Rank_Final = 'DrawS_StrDraw_FlushDraw_03B1'
                # открытое стрит-дро (вкл. гатшот с тузом)
                for i in range(0, len(Hand2) - 3):
                    if Hand2[i] - Hand2[i + 3] == 3:
                        Rank_Final = 'DrawS_StrDraw_FlushDraw_03B2'
        # ситуация 03C: натс флэш-дро плюс две оверкарты на «хорошем» флопе
        if FlopIsGood and Cards[1] == Cards[3]:
            suits = Cards[4:10].count(Cards[1])
            if suits == 2 and Cards[2] > Cards[4]:  # 2 оверкарты
                if Cards[0] == 14:  # натс
                    Rank_Final = 'DrawS_Nuts_FlushDraw_03C'
        # описание в 'if Hand_Rank == 1'
            # ситуация 03D: пара плюс натс флэш-дро
            # ситуация 03E: пара плюс слабое или среднее флэш-дро

    if Hand_Rank == 1:  # ---------------------------------------------------------------
        # ситуация 11: у меня 2 разные карты
        # ситуация 11A: у меня топ пара с 1й картой
        if Cards[0] == Cards[4]:
            # топ кикер (максимальный)
            for i in range(14, 10, -1):
                if i in [Cards[2]]:
                    Rank_Final = 'TPTK_11A'
                    break
                elif i in Cards[4:8+1]:
                    continue
                else:
                    # слабый кикер (< 10)
                    if Cards[2] < 10:
                        Rank_Final = 'TPWK_11A'
                        break
                    else:
                        # сильный кикер (10-13)
                        Rank_Final = 'TPSK_11A'
                        break
        # ситуация 11B: у меня топ пара со 2й картой
        if Cards[2] == Cards[4]:
            # топ кикер (максимальный)
            for i in range(14, 10, -1):
                if i in [Cards[0]]:
                    Rank_Final = 'TPTK_11B'
                    break
                elif i in Cards[4:8+1]:
                    continue
                else:
                    # слабый кикер (< 10)
                    if Cards[0] < 10:
                        Rank_Final = 'TPWK_11B'
                        break
                    else:
                        # сильный кикер (10-13)
                        Rank_Final = 'TPSK_11B'
                        break
        # ситуация 12: у меня вторая пара
        if Cards[6] in Cards[0:2+1]:
            Rank_Final = 'SecondPair_12'
        # ситуация 13: у меня третья пара и хуже
        if Cards[8] in Cards[0:2+1]:
            Rank_Final = 'ThirdPair_13'
        # ситуация 14: у меня карманная пара
        if Cards[0] == Cards[2]:
            # ситуация 14A: у меня овер пара
            if Cards[4] < Cards[0]:
                Rank_Final = 'OverPair_14A'
            # ситуация 14B: у меня вторая пара
            if Cards[6] < Cards[0] < Cards[4]:
                Rank_Final = 'SecondPair_14B'
            # ситуация 14C: у меня третья пара и хуже
            if Cards[0] < Cards[6]:
                Rank_Final = 'ThirdPair_14C'

        # ситуация 15: DrawM (средние дро) вторая пара или лучше ------------------------
        # ситуация 15A(02B): пара плюс открытое стрит-дро
        if 'TP' in Rank_Final or 'SecondPair' in Rank_Final:
            for i in range(0, len(Hand2) - 3):
                if Hand2[i] - Hand2[i + 3] == 3:
                    # исключим гатшот с тузом
                    if Hand2[i] != 14 and Hand2[i + 3] != 1:
                        Rank_Final = 'DrawM_StrDraw_15A'
        # ситуация 15B(02C): пара плюс гатшот
        if 'TP' in Rank_Final or 'SecondPair' in Rank_Final:
            # 'дырявый' гатшот
            for i in range(0, len(Hand2) - 3):
                if Hand2[i] - Hand2[i + 3] == 4:
                    Rank_Final = 'DrawM_Gutshot_15B'
            # гатшот с тузом
            if (Hand2[0] == 14 and Hand2[3] == 11) or (Hand2[-1] == 1 and Hand2[-4] == 4):
                Rank_Final = 'DrawM_Gutshot_15B14'
        # ситуация 15C(02H): оверпара плюс флэш-дро на монотонной доске
        if 'OverPair' in Rank_Final and Cards[5] == Cards[7] == Cards[9]:
            if Cards[1] == Cards[5] or Cards[3] == Cards[5]:
                Rank_Final = 'DrawM_FlushDraw_15C'
        # ситуация 15D(02I): оверпара плюс стрит-дро на «плохом» флопе
        if 'OverPair' in Rank_Final and not FlopIsGood:
            for i in range(0, len(Hand2) - 3):
                if Hand2[i] - Hand2[i + 3] == 3:
                    # исключим гатшот с тузом
                    if Hand2[i] != 14 and Hand2[i + 3] != 1:
                        Rank_Final = 'DrawM_StrDraw_15D'
        # ситуация 15E(02M): топ пара плюс натс флэш-дро на монотонном флопе
        if Cards[5] == Cards[7] == Cards[9] and 'TPTK' in Rank_Final:
            if Cards[1] == Cards[5] or Cards[3] == Cards[5]:
                Rank_Final = 'DrawM_Nuts_FlushDraw_15E'

        # ситуация 16: DrawS (сильные дро) ----------------------------------------------
        # ситуация 16A(03D): пара плюс натс флэш-дро
        # ситуация 16B(03E): пара плюс слабое или среднее флэш-дро
        if 'TP' in Rank_Final or 'SecondPair' in Rank_Final:
            if Cards[1] == Cards[3]:
                suits = Cards[4:10].count(Cards[1])
                if suits == 2:
                    Rank_Final = 'DrawS_FlushDraw_16AB'

    if Hand_Rank == 2:
        # ситуация 21: у меня 2 разные карты
        if Cards[0] != Cards[2]:
            if Cards[0] in Cards[4:8+1] and Cards[2] in Cards[4:8+1]:
                Rank_Final = '2Pairs_21'
            if Cards[4] == Cards[6]:
                Rank_Final = 'SecondPair_21'
            if Cards[6] == Cards[8]:
                if Cards[0] == Cards[4]:
                    if Cards[2] < 10:
                        Rank_Final = 'TPWK_21'
                    else:
                        Rank_Final = 'TPSK_21'
                if Cards[2] == Cards[4]:
                    if Cards[0] < 10:
                        Rank_Final = 'TPWK_21'
                    else:
                        Rank_Final = 'TPSK_21'

        # ситуация 22: у меня карманная пара
        if Cards[0] == Cards[2]:
            # ситуация 22A: у меня оверпара
            if Cards[4] < Cards[0]:
                Rank_Final = 'OverPair_22A'
            # ситуация 22B: у меня вторая пара
            if Cards[6] < Cards[0] < Cards[4]:
                Rank_Final = 'SecondPair_22B'
            # ситуация 22C: у меня третья пара и хуже
            if Cards[0] < Cards[6]:
                Rank_Final = 'ThirdPair_22C'

    if Hand_Rank == 3:
        # ситуация 31: у меня карманная пара (сет)
        if Cards[0] == Cards[2]:
            Rank_Final = 'Set_31'
        # ситуация 32: у меня 2 разные карты (трипс)
        if Cards[0] != Cards[2]:
            if Cards[6] in Cards[0:2+1]:
                Rank_Final = 'Set_32'
            else:  # BINGO флоп (777)
                pass

    if Hand_Rank == 4:
        Rank_Final = 'Straight'
    if Hand_Rank == 5:
        Rank_Final = 'Flush'
    if Hand_Rank == 6:
        Rank_Final = 'FullHouse'
    if Hand_Rank == 7:
        Rank_Final = 'Four'
    if Hand_Rank == 8:
        Rank_Final = 'StraightFlush'

    # пока не поменяли Rank_Final -------------------------------------------------------
    Rank_Final_Details = Rank_Final
    # определим общую силу руки ---------------------------------------------------------
    #   Rank_Final = 'Air'
    if 'DrawW' in Rank_Final:
        Rank_Final = 'DrawW'
    if 'DrawM' in Rank_Final:
        Rank_Final = 'DrawM'
    if 'DrawS' in Rank_Final:
        Rank_Final = 'DrawS'
    if 'ThirdPair' in Rank_Final:
        Rank_Final = 'ThirdPair'
    if 'SecondPair' in Rank_Final:
        Rank_Final = 'SecondPair'
    if 'TPWK' in Rank_Final:
        Rank_Final = 'TPWK'
    if 'TPSK' in Rank_Final:
        Rank_Final = 'TPSK'
    if 'TPTK' in Rank_Final:
        Rank_Final = 'TPTK'
    if 'OverPair' in Rank_Final:
        Rank_Final = 'OverPair'
    if '2Pairs' in Rank_Final:
        Rank_Final = '2Pairs'
    if 'Set' in Rank_Final:
        Rank_Final = 'Set'
    #   Rank_Final = 'Straight'
    #   Rank_Final = 'Flush'
    #   Rank_Final = 'FullHouse'
    #   Rank_Final = 'Four'
    #   Rank_Final = 'StraightFlush'
    # -----------------------------------------------------------------------------------
    return [Rank_Final, Rank_Final_Details]


def CheckFlopIsGood(Board, InTG, MyCards):
    # Good or Bad Flop is ---------------------------------------------------------------
    if Board[1] == Board[3] == Board[5] and sum(InTG) >= 3:  # одномастный флоп и мультивей
        return False
    if Board[0] == Board[2] or Board[2] == Board[4]:  # спаренный флоп
        return True
    elif Board[0] - Board[4] > 4:  # нескоординированный флоп
        return True
    elif Board[0] == 4 and Board[4] == 2:  # 4-3-2
        if MyCards[0] == 14:
            return True
        else:
            return False
    else:
        return False


def FlopMyMove(ImAgg_01, ImIP_01, ImRaised, HUPot, FlopIsGood, MyHandPowerAll, InTG, Stack, Bet, Pot, Cards):
    MyHandPower = MyHandPowerAll[0]
    MyHandPowerDetails = MyHandPowerAll[1]
    # MyHandPower in ['Air',
    #                 'DrawW', 'DrawM', 'DrawS',
    #                 'ThirdPair', 'SecondPair',
    #                 'TPWK', 'TPSK', 'TPTK',
    #                 'OverPair', '2Pairs',
    #                 'Set', 'Straight', 'Flush',
    #                 'FullHouse', 'Four', 'StraightFlush']
    if ImAgg_01:  # с инициативой ----------------------------------------------------------
        if HUPot:
            if FlopIsGood:
                if not ImRaised:
                    return 'CBet 2/3 Pot'
                else:
                    if MyHandPower in ['Air', 'DrawW', 'DrawM', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Fold'
                    elif MyHandPower in ['TPSK', 'TPTK']:
                        if MoreThenXBB(InTG, Stack, Bet, 50):  # (если >= 50BB)
                            return 'Fold'
                        else:
                            return 'Raise 3.25x || AllIn(50)'
                    elif MyHandPower in ['OverPair']:
                        if Cards[5] == Cards[7] == Cards[9]:
                            return 'Fold'
                        else:
                            if Cards[0] in [14, 13, 12] or Cards[0] - Cards[4] >= 4:
                                return 'Raise 3.25x || AllIn'
                            else:
                                if MoreThenXBB(InTG, Stack, Bet, 50):  # (если >= 50BB)
                                    return 'Fold'
                                else:
                                    return 'Raise 3.25x || AllIn(50)'
                    elif MyHandPower in ['2Pairs']:
                        if Cards[5] == Cards[7] == Cards[9]:
                            return 'Fold'
                        else:
                            return 'Raise 3.25x || AllIn'
                    else:
                        return 'Raise 3.25x || AllIn'
            else:
                if not ImRaised:
                    if MyHandPower in ['Air', 'DrawW', 'ThirdPair']:
                        return 'Check || Fold'
                    else:
                        return 'CBet 4/5 Pot'
                else:
                    if MyHandPower in ['Air', 'DrawW', 'ThirdPair']:
                        return 'Check || Fold'
                    elif MyHandPower in ['DrawM', 'SecondPair', 'TPWK']:
                        return 'Fold'
                    elif MyHandPower in ['TPSK', 'TPTK', 'OverPair', '2Pairs']:
                        if MoreThenXBB(InTG, Stack, Bet, 50):  # (если >= 50BB)
                            return 'Fold'
                        else:
                            return 'Raise 3.25x || AllIn(50)'
                    else:
                        return 'Raise 3.25x || AllIn'
        else:  # мультипот
            if FlopIsGood:
                if not ImRaised:
                    return 'CBet 2/3 Pot'
                else:
                    if MyHandPower in ['Air', 'DrawW', 'DrawM', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Fold'
                    elif MyHandPower in ['TPSK', 'TPTK', 'OverPair', '2Pairs']:
                        if MoreThenXBB(InTG, Stack, Bet, 50):  # (если >= 50BB)
                            return 'Fold'
                        else:
                            return 'Raise 3.25x || AllIn(50)'
                    else:
                        return 'Raise 3.25x || AllIn'
            else:
                if not ImRaised:
                    if MyHandPower in ['Air', 'DrawW', 'ThirdPair', 'SecondPair']:
                        return 'Check || Fold'
                    else:
                        return 'CBet 4/5 Pot'
                else:
                    if MyHandPower in ['Air', 'DrawW', 'ThirdPair', 'SecondPair']:
                        return 'Check || Fold'
                    elif MyHandPower in ['DrawM', 'TPWK', 'TPSK', 'TPTK', 'OverPair', '2Pairs']:
                        return 'Fold'
                    else:
                        return 'Raise 3.25x || AllIn'
    else:  # без инициативы -------------------------------------------------------------
        if HUPot:
            # Если я префлоп коллер против 1 игрока, и он сделал на флопе чек -
            # делать ставку 2/3 банка на любом флопе с любой рукой
            if ImIP_01 and max(Bet) == 0:
                return 'Float 2/3 Pot'

            if FlopIsGood:
                if ImIP_01:
                    if MyHandPower in ['Air', 'ThirdPair']:
                        return 'Fold'
                    elif MyHandPower in ['DrawW']:
                        if not ImRaised:
                            return RandomChoice('Raise 3.25x', 50, 'Fold', 50)
                        else:
                            return 'Fold'
                    elif MyHandPower in ['DrawM']:
                        if not ImRaised:
                            if '_15' in MyHandPowerDetails:
                                return 'Call'
                            else:
                                return 'Raise 3.25x'
                        else:
                            return 'Fold'
                    elif MyHandPower in ['SecondPair', 'TPWK', 'TPSK', 'TPTK', 'OverPair']:
                        return 'Call'
                    elif MyHandPower in ['2Pairs']:
                        if Cards[5] == Cards[7] == Cards[9]:
                            return 'Call'
                        else:
                            if not ImRaised:
                                return 'Raise 3.25x'
                            else:
                                return 'AllIn'
                    else:
                        if not ImRaised:
                            return 'Raise 3.25x'
                        else:
                            return 'AllIn'
                else:  # тоже самое, только сначала 'Check'
                    if MyHandPower in ['Air', 'ThirdPair']:
                        return 'Check, Fold'
                    elif MyHandPower in ['DrawW']:
                        if not ImRaised:
                            return RandomChoice('Check, Raise 3.25x', 50, 'Check, Fold', 50)
                        else:
                            return 'Fold'
                    elif MyHandPower in ['DrawM']:
                        if not ImRaised:
                            if '_15' in MyHandPowerDetails:
                                return 'Check, Call'
                            else:
                                return 'Check, Raise 3.25x'
                        else:
                            return 'Fold'
                    elif MyHandPower in ['SecondPair', 'TPWK', 'TPSK', 'TPTK', 'OverPair']:
                        return 'Check, Call'
                    elif MyHandPower in ['2Pairs']:
                        if Cards[5] == Cards[7] == Cards[9]:
                            return 'Check, Call'
                        else:
                            if not ImRaised:
                                return 'Check, Raise 3.25x'
                            else:
                                return 'AllIn'
                    else:
                        if not ImRaised:
                            return 'Check, Raise 3.25x'
                        else:
                            return 'AllIn'
            else:
                if ImIP_01:
                    if MyHandPower in ['Air', 'DrawW', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Fold'
                    elif MyHandPower in ['DrawM', 'TPSK', 'TPTK', 'OverPair', '2Pairs']:
                        return 'Call'
                    else:
                        if not ImRaised:
                            return 'Raise 3.25x'
                        else:
                            return 'AllIn'
                else:  # тоже самое, только сначала 'Check'
                    if MyHandPower in ['Air', 'DrawW', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check, Fold'
                    elif MyHandPower in ['DrawM', 'TPSK', 'TPTK', 'OverPair', '2Pairs']:
                        return 'Check, Call'
                    else:
                        if not ImRaised:
                            return 'Check, Raise 3.25x'
                        else:
                            return 'AllIn'
        else:  # мультипот
            if FlopIsGood:
                if ImIP_01:
                    if MyHandPower in ['Air', 'DrawW', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Fold'
                    elif MyHandPower in ['DrawM', 'TPSK', 'TPTK', 'OverPair', '2Pairs']:
                        return 'Call'
                    else:
                        if not ImRaised:
                            return 'Raise 3.25x'
                        else:
                            return 'AllIn'
                else:  # тоже самое, только сначала 'Check'
                    if MyHandPower in ['Air', 'DrawW', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check, Fold'
                    elif MyHandPower in ['DrawM', 'TPSK', 'TPTK', 'OverPair', '2Pairs']:
                        return 'Check, Call'
                    else:
                        if not ImRaised:
                            return 'Check, Raise 3.25x'
                        else:
                            return 'AllIn'
            else:
                if ImIP_01:
                    if MyHandPower in ['Air', 'DrawW', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Fold'
                    elif MyHandPower in ['DrawM', 'TPSK', 'TPTK', 'OverPair', '2Pairs']:
                        return 'Call'
                    else:
                        if not ImRaised:
                            return 'Raise 3.25x'
                        else:
                            return 'AllIn'
                else:  # тоже самое, только сначала 'Check'
                    if MyHandPower in ['Air', 'DrawW', 'DrawM', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check, Fold'
                    elif MyHandPower in ['TPSK', 'TPTK', 'OverPair', '2Pairs']:
                        return 'Check, Call'
                    else:
                        if not ImRaised:
                            return 'Check, Raise 3.25x'
                        else:
                            return 'AllIn'


def FlopMyMove_LimpPot_01(ImAgg_01, ImIP_01, ImRaised, HUPot, FlopIsGood, MyHandPowerAll, InTG, Stack, Bet, Pot, Cards):
    MyHandPower = MyHandPowerAll[0]
    MyHandPowerDetails = MyHandPowerAll[1]
    # MyHandPower in ['Air',
    #                 'DrawW', 'DrawM', 'DrawS',
    #                 'ThirdPair', 'SecondPair',
    #                 'TPWK', 'TPSK', 'TPTK',
    #                 'OverPair', '2Pairs',
    #                 'Set', 'Straight', 'Flush',
    #                 'FullHouse', 'Four', 'StraightFlush']

    if max(Bet) == 0:
        if MyHandPower in ['Air', 'DrawW', 'ThirdPair']:
            return 'Check || Fold'
        elif MyHandPower in ['DrawM', 'SecondPair']:
            return 'Bet 2/3 Pot || Fold'
        elif MyHandPower in ['DrawS']:
            return 'Bet 2/3 Pot || Call'
        elif MyHandPower in ['TPWK', 'TPSK', 'TPTK']:
            if MoreThenXBB(InTG, Stack, Bet, 30):  # (если >= 30BB)
                return 'Bet 2/3 Pot || Fold'
            else:
                return 'Bet 2/3 Pot || AllIn(30)'
        elif MyHandPower in ['OverPair']:
            if MoreThenXBB(InTG, Stack, Bet, 30):  # (если >= 30BB)
                return 'Bet 2/3 Pot || Call'
            else:
                return 'Bet 2/3 Pot || AllIn(30)'
        else:
            return 'Bet 2/3 Pot || AllIn'
    else:
        if MyHandPower in ['Air', 'DrawW', 'ThirdPair', 'SecondPair']:
            return 'Fold'
        elif MyHandPower in ['DrawM', 'DrawS', 'TPWK']:
            return 'Call'
        elif MyHandPower in ['TPSK', 'TPTK', 'OverPair']:
            if MoreThenXBB(InTG, Stack, Bet, 30):  # (если >= 30BB)
                return 'Raise 3.25x || Fold'
            else:
                return 'Raise 3.25x || AllIn(30)'
        else:
            return 'Raise 3.25x || AllIn'


def RandomChoice(*args):
    ran = random.randint(1, 100)
    sum = 0
    for i in range(0, len(args), 2):
        sum += args[i + 1]
        if ran <= sum:
            return args[i]


def MoreThenXBB(InTG, Stack, Bet, X):
    for i in range(0, 5):  # хотя бы у 1 игрока стек на начало торгов >= X
        if InTG[i] and Stack[i] + Bet[i] >= X:
            return True
    return False


def Turn(InTG, Stack, Bet, Position_i, Position_s, Board, MyCards, Pot, log_file):
    global ImIP_01, ImAgg_01, LimpPot_01
    # log_file.write('---Turn--- ' + datetime.now().strftime('%Y%m%d_%H%M%S') + '\n')

    # Power of MyHand -------------------------------------------------------------------
    MyCards_Board = []
    MyCards_Board.extend(MyCards)
    try:
        MyCards_Board.extend(Board[0:int(Board.index('-'))])
    except ValueError:
        MyCards_Board.extend(Board[0:10])
    # log_file.write(f'{MyCards_Board}\n')
    MyHandPower = TurnHandPower(MyCards_Board, log_file)

    # Turn Situation --------------------------------------------------------------------
    FlopIsGood = CheckFlopIsGood(Board[0:6], InTG, MyCards)
    MySituation = TurnSituation(MyCards_Board[4:len(MyCards_Board)], FlopIsGood)
    # уточним силу руки с одной парой и TurnSituation == 'ScaryCard'
    if MySituation == 'ScaryCard':
        MyHandPowerOnFlop = FlopHandPower(MyCards_Board[0:10], FlopIsGood, log_file)
        PairList = ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK', 'OverPair']
        if MyHandPower[0] in PairList and MyHandPowerOnFlop[0] in PairList:
            if PairList.index(MyHandPowerOnFlop[0]) > PairList.index(MyHandPower[0]):
                MyHandPowerOnFlop.extend(MyHandPower)
                MyHandPower = MyHandPowerOnFlop
    # log_file.write(f'MyHandPower = {MyHandPower}\n')
    # log_file.write(f'TurnSituation = {MySituation}\n')

    # определим MyMove --------------------------------------------------------------
    # обновим все переменные:
    ImIP_01 = CheckImIP(InTG, Position_i)
    # убедимся, что я все еще агрессор (проверка на DonkBet)
    # ImAgg_01 = True  # здесь д.б. доступно global ImAgg_01 (с Preflop) !!!! ПОТОМ УДАЛИТЬ !!!!
    if ImAgg_01:
        ImAgg_01 = CheckImAgg(Bet, Position_i)
    # log_file.write(f'ImAgg = {ImAgg_01}\n')
    HUPot = True if sum(InTG) == 2 else False
    ImRaised = True if Bet[5] > 0 else False
    # log_file.write(f'ImRaised = {ImRaised}\n')
    if LimpPot_01:
        # log_file.write(f'LimpPot = {LimpPot_01}\n')
        MyMove = TurnMyMove_LimpPot_01(ImAgg_01, ImIP_01, ImRaised, HUPot, FlopIsGood, MyHandPower, MySituation, InTG, Stack, Bet, Pot, MyCards_Board)
    else:
        MyMove = TurnMyMove(ImAgg_01, ImIP_01, ImRaised, HUPot, FlopIsGood, MyHandPower, MySituation, InTG, Stack, Bet, Pot, MyCards_Board)

    # окончательное действие на Turn ----------------------------------------------------
    # log_file.write(f'MyMove = {MyMove}\n')
    return MyMove


def TurnHandPower(Cards_unsort, log_file):
    # отсортируем карты Флопа и Терна
    Cards_sort = []
    Cards_sort.extend(Cards_unsort[0:4])
    for i in range(4, 12, 2):
        if Cards_unsort[10] > Cards_unsort[i]:
            Cards_sort.extend(Cards_unsort[10:12])
            Cards_sort.extend(Cards_unsort[i:10])
            break
        else:
            Cards_sort.extend(Cards_unsort[i:i + 2])
    Cards = Cards_sort

    # правильный порядок для Rank & Suit ------------------------------------------------
    RankOrder = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    SuitOrder = ['h', 'c', 'd', 's']
    # массивы 15 * 4 и 4 * 15 из 0
    DeckBySuits = [[0] * 15 for i in range(4)]  # (+1: Ace is 1 or 14, +1: index 0 is useless)
    DeckByRank = [[0] * 4 for i in range(15)]  # (+1: Ace is 1 or 14, +1: index 0 is useless)
    for i in range(0, len(Cards), 2):
        r = RankOrder.index(int(Cards[i]))
        s = SuitOrder.index(Cards[i + 1])
        DeckByRank[r][s] = 1
        DeckBySuits[s][r] = 1
        if r == 14:  # '14' can be '1' in Straight
            DeckByRank[1][s] = 1
            DeckBySuits[s][1] = 1

    # классификация Hand_Rank ===========================================================
    # Hand_Rank in [0 - 'Air', 1 - '1Pair', 2 - '2Pairs', 3 - 'Set', 4 - 'Straight',
    #               5 - 'Flush', 6 - 'FullHouse', 7 - 'Four', 8 - 'StraightFlush']

    # 1. найдем совпадения --------------------------------------------------------------
    Hand1 = []
    Ranges = [0, 0, 0, 0, 0]
    for i in range(4, 0, -1):  # кол-во возможных совпадений от каре и ниже
        for j in range(14, 1, -1):
            if sum(DeckByRank[j]) == i:
                Ranges[i] += 1
                for z in range(0, i):
                    Hand1.append(j)
    if Ranges[2] == 3:
        Hand1_5 = Hand1[0:4]
        Hand1_5.append(max(Hand1[5], Hand1[-1]))
    else:
        Hand1_5 = Hand1[0:5]

    # подсчитаем Hand_Rank (изначально Hand_Rank = 0)
    Hand_Rank = 0
    if Ranges[2] == 1:
        Hand_Rank = 1
    if Ranges[2] >= 2:
        Hand_Rank = 2
    if Ranges[3] == 1:
        if Ranges[2] > 0:
            Hand_Rank = 6
        else:
            Hand_Rank = 3
    if Ranges[3] == 2:
        Hand_Rank = 6
    if Ranges[4] > 0:
        Hand_Rank = 7

    # 2. найдем стрит -------------------------------------------------------------------
    Hand2 = []
    for i in range(14, 0, -1):
        if sum(DeckByRank[i]) > 0:
            Hand2.append(i)

    for i in range(0, len(Hand2) - 4):
        if Hand2[i] - Hand2[i + 4] == 4 and Hand_Rank < 4:
            Hand_Rank = 4
            Hand2_5 = Hand2[i:i + 5]

    # 3. найдем флеш --------------------------------------------------------------------
    # сколько карт каждой масти
    Hand3 = []
    for i in DeckBySuits:
        if sum(i[2:]) >= 5 and Hand_Rank < 5:
            Hand_Rank = 5
            for j in range(14, 0, -1):
                if i[j]:
                    Hand3.append(j)
            Hand3_5 = Hand3[0:5]

            # 4. проверим флеш на стрит-флеш --------------------------------------------
            for x in range(0, len(Hand3) - 4):
                if Hand3[x] - Hand3[x + 4] == 4 and Hand_Rank < 8:
                    Hand_Rank = 8
                    Hand4_5 = Hand3[x:x + 5]

    # Hand_Final - выберем сильнейшую комбинацию ----------------------------------------
    if Hand_Rank in [8]:
        Hand_Final = Hand4_5
    elif Hand_Rank in [5]:
        Hand_Final = Hand3_5
    elif Hand_Rank in [4]:
        Hand_Final = Hand2_5
    else:
        Hand_Final = Hand1_5
    # log_file.write(f'Hand_Final = {Hand_Final}\n')

    # классификация Rank_Final (полная) =================================================
    # Rank_Final in ['Air',
    #                'StrDraw', 'FlushDraw', 'PairStrDraw', 'PairFlushDraw', 'StrongDraw',
    #                'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK', 'OverPair',
    #                '2PairsW', '2PairsS', 'Set', 'Straight', 'FlushW', 'FlushS',
    #                'FullHouse', 'Four', 'StraightFlush']

    # подсчитаем Rank_Final (изначально Rank_Final = 'Air')
    Rank_Final = 'Air'
    if Hand_Rank == 0:
        # ситуация 01: StrDraw ----------------------------------------------------------
        # ситуация 01A: любой гатшот
        # 'дырявый' гатшот
        for i in range(0, len(Hand2) - 3):  # уже есть Hand2
            if Hand2[i] - Hand2[i + 3] == 4:
                if Cards[0] in Hand2[i:i + 4] or Cards[2] in Hand2[i:i + 4]:  # мои карты
                    Rank_Final = 'StrDraw_Gutshot_01A'
        # гатшот с тузом
        if Hand2[0] == 14 and Hand2[3] == 11:
            if Cards[0] in Hand2[0:4] or Cards[2] in Hand2[0:4]:  # мои карты
                Rank_Final = 'StrDraw_Gutshot_01A14'
        if Hand2[-1] == 1 and Hand2[-4] == 4:
            if Cards[0] in Hand2[-4:0] or Cards[2] in Hand2[-4:0]:  # мои карты
                Rank_Final = 'StrDraw_Gutshot_01A14'
        # ситуация 01B: открытое стрит-дро
        for i in range(0, len(Hand2) - 3):
            if Hand2[i] - Hand2[i + 3] == 3 and (Hand2[i] != 14 and Hand2[i + 3] != 1):
                if Cards[0] in Hand2[i:i + 4] or Cards[2] in Hand2[i:i + 4]:  # мои карты
                    Rank_Final = 'StrDraw_Open_01B'

        # ситуация 02: FlushDraw --------------------------------------------------------
        # ситуация 02A: флэш-дро с 2 картами
        if Cards[1] == Cards[3]:
            suits = Cards[4:12].count(Cards[1])
            if suits == 2:
                if Cards[0] in [14, 13]:
                    Rank_Final = 'FlushDrawS_02A'
                else:
                    Rank_Final = 'FlushDrawW_02A'
        # ситуация 02B: флэш-дро с одной картой
        if Cards[1] != Cards[3]:
            # 1я карта
            suits = Cards[4:12].count(Cards[1])
            if suits == 3:
                if Cards[0] in [14, 13]:
                    Rank_Final = 'FlushDrawS_02B1'
                else:
                    Rank_Final = 'FlushDrawW_02B1'
            # 2я карта
            suits = Cards[4:12].count(Cards[3])
            if suits == 3:
                if Cards[2] in [14, 13]:
                    Rank_Final = 'FlushDrawS_02B2'
                else:
                    Rank_Final = 'FlushDrawW_02B2'

        # ситуация 03: StrongDraw -------------------------------------------------------
        # ситуация 03A: стрит-дро плюс флэш-дро
        if Cards[1] == Cards[3]:
            suits = Cards[4:12].count(Cards[1])
            if suits == 2:
                # 'дырявый' гатшот
                for i in range(0, len(Hand2) - 3):
                    if Hand2[i] - Hand2[i + 3] == 4:
                        if Cards[0] in Hand2[i:i + 4] or Cards[2] in Hand2[i:i + 4]:  # мои карты
                            Rank_Final = 'StrongDraw_Str&Flush_03A1'
                # открытое стрит-дро (вкл. гатшот с тузом)
                for i in range(0, len(Hand2) - 3):
                    if Hand2[i] - Hand2[i + 3] == 3:
                        if Cards[0] in Hand2[i:i + 4] or Cards[2] in Hand2[i:i + 4]:  # мои карты
                            Rank_Final = 'StrongDraw_Str&Flush_03A2'
        # ситуация 03B: стрит-флэш дро с 2 картами
        if Cards[1] == Cards[3]:
            suits = Cards[4:12].count(Cards[1])
            if suits == 2:
                Str_FlushDraw = []
                for i in DeckBySuits:
                    if sum(i[2:]) == 4:
                        for j in range(14, 0, -1):
                            if i[j]:
                                Str_FlushDraw.append(j)
                # 'дырявый' гатшот
                for i in range(0, len(Str_FlushDraw) - 3):
                    if Str_FlushDraw[i] - Str_FlushDraw[i + 3] == 4:
                        if Cards[0] in Str_FlushDraw[i:i + 4] or Cards[2] in Str_FlushDraw[i:i + 4]:  # мои карты
                            Rank_Final = 'StrongDraw_Str-Flush_03B1'
                # открытое стрит-дро (вкл. гатшот с тузом)
                for i in range(0, len(Str_FlushDraw) - 3):
                    if Str_FlushDraw[i] - Str_FlushDraw[i + 3] == 3:
                        if Cards[0] in Str_FlushDraw[i:i + 4] or Cards[2] in Str_FlushDraw[i:i + 4]:  # мои карты
                            Rank_Final = 'StrongDraw_Str-Flush_03B2'

    if Hand_Rank == 1:  # ---------------------------------------------------------------
        # ситуация 11: PairStrDraw ------------------------------------------------------
        # ситуация 11A: пара + любой гатшот
        # 'дырявый' гатшот
        for i in range(0, len(Hand2) - 3):  # уже есть Hand2
            if Hand2[i] - Hand2[i + 3] == 4:
                if Cards[0] in Hand2[i:i + 4] or Cards[2] in Hand2[i:i + 4]:  # мои карты
                    Rank_Final = 'PairStrDraw_Gutshot_11A'
        # гатшот с тузом
        if Hand2[0] == 14 and Hand2[3] == 11:
            if Cards[0] in Hand2[0:4] or Cards[2] in Hand2[0:4]:  # мои карты
                Rank_Final = 'PairStrDraw_Gutshot_11A14'
        if Hand2[-1] == 1 and Hand2[-4] == 4:
            if Cards[0] in Hand2[-4:0] or Cards[2] in Hand2[-4:0]:  # мои карты
                Rank_Final = 'PairStrDraw_Gutshot_11A14'
        # ситуация 11B:  пара + открытое стрит-дро
        for i in range(0, len(Hand2) - 3):
            if Hand2[i] - Hand2[i + 3] == 3 and (Hand2[i] != 14 and Hand2[i + 3] != 1):
                if Cards[0] in Hand2[i:i + 4] or Cards[2] in Hand2[i:i + 4]:  # мои карты
                    Rank_Final = 'PairStrDraw_Open_11B'

        # ситуация 12: PairFlushDraw --------------------------------------------------------
        if Cards[0] in Cards[4:10 + 1] or Cards[2] in Cards[4:10 + 1]:  # мои карты
            # ситуация 12A:  пара + флэш-дро с 2 картами
            if Cards[1] == Cards[3]:
                suits = Cards[4:12].count(Cards[1])
                if suits == 2:
                    if Cards[0] in [14, 13]:
                        Rank_Final = 'PairFlushDrawS_12A'
                    else:
                        Rank_Final = 'PairFlushDrawW_12A'
            # ситуация 12B:  пара + флэш-дро с одной картой
            if Cards[1] != Cards[3]:
                # 1я карта
                suits = Cards[4:12].count(Cards[1])
                if suits == 3:
                    if Cards[0] in [14, 13]:
                        Rank_Final = 'PairFlushDrawS_12B1'
                    else:
                        Rank_Final = 'PairFlushDrawW_12B1'
                # 2я карта
                suits = Cards[4:12].count(Cards[3])
                if suits == 3:
                    if Cards[2] in [14, 13]:
                        Rank_Final = 'PairFlushDrawS_12B2'
                    else:
                        Rank_Final = 'PairFlushDrawW_12B2'

        # ситуация 13: у меня 2 разные карты --------------------------------------------
        # ситуация 13A: у меня топ пара с 1й картой
        if Cards[0] == Cards[4]:
            # топ кикер (максимальный)
            for i in range(14, 10, -1):
                if i in [Cards[2]]:
                    Rank_Final = 'TPTK_13A'
                    break
                elif i in Cards[4:10 + 1]:
                    continue
                else:
                    # слабый кикер (< 10)
                    if Cards[2] < 10:
                        Rank_Final = 'TPWK_13A'
                        break
                    else:
                        # сильный кикер (10-13)
                        Rank_Final = 'TPSK_13A'
                        break
        # ситуация 13B: у меня топ пара со 2й картой
        if Cards[2] == Cards[4]:
            # топ кикер (максимальный)
            for i in range(14, 10, -1):
                if i in [Cards[0]]:
                    Rank_Final = 'TPTK_13B'
                    break
                elif i in Cards[4:10 + 1]:
                    continue
                else:
                    # слабый кикер (< 10)
                    if Cards[0] < 10:
                        Rank_Final = 'TPWK_13B'
                        break
                    else:
                        # сильный кикер (10-13)
                        Rank_Final = 'TPSK_13B'
                        break

        # ситуация 14: у меня вторая пара
        if Cards[6] in Cards[0:2 + 1]:
            Rank_Final = 'SecondPair_14'
        # ситуация 15: у меня третья пара и хуже
        if Cards[8] in Cards[0:2 + 1] or Cards[10] in Cards[0:2 + 1]:
            Rank_Final = 'ThirdPair_15'

        # ситуация 16: у меня карманная пара
        if Cards[0] == Cards[2]:
            # ситуация 16A: у меня овер пара
            if Cards[4] < Cards[0]:
                Rank_Final = 'OverPair_16A'
            # ситуация 16B: у меня вторая пара
            if Cards[6] < Cards[0] < Cards[4]:
                Rank_Final = 'SecondPair_16B'
            # ситуация 16C: у меня третья пара и хуже
            if Cards[0] < Cards[6]:
                Rank_Final = 'ThirdPair_16C'

        # ситуация 17: StrongDraw -------------------------------------------------------
        # ситуация 17A:  пара + стрит-дро плюс флэш-дро
        if Cards[1] == Cards[3]:
            suits = Cards[4:12].count(Cards[1])
            if suits == 2:
                # 'дырявый' гатшот
                for i in range(0, len(Hand2) - 3):
                    if Hand2[i] - Hand2[i + 3] == 4:
                        if Cards[0] in Hand2[i:i + 4] or Cards[2] in Hand2[i:i + 4]:  # мои карты
                            Rank_Final = 'StrongDraw_Str&Flush_17A1'
                # открытое стрит-дро (вкл. гатшот с тузом)
                for i in range(0, len(Hand2) - 3):
                    if Hand2[i] - Hand2[i + 3] == 3:
                        if Cards[0] in Hand2[i:i + 4] or Cards[2] in Hand2[i:i + 4]:  # мои карты
                            Rank_Final = 'StrongDraw_Str&Flush_17A2'
        # ситуация 17B:  пара + стрит-флэш дро с 2 картами
        if Cards[1] == Cards[3]:
            suits = Cards[4:12].count(Cards[1])
            if suits == 2:
                Str_FlushDraw = []
                for i in DeckBySuits:
                    if sum(i[2:]) == 4:
                        for j in range(14, 0, -1):
                            if i[j]:
                                Str_FlushDraw.append(j)
                # 'дырявый' гатшот
                for i in range(0, len(Str_FlushDraw) - 3):
                    if Str_FlushDraw[i] - Str_FlushDraw[i + 3] == 4:
                        if Cards[0] in Str_FlushDraw[i:i + 4] or Cards[2] in Str_FlushDraw[i:i + 4]:  # мои карты
                            Rank_Final = 'StrongDraw_Str-Flush_17B1'
                # открытое стрит-дро (вкл. гатшот с тузом)
                for i in range(0, len(Str_FlushDraw) - 3):
                    if Str_FlushDraw[i] - Str_FlushDraw[i + 3] == 3:
                        if Cards[0] in Str_FlushDraw[i:i + 4] or Cards[2] in Str_FlushDraw[i:i + 4]:  # мои карты
                            Rank_Final = 'StrongDraw_Str-Flush_17B2'

    if Hand_Rank == 2:
        # ситуация 21: у меня 2 разные карты
        if Cards[0] != Cards[2]:
            # ситуация 21A: 2PairsW
            if Cards[0] in Cards[6:10+1] and Cards[2] in Cards[6:10+1]:
                Rank_Final = '2PairsW_21A'
            #  ситуация 21B: 2PairsS
            if Cards[0] in [Cards[4]] and Cards[2] in Cards[6:10+1]:
                Rank_Final = '2PairsS_21B'

            #  ситуация 21C: SecondPair&Worse
            if Cards[4] == Cards[6] and Cards[8] == Cards[10]:
                Rank_Final = 'Air_21C'
            if Cards[4] == Cards[6] and Cards[8] != Cards[10]:
                Rank_Final = 'SecondPair&Worse_21C1'
            if Cards[6] == Cards[8] or (Cards[4] != Cards[6] and Cards[8] == Cards[10]):
                if Cards[0] == Cards[4]:
                    if Cards[2] < 10:
                        Rank_Final = 'TPWK_21C1'
                    else:
                        Rank_Final = 'TPSK_21C1'
                elif Cards[2] == Cards[4]:
                    if Cards[0] < 10:
                        Rank_Final = 'TPWK_21C2'
                    else:
                        Rank_Final = 'TPSK_21C2'
                else:
                    Rank_Final = 'SecondPair&Worse_21C2'

        # ситуация 22: у меня карманная пара
        if Cards[0] == Cards[2]:
            # ситуация 22A: у меня оверпара
            if Cards[4] < Cards[0]:
                Rank_Final = 'OverPair_22A'
            # ситуация 22B: у меня вторая пара
            if Cards[6] < Cards[0] < Cards[4]:
                Rank_Final = 'SecondPair_22B'
            # ситуация 22C: у меня третья пара и хуже
            if Cards[0] < Cards[6]:
                Rank_Final = 'SecondPair&Worse_22C'

    if Hand_Rank == 3:
        # ситуация 31: у меня карманная пара (сет)
        if Cards[0] == Cards[2]:
            Rank_Final = 'Set_31'
        # ситуация 32: у меня 2 разные карты (трипс)
        if Cards[0] != Cards[2]:
            # ситуация 32A: трипс с 1й картой
            value = Cards[4:12].count(Cards[0])
            if value == 2:
                Rank_Final = 'Set_31A'
            # ситуация 32B: трипс со 2й картой
            value = Cards[4:12].count(Cards[2])
            if value == 2:
                Rank_Final = 'Set_31B'

    if Hand_Rank == 4:
        # натсовый стрит или нет
        if Hand2_5[0] == 14:
            Rank_Final = 'StraightS'
        else:
            if Cards[0] in Hand2_5[0:4] or Cards[2] in Hand2_5[0:4]:
                Rank_Final = 'StraightS'
            else:
                Rank_Final = 'StraightW'

    if Hand_Rank == 5:
        # ситуация 51: у меня 2 одномастные карты
        if Cards[1] == Cards[3]:
            suit = Cards[4:12].count(Cards[1])
            if suit == 3:  # на боарде 3 карты к флешу
                Rank_Final = 'FlushS_51'
            if suit == 4:  # на боарде 4 карты к флешу
                if Cards[0] in [14]:
                    Rank_Final = 'FlushS_51A14'
                elif Cards[0] in [13]:
                    Rank_Final = 'FlushS_51A13'
                else:
                    Rank_Final = 'FlushW_51A'
        # ситуация 52: у меня 2 разномастные карты
        if Cards[1] != Cards[3]:
            # ситуация 52A: флеш с 1й картой
            suit = Cards[4:12].count(Cards[1])
            if suit == 4:  # на боарде 4 карты к флешу
                if Cards[0] in [14]:
                    Rank_Final = 'FlushS_52A14'
                elif Cards[0] in [13]:
                    Rank_Final = 'FlushS_52A13'
                else:
                    Rank_Final = 'FlushW_52A'
            # ситуация 52B: флеш со 2й картой
            suit = Cards[4:12].count(Cards[3])
            if suit == 4:  # на боарде 4 карты к флешу
                if Cards[2] in [14]:
                    Rank_Final = 'FlushS_52B14'
                elif Cards[2] in [13]:
                    Rank_Final = 'FlushS_52B13'
                else:
                    Rank_Final = 'FlushW_52B'

    if Hand_Rank == 6:
        Rank_Final = 'FullHouse'
    if Hand_Rank == 7:
        Rank_Final = 'Four'
    if Hand_Rank == 8:
        Rank_Final = 'StraightFlush'

    # пока не поменяли Rank_Final -------------------------------------------------------
    Rank_Final_Details = Rank_Final
    # определим общую силу руки ---------------------------------------------------------
    if 'Air' in Rank_Final:
        Rank_Final = 'Air'
    if 'StrDraw' in Rank_Final:
        Rank_Final = 'StrDraw'
    if 'FlushDraw' in Rank_Final:
        Rank_Final = 'FlushDraw'
    if 'PairStrDraw' in Rank_Final:
        Rank_Final = 'PairStrDraw'
    if 'PairFlushDraw' in Rank_Final:
        Rank_Final = 'PairFlushDraw'
    if 'StrongDraw' in Rank_Final:
        Rank_Final = 'StrongDraw'
    if 'ThirdPair' in Rank_Final:
        Rank_Final = 'ThirdPair'
    if 'SecondPair' in Rank_Final:
        Rank_Final = 'SecondPair'
    if 'TPWK' in Rank_Final:
        Rank_Final = 'TPWK'
    if 'TPSK' in Rank_Final:
        Rank_Final = 'TPSK'
    if 'TPTK' in Rank_Final:
        Rank_Final = 'TPTK'
    if 'OverPair' in Rank_Final:
        Rank_Final = 'OverPair'
    if '2PairsW' in Rank_Final:
        Rank_Final = '2PairsW'
    if '2PairsS' in Rank_Final:
        Rank_Final = '2PairsS'
    if 'Set' in Rank_Final:
        Rank_Final = 'Set'
    if 'StraightW' in Rank_Final:
        Rank_Final = 'StraightW'
    if 'StraightS' in Rank_Final:
        Rank_Final = 'StraightS'
    if 'FlushW' in Rank_Final:
        Rank_Final = 'FlushW'
    if 'FlushS' in Rank_Final:
        Rank_Final = 'FlushS'
    #   Rank_Final = 'FullHouse'
    #   Rank_Final = 'Four'
    #   Rank_Final = 'StraightFlush'
    # -----------------------------------------------------------------------------------
    return [Rank_Final, Rank_Final_Details]


def TurnSituation(Cards_unsort, FlopIsGood):
    # классификация TurnSituation
    # TurnSituation in ['Neutral', 'ScaryCard', 'VillainStronger',
    #                   'DoubleHigh', 'Flush3', 'Str4', 'Flush4']

    # отсортируем карты боарда ----------------------------------------------------------
    Cards_sort = []
    for i in range(0, 8, 2):
        if Cards_unsort[6] > Cards_unsort[i]:
            Cards_sort.extend(Cards_unsort[6:8])
            Cards_sort.extend(Cards_unsort[i:6])
            break
        else:
            Cards_sort.extend(Cards_unsort[i:i + 2])
    Cards = Cards_sort

    # подготовим Hand2 на стрит ---------------------------------------------------------
    if Cards[0] == 14:
        Hand = [Cards[0], Cards[2], Cards[4], Cards[6], 1]
    else:
        Hand = [Cards[0], Cards[2], Cards[4], Cards[6]]
    Hand2 = list(set(Hand))
    Hand2.sort(reverse=True)

    Situation = 'Neutral'  # по умолчанию, 'Neutral' == дополнительные ауты
    # ситуация: 'страшная' карта --------------------------------------------------------
    if Cards_unsort[6] > Cards_unsort[0] and Cards_unsort[6] >= 11 and FlopIsGood:
        Situation = 'ScaryCard'

    # ситуация : диапазон оппонента усилился --------------------------------------------
    # ситуация A: спарилась 2я или 3я карта Флопа
    if Cards_unsort[6] in Cards_unsort[2:4 + 1]:
        Situation = 'VillainStronger_A'
    # ситуация B: 3я карта к стриту
    # for i in range(0, len(Hand2) - 2):
    #     if Hand2[i] - Hand2[i + 2] <= 4 and Cards_unsort[6] in Hand2[i:i + 3]:
    #         Situation = 'VillainStronger_B'

    # ситуация: спарилась старшая карта -------------------------------------------------
    if Cards_unsort[6] == Cards_unsort[0]:
        Situation = 'DoubleHigh'

    # ситуация: 3 карты к флешу ---------------------------------------------------------
    suit = Cards.count('h')
    if suit == 3:
        Situation = 'Flush3'
    suit = Cards.count('c')
    if suit == 3:
        Situation = 'Flush3'
    suit = Cards.count('d')
    if suit == 3:
        Situation = 'Flush3'
    suit = Cards.count('s')
    if suit == 3:
        Situation = 'Flush3'

    # ситуация: 4 карты к стриту --------------------------------------------------------
    # ситуация A: любой гатшот
    # 'дырявый' гатшот
    for i in range(0, len(Hand2) - 3):
        if Hand2[i] - Hand2[i + 3] == 4:
            Situation = 'Str4_A'
    # гатшот с тузом верх
    if Hand2[0] == 14 and Hand2[3] == 11:
        Situation = 'Str4_A14Up'
    # гатшот с тузом низ
    if Hand2[-1] == 1 and Hand2[-4] == 4:
        Situation = 'Str4_A14Down'
    # ситуация B: открытое стрит-дро
    for i in range(0, len(Hand2) - 3):
        if Hand2[i] - Hand2[i + 3] == 3 and (Hand2[i] != 14 and Hand2[i + 3] != 1):
            Situation = 'Str4_B'

    # ситуация: 4 карты к флешу ---------------------------------------------------------
    suit = Cards.count('h')
    if suit == 4:
        Situation = 'Flush4'
    suit = Cards.count('c')
    if suit == 4:
        Situation = 'Flush4'
    suit = Cards.count('d')
    if suit == 4:
        Situation = 'Flush4'
    suit = Cards.count('s')
    if suit == 4:
        Situation = 'Flush4'

    # пока не поменяли Situation --------------------------------------------------------
    Situation_Details = Situation
    # определим общую Situation ---------------------------------------------------------
    #   Situation = 'Neutral'
    #   Situation = 'ScaryCard'
    if 'VillainStronger' in Situation:
        Situation = 'VillainStronger'
    #   Situation = 'DoubleHigh'
    #   Situation = 'Flush3'
    if 'Str4' in Situation:
        Situation = 'Str4'
    #   Situation = 'Flush4'

    return Situation


def TurnMyMove(ImAgg_01, ImIP_01, ImRaised, HUPot, FlopIsGood, MyHandPowerAll, MySituation, InTG, Stack, Bet, Pot, Cards):
    MyHandPower = MyHandPowerAll[0]
    MyHandPowerDetails = MyHandPowerAll[1]
    # MyHandPower in ['Air',
    #                 'StrDraw', 'FlushDraw', 'PairStrDraw', 'PairFlushDraw', 'StrongDraw',
    #                 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK', 'OverPair',
    #                 '2PairsW', '2PairsS', 'Set', 'StraightW', 'StraightS', 'FlushW', 'FlushS',
    #                 'FullHouse', 'Four', 'StraightFlush']

    # MySituation in ['Neutral', 'ScaryCard', 'VillainStronger',
    #                 'DoubleHigh', 'Flush3', 'Str4', 'Flush4']

    if not ImRaised:
        if ImAgg_01:  # с инициативой ------------------------------------------------------
            if ImIP_01:
                if MySituation in ['Flush3']:
                    if MyHandPower in ['Air', 'StrDraw', 'PairStrDraw', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check'
                    elif MyHandPower in ['FlushDraw', 'PairFlushDraw']:
                        if 'FlushDrawS' in MyHandPowerDetails:
                            return 'Bet 2/3 Pot'
                        else:
                            return 'Check'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['Flush4']:
                    if MyHandPower in ['FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                        return 'Bet 2/3 Pot'
                    else:
                        return 'Check'
                if MySituation in ['Str4']:
                    if MyHandPower in ['StraightS', 'FlushW', 'FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                        return 'Bet 2/3 Pot'
                    else:
                        return 'Check'
                if MySituation in ['Neutral']:
                    if MyHandPower in ['Air', 'StrDraw', 'PairStrDraw', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check'
                    elif MyHandPower in ['FlushDraw']:  # этот elif можно не писать (входит в else)
                        if Cards[1] == Cards[3]:  # у меня 2 карты к FlushDraw
                            return 'Bet 2/3 Pot'
                        else:
                            return 'Check'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['VillainStronger']:
                    if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw', 'PairFlushDraw', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['DoubleHigh']:
                    if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw', 'PairFlushDraw',
                                       'StrongDraw', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK']:
                        return 'Check'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['ScaryCard']:
                    if MyHandPower in ['TPWK']:
                        if len(MyHandPowerAll) == 2:  # т.е. TPWK пришел на терне
                            return 'Bet 2/3 Pot'
                        else:
                            return 'Check'
                    else:
                        return 'Bet 2/3 Pot'
            else:
                if MySituation in ['Flush3']:
                    if MyHandPower in ['Air', 'StrDraw', 'PairStrDraw', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check || Fold'
                    elif MyHandPower in ['FlushDraw']:
                        if 'FlushDrawS' in MyHandPowerDetails:
                            return 'Bet 2/3 Pot'
                        else:
                            return 'Check || Fold'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['Flush4']:
                    if MyHandPower in ['FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                        return 'Bet 2/3 Pot'
                    else:
                        return 'Check || Fold'
                if MySituation in ['Str4']:
                    if MyHandPower in ['StraightS', 'FlushW', 'FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                        return 'Bet 2/3 Pot'
                    else:
                        return 'Check || Fold'
                if MySituation in ['Neutral']:
                    if MyHandPower in ['Air', 'StrDraw', 'PairStrDraw', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check || Fold'
                    elif MyHandPower in ['FlushDraw']:  # этот elif можно не писать (входит в else)
                        if Cards[1] == Cards[3]:  # у меня 2 карты к FlushDraw
                            return 'Bet 2/3 Pot'
                        else:
                            return 'Check || Fold'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['VillainStronger']:
                    if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw', 'PairFlushDraw',
                                       'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check || Fold'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['DoubleHigh']:
                    if MyHandPower in ['Air', 'StrDraw', 'PairStrDraw', 'StrongDraw',
                                       'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK']:
                        return 'Check || Fold'
                    elif MyHandPower in ['FlushDraw', 'PairFlushDraw']:  # этот elif можно не писать (входит в else)
                        if Cards[1] == Cards[3]:  # у меня 2 карты к FlushDraw
                            return 'Bet 2/3 Pot'
                        else:
                            return 'Check || Fold'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['ScaryCard']:
                    return 'Bet 2/3 Pot'
        else:  # без инициативы ---------------------------------------------------------
            if ImIP_01:
                if MySituation in ['Flush3']:
                    if MyHandPower in ['Air', 'StrDraw', 'PairStrDraw', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check || Fold'
                    elif MyHandPower in ['FlushDraw', 'PairFlushDraw']:
                        if 'FlushDrawS' in MyHandPowerDetails:
                            return 'Check || Call'
                        else:
                            return 'Check || Fold'
                    elif MyHandPower in ['StrongDraw', 'TPSK', 'TPTK', 'OverPair',
                                         '2PairsW', '2PairsS', 'Set', 'StraightW', 'StraightS']:
                        return 'Bet 2/3 Pot || Call'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                if MySituation in ['Flush4']:
                    if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw',
                                       'PairFlushDraw', 'StrongDraw', 'ThirdPair', 'SecondPair']:
                        return 'Bet 2/3 Pot || Fold'
                    elif MyHandPower in ['FlushS']:
                        if '14' in MyHandPowerDetails:
                            return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                        if '13' in MyHandPowerDetails:
                            return 'Check || Call'
                    elif MyHandPower in ['FullHouse', 'Four', 'StraightFlush']:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                    else:
                        return 'Check || Fold'
                if MySituation in ['Str4']:
                    if MyHandPower in ['Air', 'StrDraw', 'PairStrDraw', 'ThirdPair', 'SecondPair']:
                        return 'Bet 2/3 Pot || Fold'
                    elif MyHandPower in ['FlushDraw', 'PairFlushDraw', 'StrongDraw',
                                       'TPWK', 'TPSK', 'TPTK', 'OverPair', '2PairsW', '2PairsS', 'Set']:
                        return 'Check || Fold'
                    elif MyHandPower in ['StraightW']:
                        return 'Bet 2/3 Pot || Call'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                if MySituation in ['Neutral']:
                    if MyHandPower in ['Air', 'StrDraw', 'PairStrDraw', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check || Fold'
                    elif MyHandPower in ['FlushDraw', 'PairFlushDraw']:
                        if 'FlushDrawS' in MyHandPowerDetails:
                            return 'Check || Call'
                        else:
                            return 'Check || Fold'
                    elif MyHandPower in ['TPSK', 'TPTK', 'OverPair', '2PairsW']:
                        return 'Bet 2/3 Pot || Call'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                if MySituation in ['VillainStronger']:
                    if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check || Fold'
                    elif MyHandPower in ['PairFlushDraw']:
                        if 'FlushDrawS' in MyHandPowerDetails:
                            return 'Check || Call'
                        else:
                            return 'Check || Fold'
                    elif MyHandPower in ['StrongDraw', 'TPSK', 'TPTK', 'OverPair', '2PairsW']:
                        return 'Bet 2/3 Pot || Call'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                if MySituation in ['DoubleHigh']:
                    if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw', 'PairFlushDraw',
                                       'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW']:
                        return 'Check || Fold'
                    elif MyHandPower in ['StrongDraw', '2PairsS', 'Set']:
                        return 'Bet 2/3 Pot || Call'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                if MySituation in ['ScaryCard']:
                    if MyHandPower in ['Air', 'StrDraw', 'ThirdPair', 'SecondPair']:
                        return 'Check || Fold'
                    elif MyHandPower in ['FlushDraw', 'PairFlushDraw']:
                        if 'FlushDrawS' in MyHandPowerDetails:
                            return 'Check || Call'
                        else:
                            return 'Check || Fold'
                    elif MyHandPower in ['PairStrDraw', 'TPWK', 'TPSK', 'TPTK', 'OverPair', '2PairsW']:
                        return 'Check || Call'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
            else:
                if MySituation in ['Flush3']:
                    if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw',
                                       'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check, Fold'
                    elif MyHandPower in ['PairFlushDraw']:
                        if 'FlushDrawS' in MyHandPowerDetails:
                            return 'Check, Call'
                        else:
                            return 'Check, Fold'
                    elif MyHandPower in ['TPSK', 'TPTK', 'OverPair', '2PairsW',
                                         '2PairsS', 'Set', 'StraightW', 'StraightS']:
                        return 'Check, Call'
                    else:
                        return 'Check, Raise 3.25x (AllIn)'
                if MySituation in ['Flush4']:
                    if MyHandPower in ['FlushS']:
                        if '14' in MyHandPowerDetails:
                            return 'Check, Raise 3.25x (AllIn)'
                        if '13' in MyHandPowerDetails:
                            return 'Check, Call'
                    elif MyHandPower in ['FullHouse', 'Four', 'StraightFlush']:
                        return 'Check, Raise 3.25x (AllIn)'
                    else:
                        return 'Check, Fold'
                if MySituation in ['Str4']:
                    if MyHandPower in ['StraightW']:
                        return 'Check, Call'
                    elif MyHandPower in ['StraightS', 'FlushW', 'FlushS',
                                         'FullHouse', 'Four', 'StraightFlush']:
                        return 'Check, Raise 3.25x (AllIn)'
                    else:
                        return 'Check, Fold'
                if MySituation in ['Neutral']:
                    if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw',
                                       'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check, Fold'
                    elif MyHandPower in ['PairFlushDraw']:
                        if 'FlushDrawS' in MyHandPowerDetails:
                            return 'Check, Call'
                        else:
                            return 'Check, Fold'
                    elif MyHandPower in ['TPSK', 'TPTK', 'OverPair', '2PairsW']:
                        return 'Check, Call'
                    else:
                        return 'Check, Raise 3.25x (AllIn)'
                if MySituation in ['VillainStronger']:
                    if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw',
                                       'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check, Fold'
                    elif MyHandPower in ['PairFlushDraw']:
                        if 'FlushDrawS' in MyHandPowerDetails:
                            return 'Check, Call'
                        else:
                            return 'Check, Fold'
                    elif MyHandPower in ['StrongDraw', 'TPSK', 'TPTK', 'OverPair', '2PairsW']:
                        return 'Check, Call'
                    else:
                        return 'Check, Raise 3.25x (AllIn)'
                if MySituation in ['DoubleHigh']:
                    if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw', 'PairFlushDraw',
                                       'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW']:
                        return 'Check, Fold'
                    elif MyHandPower in ['StrongDraw', '2PairsS', 'Set']:
                        return 'Check, Call'
                    else:
                        return 'Check, Raise 3.25x (AllIn)'
                if MySituation in ['ScaryCard']:
                    if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw',
                                       'ThirdPair', 'SecondPair']:
                        return 'Check, Fold'
                    elif MyHandPower in ['PairFlushDraw']:
                        if 'FlushDrawS' in MyHandPowerDetails:
                            return 'Check, Call'
                        else:
                            return 'Check, Fold'
                    elif MyHandPower in ['TPWK', 'TPSK', 'TPTK', 'OverPair', '2PairsW']:
                        return 'Check, Call'
                    else:
                        return 'Check, Raise 3.25x (AllIn)'
    else:
        if MyHandPower in ['StrongDraw']:
            if MySituation in ['Flush3', 'Flush4']:
                return 'Fold'
            else:
                return 'Call'

        if MySituation in ['Flush4']:
            if MyHandPower in ['FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'AllIn'
            else:
                return 'Fold'
        elif MySituation in ['Str4']:
            if MyHandPower in ['StraightS', 'FlushW', 'FlushS',
                               'FullHouse', 'Four', 'StraightFlush']:
                return 'AllIn'
            else:
                return 'Fold'
        elif MySituation in ['Flush3']:
            if MyHandPower in ['FlushW', 'FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'AllIn'
            else:
                return 'Fold'
        # MySituation not in ['Flush4', 'Str4']
        elif not MoreThenXStackPotRatio(InTG, Stack, Bet, Pot, 2.0):
            if MyHandPower in ['StrongDraw', 'TPSK', 'TPTK', 'OverPair', '2PairsW',
                               '2PairsS', 'Set', 'StraightW', 'StraightS', 'FlushW',
                               'FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'AllIn'
            else:
                return 'Fold'
        elif MyHandPower in ['2PairsS', 'Set', 'StraightW', 'StraightS', 'FlushW', 'FlushS',
                             'FullHouse', 'Four', 'StraightFlush']:
            return 'AllIn'
        else:
            return 'Fold'


def TurnMyMove_LimpPot_01(ImAgg_01, ImIP_01, ImRaised, HUPot, FlopIsGood, MyHandPowerAll, MySituation0, InTG, Stack, Bet, Pot, Cards):
    MyHandPower = MyHandPowerAll[0]
    MyHandPowerDetails = MyHandPowerAll[1]
    # MyHandPower in ['Air',
    #                 'StrDraw', 'FlushDraw', 'PairStrDraw', 'PairFlushDraw', 'StrongDraw',
    #                 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK', 'OverPair',
    #                 '2PairsW', '2PairsS', 'Set', 'StraightW', 'StraightS', 'FlushW', 'FlushS',
    #                 'FullHouse', 'Four', 'StraightFlush']

    # MySituation in ['Neutral', 'DoubleHigh', 'Flush3', 'Str4', 'Flush4']
    if MySituation0 in ['ScaryCard', 'VillainStronger']:  # отсутствуют в LimpPot_01
        MySituation = 'Neutral'
    else:
        MySituation = MySituation0

    if max(Bet) == 0:
        if MySituation in ['Flush3']:
            if MyHandPower in ['Air', 'StrDraw', 'PairStrDraw', 'ThirdPair', 'SecondPair', 'TPWK']:
                return 'Check || Fold'
            elif MyHandPower in ['FlushDraw', 'PairFlushDraw']:
                if 'FlushDrawS' in MyHandPowerDetails:
                    return 'Bet 2/3 Pot || Fold'
                else:
                    return 'Check || Fold'
            elif MyHandPower in ['StrongDraw']:
                return 'Bet 2/3 Pot || Call'
            elif MyHandPower in ['TPSK', 'TPTK', 'OverPair', '2PairsW', '2PairsS',
                                 'Set', 'StraightW', 'StraightS']:
                return 'Bet 2/3 Pot || Fold'
            else:
                return 'Bet 2/3 Pot || AllIn'
        if MySituation in ['Flush4']:
            if MyHandPower in ['FlushW']:
                return 'Bet 2/3 Pot || Fold'
            elif MyHandPower in ['FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'Bet 2/3 Pot || AllIn'
            else:
                return 'Check || Fold'
        if MySituation in ['Str4']:
            if MyHandPower in ['StraightS', 'FlushW', 'FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'Bet 2/3 Pot || AllIn'
            else:
                return 'Check || Fold'
        if MySituation in ['Neutral']:
            if MyHandPower in ['Air', 'ThirdPair', 'SecondPair']:
                return 'Check || Fold'
            elif MyHandPower in ['StrDraw', 'PairStrDraw']:
                if FlopIsGood:
                    return 'Bet 2/3 Pot || Fold'
                else:
                    return 'Check || Fold'
            elif MyHandPower in ['FlushDraw', 'PairFlushDraw']:
                if 'FlushDrawS' in MyHandPowerDetails:
                    return 'Bet 2/3 Pot || Fold'
                else:
                    return 'Check || Fold'
            elif MyHandPower in ['StrongDraw']:
                return 'Bet 2/3 Pot || Call'
            elif MyHandPower in ['TPWK', 'TPSK', 'TPTK', 'OverPair', '2PairsW']:
                return 'Bet 2/3 Pot || Fold'
            else:
                return 'Bet 2/3 Pot || AllIn'
        if MySituation in ['DoubleHigh']:
            if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw',
                               'PairFlushDraw', 'ThirdPair', 'SecondPair']:
                return 'Check || Fold'
            elif MyHandPower in ['StrongDraw', 'TPWK', 'TPSK', 'TPTK',
                                 'OverPair', '2PairsW', '2PairsS', 'Set']:
                return 'Bet 2/3 Pot || Fold'
            else:
                return 'Bet 2/3 Pot || AllIn'
    else:
        if MySituation in ['Flush3']:
            if MyHandPower in ['Air', 'StrDraw', 'PairStrDraw', 'ThirdPair',
                               'SecondPair', 'TPWK', 'TPSK', 'TPTK']:
                return 'Fold'
            elif MyHandPower in ['FlushDraw', 'PairFlushDraw']:
                if 'FlushDrawS' in MyHandPowerDetails:
                    return 'Call'
                else:
                    return 'Fold'
            elif MyHandPower in ['StrongDraw', 'OverPair', '2PairsW', '2PairsS',
                                 'Set', 'StraightW', 'StraightS']:
                return 'Call'
            else:
                return 'Raise 3.25x || AllIn'
        if MySituation in ['Flush4']:
            if MyHandPower in ['FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'Raise 3.25x || AllIn'
            else:
                return 'Fold'
        if MySituation in ['Str4']:
            if MyHandPower in ['StraightS', 'FlushW', 'FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'Raise 3.25x || AllIn'
            else:
                return 'Fold'
        if MySituation in ['Neutral']:
            if MyHandPower in ['Air', 'StrDraw', 'PairStrDraw', 'ThirdPair', 'SecondPair']:
                return 'Fold'
            elif MyHandPower in ['FlushDraw', 'PairFlushDraw']:
                if 'FlushDrawS' in MyHandPowerDetails:
                    return 'Call'
                else:
                    return 'Fold'
            elif MyHandPower in ['StrongDraw', 'TPWK', 'TPSK', 'TPTK', 'OverPair', '2PairsW']:
                return 'Call'
            else:
                return 'Raise 3.25x || AllIn'
        if MySituation in ['DoubleHigh']:
            if MyHandPower in ['Air', 'StrDraw', 'FlushDraw', 'PairStrDraw',
                               'PairFlushDraw', 'ThirdPair', 'SecondPair']:
                return 'Fold'
            elif MyHandPower in ['StrongDraw', 'TPWK', 'TPSK', 'TPTK',
                                 'OverPair', '2PairsW', '2PairsS', 'Set']:
                return 'Call'
            else:
                return 'Raise 3.25x || AllIn'


def MoreThenXStackPotRatio(InTG, Stack, Bet, Pot, X):
    for i in range(0, 5):  # хотя бы у 1 игрока StackPotRatio на начало торгов >= X
        if InTG[i] and (Stack[i] + Bet[i]) / (Pot - Bet[i]) >= X:
            return True
    return False


def River(InTG, Stack, Bet, Position_i, Position_s, Board, MyCards, Pot, log_file):
    global ImIP_01, ImAgg_01, LimpPot_01
    # log_file.write(f'---River--- ' + datetime.now().strftime('%Y%m%d_%H%M%S') + '\n')

    # Power of MyHand -------------------------------------------------------------------
    MyCards_Board = []
    MyCards_Board.extend(MyCards)
    try:
        MyCards_Board.extend(Board[0:int(Board.index('-'))])
    except ValueError:
        MyCards_Board.extend(Board[0:10])
    # log_file.write(f'{MyCards_Board}\n')
    MyHandPower = RiverHandPower(MyCards_Board, log_file)
    # log_file.write(f'MyHandPower = {MyHandPower}\n')

    # River Situation -------------------------------------------------------------------
    FlopIsGood = CheckFlopIsGood(Board[0:6], InTG, MyCards)
    MySituation = RiverSituation(MyCards_Board[4:len(MyCards_Board)], FlopIsGood)
    # log_file.write(f'RiverSituation = {MySituation}\n')

    # определим MyMove --------------------------------------------------------------
    # обновим все переменные:
    ImIP_01 = CheckImIP(InTG, Position_i)
    # убедимся, что я все еще агрессор (проверка на DonkBet)
    # ImAgg_01 = True  # здесь д.б. доступно global ImAgg_01 (с Preflop) !!!! ПОТОМ УДАЛИТЬ !!!!
    if ImAgg_01:
        ImAgg_01 = CheckImAgg(Bet, Position_i)
    # log_file.write(f'ImAgg = {ImAgg_01}\n')
    HUPot = True if sum(InTG) == 2 else False
    ImRaised = True if Bet[5] > 0 else False
    # log_file.write(f'ImRaised = {ImRaised}\n')
    if LimpPot_01:
        # log_file.write(f'LimpPot = {LimpPot_01}\n')
        MyMove = RiverMyMove_LimpPot_01(ImAgg_01, ImIP_01, ImRaised, HUPot, FlopIsGood, MyHandPower, MySituation, InTG, Stack, Bet, Pot, MyCards_Board)
    else:
        MyMove = RiverMyMove(ImAgg_01, ImIP_01, ImRaised, HUPot, FlopIsGood, MyHandPower, MySituation, InTG, Stack, Bet, Pot, MyCards_Board)

    # окончательное действие на River ---------------------------------------------------
    # log_file.write(f'MyMove = {MyMove}\n')
    return MyMove


def RiverHandPower(Cards_unsort, log_file):
    # отсортируем карты Флопа, Терна и Ривера
    Cards_sort = []
    Cards_sort.extend(Cards_unsort[0:4])
    # Turn
    for i in range(4, 12, 2):
        if Cards_unsort[10] > Cards_unsort[i]:
            Cards_sort.extend(Cards_unsort[10:12])
            Cards_sort.extend(Cards_unsort[i:10])
            break
        else:
            Cards_sort.extend(Cards_unsort[i:i + 2])
    Cards_sort.extend(Cards_unsort[12:14])
    # River
    Cards_sort2 = []
    Cards_sort2.extend(Cards_sort[0:4])
    for i in range(4, 14, 2):
        if Cards_unsort[12] > Cards_sort[i]:
            Cards_sort2.extend(Cards_unsort[12:14])
            Cards_sort2.extend(Cards_sort[i:12])
            break
        else:
            Cards_sort2.extend(Cards_sort[i:i + 2])
    Cards = Cards_sort2

    # правильный порядок для Rank & Suit ------------------------------------------------
    RankOrder = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    SuitOrder = ['h', 'c', 'd', 's']
    # массивы 15 * 4 и 4 * 15 из 0
    DeckBySuits = [[0] * 15 for i in range(4)]  # (+1: Ace is 1 or 14, +1: index 0 is useless)
    DeckByRank = [[0] * 4 for i in range(15)]  # (+1: Ace is 1 or 14, +1: index 0 is useless)
    for i in range(0, len(Cards), 2):
        r = RankOrder.index(int(Cards[i]))
        s = SuitOrder.index(Cards[i + 1])
        DeckByRank[r][s] = 1
        DeckBySuits[s][r] = 1
        if r == 14:  # '14' can be '1' in Straight
            DeckByRank[1][s] = 1
            DeckBySuits[s][1] = 1

    # классификация Hand_Rank ===========================================================
    # Hand_Rank in [0 - 'Air', 1 - '1Pair', 2 - '2Pairs', 3 - 'Set', 4 - 'Straight',
    #               5 - 'Flush', 6 - 'FullHouse', 7 - 'Four', 8 - 'StraightFlush']

    # 1. найдем совпадения --------------------------------------------------------------
    Hand1 = []
    Ranges = [0, 0, 0, 0, 0]
    for i in range(4, 0, -1):  # кол-во возможных совпадений от каре и ниже
        for j in range(14, 1, -1):
            if sum(DeckByRank[j]) == i:
                Ranges[i] += 1
                for z in range(0, i):
                    Hand1.append(j)
    if Ranges[2] == 3:
        Hand1_5 = Hand1[0:4]
        Hand1_5.append(max(Hand1[5], Hand1[-1]))
    else:
        Hand1_5 = Hand1[0:5]

    # подсчитаем Hand_Rank (изначально Hand_Rank = 0)
    Hand_Rank = 0
    if Ranges[2] == 1:
        Hand_Rank = 1
    if Ranges[2] >= 2:
        Hand_Rank = 2
    if Ranges[3] == 1:
        if Ranges[2] > 0:
            Hand_Rank = 6
        else:
            Hand_Rank = 3
    if Ranges[3] == 2:
        Hand_Rank = 6
    if Ranges[4] > 0:
        Hand_Rank = 7

    # 2. найдем стрит -------------------------------------------------------------------
    Hand2 = []
    for i in range(14, 0, -1):
        if sum(DeckByRank[i]) > 0:
            Hand2.append(i)

    for i in range(0, len(Hand2) - 4):
        if Hand2[i] - Hand2[i + 4] == 4 and Hand_Rank < 4:
            Hand_Rank = 4
            Hand2_5 = Hand2[i:i + 5]

    # 3. найдем флеш --------------------------------------------------------------------
    # сколько карт каждой масти
    Hand3 = []
    for i in DeckBySuits:
        if sum(i[2:]) >= 5 and Hand_Rank < 5:
            Hand_Rank = 5
            for j in range(14, 0, -1):
                if i[j]:
                    Hand3.append(j)
            Hand3_5 = Hand3[0:5]

            # 4. проверим флеш на стрит-флеш --------------------------------------------
            for x in range(0, len(Hand3) - 4):
                if Hand3[x] - Hand3[x + 4] == 4 and Hand_Rank < 8:
                    Hand_Rank = 8
                    Hand4_5 = Hand3[x:x + 5]

    # Hand_Final - выберем сильнейшую комбинацию ----------------------------------------
    if Hand_Rank in [8]:
        Hand_Final = Hand4_5
    elif Hand_Rank in [5]:
        Hand_Final = Hand3_5
    elif Hand_Rank in [4]:
        Hand_Final = Hand2_5
    else:
        Hand_Final = Hand1_5
    # log_file.write(f'Hand_Final = {Hand_Final}\n')

    # классификация Rank_Final (полная) =================================================
    # Rank_Final in ['Air',
    #                'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK', 'OverPair',
    #                '2PairsW', '2PairsS', 'Set', 'Straight', 'FlushW', 'FlushS',
    #                'FullHouse', 'Four', 'StraightFlush']

    # подсчитаем Rank_Final (изначально Rank_Final = 'Air')
    Rank_Final = 'Air'
    if Hand_Rank == 0:
        pass

    if Hand_Rank == 1:  # ---------------------------------------------------------------
        # ситуация 14: у меня 2 разные карты --------------------------------------------
        # ситуация 14A: у меня топ пара с 1й картой
        if Cards[0] == Cards[4]:
            # топ кикер (максимальный)
            for i in range(14, 10, -1):
                if i in [Cards[2]]:
                    Rank_Final = 'TPTK_14A'
                    break
                elif i in Cards[4:12+1]:
                    continue
                else:
                    # слабый кикер (< 10)
                    if Cards[2] < 10:
                        Rank_Final = 'TPWK_14A'
                        break
                    else:
                        # сильный кикер (10-13)
                        Rank_Final = 'TPSK_14A'
                        break
        # ситуация 14B: у меня топ пара со 2й картой
        if Cards[2] == Cards[4]:
            # топ кикер (максимальный)
            for i in range(14, 10, -1):
                if i in [Cards[0]]:
                    Rank_Final = 'TPTK_14B'
                    break
                elif i in Cards[4:12+1]:
                    continue
                else:
                    # слабый кикер (< 10)
                    if Cards[0] < 10:
                        Rank_Final = 'TPWK_14B'
                        break
                    else:
                        # сильный кикер (10-13)
                        Rank_Final = 'TPSK_14B'
                        break

        # ситуация 15: у меня вторая пара
        if Cards[6] in Cards[0:2+1]:
            Rank_Final = 'SecondPair_15'
        # ситуация 16: у меня третья пара и хуже
        if Cards[8] in Cards[0:2+1] or Cards[10] in Cards[0:2+1] or Cards[12] in Cards[0:2+1]:
            Rank_Final = 'ThirdPair_16'

        # ситуация 17: у меня карманная пара
        if Cards[0] == Cards[2]:
            # ситуация 17A: у меня овер пара
            if Cards[4] < Cards[0]:
                Rank_Final = 'OverPair_17A'
            # ситуация 17B: у меня вторая пара
            if Cards[6] < Cards[0] < Cards[4]:
                Rank_Final = 'SecondPair_17B'
            # ситуация 17C: у меня третья пара и хуже
            if Cards[0] < Cards[6]:
                Rank_Final = 'ThirdPair_17C'

    if Hand_Rank == 2:
        # ситуация 21: у меня 2 разные карты
        if Cards[0] != Cards[2]:
            # ситуация 21A: среди наших карт 2 совпадения
            # ситуация 21A: 2PairsW
            if Cards[0] in Cards[6:12+1] and Cards[2] in Cards[6:12+1]:
                Rank_Final = '2PairsW_21A'
                if Cards[4] == Cards[6]:
                    Rank_Final = 'SecondPair&Worse_21A'
            #  ситуация 21B: 2PairsS
            if Cards[0] in [Cards[4]] and Cards[2] in Cards[6:12+1]:
                Rank_Final = '2PairsS_21B'

            #  ситуация 21C: среди наших карт 0 совпадений
            if Cards[0] not in Cards[4:12 + 1] and Cards[2] not in Cards[4:12 + 1]:
                Rank_Final = 'Air_21C'

            #  ситуация 21D: среди наших карт 1 совпадение
            #  1я карта
            if Cards[0] in Cards[4:12+1] and Cards[2] not in Cards[4:12+1]:
                if Cards[0] == Cards[4]:
                    if Cards[2] < 10:
                        Rank_Final = 'TPWK_21D1'
                    else:
                        Rank_Final = 'TPSK_21D1'
                if Cards[0] in Cards[6:12+1]:
                    Rank_Final = 'SecondPair&Worse_21D1'
                if Cards[4] == Cards[6] and Cards[8] == Cards[10]:
                    Rank_Final = 'Air_21D1'
            #  2я карта
            if Cards[0] not in Cards[4:12+1] and Cards[2] in Cards[4:12+1]:
                if Cards[2] == Cards[4]:
                    if Cards[0] < 10:
                        Rank_Final = 'TPWK_21D2'
                    else:
                        Rank_Final = 'TPSK_21D2'
                if Cards[2] in Cards[6:12 + 1]:
                    Rank_Final = 'SecondPair&Worse_21D2'
                if Cards[4] == Cards[6] and Cards[8] == Cards[10]:
                    Rank_Final = 'Air_21D2'

        # ситуация 22: у меня карманная пара
        if Cards[0] == Cards[2]:
            # ситуация 22A: у меня оверпара
            if Cards[4] < Cards[0]:
                Rank_Final = 'OverPair_22A'
            # ситуация 22B: у меня вторая пара
            if Cards[6] < Cards[0] < Cards[4]:
                Rank_Final = 'SecondPair_22B'
            # ситуация 22C: у меня третья пара и хуже
            if Cards[0] < Cards[6]:
                Rank_Final = 'ThirdPair_22C'

    if Hand_Rank == 3:
        # ситуация 31: у меня карманная пара (сет)
        if Cards[0] == Cards[2]:
            Rank_Final = 'Set_31'
        # ситуация 32: у меня 2 разные карты (трипс)
        if Cards[0] != Cards[2]:
            # ситуация 32A: трипс с 1й картой
            value = Cards[4:12].count(Cards[0])
            if value == 2:
                Rank_Final = 'Set_31A'
            # ситуация 32B: трипс со 2й картой
            value = Cards[4:12].count(Cards[2])
            if value == 2:
                Rank_Final = 'Set_31B'

    if Hand_Rank == 4:
        # натсовый стрит или нет
        if Hand2_5[0] == 14:
            Rank_Final = 'StraightS'
        else:
            if Cards[0] in Hand2_5[0:4] or Cards[2] in Hand2_5[0:4]:
                Rank_Final = 'StraightS'
            else:
                Rank_Final = 'StraightW'

    if Hand_Rank == 5:
        # ситуация 51: у меня 2 одномастные карты
        if Cards[1] == Cards[3]:
            if Cards[1] in Cards[4:14]:
                suit = Cards[4:14].count(Cards[1])
                if suit == 3:  # на боарде 3 карты к флешу
                    Rank_Final = 'FlushS_51'
                if suit >= 4:  # на боарде 4 или 5 карт к флешу
                    if Cards[0] in [14]:
                        Rank_Final = 'FlushS_51A14'
                    elif Cards[0] in [13]:
                        Rank_Final = 'FlushS_51A13'
                    else:
                        Rank_Final = 'FlushW_51A'
            else:  # мои карты не участвуют
                Rank_Final = 'Air_51C'
        # ситуация 52: у меня 2 разномастные карты
        if Cards[1] != Cards[3]:
            # ситуация 52A: флеш с 1й картой
            if Cards[1] in Cards[4:14]:
                suit = Cards[4:14].count(Cards[1])
                if suit >= 4:  # на боарде 4 или 5 карт к флешу
                    if Cards[0] in [14]:
                        Rank_Final = 'FlushS_52A14'
                    elif Cards[0] in [13]:
                        Rank_Final = 'FlushS_52A13'
                    else:
                        Rank_Final = 'FlushW_52A'
            # ситуация 52B: флеш со 2й картой
            if Cards[3] in Cards[4:14]:
                suit = Cards[4:14].count(Cards[3])
                if suit >= 4:  # на боарде 4 или 5 карт к флешу
                    if Cards[2] in [14]:
                        Rank_Final = 'FlushS_52B14'
                    elif Cards[2] in [13]:
                        Rank_Final = 'FlushS_52B13'
                    else:
                        Rank_Final = 'FlushW_52B'

    if Hand_Rank == 6:
        Rank_Final = 'FullHouse'
    if Hand_Rank == 7:
        Rank_Final = 'Four'
    if Hand_Rank == 8:
        Rank_Final = 'StraightFlush'

    # пока не поменяли Rank_Final -------------------------------------------------------
    Rank_Final_Details = Rank_Final
    # определим общую силу руки ---------------------------------------------------------
    if 'Air' in Rank_Final:
        Rank_Final = 'Air'
    if 'ThirdPair' in Rank_Final:
        Rank_Final = 'ThirdPair'
    if 'SecondPair' in Rank_Final:
        Rank_Final = 'SecondPair'
    if 'TPWK' in Rank_Final:
        Rank_Final = 'TPWK'
    if 'TPSK' in Rank_Final:
        Rank_Final = 'TPSK'
    if 'TPTK' in Rank_Final:
        Rank_Final = 'TPTK'
    if 'OverPair' in Rank_Final:
        Rank_Final = 'OverPair'
    if '2PairsW' in Rank_Final:
        Rank_Final = '2PairsW'
    if '2PairsS' in Rank_Final:
        Rank_Final = '2PairsS'
    if 'Set' in Rank_Final:
        Rank_Final = 'Set'
    if 'StraightW' in Rank_Final:
        Rank_Final = 'StraightW'
    if 'StraightS' in Rank_Final:
        Rank_Final = 'StraightS'
    if 'FlushW' in Rank_Final:
        Rank_Final = 'FlushW'
    if 'FlushS' in Rank_Final:
        Rank_Final = 'FlushS'
    #   Rank_Final = 'FullHouse'
    #   Rank_Final = 'Four'
    #   Rank_Final = 'StraightFlush'
    # -----------------------------------------------------------------------------------
    return [Rank_Final, Rank_Final_Details]


def RiverSituation(Cards_unsort, FlopIsGood):
    # классификация RiverSituation
    # RiverSituation in ['Neutral', 'AK', 'VillainStronger',
    #                    'DoubleHigh', 'Flush3', 'Str4', 'Flush4']

    # отсортируем карты Флопа, Терна и Ривера -------------------------------------------
    Cards_sort = []
    # Turn
    for i in range(0, 8, 2):
        if Cards_unsort[6] > Cards_unsort[i]:
            Cards_sort.extend(Cards_unsort[6:8])
            Cards_sort.extend(Cards_unsort[i:6])
            break
        else:
            Cards_sort.extend(Cards_unsort[i:i + 2])
    Cards_sort.extend(Cards_unsort[8:10])
    # River
    Cards_sort2 = []
    for i in range(0, 10, 2):
        if Cards_unsort[8] > Cards_sort[i]:
            Cards_sort2.extend(Cards_unsort[8:10])
            Cards_sort2.extend(Cards_sort[i:8])
            break
        else:
            Cards_sort2.extend(Cards_sort[i:i + 2])
    Cards = Cards_sort2

    # подготовим Hand2 на стрит ---------------------------------------------------------
    if Cards[0] == 14:
        Hand = [Cards[0], Cards[2], Cards[4], Cards[6], Cards[8], 1]
    else:
        Hand = [Cards[0], Cards[2], Cards[4], Cards[6], Cards[8]]
    Hand2 = list(set(Hand))
    Hand2.sort(reverse=True)

    Situation = 'Neutral'
    # ситуация: AK ----------------------------------------------------------------------
    if Cards_unsort[8] in [14, 13]:
        Situation = 'AK'

    # ситуация : диапазон оппонента усилился --------------------------------------------
    # ситуация A: спарилась 2я или 3я карта Флопа
    if Cards_unsort[8] in Cards_unsort[2:4 + 1]:
        Situation = 'VillainStronger_A'
    # ситуация B: 3я карта к стриту
    # for i in range(0, len(Hand2) - 2):
    #     if Hand2[i] - Hand2[i + 2] <= 4\
    #             and (Cards_unsort[6] in Hand2[i:i + 3] or Cards_unsort[8] in Hand2[i:i + 3]):
    #         Situation = 'VillainStronger_B'

    # ситуация: спарилась старшая карта -------------------------------------------------
    if Cards_unsort[8] == Cards_unsort[0]:
        Situation = 'DoubleHigh'

    # ситуация: 3 карты к флешу ---------------------------------------------------------
    suit = Cards.count('h')
    if suit == 3:
        Situation = 'Flush3'
    suit = Cards.count('c')
    if suit == 3:
        Situation = 'Flush3'
    suit = Cards.count('d')
    if suit == 3:
        Situation = 'Flush3'
    suit = Cards.count('s')
    if suit == 3:
        Situation = 'Flush3'

    # ситуация: 4 карты к стриту --------------------------------------------------------
    # ситуация A: любой гатшот
    # 'дырявый' гатшот
    for i in range(0, len(Hand2) - 3):
        if Hand2[i] - Hand2[i + 3] == 4:
            Situation = 'Str4_A'
    # гатшот с тузом верх
    if Hand2[0] == 14 and Hand2[3] == 11:
        Situation = 'Str4_A14Up'
    # гатшот с тузом низ
    if Hand2[-1] == 1 and Hand2[-4] == 4:
        Situation = 'Str4_A14Down'
    # ситуация B: открытое стрит-дро
    for i in range(0, len(Hand2) - 3):
        if Hand2[i] - Hand2[i + 3] == 3 and (Hand2[i] != 14 and Hand2[i + 3] != 1):
            Situation = 'Str4_B'

    # ситуация: 4 карты к флешу ---------------------------------------------------------
    suit = Cards.count('h')
    if suit == 4:
        Situation = 'Flush4'
    suit = Cards.count('c')
    if suit == 4:
        Situation = 'Flush4'
    suit = Cards.count('d')
    if suit == 4:
        Situation = 'Flush4'
    suit = Cards.count('s')
    if suit == 4:
        Situation = 'Flush4'

    # пока не поменяли Situation --------------------------------------------------------
    Situation_Details = Situation
    # определим общую Situation ---------------------------------------------------------
    #   Situation = 'Neutral'
    #   Situation = 'AK'
    if 'VillainStronger' in Situation:
        Situation = 'VillainStronger'
    #   Situation = 'DoubleHigh'
    #   Situation = 'Flush3'
    if 'Str4' in Situation:
        Situation = 'Str4'
    #   Situation = 'Flush4'

    return Situation


def RiverMyMove(ImAgg_01, ImIP_01, ImRaised, HUPot, FlopIsGood, MyHandPowerAll, MySituation, InTG, Stack, Bet, Pot, Cards):
    MyHandPower = MyHandPowerAll[0]
    MyHandPowerDetails = MyHandPowerAll[1]
    # MyHandPower in ['Air',
    #                 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK', 'OverPair',
    #                 '2PairsW', '2PairsS', 'Set', 'StraightW', 'StraightS', 'FlushW', 'FlushS',
    #                 'FullHouse', 'Four', 'StraightFlush']

    # MySituation in ['Neutral', 'AK', 'VillainStronger',
    #                  'DoubleHigh', 'Flush3', 'Str4', 'Flush4']

    if not ImRaised:
        if ImAgg_01:  # с инициативой ------------------------------------------------------
            if ImIP_01:
                if MySituation in ['Flush3']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK']:
                        return 'Check'
                    elif MyHandPower in ['OverPair', '2PairsW', '2PairsS', 'Set']:
                        return 'Bet 1/2 Pot'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['Flush4']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW', '2PairsS', 'Set',
                                       'StraightW', 'StraightS', 'FlushW']:
                        return 'Check'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['Str4']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW', '2PairsS', 'Set', 'StraightW']:
                        return 'Check'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['DoubleHigh']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW']:
                        return 'Check'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['AK']:
                    if MyHandPower in ['ThirdPair', 'SecondPair']:
                        return 'Check'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['Neutral']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair']:
                        return 'Check'
                    elif MyHandPower in ['TPWK']:
                        return 'Bet 1/2 Pot'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['VillainStronger']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK']:
                        return 'Check'
                    else:
                        return 'Bet 2/3 Pot'
            else:
                if MySituation in ['Flush3']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK']:
                        return 'Check || Fold'
                    elif MyHandPower in ['OverPair', '2PairsW', '2PairsS', 'Set']:
                        return 'Bet 1/2 Pot'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['Flush4']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW', '2PairsS', 'Set',
                                       'StraightW', 'StraightS', 'FlushW']:
                        return 'Check || Fold'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['Str4']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW', '2PairsS', 'Set', 'StraightW']:
                        return 'Check || Fold'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['DoubleHigh']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW']:
                        return 'Check || Fold'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['AK']:
                    if MyHandPower in ['ThirdPair', 'SecondPair']:
                        return 'Check || Fold'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['Neutral']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair']:
                        return 'Check || Fold'
                    elif MyHandPower in ['TPWK']:
                        return 'Bet 1/2 Pot'
                    else:
                        return 'Bet 2/3 Pot'
                if MySituation in ['VillainStronger']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK']:
                        return 'Check || Fold'
                    else:
                        return 'Bet 2/3 Pot'
        else:  # без инициативы ---------------------------------------------------------
            if ImIP_01:
                if MySituation in ['Flush3']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW', '2PairsS', 'Set']:
                        return 'Check || Fold'
                    elif MyHandPower in ['StraightW', 'StraightS']:
                        return 'Bet 1/2 Pot || Call'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                if MySituation in ['Flush4']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK']:
                        return 'Bet 2/3 Pot || Fold'
                    elif MyHandPower in ['TPTK', 'OverPair', '2PairsW', '2PairsS', 'Set',
                                         'StraightW', 'StraightS', 'FlushW']:
                        return 'Check || Fold'
                    elif MyHandPower in ['FlushS']:
                        if '14' in MyHandPowerDetails:
                            return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                        if '13' in MyHandPowerDetails:
                            return 'Bet 2/3 Pot || Call'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                if MySituation in ['Str4']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK']:
                        return 'Bet 2/3 Pot || Fold'
                    elif MyHandPower in ['TPTK', 'OverPair', '2PairsW', '2PairsS', 'Set', 'StraightW']:
                        return 'Check || Fold'
                    elif MyHandPower in ['StraightW']:
                        return 'Check || Raise 3.25x (AllIn)'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                if MySituation in ['DoubleHigh']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW']:
                        return 'Check || Fold'
                    elif MyHandPower in ['2PairsS', 'Set']:
                        return 'Bet 2/3 Pot || Call'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                if MySituation in ['AK']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair']:
                        return 'Check || Fold'
                    elif MyHandPower in ['TPWK']:
                        return 'Bet 2/3 Pot || Fold'
                    elif MyHandPower in ['TPSK', 'TPTK', 'OverPair', '2PairsW']:
                        return 'Bet 2/3 Pot || Call'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                if MySituation in ['Neutral']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check || Fold'
                    elif MyHandPower in ['TPSK']:
                        return 'Bet 2/3 Pot || Fold'
                    elif MyHandPower in ['TPTK', 'OverPair', '2PairsW']:
                        return 'Bet 2/3 Pot || Call'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
                if MySituation in ['VillainStronger']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW']:
                        return 'Check || Fold'
                    else:
                        return 'Bet 2/3 Pot || Raise 3.25x (AllIn)'
            else:
                if MySituation in ['Flush3']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW', '2PairsS', 'Set']:
                        return 'Check, Fold'
                    elif MyHandPower in ['StraightW', 'StraightS']:
                        return 'Check, Call'
                    else:
                        return 'Check, Raise 3.25x (AllIn)'
                if MySituation in ['Flush4']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW', '2PairsS', 'Set',
                                       'StraightW', 'StraightS', 'FlushW']:
                        return 'Check, Fold'
                    elif MyHandPower in ['FlushS']:
                        if '14' in MyHandPowerDetails:
                            return 'Check, Raise 3.25x (AllIn)'
                        if '13' in MyHandPowerDetails:
                            return 'Check, Call'
                    else:
                        return 'Check, Raise 3.25x (AllIn)'
                if MySituation in ['Str4']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW', '2PairsS', 'Set', 'StraightW']:
                        return 'Check, Fold'
                    else:
                        return 'Check, Raise 3.25x (AllIn)'
                if MySituation in ['DoubleHigh']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW']:
                        return 'Check, Fold'
                    elif MyHandPower in ['2PairsS', 'Set']:
                        return 'Check, Call'
                    else:
                        return 'Check, Raise 3.25x (AllIn)'
                if MySituation in ['AK']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK']:
                        return 'Check, Fold'
                    elif MyHandPower in ['TPSK', 'TPTK', 'OverPair', '2PairsW']:
                        return 'Check, Call'
                    else:
                        return 'Check, Raise 3.25x (AllIn)'
                if MySituation in ['Neutral']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK']:
                        return 'Check, Fold'
                    elif MyHandPower in ['TPTK', 'OverPair', '2PairsW']:
                        return 'Check, Call'
                    else:
                        return 'Check, Raise 3.25x (AllIn)'
                if MySituation in ['VillainStronger']:
                    if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK',
                                       'OverPair', '2PairsW']:
                        return 'Check, Fold'
                    else:
                        return 'Check, Raise 3.25x (AllIn)'
    else:
        if MySituation in ['Flush4']:
            if MyHandPower in ['FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'AllIn'
            else:
                return 'Fold'
        elif MySituation in ['Str4']:
            if MyHandPower in ['StraightS', 'FlushW', 'FlushS',
                               'FullHouse', 'Four', 'StraightFlush']:
                return 'AllIn'
            else:
                return 'Fold'
        elif MySituation in ['Flush3']:
            if MyHandPower in ['FlushW', 'FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'AllIn'
            else:
                return 'Fold'
        elif MyHandPower in ['2PairsS', 'Set', 'StraightW', 'StraightS', 'FlushW', 'FlushS',
                             'FullHouse', 'Four', 'StraightFlush']:
            return 'AllIn'
        else:
            return 'Fold'


def RiverMyMove_LimpPot_01(ImAgg_01, ImIP_01, ImRaised, HUPot, FlopIsGood, MyHandPowerAll, MySituation0, InTG, Stack, Bet, Pot, Cards):
    MyHandPower = MyHandPowerAll[0]
    MyHandPowerDetails = MyHandPowerAll[1]
    # MyHandPower in ['Air',
    #                 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK', 'OverPair',
    #                 '2PairsW', '2PairsS', 'Set', 'StraightW', 'StraightS', 'FlushW', 'FlushS',
    #                 'FullHouse', 'Four', 'StraightFlush']

    # MySituation in ['Neutral', 'DoubleHigh', 'Flush3', 'Str4', 'Flush4']
    if MySituation0 in ['AK', 'VillainStronger']:  # отсутствуют в LimpPot_01
        MySituation = 'Neutral'
    else:
        MySituation = MySituation0

    if max(Bet) == 0:
        if MySituation in ['Flush3']:
            if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK', 'TPSK', 'TPTK']:
                return 'Check || Fold'
            elif MyHandPower in ['OverPair', '2PairsW', '2PairsS', 'Set', 'StraightW', 'StraightS']:
                return 'Bet 2/3 Pot || Fold'
            else:
                return 'Bet 2/3 Pot || AllIn'
        if MySituation in ['Flush4']:
            if MyHandPower in ['FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'Bet 2/3 Pot || AllIn'
            else:
                return 'Check || Fold'
        if MySituation in ['Str4']:
            if MyHandPower in ['StraightS', 'FlushW', 'FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'Bet 2/3 Pot || AllIn'
            else:
                return 'Check || Fold'
        if MySituation in ['DoubleHigh']:
            if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK',
                               'TPSK', 'TPTK', 'OverPair', '2PairsW']:
                return 'Check || Fold'
            elif MyHandPower in ['2PairsS', 'Set']:
                return 'Bet 2/3 Pot || Fold'
            else:
                return 'Bet 2/3 Pot || AllIn'
        if MySituation in ['Neutral']:
            if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK']:
                return 'Check || Fold'
            elif MyHandPower in ['TPSK', 'TPTK', 'OverPair', '2PairsW']:
                return 'Bet 2/3 Pot || Fold'
            else:
                return 'Bet 2/3 Pot || AllIn'
    else:
        if MySituation in ['Flush3']:
            if MyHandPower in ['FlushW', 'FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'Raise 3.25x || AllIn'
            else:
                return 'Fold'
        if MySituation in ['Flush4']:
            if MyHandPower in ['FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'Raise 3.25x || AllIn'
            else:
                return 'Fold'
        if MySituation in ['Str4']:
            if MyHandPower in ['StraightS', 'FlushW', 'FlushS', 'FullHouse', 'Four', 'StraightFlush']:
                return 'Raise 3.25x || AllIn'
            else:
                return 'Fold'
        if MySituation in ['DoubleHigh']:
            if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK',
                               'TPSK', 'TPTK', 'OverPair', '2PairsW']:
                return 'Fold'
            elif MyHandPower in ['2PairsS', 'Set']:
                return 'Call'
            else:
                return 'Raise 3.25x || AllIn'
        if MySituation in ['Neutral']:
            if MyHandPower in ['Air', 'ThirdPair', 'SecondPair', 'TPWK']:
                return 'Fold'
            elif MyHandPower in ['TPSK', 'TPTK', 'OverPair', '2PairsW']:
                return 'Call'
            else:
                return 'Raise 3.25x || AllIn'
