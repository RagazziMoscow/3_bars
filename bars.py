import json
import math


## Загрузка файла, возвращает объект
def load_json():
	try:
	    with open("bars.json", "r") as json_file:
	        json_content = json_file.read()
	        return json.loads(json_content)
	except FileNotFoundError:
		return None


## Возвращает имя и число мест самого большого бара
def get_max_bar(object):

    bars_dict = {}
    for item in object:
    	# Получаем словарь типа имя бара:число мест
        bars_dict[item["Cells"]["Name"]] = item["Cells"]["SeatsCount"]
    # Сортируем словарь в порядке убывания, тем самым получая список
    I = lambda x:x[1]
    bars_list = sorted(bars_dict.items(), key=I, reverse = True)
    # Забираем из списка первый элемент
    return bars_list[0]
    

## Возвращает имя и число мест самого маленького бара
def  get_min_bar(object):

    bars_dict = {}
    for item in object:
    	# Получаем словарь типа имя бара:число мест
        bars_dict[item["Cells"]["Name"]] = item["Cells"]["SeatsCount"]
    # Сортируем словарь в полрядке возрастания, тем самым получая список
    I = lambda x:x[1]
    bars_list = sorted(bars_dict.items(), key=I, reverse = False)
    # Забираем из списка первый элемент
    return bars_list[0]


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
	name = list[0]["Cells"]["Name"]
	data = get_geo_data(list[0])
	long_data = data["long"]
	lat_data = data["lat"]
	min_dist = circle_distance(long_data , lat_data, long, lat)
	i = 1
	for item in list:
		data = get_geo_data(item)
		long_data = data["long"]
		lat_data = data["lat"]
		if (circle_distance(long_data, lat_data, long, lat)<min_dist):
			min_dist = circle_distance(long_data, lat_data, long, lat)
			name = item["Cells"]["Name"]
		
	return {"Name" : name, "distance" : round(min_dist/1000, 2)}
		

def main():

    list = load_json()
    if list is not None:
        max_bar = get_max_bar(list)
        min_bar = get_min_bar(list)
        print("Самый большой бар: ", max_bar[0], "Число мест: ", max_bar[1])
        print("Самый маленький бар: ", min_bar[0], "Число мест: ", min_bar[1])

        #e = circle_distance(55.688475, 37.909184, 41.988559, 21.463479)
        #print(e)
        print("Введите вашу широту")
        long_data= input()
        print("Введите вашу долготу")
        lat_data = input()
        nearest_bar = get_nearest_bar(list, long_data, lat_data)
        print("Ближайший бар: ", nearest_bar["Name"], ", Близость: ", nearest_bar["distance"], " км")





if __name__ == '__main__':
	main()

