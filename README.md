<div align="center">

# ronnia-web - An Interface for ronnia

</div>

**[ronnia](https://github.com/aticie/ronnia)** is a Twitch/osu! bot that sends beatmap requests from Twitch chat to the streamer's in-game messages.

ronnia-web displays the ronnia dashboard for user settings.

## Usage

You can check out ronnia dashboard at https://ronnia.me/

## Setup

To set-up frontend:

```shell
> npm install
> npm run build
```

Requirements for backend can be installed with:

`pip install fastapi uvicorn[standard] aiohttp`

Required environment variables for running:

```
OSU_CLIENT_SECRET=****
OSU_CLIENT_ID=2408
TWITCH_CLIENT_ID=****
TWITCH_CLIENT_SECRET=****
OSU_REDIRECT_URI=http://localhost:8000/identify
TWITCH_REDIRECT_URI=http://localhost:8000/twitch_identify
SECRET_KEY = "****"  # Secret key required for encoding JWT token
ALGORITHM = "HS256"  # Algorithm for encoding JWT token
DB_DIR=mount
```

### Docker 🐳

Just change the environment variables in the docker-compose template.

`docker-compose up -d`