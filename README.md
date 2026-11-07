Empath AI – Facial Emotion Detection System

1. Project Overview

Empath AI is a facial emotion detection application that uses Artificial Intelligence and Deep Learning to identify human emotions through facial expressions captured using a webcam.

The application detects seven different emotions and displays the predicted emotion through a web-based interface.

The project also implements DevOps practices using GitHub, Jenkins, Docker, Pytest, and Selenium to automate testing, building, and deployment.

2. Key Features

* Real-time face detection using a webcam.
* Facial emotion recognition using a trained deep learning model.
* Detection of seven emotions:
    * Angry
    * Disgust
    * Fear
    * Happy
    * Sad
    * Surprise
    * Neutral
* Web-based user interface using Flask.
* Confidence score display for emotion predictions.
* Docker-based application containerization.
* Automated testing using Pytest.
* UI testing using Selenium.
* Continuous Integration and Continuous Deployment using Jenkins.

3. Technologies Used

Category	Technologies
Programming Language	Python
Frontend	HTML, CSS, JavaScript
Backend	Flask
Machine Learning	TensorFlow, Keras
Image Processing	OpenCV, NumPy, Pillow
Version Control	Git, GitHub
Containerization	Docker
CI/CD	Jenkins
Unit Testing	Pytest
UI Testing	Selenium
Server	Gunicorn

4. Project Architecture

The project follows this workflow:

1. Webcam captures the user’s face.
2. The application processes the captured image.
3. The trained deep learning model predicts the facial emotion.
4. Flask handles the prediction request.
5. The predicted emotion and confidence are displayed on the web interface.

DevOps Workflow

GitHub → Jenkins → Automated Testing → Build Verification → Docker Build → Docker Deployment → Deployment Verification → Selenium UI Testing

5. Project Structure

EmpathAi-Jenkins/
│
├── web/
│   ├── app.py
│   └── templates/
│       └── index.html
│
├── tests/
│   └── test_app.py
│
├── test_selenium.py
├── Dockerfile
├── docker-requirements.txt
├── Jenkinsfile
├── fer2013_best_model.keras
└── README.md

6. Running the Application Using Docker

Prerequisites

* Python 3.11
* Docker Desktop
* Git

Step 1: Clone the Repository

git clone https://github.com/nsrahul03/EmpathAi.git
cd EmpathAi

Step 2: Build the Docker Image

docker build -t empath-ai:1.0 .

Step 3: Run the Docker Container

docker run -d --name empath-ai-container -p 5002:5000 empath-ai:1.0

Step 4: Access the Application

Open the following address in your browser:

http://localhost:5002/

Step 5: Check Running Containers

docker ps

Step 6: Stop the Container

docker stop empath-ai-container

7. Testing

The project uses automated testing to verify application functionality.

Unit Testing – Pytest

python3.11 -m pytest -v test_app.py

Selenium UI Testing

python3.11 -m pytest -v test_selenium.py

Selenium is used to verify important UI elements, including:

* Application page title.
* Application heading.
* Webcam video element.
* Emotion display element.
* Status element.
* Camera initialization.

8. CI/CD Pipeline Using Jenkins

Jenkins automates the application’s build, testing, and deployment process.

The Jenkins pipeline contains the following stages:

1. Checkout: Retrieves the latest source code from GitHub.
2. Install Dependencies: Installs the required testing dependencies.
3. Unit Testing: Executes automated tests using Pytest.
4. Build Verification: Checks Python application syntax.
5. Docker Build: Builds the Docker image.
6. Docker Deploy: Runs the application inside a Docker container.
7. Deployment Verification: Checks whether the deployed application is accessible.
8. Selenium UI Testing: Performs automated browser-based UI testing.

The Jenkins pipeline is defined in the Jenkinsfile.

9. Expected Output

After successful deployment:

* The Empath AI web application opens in the browser.
* The webcam interface is displayed.
* Facial expressions are processed by the trained model.
* The predicted emotion and confidence are displayed.

10. Project Objectives

* Develop an AI-based facial emotion recognition application.
* Integrate machine learning with a web application.
* Implement containerization using Docker.
* Automate testing and deployment using Jenkins.
* Perform application and UI testing.
* Understand practical DevOps and CI/CD workflows.

11. Future Enhancements

* Improve emotion recognition accuracy.
* Add user authentication.
* Store emotion analysis history.
* Deploy the application to a cloud platform.
* Add monitoring and logging.
* Implement automated security scanning.

12. Author

Project: Empath AI – Facial Emotion Detection System

GitHub Repository: https://github.com/nsrahul03/EmpathAi
