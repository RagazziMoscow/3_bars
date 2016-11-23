import json
import math
import sys
import os.path


def load_json(file_path):
    if(os.path.exists(file_path)):
        with open(file_path, "r") as json_file:
            json_content = json_file.read()
            return json.loads(json_content)
    else:
        return None


def get_maximal_bar(bar_list):
    max_bar = max(bar_list, key=lambda x: x["Cells"]["SeatsCount"])
    return {"Name": max_bar["Cells"]["Name"],
            "SeatsCount": max_bar["Cells"]["SeatsCount"]}


def get_minimal_bar(bar_list):
    min_bar = min(bar_list, key=lambda x: x["Cells"]["SeatsCount"])
    return {"Name": min_bar["Cells"]["Name"],
            "SeatsCount": min_bar["Cells"]["SeatsCount"]}


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
    delta = math.acos(sin1*sin2 + cos1*cos2*cos12)  # Получаем угловое расстояние

    distance = 6367444.6571225 * delta  # умножаем угловое расстояние на радиус Земли
    return distance


def get_geo_data(bar_item):
    return {"long": bar_item["Cells"]["geoData"]["coordinates"][1],
            "lat": bar_item["Cells"]["geoData"]["coordinates"][0]}


def get_nearest_bar(bar_list, long, lat):
    long = float(long)
    lat = float(lat)
    bar_name = bar_list[0]["Cells"]["Name"]
    geo_data = get_geo_data(bar_list[0])
    long_data = geo_data["long"]
    lat_data = geo_data["lat"]
    min_dist = circle_distance(long_data, lat_data, long, lat)
    for item in bar_list:
        geo_data = get_geo_data(item)
        long_data = geo_data["long"]
        lat_data = geo_data["lat"]
        if (circle_distance(long_data, lat_data, long, lat) < min_dist):
            min_dist = circle_distance(long_data, lat_data, long, lat)
            bar_name = item["Cells"]["Name"]

    return {"Name": bar_name, "distance": round(min_dist/1000, 2)}


def main():

    bar_list = load_json(sys.argv[1])
    if bar_list is not None:
        max_bar = get_maximal_bar(bar_list)
        min_bar = get_minimal_bar(bar_list)
        print("Самый большой бар: ", max_bar["Name"],
              "Число мест: ", max_bar["SeatsCount"])
        print("Самый маленький бар: ", min_bar["Name"],
              "Число мест: ", min_bar["SeatsCount"])

        #e = circle_distance(55.688475, 37.909184, 41.988559, 21.463479)
        #print(e)
        long_data = input("Введите вашу широту\n")
        lat_data = input("Введите вашу долготу\n")
        nearest_bar = get_nearest_bar(bar_list, long_data, lat_data)
        print("Ближайший бар: ", nearest_bar["Name"],
              ", Близость: ", nearest_bar["distance"], " км")
    else:
        print("Файл, путь до которого вы указали, не существует, или путь задан некорректно")


if __name__ == '__main__':
    main()