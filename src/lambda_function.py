import time, json, traceback
import logging
from urllib.parse import urlparse
from webdriver_wrapper import WebDriverWrapper

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    # Log the input
    logger.info('got event{}'.format(event))

    url = event['url']
    width = int(event['width'])
    height = int(event['height'])
    page_source = ProcessUrl(url, width, height)

    return {
        'statusCode' : 200,
        'headers': {'CDontent-Type' : 'application/json' },
        'body' : json.dumps({'page_source': page_source})
    }
    

def ProcessUrl(url, width, height):
    currentOrientation = "landscape"
    if width >= 1000:
        currentOrientation = "portrait"
    
    width, height = DetermineSizeFromOrientation(currentOrientation)

    try:
        # Start up the web driver.
        driver = WebDriverWrapper(str(width), str(height))
        driver.get_url(url)
        # Allow the dashboards to load, to allow the web report sections done increment or decrement the counter
        time.sleep(3)
        isReady = False

        while not isReady:
            try:
                WebDriverWait(driver.get_driver(), 32).until(lambda d: d.execute_script('return window.webReportSectionsDone'))
                time.sleep(1)
                isReady = driver.execute_script('return window.webReportSectionsDone')
            except Exception as e:
                # Catch invalid operation exception if the page is not loaded yet but code need to access 'webReportSectionsDone'
                logger.info("ERROR: " + traceback.format_exc())
                time.sleep(1)
                isReady = False

        logger.info('Finished loading page, getting source.')
        # Get the page source
        outputCDontents = driver.page_source()

        #TODO: driver.Navigate().GoToUrl(new Uri(url).GetLeftPart(UriPartial.Authority) + "/#/logout");
        #Initiate a logout request so the next time we use this instance, we don't reuse the session
        parsed_uri = urlparse(url)
        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        driver.get_url(result + '#/logout')

        return outputCDontents
    finally:
        driver.close()
        #TODO: This

def DetermineSizeFromOrientation(orientation):
    # These numbers were based off the sizes set in the css theme files.
    # Some may be slightly tweaked for the web.
    # The first set is landscape orientation, second is portrait.
    # For the portrait theme labels to display correctly in PDF report,
    # and in order to render the chart in a proper size for portrait theme,
    # the minimum width should be 1428 for both one-column and two-column report layout.
    # CHANING THIS WILL AFFECT THE WEB PDF REPORT CHART SIZE GREATLY.
    # SO PLEASE DO NOT CHANGE THIS UNLESS YOU HAVE A GOOD REASON.
    if orientation == "landscape":
        return 1932, 1428
    else:
        return 1428, 1932