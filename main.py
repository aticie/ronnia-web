import os

import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.api:create_api", host=os.getenv("PUBLISH_HOST"), port=int(os.getenv('PUBLISH_PORT')), reload=True,
                reload_dirs=['./backend', './frontend/src'], factory=True)
