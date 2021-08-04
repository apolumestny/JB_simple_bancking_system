# Write your code here
import curses.ascii
import random
import sqlite3


class CreditCart():
    def __init__(self):
        self.create_db()
        bank_menu = True
        # db = {}
        while bank_menu:
            user_choice = int(input('1. Create an account\n2. Log into account\n0. Exit\n'))
            if user_choice == 0:
                bank_menu = False
            if user_choice == 1:
                card = self.generate_card()
                pin = self.generate_pin()
                print(f'Your card number:\n{card}')
                print(f'Your card PIN:\n{pin}')
                # if card in db:
                #    card = self.generate_card()
                # db[card] = pin
                self.insert_card_info(card_num=card, card_pin=pin)
                chek_sum = self.generate_checksum(iin=card[0:6], can=card[6:15])
                #print(card[0:6],card[6:15], chek_sum)
            if user_choice == 2:
                card = input('Enter your card number:\n')
                pin = input('Enter your PIN:\n')
                if self.check_if_card_exist(card_num=card) == 0:
                    print('Wrong card number or PIN!')
                    continue
                if self.get_card_pin(card_num=card) != pin:
                    print('Wrong card number or PIN!')
                    # print('pin')
                    continue
                print('You have successfully logged in!')
                acc_menu = True
                while acc_menu:
                    user_choice = int((input('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n')))
                    if user_choice == 1:
                        balance = self.get_balance(card_num=card)
                        print(f'Balance: {balance}')
                    if user_choice == 2:
                        income = int(input('Enter income:\n'))
                        self.add_income(card=card, amount=income)
                    if user_choice == 3:
                        to_card = input('Enter card number:\n')
                        if self.generate_checksum(iin=to_card[0:6], can=to_card[6:15]) != int(to_card[len(to_card)-1:len(to_card)]):
                            print('Probably you made a mistake in the card number. Please try again!')
                            continue
                        if card == to_card:
                            print("You can't transfer money to the same account!")
                            continue
                        if self.check_if_card_exist(to_card) == 0:
                            print('Such a card does not exist.')
                            continue
                        amount = int(input('Enter how much money you want to transfer:\n'))
                        self.do_transfer(from_card=card, to_card=to_card, amount=amount)
                    if user_choice == 4:
                        self.close_account(card_num=card)
                    if user_choice == 5:
                        acc_menu = False
                    if user_choice == 0:
                        acc_menu = False
                        bank_menu = False

    def generate_card(self):
        iin = '400000'
        can = format(random.randint(000000000, 999999999), '09d')
        checksum = self.generate_checksum(iin, can)
        return f'{iin}{can}{checksum}'

    def generate_checksum(self, iin, can):
        num = f'{iin}{can}'
        #print('num',num)
        digit = []
        #print('digit',digit)
        for id, dig in enumerate(num):
            if (id + 1) % 2 != 0:
                n = int(dig) * 2
                if n > 9:
                    n = n - 9
                digit.append(n)
            else:
                digit.append(int(dig))
        fin_sum = sum(digit)
        # print(fin_sum)
        if fin_sum % 10 == 0:
            checksum = 0
            #print('1', checksum)
            return checksum
        else:
            checksum = 10 - int(str(fin_sum)[-1])
            #print('2', checksum)
            return checksum

    def generate_pin(self):
        pin = format(random.randint(0000, 9999), '04d')
        return pin

    def create_db(self):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        if self.check_if_table_exist('card') == 0:
            create_statement = 'CREATE table card' \
                           '(id INTEGER,' \
                           'number TEXT,' \
                           'pin TEXT,' \
                           'balance INTEGER DEFAULT 0)'
            cur.execute(create_statement)
            conn.commit()
    def insert_card_info(self, card_num, card_pin):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        insert_statement = f'INSERT into card(number, pin) VALUES ({card_num}, {card_pin})'
        cur.execute(insert_statement)
        conn.commit()

    def check_if_card_exist(self, card_num):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        query = f'SELECT count(1) from card WHERE number = {card_num}'
        cur.execute(query)
        return cur.fetchone()[0]

    def get_card_pin(self, card_num):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        query = f'SELECT pin from card WHERE number = {card_num}'
        cur.execute(query)
        return cur.fetchone()[0]


    def check_if_table_exist(self, table_name):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        cur.execute(query)
        try:
            if cur.fetchone()[0] == 1:
                return 1
        except TypeError:
            return 0

    def get_balance(self, card_num):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        query = f"SELECT balance FROM card WHERE number = {card_num}"
        cur.execute(query)
        balance = cur.fetchone()[0]
        return balance

    def add_income(self, card, amount):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        query = f"UPDATE card set balance = balance + {amount} where number = {card}"
        cur.execute(query)
        conn.commit()

    def rise_balance(self, card, amount):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        query = f"UPDATE card set balance = balance - {amount} where number = {card}"
        cur.execute(query)
        conn.commit()

    def close_account(self, card_num):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        query = f"DELETE FROM card WHERE number = {card_num}"
        cur.execute(query)
        conn.commit()

    def do_transfer(self, from_card, to_card, amount):
        current_balance = self.get_balance(card_num=from_card)
        if current_balance < amount:
            print('Not enough money!')
            return
        self.rise_balance(card=from_card, amount=amount)
        self.add_income(card=to_card, amount=amount)
        print('Success!')


if __name__ == '__main__':
    bank = CreditCart()
    to_card = '4000001639660216'
    c = bank.generate_checksum(can='400000', iin='163966033')
    print('sum',c)
