from vercel_python_wsgi import serve
from app import app

def handler(event, context):
    return serve(app, event, context)
