from colorama import Fore, Back, Style
import requests
from bs4 import BeautifulSoup
import random
import re
import unicodedata
import pandas


def main():

    cars = []

    marque = input("Brand : ").upper()

    for letter in marque:
        if letter.isdigit():
            print("The brand you entered invalid, you have one more try before ending.")
            marque = input("Brand : ").upper()
            for l in marque:  
                if l.isdigit():
                    erreur()
                    return None
                else:
                    pass
        else:
            pass

    year_min = int(input("Minimum year : "))

    if year_min > 2023 or year_min < 1900 :
        year_min = int(input(f"Enter a date between {Back.RED}1900{Back.RESET} and {Back.RED}2023{Back.RESET}( one more try before ending ):"))
        if year_min > 2023 or year_min < 1900 :
            erreur()
            return None

    year_max = int(input("Maximum Year: "))

    if year_max > 2023 or year_max < 1900 :
        year_max = int(input(f"Enter a date between {Back.RED}1900{Back.RESET} and {Back.RED}2023{Back.RESET}( one more try before ending ):"))
        if year_max > 2023 or year_max < 1900 :
            erreur()
            return None
    
    mileage_max = int(input("Maximum mileage : "))

    energies = int(input(f"Energies : {Fore.BLUE}1 -> Petrol{Fore.RESET}; {Fore.GREEN}2 -> Electricity{Fore.RESET}; {Fore.YELLOW}3 -> Diesel{Fore.RESET}\n"))

    if energies == 1:
        energies = "ess"
    elif energies == 2:
        energies = "elec"
    elif energies == 3:
        energies = "dies"
    else:
        erreur()
        return None
        
    gearbox = int(input(f"Gearbox : {Fore.BLUE}1 -> Manual{Fore.RESET}; {Fore.GREEN}2 -> Automatic{Fore.RESET};\n"))

    if gearbox == 1:
        gearbox = "MANUAL"
    elif gearbox == 2:
        gearbox == "AUTO"
    else:
        erreur()
        return None

    print(f"{Fore.GREEN}\nRequest sent successfully{Fore.RESET}\n")    

    for pages in range(10): # changer le range pour définir le nombre de pages

        user_agents = [ 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
            'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
        ]

        user_agent = random.choice(user_agents)
        headers = {'User-Agent': user_agent}

        url = f"https://www.lacentrale.fr/listing?makesModelsCommercialNames={marque}&yearMin={year_min}&yearMax={year_max}&mileageMax={mileage_max}&energies={energies}&gearbox={gearbox}&page={pages}"
        # url = f"https://www.lacentrale.fr/listing?makesModelsCommercialNames=AUDI&page={pages}"
        # url = f"https://www.lacentrale.fr/listing?energies=ess&gearbox=MANUAL&makesModelsCommercialNames=AUDI&mileageMax=1000000&options=&page={pages}&yearMax=2023&yearMin=1900"

        response = requests.get(url, headers=headers) # Avec UserAgent pour essayer de bypass


        soup = BeautifulSoup(response.content, "html.parser")
        car_card = soup.find_all("div", class_="searchCard")

        caracs_car = []
        temp_liste = []  
        cats = ["brand","model","motor","year","mileage","energy","price"]

        brand_car = []
        name_car = []
        motor_car = []
        year_car = []
        mileage_car = []
        energy_car = []
        price_car = []

        car_beg = []

        for car in car_card:

            name = car.find("h3").text
            price = car.find("span",class_="Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2").text
            brand = name.split()[0]
            motor = car.find(class_="Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2").text

            numbers = [int(n) for n in re.findall(r'\d+',price)]
            numbers = int(''.join(str(number).replace(' ', '') for number in numbers))

            name_car.append(name)
            price_car.append(numbers)
            brand_car.append(brand)
            motor_car.append(motor)

        big = soup.find_all("div",class_="Vehiculecard_Vehiculecard_characteristics")
        subclasses = soup.find_all("div", class_="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")

        for classe in subclasses:

            if "km" in classe.text:                                 # POUR LE KILOMETRAGE ICI

                string = unicodedata.normalize("NFKD", classe.text)
                string = string.replace("km", "")
                string = string.replace(" ", "")
                string = int(string)
                temp_liste.append(string)

            elif classe.text.isdigit():                             # POUR LES ANNEES ICI

                annee = int(classe.text)
                temp_liste.append(annee)

            else:                                                   # POUR LE RESTE (energie + boite de vitesse)            
                temp_liste.append(classe.text)

        caracs_car = []                                             # Pour transformer la liste en 3D Liste avec 4 elements à l'intérieur
        for i in range(0, len(temp_liste), 4):
            sous_liste = temp_liste[i:i+4]
            caracs_car.append(sous_liste)

        for a in caracs_car:                                        # Pour balancer les années, kilometrages et energies depuis "caracs_car" vers des listes propres à chacunes
            year_car.append(a[0])
        year_car.pop(0)  
        for a in caracs_car:
            mileage_car.append(a[1])
        mileage_car.pop(0)
        for a in caracs_car:
            energy_car.append(a[3])
        energy_car.pop(0)

        car_beg = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        for i, sous_liste in enumerate(car_beg):
            sous_liste.append(brand_car[i])
            sous_liste.append(name_car[i])
            sous_liste.append(motor_car[i])
            sous_liste.append(year_car[i])
            sous_liste.append(mileage_car[i])
            sous_liste.append(energy_car[i])
            sous_liste.append(price_car[i])

        cars += car_beg
        dataframe = pandas.DataFrame(cars)
        dataframe.columns = cats
        dataframe.to_csv("csv_format.csv", index=False)
        dataframe.to_excel("excel_format.xlsx", index=False)

def erreur():
    print(f"{Fore.RED}Error while executing function, escaping ...{Fore.RESET}")


if __name__ == "__main__":
    main()