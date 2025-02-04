import os
from aiohttp import web

# Retrieve your bot's username from the environment.
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")
if BOT_USERNAME == "default_bot_username":
    print("WARNING: BOT_USERNAME is not set correctly in your environment!")

# Handler for favicon requests – returns 204 No Content to prevent 404 errors.
async def favicon_handler(request):
    return web.Response(status=204)

# Main handler for deep-link redirection.
async def index(request):
    # Debug: Log request details.
    full_url = str(request.url)
    path = request.path
    query_params = dict(request.query)
    print("DEBUG: Full URL:", full_url)
    print("DEBUG: Path:", path)
    print("DEBUG: Query Params:", query_params)
    
    # Check for the "start" query parameter.
    start_param = request.query.get("start")
    if start_param:
        # Build the Telegram deep‑link using your BOT_USERNAME.
        deep_link = f"tg://resolve?domain={BOT_USERNAME}&start={start_param}"
        print("DEBUG: Generated deep-link:", deep_link)
        
        # Build an HTML page that redirects to Telegram.
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
        # Fallback response if no "start" parameter is provided.
        return web.Response(
            text="No 'start' parameter provided. This page is for Telegram deep-link redirection.",
            content_type="text/plain"
        )

# Create the aiohttp application and register routes.
app = web.Application()
app.router.add_get("/favicon.ico", favicon_handler)
app.router.add_get("/", index)
app.router.add_get("/{tail:.*}", index)

if __name__ == "__main__":
    # Railway provides the PORT environment variable.
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
