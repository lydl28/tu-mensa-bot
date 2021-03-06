import requests
import json
from lxml import html
import string

def food(type, page):

	tree = html.fromstring(page.content)	
	counter = 1
	typearr = []

	while True:
		path = '//div[@class="mensa_day mensa_day_speise {}"]//tr[@class="mensa_day_speise_row"][{}]//td[@class="mensa_day_speise_'
		path = path.format(type, str(counter))
		
		pathyfy = lambda x, y : tree.xpath(path+x+'"]'+y)

		name = pathyfy('name', '/text()')

		if name == []:
			break

		#init food dict
		food = {'Name': None, 'Type': type, 'Price': None, 'Ampel': None, 'Veg': None, 'Bio': None, 'Klimaessen': None}

		#get name
		if name[1] == '        ':
			food['Name'] = string.rstrip(name[2], None)
		else:
			food['Name'] = string.strip(name[1], None)


		price = pathyfy('preis', '/text()')
		
		food['Price'] = string.rstrip(price[0], None)

		#get Ampel
		food['Ampel'] = pathyfy('name', '//a/@href')[0]

		#Vegetarian/Vegan option
		if pathyfy('name', '//img[@alt="Vegan"]') != []:
			food['Veg'] = 'vegan'
		elif pathyfy('name', '//img[@alt="Vegetarisch"]') != []:
			food['Veg'] = 'vegetarisch'

		#Bio option
		if pathyfy('name', '//img[@alt="Bio"]') != []:
			food['Bio'] = True

		#Klimaessen
		if pathyfy('name', '//img[@alt="Klimaessen"]') != []:
			food['Klimaessen'] = True

		typearr.append(food)
		counter += 1	

	return typearr

def today(type):
	page = requests.get('http://www.studentenwerk-berlin.de/mensen/speiseplan/tu/index.html')
	return(food(type, page))

def tomorrow(type):
	page = requests.get('http://www.studentenwerk-berlin.de/mensen/speiseplan/tu/01.html')
	return(food(type, page))

def dayAfterT(type):
	page = requests.get('http://www.studentenwerk-berlin.de/mensen/speiseplan/tu/02.html')
	return(food(type, page))


if __name__ == '__main__':
	print(today('food'))

#returns all dishes and prices in an array of dicts
#usage: today('type') #options: starters, salads, soups, special, food, side_dishes, desserts

