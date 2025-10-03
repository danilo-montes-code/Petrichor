# Petrichor

Petrichor is a mutlipurpose Discord Bot for my server with my friends.

## Functions
* send messages from archive server to friend server channel (useful for game clips)
* occassionally send responses to messages with embeds (and embed fails)
* crazy? i was crazy once.
* changes pinging channel to a random friend everyday at midnight

## Slash Commands
* `/rtp` - "roll the ping", chooses a random active member and pings them
    * `/ping-counts perpetrator` - show a ranking of `/rtp` command runners
    * `/ping-counts victim` - show a ranking of `/rtp` command receivers
* `/last-clip` - get your most recently posted game clip
    * `game` - **(optional)** the game to search for, doesn't check for game by default (only works on clips sent as links)
    * `limit` - **(optional)** the maximum number of messages to search through, 100 by default
    * `skip` - **(optional)** the number of successfully found clips to skip over, 0 by default
* `/euoh` commands - add and fetch a person's euoh counts
    * `/euoh vc add` - add a VC Meuohment of a given type to a person
    * `/euoh vc get` - get a person's VC Meuohment counts
* `/pingus` - get the latency of the bot

## Useful Documentation / References
* https://docs.replit.com/tutorials/python/build-basic-discord-bot-python
* https://dev.to/mannu/4slash-commands-in-discordpy-ofl 
* https://discordpy.readthedocs.io/en/stable/index.html