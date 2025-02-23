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
                bat """
                    python -m venv %VENV_NAME%
                    call %VENV_NAME%\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install numpy==1.24.3
                    pip install scipy==1.10.1
                    pip install scikit-learn==1.0.2
                    pip install -r requirements.txt
                """
            }
        }
        
        stage('Run Tests') {
            steps {
                bat """
                    call %VENV_NAME%\\Scripts\\activate.bat
                    pytest tests/
                """
            }
        }
        
        stage('Deploy API') {
            steps {
                bat """
                    call %VENV_NAME%\\Scripts\\activate.bat
                    start /B uvicorn app:app --host 0.0.0.0 --port 8000
                """
            }
        }
        
        stage('Deploy Web Interface') {
            steps {
                bat """
                    call %VENV_NAME%\\Scripts\\activate.bat
                    start /B python web_app.py
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
