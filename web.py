import os
from aiohttp import web

# Retrieve your bot's username from environment variables.
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")

async def index(request):
    start_param = request.rel_url.query.get("start")
    if start_param:
        # Build the Telegram deep link.
        deep_link = f"tg://resolve?domain={BOT_USERNAME}&start={start_param}"
        
        # Build an HTML page that redirects to Telegram and then tries to close itself.
        html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Launching Telegram...</title>
    <meta http-equiv="refresh" content="2; url={deep_link}">
    <script type="text/javascript">
      function redirectAndClose() {{
          // Redirect to Telegram.
          window.location.href = "{deep_link}";
          // After a short delay, try to close the window.
          setTimeout(function() {{
              // This trick attempts to close the current window.
              window.open('', '_self', '');
              window.close();
          }}, 1500);
      }}
      window.onload = redirectAndClose;
    </script>
  </head>
  <body>
    <p>Redirecting to Telegramâ€¦ If nothing happens, <a href="{deep_link}">click here</a> to open Telegram.</p>
    <p>If the window does not close automatically, please close it manually.</p>
  </body>
</html>"""
        return web.Response(text=html_content, content_type="text/html")
    else:
        return web.Response(text="Welcome to Codeflix FileStore")

app = web.Application()
app.router.add_get("/", index)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
