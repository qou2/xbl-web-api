# xbl-web-api

![python3 badge](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6.svg)
![Quart](https://img.shields.io/badge/Quart-0.19+-purple.svg)
![Xbox Live API](https://img.shields.io/badge/Xbox%20Live-API%20v2-107C10.svg)
![Original](https://img.shields.io/badge/original-jcxldn-blue.svg)
![Fork Status](https://img.shields.io/badge/fork-maintained-success.svg)

All routes return JSON unless otherwise specified.

## Fixes in This Fork

Original by [jcxldn](https://github.com/jcxldn). This fork fixes the entire auth flow for Xbox auth v2, as well as fixing deprecated Python libraries that cause the original to fail.

### Authentication Flow Fixes (Xbox Auth v2)

#### SSL Certificate Issues (`main.py`)
- Added SSL verification bypass for Windows systems where certificate validation fails
- Implemented `aiohttp.TCPConnector(verify_ssl=False)` in ClientSession
- Added global SSL context override for compatibility with Xbox Live authentication endpoints
- These changes resolve `SSLError` and certificate verification failures that prevented authentication

#### Manual Authentication Script (`manual_auth.py`)
- Added new authentication script for initial token generation (although the command `xbox-authenticate` can still work sometimes)
- Allows users to complete OAuth flow and generate initial `tokens.json` file

### Deprecated Library Fixes

#### Quart 0.19+ Compatibility (`server.py`)
- Replaced deprecated `quart.flask_patch` with manual `nest_asyncio` implementation
- `quart.flask_patch` is no longer available in Quart 0.19+
- Manually implements `loop.sync_wait()` method required by QuartDecoratorProvider
- `nest_asyncio` provides better Windows event loop handling for nested async operations
- Fixed `index()` route to use async/await pattern consistently

#### Type Hint Modernization (`routes/__init__.py`)
- Corrected `register_batch` parameter type hint from `dict[Type]` to `List[Type]`
- Parameter actually accepts a list of route classes, not a dictionary

### Technical Details

The original implementation failed due to:
1. **SSL errors** when connecting to Xbox Live authentication servers on Windows
2. **Import errors** from `quart.flask_patch` being removed in newer Quart versions
3. **Missing initial authentication** - no way to generate the first `tokens.json` file (although again, `xbox-authenticate` can work in some cases)

This fork resolves all these issues while maintaining backward compatibility with the existing codebase.


## Routes

- `/titleinfo/<int:titleid>`

  Get title information by its title ID.

- `/legacysearch/<str:query>`

  Search the Xbox 360 Marketplace.

- `/gamertag/check/<str:username>`

  Check if the specified gamertag is available or taken.

- `/usercolors/define/<str:primary>/<str:secondary>/<str:tertiary>`

  Get an SVG representation of the defined colors.

- `/usercolors/get/xuid/<int:xuid>`

  Get an SVG representation of the user's colors.

- `/usercolors/get/gamertag/<gamertag>`

  Get an SVG representation of the user's colors.

### Profiles

- `/profile/xuid/<int:xuid>`

  Get a profile by the user's XUID.

- `/profile/gamertag<str:gamertag>`

  Get a profile by the user's gamertag.

- `/profile/settings/xuid/<int:xuid>`

  Get profile settings (less data) by the user's XUID.

- `/profile/settings/gamertag/<str:gamertag>`

  Get profile settings (less data) by the user's gamertag.

### Friends

- `/friends/summary/xuid/<int:xuid>`

  Get a user's friend summary (followers and following count) by their XUID.

- `/friends/summary/gamertag/<gamertag>`

  Get a user's friend summary (followers and following count) by their gamertag.

### Presence

- `/presence/xuid/<int:xuid>`

  Get a user's presence (status) by their XUID.

- `/presence/gamertag/<str:gamertag>`

  Get a user's presence (status) by their gamertag.

### User Stats

- `/userstats/xuid/<int:xuid>/titleid/<int:titleid>`

  Get a user's stats for a game by Title ID and user XUID.

- `/userstats/gamertag/<str:gamertag>/titleid/<int:titleid>`

  Get a user's stats for a game by Title ID and user gamertag.

### XUIDs

- `/xuid/<str:gamertag>`

  Get a user's XUID by their gamertag.

- `/xuid/<str:gamertag>/raw`

  Get a user's XUID by their gamertag and return as text.

### Achievements

- `/achievements/1/recent/<int:xuid>`

  Get the recent Xbox One achievements for a user XUID.

- `/achievements/360/recent/<int:xuid>`

  Get the recent Xbox 360 achievements for a user XUID.

- `/achievements/1/titleprogress/<int:xuid>/<int:titleid>`

  Get all achievements (both unlocked and locked) for an Xbox One user from their XUID and the game's Title ID.

- `/achievements/360/titleprogress/all/<int:xuid>/<int:titleid>`

  Get all available achievements for an Xbox 360 user from their XUID and the game's Title ID.

- `/achievements/360/titleprogress/earned/<int:xuid>/<int:titleid>`

  Get all earned / unlocked achievements for an Xbox 360 user from their XUID and the game's Title ID.

- `/achievements/1/titleprogress/detail/<int:xuid>/<uuid:scid>/<int:achievementid>`

  Get the achievement details for an Xbox One user from their XUID, the game's SCID (Service Config ID) and an achievement ID.
