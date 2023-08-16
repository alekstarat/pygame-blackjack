import pygame as pg
import os
from random import shuffle


pg.init()                                                   # Инициализация
pg.font.init()
font = pg.font.SysFont('Comic Sans MS', 30)
screen = pg.display.set_mode((1280, 800))
pg.display.set_caption('Blackjack')
background = (100, 150, 255)


def take_one(deck : object, player1 : object):              # Функция добавления карты из колоды в руки игрока/дилера
    player1.add_card(Card(deck.take_card()))



class Card:                                                 # Класс для определения цены и масти конкретной карты          

    '''Для объектов типа Card.
       name - str значение карты,
       val - цена карты,
       img_object - привязка экземпляра класса к конкретному изображению'''

    def __init__(self, name : str):
        self.name = name
        self.val = name[:-1]
        self.img_object = pg.image.load(f'src/{name}.png')                     
        if any([self.val == i for i in ['J', 'Q', 'K']]): self.val = 10
        elif self.val == 'A': self.val = 1
        else: self.val = int(self.val)


class Deck:

    '''Для инициализации всей колоды.
       all_cards - str значения всей колоды карт'''

    def __init__(self):
        self.all_cards = [i.replace('.png', '') for i in os.listdir('src')]
        shuffle(self.all_cards)

    def take_card(self):                        # Метод для удаления карты из конца колоды и перемещения её в руки игрока

        res = self.all_cards[-1]
        self.all_cards.pop(-1)
        return res


class Hand:

    '''Класс для создания руки конкретного игрока.
       hand_cards - массив с экземплярами класса Card'''

    def __init__(self):
        self.hand_cards = []

    def add_card(self, card : object):                  # Метод для добавления объекта Card в hand_cards
        self.hand_cards.append(card)

    def get_sum(self):                                  # Метод для посчёта суммы всех карт в руке игрока (без и с учётом тузов)
        if not(any(['A' in i.name for i in self.hand_cards])):
            return [sum([i.val for i in self.hand_cards])]
        else:
            return [sum([i.val for i in self.hand_cards]), sum([i.val for i in self.hand_cards]) + 9]
    
    def print_cards(self):                              # Метод для отображения руки игрока в консоли
        print('Рука игрока: ', [[i.name, i.val] for i in self.hand_cards], *self.get_sum())


class Dealer(Hand):
    
    '''Класс отвечающий за карты дилера (parent=Hand)'''

    def __init__(self):
        self.hand_cards = []

    def get_sum_while_game(self):                       # Метод скрывающий от игрока реальную сумму карт дилера во время игры       
        if not(any(['A' in i.name for i in self.hand_cards[1:]])):
            return [sum([i.val for i in self.hand_cards[1:]])]
        else:
            return [sum([i.val for i in self.hand_cards[1:]]), sum([i.val for i in self.hand_cards[1:]]) + 9]

    def print_cards(self):
        print('Рука дилера: ', [[i.name, i.val] for i in self.hand_cards], *self.get_sum())

state = None

class Game:

    '''Класс для создания экземпляров всех участвующих в игре классов
       и определения методов для правильного хода игры.'''

    def __init__(self):
        self.deck = Deck()
        self.player1 = Hand()
        self.dealer = Dealer()
        self.perebor = False
        self.isStarted = 0
        self.isEnded = 0
        
    def start(self):                                            # В самом начале игры выдать игроку и дилеру по 2 карты
        for i in range(2):
            self.player1.add_card(Card(self.deck.take_card()))
        for i in range(2):
            self.dealer.add_card(Card(self.deck.take_card()))

        self.isStarted += 1                                     # Флаг, говорящий о начале игры

    def more(self):                                             # Добавить игроку и дилеру по 1 карте
        
        take_one(self.deck, self.player1)
        take_one(self.deck, self.dealer)

    def end_game(self):                                         # Метод для запуска конца игры
        self.isEnded +=1                                        # Флаг, говорящий о конце игры
        if len(self.dealer.get_sum()) == 1:
            dealer_count = font.render(f'Счёт дилера: {str(self.dealer.get_sum())}', False, (255, 255, 255))
        else:
            dealer_count = font.render(f'Счёт дилера: {str(self.dealer.get_sum()[0])} ({str(self.dealer.get_sum()[1])})', False, (255, 255, 255))
        print(f'Счёт дилера: {self.dealer.get_sum()}')
        print(f'Ваш счёт: {self.player1.get_sum()}')
        if self.player1.get_sum()[0] > 21:
            if self.dealer.get_sum()[0] > self.player1.get_sum()[0]:
                print('Победа игрока 1')
            elif self.dealer.get_sum()[0] == self.player1.get_sum()[0]:
                print('Ничья')
            else:
                print('Победа дилера')
        if self.player1.get_sum()[0] == 21:                                 # Финальный подсчёт очков игрока и дилера
            if self.dealer.get_sum()[0] == 21:
                print('Ничья')
            if self.dealer.get_sum()[0] < 21 or self.dealer.get_sum()[0] > 21:
                print('Победа игрока 1')
        if self.player1.get_sum()[0] < 21:
            if self.dealer.get_sum()[0] < 21:
                if self.player1.get_sum()[0] < self.dealer.get_sum()[0]: print('Победа дилера')
                if self.player1.get_sum()[0] > self.dealer.get_sum()[0]: print('Победа игрока 1')
            if self.dealer.get_sum()[0] > 21: print('Победа игрока 1')

        
rect1 = pg.Rect(0, 500, 200, 300)
rect2 = pg.Rect(10, 510, 180, 280)
lots_dealer = [pg.Rect(i, 0, 200, 300) for i in [250, 450, 650, 850, 1050]]
inner_lots_dealer = [pg.Rect(i, 10, 180, 280) for i in [260, 460, 660, 860, 1060]]
lots = [pg.Rect(i, 500, 200, 300) for i in [250, 450, 650, 850, 1050]]
inner_lots = [pg.Rect(i, 510, 180, 280) for i in [260, 460, 660, 860, 1060]]
back = pg.image.load('back.png')
mor = font.render('Взять ещё?', False, (255, 255, 255))
yes = font.render('Да', False, (255, 255, 255))
yesRect = pg.Rect(50, 580, 100, 50)
no = font.render('Нет', False, (255, 255, 255))
noRect =  pg.Rect(50, 650, 100, 50)

clock = pg.time.Clock()

game = Game()


while True:
    clock.tick(60)
    screen.fill(background)
    for lot in lots_dealer:
        pg.draw.rect(screen, (255, 255, 255), lot, 0)
    for inner_lot in inner_lots_dealer:
        pg.draw.rect(screen, (100, 150, 255), inner_lot, 0)
    for lot in lots:
        pg.draw.rect(screen, (255, 255, 255), lot, 0)
    for inner_lot in inner_lots:
        pg.draw.rect(screen, (100, 150, 255), inner_lot, 0)
    pg.draw.rect(screen, (255, 255, 255), rect1, 0)
    pg.draw.rect(screen, (100, 150, 255), rect2, 0)
    
    if len(game.player1.get_sum()) == 1:
        count = font.render(f'Ваш счёт: {str(game.player1.get_sum())}', False, (255, 255, 255))
    else:
        count = font.render(f'Ваш счёт: {str(game.player1.get_sum()[0])} ({str(game.player1.get_sum()[1])})', False, (255, 255, 255))
    if len(game.dealer.get_sum_while_game()) == 1:
        dealer_count = font.render(f'Счёт дилера: >{str(game.dealer.get_sum_while_game())}', False, (255, 255, 255))
    else:
        dealer_count = font.render(f'Счёт дилера: >{str(game.dealer.get_sum_while_game()[0])} ({str(game.dealer.get_sum_while_game()[1])})', False, (255, 255, 255))
    screen.blit(count, (10, 10))
    screen.blit(dealer_count, (0, 400))
    screen.blit(mor, (15, 510))
    yesRect = pg.draw.rect(screen, (200, 200, 200), yesRect, 0)
    screen.blit(yes, (80, 580))
    noRect = pg.draw.rect(screen, (200, 200, 200), noRect, 0)
    screen.blit(no,  (75, 650))
    if game.isStarted == 0:
        game.start()
    screen.blit(pg.transform.scale(back, (290, 350)), inner_lots_dealer[-1])
    for rect, card in enumerate(game.dealer.hand_cards[1:]):
        screen.blit(pg.transform.scale(card.img_object, (190, 290)), inner_lots_dealer[rect])
    for rect, card in enumerate(game.player1.hand_cards):
        screen.blit(pg.transform.scale(card.img_object, (190, 290)), inner_lots[rect])
    
    for event in pg.event.get():
        
        if event.type == pg.MOUSEBUTTONDOWN:
            mousePos = pg.mouse.get_pos()
            if yesRect.collidepoint(mousePos):
                game.more()
            if noRect.collidepoint(mousePos):
                if game.isEnded == 0:
                    back = pg.transform.scale(pg.image.load('src/'+str(game.dealer.hand_cards[0].name)+'.png'), (150, 190))
                    
                    game.end_game()
        pg.display.update()
        if event.type == pg.QUIT:
            pg.quit()
            quit()