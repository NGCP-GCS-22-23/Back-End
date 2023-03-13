import requests, time, sys, argparse
from inspect import getmembers, isfunction


def mission_waypoint(**kwargs):
  # Handle exception where GET request is called at exactly the same time as a POST request, which can causes JSON decoding issues 
  try:
    # GET search area coords from database
    response = requests.get("http://{}:5000/getMissionWaypoint/{}".format(
      # Defaults IP to localhost if not provided
      kwargs["ip_address"] if kwargs["ip_address"] else '127.0.0.1',
      kwargs['vehicle_name']
    ))
    print(response.json())
  except requests.exceptions.JSONDecodeError:
    print("JSONDecodeError: cannot return response body at this time")
  # Cool down period of 0.5 seconds
  time.sleep(kwargs['interval'] if kwargs['interval'] else 0.5)


def home_coordinates(**kwargs):
  # Handle exception where GET request is called at exactly the same time as a POST request, which can causes JSON decoding issues 
  try:
    # GET search area coords from database
    response = requests.get("http://{}:5000/getHomeCoordinates/{}".format(
      # Defaults to localhost IP address if it is not given
      kwargs["ip_address"] if kwargs["ip_address"] else '127.0.0.1',
      kwargs['vehicle_name']
    ))
    print(response.json())
  except requests.exceptions.JSONDecodeError:
    print("JSONDecodeError: cannot return response body at this time")
  # Cool down period of 0.5 seconds
  time.sleep(kwargs['interval'] if kwargs['interval'] else 0.5)


def search_area(**kwargs):
  # GET search area coords from database
  # Defaults IP to localhost if not provided
  response = requests.get("http://{}:5000/getSearchArea".format(
    kwargs["ip_address"] if kwargs["ip_address"] else '127.0.0.1'
  ))
    
    # Handle exception where GET request is called at exactly the same time as a POST request, which can causes JSON decoding issues 
  try:
    print(response.json())
  except requests.exceptions.JSONDecodeError:
    print("JSONDecodeError: cannot return response body at this time")
    
  # Cool down period of 0.5 second
  time.sleep(kwargs['interval'] if kwargs['interval'] else 0.5)


def geofence(**kwargs):
  # Raises an exception if vehicle name is not given
  if not kwargs["vehicle_name"]:
    raise Exception("This function requires argument 'vehicle_name', but it was not provided")
  # GET search area coords from database
  # Also handle exception where GET request is called at exactly the same time as a POST request, which can causes JSON decoding issues 
  try:
    response = requests.get("http://{}:5000/getGeofence/{}".format(
      # Defaults IP address to localhost if IP address is not given
      kwargs["ip_address"] if kwargs["ip_address"] else '127.0.0.1', 
      kwargs["vehicle_name"]
    ))
    print(response.json())
  except requests.exceptions.JSONDecodeError:
    print("JSONDecodeError: cannot return response body at this time")
  
  # Cool down period of 0.5 second
  time.sleep(kwargs['interval'] if kwargs['interval'] else 0.5)
  return


# List of all functions that can be tested
FUNCTIONS_LIST = [mission_waypoint, home_coordinates, search_area, geofence]


# Create argument parser for flagged keyword arguments
# For more information, run `py get_post.py -h` for info on all functions
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--function", dest="function", type=str, help="The function you want to test")
parser.add_argument("-i", "--ip", dest="ip_address", type=str, help="The IP address of the API server")
parser.add_argument("-v", "--vehicle", dest="vehicle_name", type=str, help="The name of the vehicle (i.e., MEA, MAC, ERU)")
parser.add_argument("-ls", "--list", dest="list_functions", type=bool, help="List all functions")
  
args = parser.parse_args()


# Command line format: 
# `python get_only.py --function FUNCTION --vehicle VEHICLE_NAME --ip IP_ADDRESS` (PI will default to localhost if not provided)
if __name__ == '__main__':  
  if args.list_functions:
    print("ALL FUNCTIONS AVAILABLE FOR TESTING:\n")
    for func in FUNCTIONS_LIST:
      print(str(func).split(' ')[1])

  # Call all functions if the given `-f` function setting is `all`
  elif args.function == 'all':
    while True:
      for func in FUNCTIONS_LIST:
        func(
          ip_address=args.ip_address, 
          vehicle_name=args.vehicle_name, 
          interval=(1 / len(FUNCTIONS_LIST))
        )
  
  else:
    # Call the according function with its keyword arguments 
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
