// This file relates to internal XMOS infrastructure and should be ignored by external users

@Library('xmos_jenkins_shared_library@v0.38.0') _

getApproval()

def runningOn(machine) {
  println "Stage running on:"
  println machine
}

pipeline {
  agent {
    label 'x86_64 && linux'
  }
  options {
    buildDiscarder(xmosDiscardBuildSettings())
    skipDefaultCheckout()
    timestamps()
  }
  parameters {
    string(
      name: 'TOOLS_VERSION',
      defaultValue: '15.3.1',
      description: 'The XTC tools version'
    )
  }
  environment {
    REPO = "lib_uart"
    REPO_NAME = "lib_uart"
  }
  stages {
    stage("Checkout and build"){
      steps {
        runningOn(env.NODE_NAME)
        dir("${REPO}") {
          checkoutScmShallow()
          withTools(params.TOOLS_VERSION) {
            dir("examples") {
              xcoreBuild()
            }
          } // tools
        }
      }
    } // Checkout and build
  }
}
