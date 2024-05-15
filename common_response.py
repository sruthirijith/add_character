# common_response.py

from fastapi.responses import JSONResponse

def success_response(status_code: int, message: str, data: dict = None):
    response_data = {
        "status_code": status_code,
        "message": message,
        "data": data
    }
    return JSONResponse(status_code=status_code, content=response_data)

def error_response(status_code: int, message: str):
    response_data = {
        "status_code": status_code,
        "message": message
    }
    return JSONResponse(status_code=status_code, content=response_data)
