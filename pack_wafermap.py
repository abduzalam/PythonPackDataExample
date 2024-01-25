import struct
import zlib
import pyodbc



class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
        
    def connect(self):
        if self.connection is None:
            self.connection = pyodbc.connect(self.connection_string)
        return self.connection

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def __enter__(self):
        return self.connect()
        
    def __exit__(self, type, value, traceback):
        if type is None:  # No exception was raised
            self.connection.commit()
        else:
            self.connection.rollback()  # Optional: rollback on exception
        self.close()

class WaferMap:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
        
    
    def pack_and_compress(self, data):
      # Pack the data using struct
      packed_data = struct.pack(f'{len(data)}f', *data)
      # Compress the packed data using zlib
      compressed_data = zlib.compress(packed_data)
      return compressed_data

    def insert_wafermap(self, wafer_id, map_type, compressed_map_data):
        with Database(self.connection_string) as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO WaferMaps (WaferId, MapType, CompressedMapData, CreatedAt) VALUES (?, ?, ?, GETDATE())", wafer_id, map_type, compressed_map_data)
    def retrieve_and_print_data(self,wafer_id):
        with Database(self.connection_string) as db:
            cursor = db.cursor()
            cursor.execute("SELECT CompressedMapData FROM WaferMaps WHERE WaferId = ?", wafer_id)
            row = cursor.fetchone()
            if row:
                compressed_map_data = row[0]
                packed_data = zlib.decompress(compressed_map_data)
                unpacked_data = struct.unpack(f'{len(packed_data)//4}f', packed_data)
                print(unpacked_data)
            else:
                print(f'No wafermap found for wafer {wafer_id}')

if __name__ == '__main__':
  connection_string = 'Driver={SQL Server};Server=localhost;Database=TestDB;Trusted_Connection=yes;'
  # Define a 3x3 wafer map as a flat list of float values
  wafer_map_data = [1.0, 0.0, 0.5, 0.8, 1.1, 0.0, 0.6, 0.9, 1.2]
  wafer_id = 2
  map_type = 'Dense'
  wafer_map = WaferMap(connection_string)
  #wafer_map = WaferMap()
  compressed_map_data = wafer_map.pack_and_compress(wafer_map_data)
  wafer_map.insert_wafermap(wafer_id, map_type, compressed_map_data)
  wafer_map.retrieve_and_print_data(wafer_id)

