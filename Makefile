.PHONY: help init clean validate mock create delete info deploy
.DEFAULT_GOAL := help
environment = "example"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

create: ## create env
	@sceptre launch-env $(environment)

delete: ## delete env
	@sceptre delete-env $(environment)

info: ## describe resources
	@sceptre describe-stack-outputs $(environment) elasticsearch

lambda-build-zip: ## build the lambda
	docker build -t my-lambda .

lambda-dist: lambda-build-zip ## create a new lambda.zip in 'dist' directory
	mkdir -p dist
	./copy_from_docker.sh

#lambda-upload-zip: lambda-dist ## upload lambda.zip to environment needs ENVIRONMENT=st
#	./upload_s3.sh

#deploy-lambda: lambda-upload-zip ## deploy the lambda
