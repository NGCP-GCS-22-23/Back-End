import requests, time, sys, argparse



def search_area(ip_address: str = 'localhost'):
  # Defaults to localhost IP address if it is not given
  if ip_address == None:
    ip_address = '127.0.0.1'
  
  while True:
    # GET search area coords from database
    response = requests.get(f"http://{ip_address}:5000/getSearchArea")
    
    # Handle exception where GET request is called at exactly the same time as a POST request, which can causes JSON decoding issues 
    try:
      print(response.json())
    except requests.exceptions.JSONDecodeError:
      print("JSONDecodeError: cannot return response body at this time")
    
    # Cool down period of 1 second
    time.sleep(1)


# Command line format: 
# `python get_only.py --function FUNCTION --vehicle VEHICLE_NAME --ip IP_ADDRESS` (PI will default to localhost if not provided)
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
    
    