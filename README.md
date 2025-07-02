# CI/CD pipeline to push your newly created small script to the production

1. Pipeline starts automatically on git push to the main branch. Performing initial validations including syntax checks, linters, code scanners.
2. Runing unit tests.
3. Building the docker image, performing the security scan, running various tests (integration tests, functional tests, security tests)
4. Uploading image to the registry
5. Manual code review
6. Deploying the applicaion in the kubernetes cluster, verifying and updating it's configuration if necessary

If any of the the steps or checks fail, stop the pipeline and inform developers about the problem.
