import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

# Configure Chrome
options = Options()
options.add_argument("--headless=new")
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--use-fake-device-for-media-stream")
options.add_argument("--no-sandbox")

# Start browser
driver = webdriver.Chrome(options=options)

try:
    print("Starting Selenium testing...")

    # Open deployed application
    driver.get("http://localhost:5002/")

    wait = WebDriverWait(driver, 20)

    # Test 1: Page title
    assert driver.title == "Empath AI"
    print("TEST 1 PASSED: Page title verified")

    # Test 2: Main heading
    heading = driver.find_element(By.TAG_NAME, "h1")
    assert heading.text == "Empath AI"
    print("TEST 2 PASSED: Application heading verified")

    # Test 3: Webcam element
    video = driver.find_element(By.ID, "video")
    assert video is not None
    print("TEST 3 PASSED: Webcam element found")

    # Test 4: Emotion display
    emotion = driver.find_element(By.ID, "emotion")
    assert emotion is not None
    print("TEST 4 PASSED: Emotion display found")

    # Test 5: Status element
    status = driver.find_element(By.ID, "status")
    assert status is not None
    print("TEST 5 PASSED: Status element found")

    # Test 6: Camera initialization
    wait.until(
        lambda d: "Camera connected" in
        d.find_element(By.ID, "status").text
        or "Unable to access camera" in
        d.find_element(By.ID, "status").text
    )

    print("TEST 6: Camera initialization checked")

    # Capture screenshot
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot("screenshots/selenium-test.png")

    print("Screenshot saved successfully")
    print("ALL SELENIUM TESTS COMPLETED")

finally:
    driver.quit()
