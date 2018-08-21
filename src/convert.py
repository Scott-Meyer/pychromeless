from webdriver_wrapper import WebDriverWrapper
from urllib.parse import urlparse

def ProcessUrl(url, width, height):
    currentOrientation = "landscape"
    if width >= 1000:
        currentOrientation = "portrait"
    
    width, height = DetermineSizeFromOrientation(currentOrientation)

    try:
        # Start up the web driver.
        driver = WebDriverWrapper(width, height)
        driver.get_url(url)
        # Allow the dashboards to load, to allow the web report sections done increment or decrement the counter
        self.sleep(3000)

        WebDriverWait()
        wait = WebDriverWait(driver, 32)

        isReady = False
        while not isReady:
            try:
                wait.Until(driver.execute_script('return window.webReportSectionsDone'))
            except WebDriverTimeoutException as e:
                # Catch timeout exceptions here as this means that at least one of the sections times out while loading.
                # If one section times out in a report, the entire report should not be generated.
                #cancellationToken.ThrowIfCancellationRequested();
            except InvalidOperationException as e:
                # Catch invalid operation exception if the page is not loaded yet but code need to access 'webReportSectionsDone'
                isReady = driver.execute_script('return window.webReportSectionsDone')
                #cancellationToken.ThrowIfCancellationRequested();

        # Get the page source
        outputCDontents = driver.page_source

        #TODO: driver.Navigate().GoToUrl(new Uri(url).GetLeftPart(UriPartial.Authority) + "/#/logout");
        #Initiate a logout request so the next time we use this instance, we don't reuse the session
        parsed_uri = urlparse(url)
        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        driver.get_url(result + '#/logout')

        return outputCDontents
    finally:
        #TODO: This

def DetermineSizeFromOrientation(orientation, strWidth, strHeight):
    # These numbers were based off the sizes set in the css theme files.
    # Some may be slightly tweaked for the web.
    # The first set is landscape orientation, second is portrait.
    # For the portrait theme labels to display correctly in PDF report,
    # and in order to render the chart in a proper size for portrait theme,
    # the minimum width should be 1428 for both one-column and two-column report layout.
    # CHANING THIS WILL AFFECT THE WEB PDF REPORT CHART SIZE GREATLY.
    # SO PLEASE DO NOT CHANGE THIS UNLESS YOU HAVE A GOOD REASON.
    if orientation == "landscape":
        return "1932", "1428"
    else:
        return "1428", "1932"