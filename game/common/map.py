from game.config import MAX_TICKS

#This needs to be a game object desperately
# STATIC METHODS BAAAAAAAAAAADDDDDDDDDDD
class Map():
    cities = dict()
    roads = dict()

    # This part is probs obsolete
    @staticmethod
    def getRoadByName(name):
        return roads[name]

    # This part is probs obsolete
    @staticmethod
    def getCityByName(name):
        return cities[name]
    
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

        # Generates turns
        for i in range(1, MAX_TICKS):
            data[i] = dict()

        return data


        
