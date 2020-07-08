# class Map():
    
#     def __init__(self):
#         self.cities = dict()
#         self.roads = dict()


#     def getRoadByName(self, name):
#         return self.roads[name]

#     def getCityByName(self, name):
#         return self.cities[name]
    
#     def getData(self):
#         data = dict()
#         b=list()
#         for a in self.cities:
#             b.append(self.cities[a].to_json())
#         data['cities'] = b
#         c=list()
#         for d in self.roads:
#             c.append(self.roads[d].to_json())
#         data['roads'] = c
#         return data

#Old version
class Map():
    
    cities = dict()
    roads = dict()

    @staticmethod
    def getRoadByName(name):
        return Map.roads[name]

    @staticmethod
    def getCityByName(name):
        return Map.cities[name]
    
    @staticmethod
    def getData():
        data = dict()
        b=list()
        for a in Map.cities:
            b.append(Map.cities[a].to_json())
        data['cities'] = b
        c=list()
        for d in Map.roads:
            c.append(Map.roads[d].to_json())
        data['roads'] = c
        return data


        
