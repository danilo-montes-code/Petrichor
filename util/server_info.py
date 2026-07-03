"""server_info.py

Holds namedtuples that hold server information.
"""

from typing import NamedTuple

from util.env_vars import get_id


class ServerInfo(NamedTuple):
    guild_flag: str
    guild_id: int
    repost_channel_id: int

kidnamedsoub = ServerInfo(
    guild_flag="kns",
    guild_id=get_id("KNS_ID"),
    repost_channel_id=get_id("KNS_POV_ID")
)

guard = ServerInfo(
    guild_flag="guard",
    guild_id=get_id("GUARD_ID"),
    repost_channel_id=get_id("GUARD_POV_ID")
)

SERVERS : dict[str, ServerInfo] = {
    "kns" : kidnamedsoub,
    "guard" : guard
}
