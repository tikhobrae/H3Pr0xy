import geoip2.database  # Import the geoip2 library for IP geolocation
import os  # Import os for file path handling

class IPLookup:
    def __init__(self, db_path=None):
        # If no database path is provided, set a default path for the GeoLite2 database
        if db_path is None:
            self.db_path = os.path.join(os.path.dirname(__file__), 'ip_db', 'GeoLite2-City.mmdb')
        else:
            self.db_path = db_path  # Use the provided database path

        # Check if the database file exists, raise an error if not found
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found at {self.db_path}")

        # Open the GeoIP2 database reader
        self.reader = geoip2.database.Reader(self.db_path)

    def get_ip_info(self, ip_address):
        # Retrieve geolocation information for the provided IP address
        try:
            response = self.reader.city(ip_address)  # Get city-level data for the IP
            ip_info = {
                "ip": ip_address,  # Store the IP address
                "country": response.country.name,  # Get the country name
                "country_code": response.country.iso_code,  # Get the country ISO code
                "city": response.city.name,  # Get the city name
            }
            return ip_info  # Return the IP information as a dictionary
        except geoip2.errors.AddressNotFoundError:
            return {"error": "not avail data for this!"}  # Return an error if the IP address is not found

    def close(self):
        # Close the database reader when done
        self.reader.close()
