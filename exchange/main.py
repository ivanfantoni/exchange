import pyfiglet
from rich.console import Console
from rich.table import Table
import os
import sys
import time

from .exchange import Exchange

class Main:
    def __init__(self):
        self.cs = Console()

    def start(self):
        self.title()
        try:
            self.count = 0
            self.from_currency = self.cs.input('[bold cyan1]From: [/bold cyan1]')
            if self.from_currency == '':
                self.from_currency = 'eur'
            self.to_currency = self.cs.input('[bold cyan1]To: [/bold cyan1]')
            self.amount = self.cs.input('[bold cyan1]Amount: [/bold cyan1]')
            while True:
                if self.to_currency == 'world':
                    self.rate()
                    break
                else:
                    self.amount_handling()
                    self.results()
                    self.count +=1
                self.cs.print('\n[magenta]Type "r" to reverse the currencies[/magenta]\n')
                self.amount = self.cs.input('[bold green1]New amount: [/bold green1]')
        except KeyboardInterrupt:
            self.title()
            sys.exit()
        except KeyError as key:
            self.cs.print(f'[bold red1]\n{key} Is not available!\nCheck the list of available currencies.[/bold red1]\n')
            time.sleep(3)
            self.from_currency = 'EUR'
            self.rate()


    def title(self):
            os.system('clear')
            title = pyfiglet.figlet_format('EXCHANGE', font='big')
            self.cs.print(f'[bold gold1]{title}[/bold gold1]')
            self.cs.print('#'*56, style='magenta1')
            self.cs.print(f'[magenta1]#     [bold]Version 1.0.0 - Powered by exchangerate.host[/bold]     #[/magenta1]')
            self.cs.print('#'*56, style='magenta1')
            print()

                         
    def results(self):
        if self.count == 0:
            self.result = Exchange(self.from_currency, self.to_currency, 1).convert()
            self.codes = Exchange.symbols()
            self.cs.clear()
            self.title()
        else:
            self.cs.clear()
            self.title()
        self.tab = Table(show_header=False, header_style='bold green1', width=56,
                         title='***' + ' '*12 + f'CONVERSION FROM [red1]{self.from_currency.upper()}[/red1] TO [red1]{self.to_currency.upper()}[/red1]' + ' '*12 + '***', 
                         title_style='bold green1',
                         title_justify='left')
        self.tab.add_column(f'', style='bold cyan1', justify='left')
        self.tab.add_column( '-', style='bold cyan1', justify='center')
        self.tab.add_column('$$$', style='bold cyan1', justify='left')
   
        self.tab.add_row(self.codes[self.from_currency.upper()]['description'], self.from_currency.upper(), str(self.amount))
        self.tab.add_row(self.codes[self.to_currency.upper()]['description'], self.to_currency.upper(), str(round(self.result['result'] *self.amount, 3)))
        print()
        self.cs.print(self.tab)


    def rate(self):
        result = Exchange(self.from_currency, 1).latest_rate()
        codes = Exchange.symbols()
        tab = Table(show_header=True, header_style='bold green1', title_justify='center')
        tab.add_column(f'***       RATING FROM {self.from_currency.upper()}       ***', style='bold cyan1', justify='left')
        tab.add_column('TO', style='bold cyan1', justify='center')
        tab.add_column('***', style='bold cyan1', justify='left')
        for rate in result['rates']:
            description = codes[rate]['description']
            tab.add_row(description, rate, str(round(result['rates'][rate], 2)))
        print()
        self.cs.print(tab)


    def amount_handling(self):
        handling = self.amount
        handling = handling.replace(',', '')
        handling = handling.replace('.', '')
        if self.amount == '':
            self.amount = '1'
        elif self.amount == 'r':
            self.amount = '1'
            self.reverse_currencies()
        elif not handling.isnumeric():
            self.cs.print(f'[bold red1]\n"{self.amount}" Is not a number![/bold red1]\n')
            self.amount = self.cs.input('[bold cyan1]Amount: [/bold cyan1]')
        self.int_or_float() 


    def int_or_float(self):
        try:
            if '.' in self.amount:
                self.amount = float(self.amount)
            else:
                self.amount = int(self.amount)
        except ValueError as e:
            try:
                handling = str(self.amount.replace(',', '.'))
                self.amount = float(handling)
            except ValueError:
                self.amount_handling()

    def reverse_currencies(self):
        self.result['result'] = float(self.amount)/float(self.result['result'])
        n_from = self.to_currency
        n_to = self.from_currency
        self.to_currency = n_to
        self.from_currency = n_from

        


if __name__ == '__main__':
    Main().start()


