# Scratch API Test

This is the technical test for Scratchpay. Please do this on a public git repo of your choice and share it with your Scratchpay hiring contact.

The technical test will test your skills in accordance with what Scratchpay is looking for, so please treat it accordingly.

## Step 1: API

This section is to verify your competency in writing code.

You will find a [swagger spec](./swagger.yaml) defining an API that you must create. It is a simple user system with a single endpoint. Please use the specification and write an API in the language of your choosing. Keep in mind that you will need to store the user information.

## Step 2: Local Setup

This step is to verify your competency in development workflow.

Create a local environment that can be used to verify the code. Please keep in mind that a large number of projects are done with various setups (Unix- and Windows-based), so on any local setup please take into consideration this limitation (i.e. make sure it works across platforms). There is a [CSV](./data.csv) containing data that should be able to be loaded in order to test your setup; please think of a creative way to make loading the data easier.

## Step 3: Containerization and Orchestration

This step is to test your understanding of containerization, automation and orchestration.

Please containerize your application and create the required manifests/configuration to deploy your application to a Kubernetes cluster. Please use best practices when setting this up (treat it as if it were going into production). Part of the process should include the automation of loading the data into the storage that you have chosen.

_NB:_ Scratchpay is a Fintech company, so while we believe in innovation, this should not be at the cost of compromising on security.
