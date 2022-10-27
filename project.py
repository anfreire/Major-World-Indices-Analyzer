from time import sleep
import pandas as pd
import yfinance as yf
from termcolor import colored
import playsound
from datetime import date
import plotext as plt
import warnings

def main():
	warnings.simplefilter(action='ignore', category=FutureWarning)
	init_message()
	main_menu()

#MESSAGES
def print_menu():
	menu_options = {
    1: "Analyze an Index Fund",
    2: "Save the Major 36 Index Funds data as an .xlsl file (Excel Default Format)",
    3: "Exit",
	}
	print()
	for key in menu_options.keys():
		print('\033[1m' + colored(f"{key} -- {menu_options[key]}", "blue") + '\033[0m')
	print()

def print_indexs():
	data = pd.read_html('https://finance.yahoo.com/world-indices/')[0]
	data = data[['Name']]
	print('\033[1m' + "\nSelect the requested index fund.\n" + '\033[0m')
	i = 1
	for name in data['Name']:
		print('\033[1m' + colored(f"{i} -- {name}", "blue") + '\033[0m')
		i = i + 1
	print()

def print_period():
	options = {
    0: "Expected: Number(int) Period(str)",
    1: "ex: 15 days",
    2: "ex: 3 months",
    3: "ex: 1 year",
    4: "ex: 6 years",
	}
	print('\033[1m' + colored("Choose the Period\n") + '\033[0m')
	for option in options.keys():
		print('\033[1m' + colored(options[option], "blue") + '\033[0m')
	print()

def init_message():
	play_sound('./files/init.mp3')
	string = "Major World Indices Analyzer"
	string = '\033[1m' + string + '\033[0m'
	print(colored('\n' + string, 'blue'))


def return_menu_message():
	sleep(1.2)
	play_sound('./files/return_menu.mp3')
	print(colored(f"\nReturning to the Main Menu\n", 'green'))
	sleep(1.2)


def print_stocks(df, name):
	dtypes = ['Open',
			'High',
			'Low',
			'Close',
			'Volume',]
	for type in dtypes:
		plt.scatter(df['Date'], df[type])
		plt.title(f"{name} {type} Data")
		print()
		plt.show()
		plt.clear_data()

def prompt_download_data(name):
	menu_options = {
    1: f"Save the {name} data as an .xlsl file (Excel Default Format)",
    2: "Go Back to the Main Menu",
    3: "Exit",
	}
	print()
	for key in menu_options.keys():
		print('\033[1m' + colored(f"{key} -- {menu_options[key]}", "blue") + '\033[0m')
	print()


#FUNCTIONS
def validate_option(option, range):
	if option not in range:
		raise ValueError
	else:
		return option

def validate_period(answer):
	number, option = answer.lower().split(" ", maxsplit=1)
	number = int(number)
	if option == "day" or option == "days":
		period = str(number) + "d"
	elif option == "month" or option == "months":
		period = str(number) + "mo"
	elif option == "year" or option == "years":
		period = str(number) + "y"
	else:
		raise ValueError
	return period

def save_xlsl_data(df, name):
	name = name.replace(' ', '_')
	if len(name) > 31:
		raise ValueError
	writer = pd.ExcelWriter(f'{name}.xlsx', engine='xlsxwriter')
	df.to_excel(writer, sheet_name=name, index=False)
	writer.save()
	print("\n" + colored(f"\n{name}.xlsx Saved!\n", 'green'))
	playsound.playsound('./files/file_saved.mp3')

def save_xlsl_36indexs(name):
	data = pd.read_html('https://finance.yahoo.com/world-indices/')[0]
	data = data[['Symbol', 'Name', 'Last Price', 'Change', '% Change']]
	df = pd.DataFrame(data)
	today = date.today()
	today = today.strftime("%d_%m_%Y")
	name = name + today
	if len(name) > 31:
		name = name[0:31]
	save_xlsl_data(df, name)
	return_menu_message()
	init_message()

def get_stock(df, name):
	try:
		df['Date'] = df.index.to_pydatetime()
		df['Date'] = df.index.strftime("%d/%m/%Y")
		df = df[['Date','Open','High','Low','Close','Volume']]
		print_stocks(df, name)
		stock_menu(df, name)
	except AttributeError:
		print(colored("\nUnable to get data from this stock.\nSorry for the inconvience\n", "red"))

def exiting_program():
	print(colored("\nExiting...\n", 'green'))
	play_sound('./files/exit.mp3')
	exit()

def play_sound(path):
	try:
		playsound.playsound(path)
	except:
		raise ValueError









#MENUS
def main_menu():
	while(True):
		print_menu()
		option = ''
		try:
			option = int(input('Enter your choice: '))
			option = validate_option(option, range(1, 4))
		except:
			print(colored('Invalid option. Please enter a number between 1 and 3.', 'red'))
		if option == 1:
			analyzer_menu()
		elif option == 2:
			save_xlsl_36indexs("Major_36_Index_Funds_")
		elif option == 3:
			exiting_program()

def analyzer_menu():
	print_indexs()
	while True:
		option = ''
		try:
			option = int(input("Enter your choice: "))
			option = validate_option(option, range(1, 37))
		except:
			print_indexs()
			print(colored("\nPlease enter a number listed above, between 1 and 36\n", 'red'))
		else:
			stock_analyzer(option - 1)
			return_menu_message()
			init_message()
			break

def stock_analyzer(option):
	data = pd.read_html('https://finance.yahoo.com/world-indices/')[0]
	data = data[['Symbol', 'Name']]
	name = data['Name'][option]
	print(colored(f"\n{name} Index Fund Selected!\n", 'green'))
	index = yf.Ticker(data['Symbol'][option])
	while True:
		print_period()
		period = ''
		answer = ''
		try:
			answer = input('Enter your choice: ')
			period = validate_period(answer)
		except:
			print(colored('\nOption is not valid. Please enter a number followed by a period (separated by a space).\n', 'red'))
			continue
		index = index.history(period=period)
		get_stock(index, name)
		break

def stock_menu(df, name):
	while(True):
			prompt_download_data(name)
			option = ''
			try:
				option = int(input('Enter your choice: '))
				option = validate_option(option, range(1, 4))
			except:
				print(colored('Invalid option. Please enter a number between 1 and 3.', 'red'))
			if option == 1:
				if len(name) > 31:
					name = name[0:31]
				save_xlsl_data(df, name)
				break
			elif option == 2:
				break
			elif option == 3:
				exiting_program()

if __name__=='__main__':
    main()