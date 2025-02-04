import os
from aiohttp import web

# Retrieve your bot's username using your existing environment variable.
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")
if BOT_USERNAME == "default_bot_username":
    print("WARNING: BOT_USERNAME is not set correctly in your environment!")

async def favicon_handler(request):
    # Return a 204 No Content response for favicon requests.
    return web.Response(status=204)

async def index(request):
    # Debug logging: print out the full URL, path, and query parameters.
    full_url = str(request.url)
    path = request.path
    query_params = dict(request.query)
    print("DEBUG: Full URL:", full_url)
    print("DEBUG: Path:", path)
    print("DEBUG: Query Params:", query_params)
    
    # Check if the "start" query parameter is present.
    start_param = request.query.get("start")
    if start_param:
        # Build the Telegram deep-link using your BOT_USERNAME.
        deep_link = f"tg://resolve?domain={BOT_USERNAME}&start={start_param}"
        print("DEBUG: Generated deep-link:", deep_link)
        
        # Build an HTML page that attempts to redirect to Telegram.
        html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Launching Telegram...</title>
    <!-- Meta-refresh fallback (2-second delay) -->
    <meta http-equiv="refresh" content="2; url={deep_link}">
    <script type="text/javascript">
      function redirectToTelegram() {{
          window.location.href = "{deep_link}";
          window.location.replace("{deep_link}");
      }}
      window.onload = function() {{
          setTimeout(redirectToTelegram, 500);
      }};
    </script>
    <style>
      body {{
         font-family: Arial, sans-serif;
         text-align: center;
         padding-top: 50px;
      }}
    </style>
  </head>
  <body>
    <p>Attempting to open Telegram...</p>
    <p>If nothing happens, please <a href="{deep_link}">click here</a>.</p>
    <p>(If the page does not close automatically, please close it manually.)</p>
  </body>
</html>"""
        return web.Response(text=html_content, content_type="text/html")
    else:
        # If no "start" parameter is provided, return a default message.
        return web.Response(
            text="No 'start' parameter provided. Thi page is for Telegram deep-link redirection.",
            content_type="text/plain"
        )

# Create the aiohttp application and register routes.
app = web.Application()
# Register the favicon route to avoid 404 errors.
app.router.add_get("/favicon.ico", favicon_handler)
# Explicitly register the root route.
app.router.add_get("/", index)
# Also register a catch-all route to handle cases where the trailing slash might be omitted.
app.router.add_get("/{tail:.*}", index)

if __name__ == "__main__":
    # Railway provides the PORT environment variable.
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
