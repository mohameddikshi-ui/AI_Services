from fastapi import Request

from fastapi.responses import JSONResponse

import traceback

import logging


# ==========================================
# LOGGER CONFIG
# ==========================================

logging.basicConfig(

    level=logging.ERROR,

    filename="app.log",

    format="""
    %(asctime)s |
    %(levelname)s |
    %(message)s
    """
)

logger = logging.getLogger(__name__)


# ==========================================
# GLOBAL EXCEPTION HANDLER
# ==========================================

async def global_exception_handler(

    request: Request,

    exc: Exception
):

    # ==========================================
    # LOG ERROR
    # ==========================================

    logger.error(

        traceback.format_exc()
    )

    # ==========================================
    # STANDARD ERROR RESPONSE
    # ==========================================

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "message":
            "Something went wrong while processing the AI request.",

            "error_code": "AI_500"
        }
    )