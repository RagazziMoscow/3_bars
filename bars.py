import json
import math


## Загрузка файла, возвращает объект
def load_json():
	file = open("bars.json", "r")
	result = file.read()
	return json.loads(result)

## Возвращает имя и число мест самого большого бара
def get_max_bar(object):
	max = object[0]["Cells"]["SeatsCount"]
	name = ""
	for item in object:
		if item["Cells"]["SeatsCount"]>max:
			max = item["Cells"]["SeatsCount"]
			name = item["Cells"]["Name"]
	return {"Name": name, "SeatsCount": max}

## Возвращает имя и число мест самого маленького бара
def  get_min_bar(object):
	min = object[0]["Cells"]["SeatsCount"]
	name = ""
	for item in object:
		if item["Cells"]["SeatsCount"]<min:
			min = item["Cells"]["SeatsCount"]
			name = item["Cells"]["Name"]
	return {"Name": name, "SeatsCount": min}

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

## Возвращает геоданные (широту и долготу)
def  get_geoData(object):
	return {"long" : object["Cells"]["geoData"]["coordinates"][1], "lat" : object["Cells"]["geoData"]["coordinates"][0]}



##Возвращает самый ближайший бар в виде имени и расстояния до него
## Принимает в параметры список баров и текущие координаты
def get_nearest_bar(list, long, lat):
	long = float(long)
	lat = float(lat)
	name = list[0]["Cells"]["Name"]
	Data = get_geoData(list[0])
	longData = Data["long"]
	latData = Data["lat"]
	min_dist = circle_distance(longData , latData, long, lat)
	i = 1
	for item in list:
		Data = get_geoData(item)
		longData = Data["long"]
		latData = Data["lat"]
		if (circle_distance(longData, latData, long, lat)<min_dist):
			min_dist = circle_distance(longData, latData, long, lat)
			name = item["Cells"]["Name"]
		
	return {"Name" : name, "distance" : round(min_dist/1000, 2)}
		



list = load_json()

b = get_max_bar(list)
c = get_min_bar(list)
print("Самый большой бар: ", b["Name"], "Число мест: ", b["SeatsCount"])
print("Самый маленький бар: ", c["Name"], "Число мест: ", c["SeatsCount"])

#e = circle_distance(55.688475, 37.909184, 41.988559, 21.463479)
#print(e)
print("Введите вашу широту")
longData= input()
print("Введите вашу долготу")
latData = input()
e = get_nearest_bar(list, longData, latData)
print("Ближайший бар: ", e["Name"], ", Близость: ", e["distance"], " км")

