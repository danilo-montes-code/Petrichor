# Petrichor

Petrichor is a mutlipurpose Discord Bot for my server with my friends.

## Functions
* send messages from archive server to friend server channel (useful for game clips)
* occassionally send responses to messages with embeds (and embed fails)
* crazy? i was crazy once.
* changes pinging channel to a random friend everyday at midnight
* reassigns Grok role to a random friend everyday at midnight

## Slash Commands
* `/help` - shows available commands and functions
* `/pingus` - get the latency of the bot
* `/dailies` - get links to daily activities
* `/who-has` - fetch the server Members that have the given role
* `/rtp` - "roll the ping", chooses a random active member and pings them
    * `/ping-counts perpetrator` - show a ranking of `/rtp` command runners
    * `/ping-counts victim` - show a ranking of `/rtp` command receivers
* `/last-clip` - get your most recently posted game clip
    * `game` - **(optional)** the game to search for, doesn't check for game by default (only works on clips sent as links)
    * `limit` - **(optional)** the maximum number of messages to search through, 100 by default
    * `skip` - **(optional)** the number of successfully found clips to skip over, 0 by default
* `/euoh` commands - add and fetch a person's euoh counts
    * `euoh` types: `vc`, `apex`
    * `/euoh <euoh_type> add` - add a Meuohment of a given type to a person
    * `/euoh <euoh_type> get` - get a person's Meuohment counts of a given type
    * `/euoh <euoh_type> info` - view the euoh types and their definition within a given type
* `/kaeley` commands
    * `/kaeley days-since-last-side-eye` - gets the number of days since Kaeley last sent a side eye emoji, sticker, or reaction
    * `/kaeley longest-side-eye-drought` - gets the longest number of days where Kaeley went without sending a side eye
    * `/kaeley total-side-eye-count` - gets the number of times Kaeley reacted with a side eye (since the counting started)

## Useful Documentation / References
* https://docs.replit.com/tutorials/python/build-basic-discord-bot-python
* https://dev.to/mannu/4slash-commands-in-discordpy-ofl 
* https://discordpy.readthedocs.io/en/stable/index.html