import requests, time, random, sys, argparse



# 127.0.0.1 is the default internal IP address for when you want to run & test an API server on your local machine
def search_area(ip_address: str):
  # Defaults to localhost IP address if it is not given
  if ip_address == None:
    ip_address = '127.0.0.1'
  
  # GET search area coords from database
  response = requests.get(f"http://{ip_address}:5000/getSearchArea")
  # Handle exception where GET request is called at exactly the same time as a POST request, which can causes JSON decoding issues 
  try:
    print(response.json())
  except requests.exceptions.JSONDecodeError:
    print("JSONDecodeError: cannot return response body at this time")
  # Cool down period of 0.5 seconds
  time.sleep(0.5)
  request_body = {
    "search_area": [
      {
        "lat": random.randint(-50,50),
        "lng": random.randint(-50,50)
      },
      {
        "lat": random.randint(-50,50),
        "lng": random.randint(-50,50)
      },
      {
        "lat": random.randint(-50,50),
        "lng": random.randint(-50,50)
      }
    ]
  }
  # POST updated search area coords onto the database 
  try:
    response = requests.post(f"http://{ip_address}:5000/postSearchArea", json=request_body)
  except requests.exceptions.JSONDecodeError:
    print("JSONDecodeError: cannot return response body at this time")
    
  # Cool down period of 0.5 seconds
  time.sleep(0.5)


def geofence(ip_address: str = '127.0.0.1', vehicle_name: str = None):
  # Assign the IP address to the local host if IP address is not given
  if ip_address == None:
    ip_address = '127.0.0.1'
  # Raises an exception if vehicle name is not given
  if vehicle_name == None:
    raise Exception("This function requires argument 'vehicle_name', but it was not provided")
  

  # GET search area coords from database
  # Also handle exception where GET request is called at exactly the same time as a POST request, which can causes JSON decoding issues 
  try:
    response = requests.get(f"http://{ip_address}:5000/getGeofence/{vehicle_name}")
    print(response.json())
  except requests.exceptions.JSONDecodeError:
    pass
    
  # Cool down period of 0.5 seconds
  time.sleep(0.5)
    
  request_body = {
    "geofence": [
      {
        "coordinates": [
          {
            "lat": random.randint(-50,50),
            "lng": random.randint(-50,50)
          },
          {
            "lat": random.randint(-50,50),
            "lng": random.randint(-50,50)
          },
          {
            "lat": random.randint(-50,50),
            "lng": random.randint(-50,50)
          },
        ],
        # Return a random boolean value for testing
        "keep_in": random.getrandbits(1)
      }
      # Return an array of geofence coordinates between 2-5 objects
      for i in range(3)
    ]
  }
    
  # POST updated search area coords onto the database 
  try:
    response = requests.post(f"http://{ip_address}:5000/postGeofence/{vehicle_name}", json=request_body)
  except requests.exceptions.JSONDecodeError:
    print("JSONDecodeError: cannot return response body at this time")
  # Cool down period of 0.5 seconds
  time.sleep(0.5)
    
  pass


# Command line format: 
# `python get_post.py --function FUNCTION --vehicle VEHICLE_NAME --ip IP_ADDRESS` (IP will default to localhost if not provided)
if __name__ == '__main__':  
  # Create argument parser for flagged keyword arguments
  # For more information, run `py get_post.py -h` for info on all functions
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--function", dest="function", type=str, help="The function you want to test")
  parser.add_argument("-i", "--ip", dest="ip_address", type=str, help="The IP address of the API server")
  parser.add_argument("-v", "--vehicle", dest="vehicle_name", type=str, help="The name of the vehicle (i.e., MEA, MAC, ERU)")
  parser.add_argument("-ls", "--list", dest="list_functions", type=bool, help="List all functions")
  
  args = parser.parse_args()
  
  if args.list_functions:
    print("FUNCTIONS\n")
    print("search_area()")
    print("geofence()")

  elif args.function == 'all':
    while True:
      search_area(ip_address=args.ip_address)
      geofence(ip_address=args.ip_address, vehicle_name=args.vehicle_name)
    
  else:
    # Call the according function with its keyword arguments 
    try:
      while True:
        globals()[args.function](ip_address=args.ip_address, vehicle_name=args.vehicle_name)
      
    except KeyError:
      raise Exception("Please enter a function name using the '-f' or '--function' flag to run test")
      
    except TypeError:
      while True:
        globals()[args.function](ip_address=args.ip_address)