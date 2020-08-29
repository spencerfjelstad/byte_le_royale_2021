class Map():
    #This needs work but oh well
    cities = dict()
    roads = dict()

    @staticmethod
    def getRoadByName(name):
        return roads[name]

    @staticmethod
    def getCityByName(name):
        return cities[name]
    
    # Spits out JSON
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


        
