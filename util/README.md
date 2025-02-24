# Database Schemas

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
    ping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pinger VARCHAR(20) REFERENCES users(user_id),
    pingee VARCHAR(20) REFERENCES users(user_id),
    guild_id VARCHAR(20),
    ping_time TIMESTAMP
);
```


