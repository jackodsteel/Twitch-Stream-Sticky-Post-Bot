Reddit Twitch Sticky Bot
=================

A Reddit bot which polls a Twitch.tv stream and creates/removes a sticky when they're online

Usage
-----

 0. Have Python (at least 3.6) installed, along with PRAW:
    `pip install praw`
 1. Register your bot with Twitch at https://dev.twitch.tv/console/apps, and take the Client ID for the config.
 2. Create a Reddit account for the bot, and make it a mod on the subreddit you want it to work on.
 3. Follow the OAuth setup steps at https://www.reddit.com/r/RequestABot/comments/cyll80/a_comprehensive_guide_to_running_your_reddit_bot/ to get your client_id and client_secret.
 4. Clone this repository, or download as a zip.
 5. Copy `config.example.ini` to `config.conf`.
 6. Open up `config.ini` and fill in the required fields.
 7. Run the bot as `python reddit_twitch_sticky_bot`.

