pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.8'
        VENV_NAME = 'venv'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                sh """
                    python3 -m venv ${VENV_NAME}
                    . ${VENV_NAME}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }
        
        stage('Run Tests') {
            steps {
                sh """
                    . ${VENV_NAME}/bin/activate
                    pytest tests/
                """
            }
        }
        
        stage('Deploy API') {
            steps {
                sh """
                    . ${VENV_NAME}/bin/activate
                    nohup uvicorn app:app --host 0.0.0.0 --port 8000 &
                """
            }
        }
        
        stage('Deploy Web Interface') {
            steps {
                sh """
                    . ${VENV_NAME}/bin/activate
                    nohup python web_app.py &
                """
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
