from app import app

# This is a special file for Vercel serverless deployment
# It's located in the api directory to match Vercel's expected path

# Handler for Vercel serverless function
def handler(request, context):
    return app(request, context)
