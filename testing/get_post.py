import requests, time, random, sys, argparse


def search_area(**kwargs):
  # Handle exception where GET request is called at exactly the same time as a POST request, which can causes JSON decoding issues 
  try:
    # GET search area coords from database
    response = requests.get("http://{}:5000/getSearchArea".format(
      # Defaults to localhost IP address if it is not given
      kwargs["ip_address"] if kwargs["ip_address"] else '127.0.0.1'
    ))
    print(response.json())
  except requests.exceptions.JSONDecodeError:
    print("JSONDecodeError: cannot return response body at this time")
  # Cool down period of 0.5 seconds
  time.sleep(0.2)
  
  
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
    response = requests.post(
      "http://{}:5000/postSearchArea".format(
        kwargs["ip_address"] if kwargs["ip_address"] else '127.0.0.1'
      ), 
      json=request_body
    )
  except requests.exceptions.JSONDecodeError:
    print("JSONDecodeError: cannot return call POST request at this time")
    
  # Cool down period of 0.5 seconds
  time.sleep(0.2)


def geofence(**kwargs):
  # Raises an exception if vehicle name is not given
  if not kwargs["vehicle_name"]:
    raise Exception("This function requires argument 'vehicle_name', but it was not provided")
  # GET search area coords from database
  # Also handle exception where GET request is called at exactly the same time as a POST request, which can causes JSON decoding issues 
  try:
    response = requests.get("http://{}:5000/getGeofence/{}".format(
      # Defaults IP address to localhost if IP address is not given
      kwargs['ip_address'] if kwargs["ip_address"] else '127.0.0.1', 
      kwargs["vehicle_name"]
    ))
    print(response.json())
  except requests.exceptions.JSONDecodeError:
    print("JSONDecodeError: cannot return response body at this time")
    
  # Cool down period of 0.5 seconds
  time.sleep(0.2)
    
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
    response = requests.post(
      "http://{}:5000/postGeofence/{}".format(
        # Defaults IP address to localhost if IP address is not given
        kwargs['ip_address'] if kwargs["ip_address"] else '127.0.0.1', 
        kwargs["vehicle_name"]
      ), 
      json=request_body
    )
  except requests.exceptions.JSONDecodeError:
    print("JSONDecodeError: cannot return response body at this time")
  # Cool down period of 0.5 seconds
  time.sleep(0.2)
    
  pass




# List of all functions that can be tested
FUNCTIONS_LIST = [search_area, geofence]

# Create argument parser for flagged keyword arguments
# For more information, run `py get_post.py -h` for info on all functions
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--function", dest="function", type=str, help="The function you want to test")
parser.add_argument("-i", "--ip", dest="ip_address", type=str, help="The IP address of the API server")
parser.add_argument("-v", "--vehicle", dest="vehicle_name", type=str, help="The name of the vehicle (i.e., MEA, MAC, ERU)")
parser.add_argument("-ls", "--list", dest="list_functions", type=bool, help="List all functions")
  
args = parser.parse_args()


# Command line format: 
# `python get_post.py --function FUNCTION --vehicle VEHICLE_NAME --ip IP_ADDRESS` (IP will default to localhost if not provided)
if __name__ == '__main__':  
  if args.list_functions:
    print("ALL FUNCTIONS AVAILABLE FOR TESTING:\n")
    for f in FUNCTIONS_LIST:
      print(str(f).split(" ")[1])

  elif args.function == 'all':
    while True:
      for func in FUNCTIONS_LIST:
        func(ip_address=args.ip_address, vehicle_name=args.vehicle_name)
  # Call the according function with its keyword arguments 
  else:
    try:
      while True:
        globals()[args.function](ip_address=args.ip_address, vehicle_name=args.vehicle_name)
    except KeyError:
      raise Exception("""
      Please enter a valid function name using the '-f' or '--function' flag to run test!
      For more info on available functions, use:
      
      python [filename] -ls true
      """
      )