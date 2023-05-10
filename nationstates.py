import requests
from defusedxml import ElementTree as ET
from RegionClass import Region
from RegionBlock import RegionBlock

# TODO:
# This will be an array of utilities to work with the NS api
# E.g. - fetch the update time of a given region, or the number of endos on a given nation

def makeHeaders(mainNation): # Allow overriding headers easily
    headers = { 
        "User-Agent":f"Scarab/0.1, Developed by Hesskin Empire and Volstrostia, in use by {mainNation}",
    }
    return headers

headers = { 
    "User-Agent":f"Scarab/0.1, Developed by Hesskin Empire and Volstrostia",
}

def perform_request(url,headers=headers,data=None):
    # From https://www.nationstates.net/pages/api.html#ratelimits, retrieved on 13 April 2023
    #    RateLimit-Limit: Set to "50"; which means that there are a total of 50 requests available in the current time window. Use instead of hardcoding.
    #    RateLimit-Remaining: How many more requests can be made within the current time window.
    #    RateLimit-Reset: Number of seconds remaining in the current time window.
    #    Retry-After: Once blocked from accessing the API, your script should wait this amount of seconds before trying again.
    #
    # A "request" is an HTTP request to the site for any amount of information and any number of shards.
    # That is, an HTTP request like this is a single request, even though it gathers information on three shards.

    #r = requests.get("https://www.nationstates.net/cgi-bin/api.cgi?nation=testlandia&q=ping",headers={"User-Agent":"cURL", "X-Password":"lolnicetry")

    if not headers:
        print("Headers missing from request")
        return None

    if not data: #do we POST?
        r = requests.get(url,headers=headers) #no :(
    else:
        r = requests.post(url,headers=headers,data=data) #yes :3

    if r.status_code == 200: # We did it! All done!
        return r # In case we need to extract other data

    elif r.status_code == 429: #Too many requests!
        if "Retry-After" in r.headers:
            time.sleep(int(r.headers['Retry-After']) + 0.5) #Extra half a second to ensure we don't hit against the wall
        else:
            if "Ratelimit-Reset" in r.headers:
                time.sleep(int(r.headers['Ratelimit-Reset']) + 0.5)
            else:
                time.sleep(31) #Well, we tried. Sleeping a full 31 seconds as a last resort.

        # We have now slept - give it a second go.

        if not data:
            r = requests.get(url,headers=headers)
        else:
            r = requests.post(url,headers=headers,data=data)

        if r.status_code == 200:
            return r

        else:
            raise requests.exceptions.RetryError("Request failed twice in a row! Please file a bug report.")

    else: #Some other bad evil status code we should never see
        raise requests.exceptions.RequestException("ERROR: Response code {}".format(r.status_code))

def download_file(url,headers=headers):
#    print(f"Downloading {url}")
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True, headers=headers) as r: # TODO: Ensure rate-limiting compliance? Should be fine though
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    
    return local_filename

def nsify(string):
    return string.lower().replace(" ","_")

def verify_nation(nation,code,headers=headers):
#    https://www.nationstates.net/cgi-bin/api.cgi?a=verify&nation=(Nation Name)&checksum=(code)
    r = perform_request(f"https://www.nationstates.net/cgi-bin/api.cgi?a=verify&nation={nation}&checksum={code}",headers=headers)
#    print(r.text)
    if "1" in str(r.text):
        return True
    else:
        return False
