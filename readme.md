# Spotify Dashboard
This app is designed to help you to explore the data given by Spotify API via Flask framework.

## Installation
After downloading th repository, you should create a file named `.credentialy.py` in the root directory of the project. This file should contain the following variables:
``` python
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
```

### How to get credentials?
1. Go to [Spotify for Developers](https://developer.spotify.com/dashboard/applications) and log in with your Spotify account.
2. Click on `CREATE AN APP` button.
3. Fill the form and click on `CREATE` button. While filling, you should remember the `Redirect URIs` field. It should be `http://127.0.0.1:5000/callback`
4. After creating the app, you will see your `Client ID` and `Client Secret`. Copy them and paste into `.credentialy.py` file as mentioned above.

## Usage
After handling the installation process, you can run the app by typing `python app.py` in the terminal. Then, you can go to `http://127.0.1:5000` in your browser and use the app.
In the index page, you fill find the following, and click `Authenticate`. <br>
![Index Page](images/index.jpg?raw=true)
At that point, you will be redirected to Spotify login page. After logging in, you will be redirected to the dashboard page. <br>
![Dashboard Page](images/dashboard.jpg?raw=true)
In the dashboard page, you can see your top artists and tracks based on your data of last 6 months. You can also see your recently played tracks. Therefore, you can see part of your wrapped data without waiting the end of the year :). <br>
## Future Work
- [ ] Add more features to the dashboard page as much as Spotify API data allows.