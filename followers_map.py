'''
Web aplication that creates map of 50 followers of given user.
To use it API keys are required.
'''
import requests
import folium
import geopy
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable
from flask import Flask, render_template, request

app = Flask(__name__)

def collecting (data: dict) -> list:
    '''
    Gets dictionary and retuurns list of tuples with all users coordinates
    '''
    info = []
    geolocator = geopy.Nominatim (user_agent='my-aplication')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds = 1)
    locations = set()
    for user in data['users']:
        try:
            location = geolocator.geocode(user['location'])
            coordinates = [location.latitude, location.longitude]
            while tuple(coordinates) in locations:
                coordinates[0] += 0.0001
                coordinates[1] += 0.0001
            locations.add(tuple(coordinates))
            info.append((user['screen_name'], coordinates[0], coordinates[1]))
        except  GeocoderUnavailable:
            continue
        except AttributeError:
            continue
    return info


def generate_map (info:list):
    '''
    Generates needed map
    '''
    my_map = folium.Map ()
    fg_friends = folium.FeatureGroup(name ='user friends')

    for friend in info:
        fg_friends.add_child(folium.Marker(location = [friend[1], friend[2]], popup = friend[0]))


    my_map.add_child(fg_friends)
    my_map.add_child(folium.LayerControl())
    my_map.save('templates/Friend_map.html')

def sending_request(bearer_token: str, screen_name: str):
    '''
    Sends request to Twitter using API bearer token abd returns json that represents
    data about first 50 followers of user with given screen_name
    '''
    base_url = "https://api.twitter.com/"
    search_url = '{}1.1/friends/list.json'.format(base_url)
    search_headers = {
        'Authorization': 'Bearer {}'.format(bearer_token)
    }
    search_params = {
        'screen_name': '{}'.format(screen_name),
        'count': 50
    }

    response = requests.get(search_url, headers = search_headers, params = search_params)
    return response.json()

@app.route("/")
def index():
    '''
    Returns main page of the site
    '''
    return render_template("index.html")


@app.route("/map", methods=["POST"])
def building_map():
    '''
    Returns map with information about folowers
    '''
    try:
        name = request.form.get("screen_name")
        token = request.form.get("bearer_token")
        if not name or not token:
            return render_template("failure.html")
        data = sending_request(token, name)
        generate_map(collecting(data))

        return render_template("Friend_map.html")
    except KeyError:
        return render_template("failure.html")

if __name__ == "__main__":
    app.run(debug=False)
