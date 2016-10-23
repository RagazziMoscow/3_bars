import json
import math
import sys


## Загрузка файла, возвращает объект
def load_json():
    try:
        with open(sys.argv[1], "r") as json_file:
            json_content = json_file.read()
            return json.loads(json_content)
    except FileNotFoundError:
        return None


## Возвращает имя и число мест самого большого бара
def get_max_bar(object):

    bars_seats_list = [] # Список числа мест для всех баров
    for item in object:
        bars_seats_list.append(item["Cells"]["SeatsCount"])

    max_count = max(bars_seats_list) # Получаем максимальное число мест
    for item in object:
        if(item["Cells"]["SeatsCount"]==max_count):
            return {"Name" : item["Cells"]["Name"], "SeatsCount" : item["Cells"]["SeatsCount"]}



## Возвращает имя и число мест самого маленького бара
def  get_min_bar(object):

    bars_seats_list = [] # Список числа мест для всех баров
    for item in object:
        bars_seats_list.append(item["Cells"]["SeatsCount"])

    min_count = min(bars_seats_list) # Получаем максимальное число мест
    for item in object:
        if(item["Cells"]["SeatsCount"]==min_count):
            return {"Name" : item["Cells"]["Name"], "SeatsCount" : item["Cells"]["SeatsCount"]}

##Считает расстояние по дуге на Земле между двумя точками, заданными широтой и долготой в градусах
## Принимает в качестве параметров значения широт и долгот двух точек, расстояние между которыми требуется определить
def circle_distance(long1, lat1, long2, lat2):
    long1 = math.radians(long1)
    lat1 = math.radians(lat1)
    long2 = math.radians(long2)
    lat2 = math.radians(lat2)


    sin1 = math.sin(lat1)
    sin2 = math.sin(lat2)
    cos1 = math.cos(lat1)
    cos2 = math.cos(lat2)
    cos12 = math.cos(long2-long1)
    delta = math.acos(sin1*sin2 + cos1*cos2*cos12) # Получаем угловое расстояние

    distance = 6367444.6571225 * delta # умножаем угловое расстояние на радиус Земли
    return distance

## Возвращает словарь и геоданными(широту и долготу)
def  get_geo_data(object):
    return {"long" : object["Cells"]["geoData"]["coordinates"][1], "lat" : object["Cells"]["geoData"]["coordinates"][0]}



##Возвращает самый ближайший бар в виде имени и расстояния до него
## Принимает в параметры список баров и текущие координаты
def get_nearest_bar(list, long, lat):
    long = float(long)
    lat = float(lat)
    bar_name = list[0]["Cells"]["Name"]
    geo_data = get_geo_data(list[0])
    long_data = geo_data["long"]
    lat_data = geo_data["lat"]
    min_dist = circle_distance(long_data , lat_data, long, lat)
    i = 1
    for item in list:
        geo_data = get_geo_data(item)
        long_data = geo_data["long"]
        lat_data = geo_data["lat"]
        if (circle_distance(long_data, lat_data, long, lat)<min_dist):
            min_dist = circle_distance(long_data, lat_data, long, lat)
            bar_name = item["Cells"]["Name"]

    return {"Name" : bar_name, "distance" : round(min_dist/1000, 2)}


def main():

    list = load_json()
    if list is not None:
        max_bar = get_max_bar(list)
        min_bar = get_min_bar(list)
        print("Самый большой бар: ", max_bar["Name"], "Число мест: ", max_bar["SeatsCount"])
        print("Самый маленький бар: ", min_bar["Name"], "Число мест: ", min_bar["SeatsCount"])

        #e = circle_distance(55.688475, 37.909184, 41.988559, 21.463479)
        #print(e)
        print("Введите вашу широту")
        long_data= input()
        print("Введите вашу долготу")
        lat_data = input()
        nearest_bar = get_nearest_bar(list, long_data, lat_data)
        print("Ближайший бар: ", nearest_bar["Name"], ", Близость: ", nearest_bar["distance"], " км")
    else:
        print("Файл, путь до которого вы указали, не существует, или путь задан некорректно")





if __name__ == '__main__':
    main()

