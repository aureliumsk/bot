import sqlite3
from config import *
import matplotlib
from uuid import uuid4
matplotlib.use('Agg')
import matplotlib.figure as fg
import cartopy.crs as ccrs


class DB_Map():
    def __init__(self, database):
        self.database = database
    
    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.commit()

    def add_city(self,user_id, city_name ):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]  
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1
            else:
                return 0

            
    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT cities.city 
                            FROM users_cities  
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))

            cities = [row[0] for row in cursor.fetchall()]
            return cities


    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT lat, lng
                            FROM cities  
                            WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates

    def create_grapf(self, path: str, cities: list):
        fig = fg.Figure()
        ax = fig.add_subplot(projection=ccrs.PlateCarree())
        ax.stock_img()
        for city in cities:
            coordinates = self.get_coordinates(city)
            if coordinates is None:
                continue
            lat, lon = coordinates
            ax.plot(lon, lat, "bo")
            ax.text(lon, lat - 13, city)
        fig.savefig(path)
        
    def draw_distance(self, city1, city2):
        pass

if __name__=="__main__":    
    m = DB_Map(DATABASE)
    m.create_user_table()
    # m = DB_Map(DATABASE)
    # m.create_grapf("image.png", ["New York", "Moscow"])
