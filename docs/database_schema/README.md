# ERD for Petrichor Database
![ERD for Petrichor database](PetrichorERD.png)

# Database Schema

## `users` Table
Used to hold data relating to the users of the bot.

```sql
CREATE TABLE IF NOT EXISTS users(
    user_id VARCHAR(20) PRIMARY KEY,
    username TEXT
);
```


## `roll_the_pings` Table
Used to hold the results of all instances of `/rtp` used.

```sql
CREATE TABLE IF NOT EXISTS roll_the_pings(
    message_id VARCHAR(20) PRIMARY KEY,
    pinger_id VARCHAR(20) REFERENCES users(user_id),
    pingee_id VARCHAR(20) REFERENCES users(user_id),
    guild_id VARCHAR(20),
    ping_time TIMESTAMPTZ
);
```


## `euoh` Tables
Used to hold the results of all instances of `/euoh <type>` used.

```sql
CREATE TABLE IF NOT EXISTS vc_euohs(
    vc_euoh_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    recipient_id VARCHAR(20) REFERENCES users(user_id),
    euoh_type TEXT,
    reporter_id VARCHAR(20) REFERENCES users(user_id),
    guild_id VARCHAR(20),
    ping_time TIMESTAMPTZ
);
```

## `val_side_eyes` Table
Used to hold the occurrences of valentine reacting with or messaging a side eye emoji.

```sql
CREATE TABLE IF NOT EXISTS kaeley_side_eyes(
    side_eye_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    guild_id VARCHAR(20),
    channel_id VARCHAR(20),
    message_id VARCHAR(20),
    emoji_id VARCHAR(20),
    media_type BOOLEAN,
    message_type BOOLEAN,
    message_time TIMESTAMPTZ
);
```
`media_type` : `boolean`
- true for Emoji
- false for Sticker

`message_type` : `boolean`
- true for TextMessage
- false for Reaction