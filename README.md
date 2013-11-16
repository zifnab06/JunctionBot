JunctionBot
=========

Fork of [RedditBot](http://github.com/buttscicles/RedditBot) used on Junction's IRC network

### Running
    # Clone this repo and init all submodules 
    $ git clone git://github.com/zifnab06/JunctionBot.git --recursive  
    $ cd JunctionBot/

    # Install requirements using pip
    $ pip install -r requirements.txt

    # Create and edit a config file
    $ cp config.py.default JunctionBot/config.py
    $ $EDITOR JunctionBot/config.py

    # Run!
    $ python run.py
