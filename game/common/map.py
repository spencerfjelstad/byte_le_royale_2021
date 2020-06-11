class Map():
    cities = list()
    roads = list()

    @staticmethod
    def getRoadByName(name):
        for i in Map.roads:
            if i.road_name == name:
                return i

    @staticmethod
    def getCityByName(name):
        for i in Map.cities:
            if i.city_name == name:
                return i 
    
    @staticmethod
    def getData():
        data = dict()
        b=list()
        for a in Map.cities:
            b.append(a.to_json())
        data['cities'] = b
        c=list()
        for d in Map.roads:
            c.append(d.to_json())
        data['roads'] = c
        return data


        
