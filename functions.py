import requests
import json


def get_request(status=None, location=None, plate_no=None, body_no=None, start=None, end=None):
    url = 'google_apps_script_link'
    params = {}
    
    if status:
        params['status'] = status
        
    if location:
        params['location'] = location
    
    if plate_no:
        params['plate_no'] = plate_no
    
    if body_no:
        params['body_no'] = body_no
    
    if start:
        params['start'] = start
    
    if end:
        params['end'] = end
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()  # Parse the JSON response
        return results
    
    else:
        print(f"Error: {response.status_code}")
        return None

 
def post_request(data=None, type=None, new_location=None, new_status=None, plate_no=None, body_no = None):
    url = 'https://script.google.com/macros/s/AKfycbw39GDcsVzUi7sWkeeSkWrMB0Hg5WshJXksiT2YaGKc7wMksD9pXU37m6UJ28YRrCGh/exec'
    
    params = {}
    if type:
        params['type'] = type
    if new_location:
        params['new_location'] = new_location
    if new_status:
        params['new_status'] = new_status
    if plate_no:
        params['plate_no'] = plate_no
    if body_no:
        params['body_no'] = body_no
    
    # Create the query string from params
    if params:
        url += '?' + '&'.join(f'{key}={value}' for key, value in params.items())

    # Make the POST request
    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    # Print response
    print(response.text)


# # Get all a truck did last month
# last_month = get_request(start='05/2024', end='08/2024',plate_no='ABC124')
# print("Last Month:")
# for row in last_month:
#     print(row)

# # Get all trucks
# all_trucks = get_request()
# print("All Trucks:")
# for row in all_trucks:
#     print(row)

# # Get only active trucks
# active_trucks = get_request(status='active')
# print("Active Trucks:")
# for row in active_trucks:
#     print(row)

# # Get all a truck did last year
# last_year = get_request(status='year',plate_no='AAB334')
# print("Last Year:")
# for row in last_year:
#     print(row)

# # Get where the current truck is
# location = get_request(status='location',plate_no='AAB334')
# print("Latest Location:")
# for loc in location:
#     print(loc)

# # Add a new truck
# entry = ["ABE123", 'bruh_test']
# post_request(entry, 'truck')

# # Add a new trip
# entry_2 = ['ABE123', 'Makati', "03/2024", 'did some work']
# post_request(entry_2, 'trip')

# # Change the truck status 
# post_request('inactive','truck','ABC124')

# # Change the truck status 
# post_request(new_status='SOLD',body_no='DP1')
