"""
main class should be called to have the service up and running

"""

import uvicorn
from fastapi import FastAPI, Request
from starlette.config import Config

from src import *
from src.service import Service
from src.utils.logger_utils import Logger

LOGGER = Logger.get_instance()

app = FastAPI()
config = Config("configs/props.env")


@app.get('/')
async def check_status():
    """
    To check if the service is up and running
    :return:
    """
    LOGGER.logger.info("Checking if service is up and running")
    return {"status": 200, "message": "Service is up and running"}


@app.get('/props')
async def check_props():
    """
    To check service properties and connection info
    :return:
    """
    try:
        LOGGER.logger.info("Accessing service properties")
        return {"status": 200, "props": config.file_values}
    except (TypeError, ValueError, IOError) as ex:
        LOGGER.log_err.exception("Error while retrieving props: " + str(ex))
        return {"status": 400, "message": str(ex)}


@app.post("/matchscore")
async def matchscore(inp: Request):
    """
    matching mentor and mentee and returning results
    :param inp:
    :return:
    """
    try:
        req = await inp.json()
        for col in [MENTEE_HT, MENTEE_EXP, MENTOR_HT, MENTOR_EXP, MENTOR_MAJOR]:
            if col in req and type(req[col]) != list:
                return {"status": 200, "message": "wrong input data format", "match": 0}
        if (len(req[MENTEE_HT]) == 0 and len(req[MENTEE_EXP]) == 0) or (len(req[MENTOR_HT]) == 0 and len(req[MENTOR_EXP]) == 0 and len(req[MENTOR_MAJOR]) == 0):
            return {"status": 200, "message": "insufficient data", "match": 0}
        return {"status": 200, "match_score": int(Service.match_data(req))}
    except Exception as e:
        LOGGER.log_err.exception("Error while accesing match score endopint: " + str(e))
        return {"status": 400, "message": "Error " + str(e)}


if __name__ == '__main__':
    uvicorn.run("main:app", host=config("HOST", str, default="0.0.0.0"),
                port=config.get("PORT", int, default=8000),
                workers=config.get("WORKERS", int, default=2))
