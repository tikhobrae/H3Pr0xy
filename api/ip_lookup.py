import geoip2.database
import os

class IPLookup:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = os.path.join(os.path.dirname(__file__), 'ip_db','GeoLite2-City.mmdb')
        else:
            self.db_path = db_path

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found at {self.db_path}")

        self.reader = geoip2.database.Reader(self.db_path)

    def get_ip_info(self, ip_address):
        try:
            response = self.reader.city(ip_address)
            ip_info = {
                "ip": ip_address,
                "country": response.country.name,
                "country_code": response.country.iso_code,
                "city": response.city.name,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
            }
            return ip_info
        except geoip2.errors.AddressNotFoundError:
            return {"error": "not avail data for this!"}

    def close(self):
        self.reader.close()
