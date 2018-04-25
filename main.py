"""
Spotify Demo Application

Logs into the spotify web api using the Spotipy library

See the Spotipy docs here: https://spotipy.readthedocs.io/en/latest/
These docs also provide more examples of sample bots, and what you can do
using this library and the spotify web api.

Installation:

python3 -m pip install -r requirements.txt

Usage:

python3 main.py spotifyUserNameGoesHere

"""

import sys
import time
import pprint

# install from requirements.txt
# using pip install -r requirements.txt
import spotipy
import spotipy.util

if __name__ == '__main__':
    # check the amount of arguments given
    if len(sys.argv) > 1:
        # if valid, use the first argument as the username
        username = sys.argv[1]
    else:
        # print an error message when the input is invalid
        print("Usage: %s username " % (sys.argv[0],))
        sys.exit()


    # Scopes are the different permissions that your application
    # has granted to it by the users of the application
    # Read more about scopes here: https://beta.developer.spotify.com/documentation/general/guides/scopes/

    # for example, to only use the 'user-library-read' scope, you would do
    # scopes = 'user-library-read'

    # to use multiple scopes, you will need a comma separated list of scopes like this
    # scopes = 'user-library-read, user-top-read'

    # users may be hesitant to allow any application access to their personal data
    # so only include the scopes that you actually use

    # need permission to get currently playing track
    scopes = 'user-read-currently-playing'

    # These environment variables either need to be set, or passed as parameters to the
    # prompt_for_user_token method.

    # SPOTIPY_CLIENT_ID
    # SPOTIPY_CLIENT_SECRET

    # Normally, when you integrate your application with Spotify (think how Discord does it), the user
    # will be taken to the spotify website, prompted if they want to enable the application, then
    # redirected to a confirmation page.
    # Because we aren't actually hosting a web server, or a full application, we are not going to have
    # this redirect at all. Instead, set the redirect url to localhost. The prompt in the console
    # is going to ask you to copy the contents of the address bar in the console anyways.

    user_token = spotipy.util.prompt_for_user_token(username, scopes, redirect_uri='http://localhost/')

    # log into the spotify web api now
    sp = spotipy.Spotify(auth=user_token)

    # Debug flags to set
    # sp.trace = True
    # sp.trace_out = True

    # loop forever
    while True:
        # use the web api to get information about the current user's playback
        current_playback = sp.current_playback()

        # display this information in the console
        pprint.pprint(current_playback)

        # wait for 5 seconds

        # many APIs, Spotify included, implement a concept called 'rate limits'
        # if you poll the same API too quickly, they may throttle your connection to the service
        # to prevent spamming the server with too much traffic
        time.sleep(5)