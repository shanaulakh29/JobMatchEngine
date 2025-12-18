from fastapi import Request


async def login_middleware(request: Request, call_next):
    if request.headers.get("content-type", "").startswith("application/x-www-form-urlencoded"):
        form = await request.form()
        request.state.form_data = dict(form)
    response = await call_next(request)
    return response