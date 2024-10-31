import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import employee, users
from restapi.db import MongoDB


app = FastAPI()
db = MongoDB.get_db()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


app.include_router(users.router)
app.include_router(employee.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8050)