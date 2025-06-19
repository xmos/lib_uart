// This file relates to internal XMOS infrastructure and should be ignored by external users

@Library('xmos_jenkins_shared_library@v0.39.0') _

getApproval()

def runningOn(machine) {
  println "Stage running on:"
  println machine
}

def clone_test_deps() {
  dir("${WORKSPACE}") {
    sh "git clone git@github.com:xmos/test_support"
    sh "git -C test_support checkout e62b73a1260069c188a7d8fb0d91e1ef80a3c4e1"
  }
}

pipeline {
  agent {
    label 'x86_64 && linux && documentation'
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
    string(
          name: 'XMOSDOC_VERSION',
          defaultValue: 'v7.1.0',
          description: 'The xmosdoc version'
    )
    string(
      name: 'INFR_APPS_VERSION',
      defaultValue: 'v2.1.0',
      description: 'The infr_apps version'
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
    stage("Docs"){
      steps {
        dir("${REPO}") {
          buildDocs()
        }
        warnError("lib checks") {
          runLibraryChecks("${WORKSPACE}/${REPO}", "${params.INFR_APPS_VERSION}")
        }
      }
    }// Docs
    stage("Tests"){
      steps{
        clone_test_deps()
        withTools(params.TOOLS_VERSION) {
          dir("${REPO}/tests") {
            createVenv(reqFile: "requirements.txt")
            withVenv{
              runPytest("--numprocesses=auto --dist=worksteal -v")
            }
          }
        } // tools
      }
    } // Tests
    stage("Archive sandbox"){
      steps {
        archiveSandbox(REPO)
      }
    } // Archive sandbox
  }
  post {
    cleanup {
      xcoreCleanSandbox()
    }
  }
}
