# SpotifyLogger

A test application using the [spotipy library][spotipy-lib] and the [Spotify Web API][spotify-web-api] 
that logs into the API for the supplied user, and prints out information about the song they are listening to
every 5 seconds.

## Installation

All of the software dependencies are contained in `requirements.txt`. Only python 3.5 or greater
is supported, so use that. You can check with `python3 --version`.

Install the prerequisites with:

```bash
python3 -m pip install -r requirements.txt 
```

## Registering a Spotify Application

After the software requirements have been installed, 
you'll need to [set up a Spotify Web API application][spotify-web-api-setup].

[The spotipy library documentation provides a more in-depth example and explanation of this.][spotipy-lib-docs-getting-started]

1. Navigate to the [Spotify Web API dashboard.][spotify-web-api-setup]
2. Click on the 'Create a Client ID' button. A window should appear.
   
   Give your application a name and a brief description. These are shown to a user when they allow your application
   access to your account.
   
   You'll probably want to specify "I don't know" under the "What are you building?" section. Spotify just wants
   to ensure that you are not breaking the terms of service and understand the terms of a non-commercial application.
   
   Agree to the terms of you non-commercial app. You will be redirected to the dashboard.
   
3. Set up your environment variables for the spotipy library.
   
   Note: The library can handle reading environment variables for you, but if you would rather manage these
   yourself, they can be passed as arguments into [prompt_for_user_token][spotipy-prompt-user-token].
   
   Spotipy will need access to your applications client ID and client secret. These can be found on your
   application dashboard. **It is very important that your client secret and user tokens are not exposed, these
   give applications authority to use the API on your behalf.**
   
   Export your environment variables:
   
   ```bash
   export SPOTIPY_CLIENT_ID='your client id should go here with single quotes'
   export SPOTIPY_CLIENT_SECRET='your secret should go here with single quotes'
   ```
   
   If you wish to preserve these settings between sessions you can add it to your `~/.bashrc`, however
   this may risk exposing them to other applications.

4. Set up your redirect URL in the Spotify Dashboard.

   For most other applications, you get redirected to spotify and back when connecting them to other services.
   That's great, but we aren't bothering with webhosting for this project. The spotipy library gives you a utility
   function that runs the automation process for you, but it tries to redirect for the webpage for your app.

   By making your redirect url `http://localhost/`, you can get set up locally without the need for a web server.
   
## Usage

You can run the application using the following command:

```bash
python3 main.py yourSpotifyUsername
```

### Example output

```
$ python3 main.py yourSpotifyUsername
Title: Main's Groan
By: No Mana
Title: Main's Groan
By: No Mana
Title: Mind Mischief
By: Tame Impala
Title: Mind Mischief
By: Tame Impala
```

#### First Time Usage Details

When running the application for the first time, you'll need to log in to the spotify web API and also authorize
the application to have access to your spotify account. [The spotify web API docs explain this better than I can.][spotify-web-auth-guide]

Normally, this goes to spotify and prompts the user to log-in and allow permissions for your application. After they 
hit OK, it will redirect back to the application with the user's login token. However, since we aren't hosting a web
application, this just redirects to localhost. Follow the prompts given by the library and paste the full URL you are
given into the console window. 

A new file will appear called `.cache-yourSpotifyUsername`. **Do not** check this into version control, and **do not** 
leak this file. This contains a user token that allows your application to interact with user data.

[spotipy-lib]: https://github.com/plamere/spotipy
[spotipy-lib-docs-getting-started]: http://spotipy.readthedocs.io/en/latest/#installation
[spotipy-prompt-user-token]: http://spotipy.readthedocs.io/en/latest/#spotipy.util.prompt_for_user_token
[spotify-web-api]: https://developer.spotify.com/web-api/
[spotify-web-api-setup]: https://beta.developer.spotify.com/dashboard/applications
[spotify-web-auth-guide]: https://beta.developer.spotify.com/documentation/general/guides/authorization-guide/
