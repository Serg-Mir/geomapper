import folium


class GeoMapper:
    def __init__(self, location, zoom_start=12):
        self.location = location
        self.zoom_start = zoom_start
        self.map = folium.Map(location=location, zoom_start=zoom_start)

    def add_marker(self, location, popup=None, icon="info-sign"):
        marker = folium.Marker(
            location=location, popup=popup, icon=folium.Icon(color="blue", icon=icon)
        )
        marker.add_to(self.map)

    def save_map(self, file_path):
        self.map.save(file_path)
