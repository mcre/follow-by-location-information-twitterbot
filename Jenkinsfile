pipeline {
    agent { docker 'mcre/geopandas' }
    stages {
        stage('setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('build') {
            steps {
                retry(10) { sh 'wget --no-check-certificate https://github.com/dataofjapan/land/raw/master/tokyo.geojson -P data' }
                retry(10) { sh 'python convert.py' }
                retry(10) { sh 'python main_meguro.py' }
            }
        }
    }
    post {
        success {
            send_mail('成功')
        }
        failure {
            send_mail('失敗')
        }
    }
}

def send_mail(result) {
    mail to: 'mc@mchs-u.net',
        subject: "${env.JOB_NAME} #${env.BUILD_NUMBER} ${result}",
        body: "Build URL: ${env.BUILD_URL}\n\n"
}