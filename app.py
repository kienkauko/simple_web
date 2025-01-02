import logging
import json
import os
import requests
from sys import exc_info
from flask import Flask, render_template, request, redirect

# Setup logging mechanism
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Setup up a Flask instance
app = Flask(__name__)

# Obtain time from public api
def query_time():
    try:
        response = requests.get(
            url="http://worldtimeapi.org/api/timezone/america/new_york",
            timeout=5
        )

        if response.status_code == 200:
            time = (json.loads(response.text))['datetime']
            logger.info('Successfully queried public API')
            return time
        elif response.status_code != 200:
            logger.error(
                f"Error querying API.  Status code: {response.status_code}")
            return "Unavailable"
            
    except Exception:
        logger.error('Failed to contact public api', exc_info=True)
        return "Unavailable"

# Check internet access
def check_internet_access():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            logger.info("Internet access is available")
            return "Internet access is available"
        else:
            logger.warning("Internet access is unavailable")
            return "Internet access is unavailable"
    except Exception as e:
        logger.error("Failed to verify internet access", exc_info=True)
        return "Internet access is unavailable"

def get_ip(web_request):
    if 'X-Forwarded-For' in web_request.headers:
        xforwardfor = web_request.headers['X-Forwarded-For']
        return web_request.remote_addr + f" and X-Forwarded-For header value of {xforwardfor}"
    else:
        return web_request.remote_addr

# Render the template
@app.route("/")
def index():
    ipinfo = get_ip(web_request=request)
    todaystime = query_time()
    internet_status = check_internet_access()
    return render_template('index.html', time=todaystime, ip=ipinfo, internet_status=internet_status)

app.run(host="0.0.0.0", port=8080)
