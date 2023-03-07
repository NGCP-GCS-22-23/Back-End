# Ground Communication System (GCS) - API Repository
A repository for the application programming interface (API) of the Northrop Grumman Collaboration Project. Built using Python, Flask, and SQLite.

## Summary
-
-

## Required Software
- Python 3.7-3.10.6 (Python 3.11+ does not work)
- Install `pip` (Python's package installer)
  - [pip documentation and installation guide](https://pip.pypa.io/en/stable/installation/)

## Getting Started
1. Install `virtualenv`:
```bash
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:
```bash
$ virtualenv env
```

3. Run the command:
```bash
# For Powershell / Command Prompt
$ .\env\Scripts\activate
# oFor Git Bash
$ source env/Scripts/activate
```

4. Install the dependencies:
```bash
$ (env) pip install -r requirements.txt
```

5. Finally start the server:
```bash
$ (env) python app.py
```

6. After running the server, you should see this message on your terminal:
```bash
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use 
a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://10.110.245.63:5000
Press CTRL+C to quit
```


## API Endpoints:
The API documentation has been moved to the repository's wiki section. 


### _Example Geofence format (for MAC, MEA, and ERU)_
```
{
    "geofence": [
        {
          "coordinates": [
            {
              "lat": 0.0,
              "lng": 0.0
            },
            {
              "lat": 0.0,
              "lng": 0.0
            },
            {
              "lat": 0.0,
              "lng": 0.0
            },
          ],
          "keep_in": true
        },
        {
          "coordinates": [
            {
              "lat": 0.0,
              "lng": 0.0
            },
            {
              "lat": 0.0,
              "lng": 0.0
            },
            {
              "lat": 0.0,
              "lng": 0.0
            },
          ],
          "keep_in": false
        }
      ]
}
NOTE: Geofence is an array of objects. Each object represents a single polygon. A polygon is composed of the boolean 'Keep_in' and an array that can contain any number of coordinates. Also keeping track of circle inputs for repopulating GUI with previous inputs.
```

### _Example Search Area format_
```
{
    "search_area": [
        {
          "lng": 0.0,
          "lat": 0.0
        },
        {
          "lng": 0.0,
          "lat": 0.0
        },
        {
          "lng": 0.0,
          "lat": 0.0
        }
      ]
}
NOTE: Search Area is an array of objects that describe an area made up of longitudes and latitudes pairs
```

### _Example Home Coordinates format_
```
{
    "home_coordinates": {
        "1": {
          "vehicle": "MAC",
          "lat": 33.93368449228065,
          "lng": -117.63028265435334
        },
        "2": {
          "vehicle": "MEA",
          "lat": 33.934454472545525,
          "lng": -117.63246060807343
        },
        "3": {
          "vehicle": "ERU",
          "lat": 33.93368449228065,
          "lng": -117.63077618081208
        }
      },
}
NOTE: Each vehicle has its own home coordinates
```

### _Example Drop Coordinates format_
```
{
  "drop_coordinates":
    {
      "lat": 33.93436545784193,
      "lng": -117.6308888335907
    }
}
Note: Drop coordinates are for MAC
```

### _Example Evacuation Coordinates format_
```
{
  "evacuation_coordinates":
  {
    "lat": 33.934071708659815,
    "lng": -117.63107658822175
  }
}
Note: Evacuation coordinates are for MEA and ERU
```
## Load Testing
**NOTE:** Change your directory into the `testing` folder before running any testing scripts:
* To search for all available test functions, use this commmand:
```bash
python get_post.py -ls true
```
* To run every second GET requests only, follow this convention: 
```bash
python get_only.py -f [function] -v [vehicle_name]
# Example: python get_only.py -f search_area
```

* To run every second GET & POST requests, follow this convention:
```bash
python get_only.py -f [function] -v [vehicle_name]
# Example: python get_post.py -f geofence -v MAC
```

* Alternatively, you can run the `get_post.py` script with the `-f all` setting, which will run all requests sequentially (only `geofence` and `search_area` are currently available)
```bash
python get_only.py -f all -v [vehicle_name]
# Example: python get_post.py -f all -v ERU
```