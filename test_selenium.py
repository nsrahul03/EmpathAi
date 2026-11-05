import os
import time
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    options = Options()

    # Headless Chrome configuration
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")
    options.add_argument("--window-size=1440,1000")

    browser = webdriver.Chrome(options=options)

    yield browser

    browser.quit()


def test_application_title(driver):
    driver.get("http://localhost:5002/")

    assert driver.title == "Empath AI"

    print("TEST 1 PASSED: Application title verified")


def test_main_heading(driver):
    driver.get("http://localhost:5002/")

    heading = driver.find_element(By.TAG_NAME, "h1")

    assert heading.text == "Empath AI"

    print("TEST 2 PASSED: Main heading verified")


def test_webcam_element(driver):
    driver.get("http://localhost:5002/")

    video = driver.find_element(By.ID, "video")

    assert video.is_displayed()

    print("TEST 3 PASSED: Webcam element verified")


def test_emotion_display(driver):
    driver.get("http://localhost:5002/")

    emotion = driver.find_element(By.ID, "emotion")

    assert emotion.is_displayed()

    print("TEST 4 PASSED: Emotion display verified")


def test_confidence_display(driver):
    driver.get("http://localhost:5002/")

    confidence = driver.find_element(By.ID, "confidence")

    assert confidence.is_displayed()

    print("TEST 5 PASSED: Confidence display verified")


def test_status_element(driver):
    driver.get("http://localhost:5002/")

    status = driver.find_element(By.ID, "status")

    assert status.is_displayed()

    print("TEST 6 PASSED: Status element verified")


def test_camera_initialization(driver):
    driver.get("http://localhost:5002/")

    wait = WebDriverWait(driver, 20)

    wait.until(
        lambda d: (
            "Camera connected" in d.find_element(By.ID, "status").text
            or "Unable to access camera" in d.find_element(By.ID, "status").text
        )
    )

    print("TEST 7 PASSED: Camera initialization checked")


def test_screenshot(driver):
    driver.get("http://localhost:5002/")

    time.sleep(3)

    os.makedirs("screenshots", exist_ok=True)

    screenshot_path = "screenshots/selenium-test.png"

    assert driver.save_screenshot(screenshot_path)

    assert os.path.exists(screenshot_path)

    print("TEST 8 PASSED: Screenshot captured")


def test_application_response(driver):
    driver.get("http://localhost:5002/")

    assert driver.current_url.startswith("http://localhost:5002")

    print("TEST 9 PASSED: Application response verified")