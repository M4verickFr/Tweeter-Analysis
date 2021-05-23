class City(object):
    def __init__(self, place_id, display_name, polygon, lat, lon):
        self.place_id = place_id
        self.display_name = display_name
        self.polygon = polygon
        self.lat = lat
        self.lon = lon
    
    @staticmethod
    def insert(bdd,place):
        bdd.insert("city", {
            "place_id": place.id,
            "display_name": place.full_name, 
            "polygon": str(place.bounding_box.coordinates),
            "lat": place.centroid[1],
            "lon": place.centroid[0]
        })
    
    @staticmethod
    def exist(bdd, id):
        nb_city = bdd.request_fetchone(f"SELECT COUNT(*) FROM city WHERE place_id='{id}'")
        return nb_city > 0