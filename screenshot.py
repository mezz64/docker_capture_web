"""
Thanks
======
https://github.com/mrcoles/full-page-screen-capture-chrome-extension/blob/master/page.js
"""

import os
import sys
import time
from collections import namedtuple
from io import BytesIO
from logging import getLogger, basicConfig, DEBUG, INFO, CRITICAL

from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver

ClientInfo = namedtuple("ClientInfo", "full_width full_height window_width window_height")
logger = getLogger(__name__)


def main():
    """Main function."""
    url = sys.argv[1]
    filename = sys.argv[2]
    window_size = sys.argv[3]
    user_agent = sys.argv[4]
    wait_time = int(sys.argv[5])
    refresh_delay = int(sys.argv[6])
    log_level = sys.argv[7]

    window_size = [int(x) for x in window_size.split("x")]

    basicConfig(level=log_level, format='%(asctime)s@%(name)s %(levelname)s # %(message)s')

    while True:
        try:
            capture_simple_screenshot(url, filename, window_size=window_size, wait=wait_time)
        except:
            continue

        time.sleep(refresh_delay)

    # capture_full_screenshot(url, filename, window_size=window_size, user_agent=user_agent,
    #                         wait=wait_time)


def capture_simple_screenshot(url, filename, window_size=None, wait=None):
    """Capture simple screen shot using built-in function """
    options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument("--test-type")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(chrome_options=options)

    if window_size:
        driver.set_window_size(window_size[0], window_size[1])

    driver.get(url)
    time.sleep(wait or 0.2)
    driver.save_screenshot('temp.png')

    add_timestamp('temp.png', filename)

    client_info = get_client_info(driver)
    # ua = driver.execute_script("return navigator.userAgent")
    logger.info(client_info)

    driver.close()

def add_timestamp(input_file, output_file):
    """ Print timestamp on image. """
    fontSize = 5
    topLeftWidthDivider = 5 # increase to make the textbox shorter in width
    topLeftHeightDivider = 23 # increase to make the textbox shorter in height
    textPadding = 2

    timeInfo = time.strftime("%m/%d - %H:%M:%S")

    im = Image.open(input_file)
    #myfont = ImageFont.truetype(fontFile, fontSize)
    myfont = ImageFont.load_default()
    topLeftWidth = int(im.size[0] - (im.size[0] / topLeftWidthDivider))
    topLeftHeight = int(im.size[1] - (im.size[1] / topLeftHeightDivider))
    draw = ImageDraw.Draw(im)
    draw.rectangle([topLeftWidth, topLeftHeight, im.size[0], im.size[1]], fill="black")
    draw.text([topLeftWidth + textPadding, topLeftHeight + textPadding], timeInfo, fill="white", font=myfont)
    del draw

    #write image
    im.save(output_file, 'PNG')


def capture_full_screenshot(url, filename, window_size=None, user_agent=None, wait=None):
    """

    :param url:
    :param filename:
    :param None|tuple window_size: browser window size. tuple of (width, height)
    :param None|str user_agent:
    :param None|float wait:
    :return:
    """
    options = webdriver.ChromeOptions()
    options.set_headless()
    options.add_argument('--no-sandbox')
    desired_capabilities = dict(acceptInsecureCerts=True)
    if user_agent:
        options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)

    if window_size:
        driver.set_window_size(window_size[0], window_size[1])

    driver.get(url)
    prepare_capture(driver)
    client_info = get_client_info(driver)

    ua = driver.execute_script("return navigator.userAgent")
    logger.info((client_info, ua))
    capture_screen_area(driver, filename, client_info, wait=wait)
    driver.close()


def capture_screen_area(driver: webdriver.Chrome, filename, client_info: ClientInfo, wait):
    for y_pos in range(0, client_info.full_height - client_info.window_height, 300):
        scroll_to(driver, 0, y_pos)
        time.sleep(wait or 0.2)

    client_info = get_client_info(driver)

    y_pos = client_info.full_height - client_info.window_height
    x_delta = client_info.window_width
    y_delta = client_info.window_height - 200

    canvas = Image.new('RGB', (client_info.full_width, client_info.full_height))
    while y_pos > -y_delta:
        x_pos = 0
        while x_pos < client_info.full_width:
            scroll_to(driver, x_pos, y_pos)
            sleep(wait or 0.2)
            cur_x, cur_y = get_current_pos(driver)
            logger.info(f"scrolling to {(x_pos, y_pos)}, current pos is {(cur_x, cur_y)}")
            img = Image.open(BytesIO(driver.get_screenshot_as_png()))  # type: Image.Image
            resized_image = img.resize((client_info.window_width, client_info.window_height))
            canvas.paste(resized_image, (cur_x, cur_y))
            img.close()
            resized_image.close()
            x_pos += x_delta
        y_pos -= y_delta
    canvas.save(filename)


def prepare_capture(driver):
    driver.execute_script('''
        document.body.style.overflowY = 'visible';
        document.documentElement.style.overflow = 'hidden';
    ''')


def get_client_info(driver):
    return ClientInfo(*driver.execute_script(FULL_SIZE_JS))


FULL_SIZE_JS = '''
function max(nums) {
    return Math.max.apply(Math, nums.filter(function(x) { return x; }));
}

return [
    max([
            document.documentElement.clientWidth,
            document.body ? document.body.scrollWidth : 0,
            document.documentElement.scrollWidth,
            document.body ? document.body.offsetWidth : 0,
            document.documentElement.offsetWidth
    ]),
    max([
            document.documentElement.clientHeight,
            document.body ? document.body.scrollHeight : 0,
            document.documentElement.scrollHeight,
            document.body ? document.body.offsetHeight : 0,
            document.documentElement.offsetHeight
    ]),
    window.innerWidth,
    window.innerHeight
    ];
'''


def scroll_to(driver, x, y):
    driver.execute_script('window.scrollTo.apply(null, arguments)', x, y)


def get_current_pos(driver):
    return driver.execute_script('return [window.scrollX, window.scrollY]')


if __name__ == '__main__':
    main()
