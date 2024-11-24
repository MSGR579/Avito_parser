from parser import Parser
from card_description import CardDescription
from transliterate import translit

def convert_city_name(city):
    return translit(city, 'ru', reversed=True).lower()


city = input("Введите название города: ")
translated_city = convert_city_name(city)

url_base = f"https://www.avito.ru/{translated_city}?q="
req_value = input("Введите что будем искать: ")
p = Parser(url_base, req_value)
res_parsing = CardDescription(p.parsed_links, req_value,city)