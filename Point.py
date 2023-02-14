class Point:
    def __init__(self, lat, lng, elev):
        self.lat = lat
        self.lng = lng
        self.elev = elev

    def __repr__(self):
        return f"Point({self.lat}, {self.lng}, {self.elev})"    

