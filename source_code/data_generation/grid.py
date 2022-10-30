class Grid:
    def __init__(self, grid_id, min_lat, max_lat, min_long, max_long):
        self.grid_id = grid_id
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_long = min_long
        self.max_long = max_long

    def to_string(self):
        return str(self.grid_id) + ',' + str(self.min_lat) + ',' + str(self.max_lat) + ',' + str(
            self.min_long) + ',' + str(self.max_long)
