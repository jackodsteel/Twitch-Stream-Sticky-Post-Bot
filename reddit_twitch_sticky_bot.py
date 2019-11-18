#!/usr/bin/python3

from configparser import ConfigParser
import praw
import requests
import os
import time

USER_AGENT = "script:git i:v0.1:written by /u/iPlain"
CONFIG_FILE_NAME = "config.ini"
TWITCH_STREAMER_INFO_URL = "https://api.twitch.tv/helix/streams"
DELAY_BETWEEN_POLL_SECONDS = 30


def get_twitch_status(streamer_name, client_id):
    response = requests.get(TWITCH_STREAMER_INFO_URL,
                            headers={"Client-ID": client_id},
                            params={"user_login": streamer_name}
                            )
    if response.status_code != 200:
        raise RuntimeError(f"Got status code: {response.status_code} instead of expected 200")

    data = response.json()["data"]
    if len(data) != 1:
        return None
    return data[0]


def read_current_sticky_file(file_name):
    """
    Get the current sticky post ID if one exists else None
    :param file_name:
    :return: A string representing the Reddit ID of the current sticky post if one exists else None
    """
    try:
        with open(file_name, "r") as reader:
            return reader.readline().strip()
    except IOError:
        return None


def write_current_sticky_to_file(sticky_id: str, file_name: str):
    with open(file_name, "w") as writer:
        return writer.write(sticky_id)


def remove_current_sticky_file(file_name: str):
    os.remove(file_name)


def load_config(file_name):
    config = ConfigParser()
    with open(file_name) as f:
        config.read_file(f)
        return config


def login(config):
    return praw.Reddit(
        username=config.get("Settings", "username"),
        password=config.get("Settings", "password"),
        client_id=config.get("Settings", "client_id"),
        client_secret=config.get("Settings", "client_secret"),
        user_agent=USER_AGENT)


def post_sticky(title: str, url: str, subreddit: praw.reddit.models.Subreddit) -> str:
    submission: praw.reddit.models.Submission = subreddit.submit(
        title=title,
        url=url
    )
    submission.mod.sticky()
    return submission.id


def remove_sticky(sticky_id: str, reddit: praw.Reddit):
    reddit.submission(id=sticky_id).delete()


def main():
    print("Starting up")
    config = load_config(CONFIG_FILE_NAME)

    sticky_filename = config.get("Settings", "filename")
    streamer = config.get("Settings", "streamer")
    title = config.get("Settings", "title")

    twitch_client_id = config.get("Settings", "twitch_client_id")

    reddit = login(config)
    current_sticky_id = read_current_sticky_file(sticky_filename)
    subreddit = reddit.subreddit(config.get("Settings", "subreddit"))
    print("Logged in")

    while True:
        try:
            current_status = get_twitch_status(streamer, twitch_client_id)
            is_live = current_status is not None
            print(f"Currently live: {is_live}")
            if is_live and current_sticky_id is None:
                print("Just went live, posting sticky!")
                current_sticky_id = post_sticky(title=title, url=f"https://twitch.tv/{streamer}", subreddit=subreddit)
                write_current_sticky_to_file(current_sticky_id, sticky_filename)
                print(f"Current sticky post ID is: {current_sticky_id}")
            elif not is_live and current_sticky_id is not None:
                print("Went offline, removing sticky!")
                remove_sticky(current_sticky_id, reddit)
                remove_current_sticky_file(sticky_filename)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Error!")
            print(e)

        time.sleep(DELAY_BETWEEN_POLL_SECONDS)


if __name__ == "__main__":
    main()
