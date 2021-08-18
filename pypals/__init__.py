"""
    pypals
    ====================================

    pypals now has a cli interface. check __main__.py for usage

"""

__version__ = "1.0.2"

class DefaultCommands():
    """ default commands that come with first pypal """

    HELLO = """def run(o, *args, **kwargs):
    print(f"Hello, to you { o.o['friend']}!")
    return True
    """
    
    QUIT = """def run(o, *args, **kwargs):
    import sys
    sys.exit(0)
    """

    GOOGLE = """def run(o, *args, **kwargs):
    import webbrowser
    webbrowser.open( f"https://www.google.com/search?q={args[0]}" )
    return True
    """

    BING = """def run(o, *args, **kwargs):
    import webbrowser
    webbrowser.open( f"https://www.bing.com/search?q={args[0]}" )
    return True
    """
    
    UPDATE_TWITTER = """def run(o, *args, **kwargs):
    import os
    import subprocess
    import sys
    import time
    import tweepy
    from pypal import __version__
    from pypal.config import Config
    from pypal.twitter import *
    from pypal.twitter.auth import *
    
    config = Config()
    auth = tweepy.OAuthHandler(config.twitter.consumer_key, config.twitter.consumer_secret)
    auth.set_access_token(config.twitter.access_token, config.twitter.access_token_secret)
    api = tweepy.API(auth)

    if not os.path.exists("./pypal/twitter/tweets.txt"):
        with open("./pypal/twitter/tweets.txt", "w") as f:
            f.write("")
    
    with open("./pypal/twitter/tweets.txt", "r") as f:
        tweets = f.readlines()
    
    if args[0] in tweets:
        print(f"{args[0]} already tweeted")
        return True
    
    with open("./pypal/twitter/tweets.txt", "a") as f:
        f.write(f"{args[0]}\n")
    
    api.update_status(f"{args[0]}")
    print(f"Tweeted {args[0]}")
    return True
    """


    # copilot generated commands
    # ASSERT = """def run(o, *args, **kwargs):
    # if not args:
    #     print("You must provide a condition to assert")
    #     return False
    # if args[0] == "True":
    #     print("Assertion was true")
    #     return True
    # else:
    #     print("Assertion was false")
    #     return False
    # """
    
    # COMPLAINT = """def run(o, *args, **kwargs):
    # print(f"I'm sorry, {o.o['friend']}, I'm afraid I can't do that.")
    # return False
    # """
    
    # AFFIRMATIVE = """def run(o, *args, **kwargs):
    # print("affirmative")
    # return True
    # """

    # NEGATIVE = """def run(o, *args, **kwargs):
    # print("negative")
    # return False
    # """




class Utils():

    @staticmethod
    def y_n(x):
        """ returns a boolean for any given input """
        if isinstance(x, bool):
            return x
        elif isinstance(x, (int, float)):
            return bool(x)
        elif isinstance(x, str):
            reply = x.lower()
            if reply.lower() in ['yeah', "y", "yes", "yup", "si", "yep", "yeah", "yep", "sure", "ok", "go ahead", "certainly", "do", "1", "too right"]:
                return True
            elif reply.lower() in ['nah', "no", "nope", "n", "dont", "0", "nop", "naa", "naaa"]:
                return False

            if 'y' in x[0].lower():
                return True
            elif 'n' in x[0].lower():
                return False
        else:
            raise ValueError(f"{x} is not a valid input")
