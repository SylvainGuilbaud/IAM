This is a readme file for InterSystems API Manager (IAM) version 3.4.3.11.
Everything you need can be found inside this tarball.

### Prerequisites
In order to run IAM make sure you fulfill the following prerequisites:

*) The Docker engine version 17.04.0+ is available.
*) The docker-compose cli tool 1.12.0+ is installed (https://docs.docker.com/compose/)
*) InterSystems IRIS 2019.2+ is installed and available.
*) In case you are upgrading to 3.4.3.11 from an older version, make sure to backup your database before you begin.

### Contents of this tarball

|iam_image.tar           The IAM docker image
|readme.txt              This readme file
|EULA.pdf                The EULA for IAM
|scripts                 Contains scripts for your convenience
|-docker-compose.yml     A docker-compose script in order to start and stop IAM
|-iam-setup.sh           A script to configure all required environment variables. Must be run before you start IAM.
|-iam-test.sh            A script running a basic test checking connectivity with your InterSystems IRIS instance.

### Step by step instructions
1) Load the IAM image

  1a) Execute the following command to load the IAM image:

    docker load -i iam_image.tar

2) Configure your InterSystems IRIS instance

  2a) Enable the /api/IAM web application
  2b) Enable the IAM user
  2c) Change the password for the IAM user

3) Configure your IAM container

  3a) Navigate to the /scripts directory
  3b) Run the iam-setup script. This script will ask you some questions and set up required environment variables. CAUTION: You have to source the script, otherwise the script can't make the required changes to the environment variables. Execute one of the following commands:

    . ./iam-setup.sh
    source ./iam-setup.sh

4) In case you are upgrading to 3.4.3.11 from an older version and your database is postgres:9.6, you will have to 
    follow the steps mentioned in the /scripts/iam-upgrade-db/README.md file. If your old database is postgres:14.5,
    you should skip this step

5) Start your IAM container

  5a) Navigate to the /scripts directory
  5b) Execute the following command to start IAM:

    docker compose up -d

6) Access your IAM user interface

  6a) You can access the user interface with the following link: http://localhost:8002

7) Test your IAM container

  7a) Navigate to the /scripts directory
  7b) Run the iam-test script. This script sets up a route and a service in IAM and allows you to check connectivity with your InterSystems IRIS instance. If you are running on Ubuntu, make sure to source the script again, otherwise it can't pick up the required environment variables.

8) Stop your IAM container

  8a) Navigate to the /scripts directory
  8b) Execute the following command to stop IAM:

    docker compose down

### Further resources

If you would like to learn more about IAM:

Documentation can be found here: https://docs.intersystems.com/components/csp/docbook/DocBook.UI.Page.cls?KEY=PAGE_apimgr


Copyright © 2024 InterSystems Corporation, Cambridge, MA