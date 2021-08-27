import os

import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.api:create_api", host="0.0.0.0", port=int(os.getenv('PUBLISH_PORT')), reload=True,
                reload_dirs=['./backend', './frontend/src'], factory=True)
