PROJECT=aws-ml-api
REGION=us-east-1
ACCOUNT_ID := $(shell aws sts get-caller-identity --query Account --output text)
ECR_URI=$(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(PROJECT):latest

.PHONY: model
model:
	python3 -m venv .venv && . .venv/bin/activate && pip install --only-binary :all: -r app/requirements.txt && python train.py

.PHONY: ecr
ecr:
	aws ecr describe-repositories --repository-names $(PROJECT) --region $(REGION) >/dev/null 2>&1 || \
	aws ecr create-repository --repository-name $(PROJECT) --region $(REGION)

.PHONY: docker-login
docker-login:
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com

.PHONY: image
image:
	docker build --provenance=false -t $(PROJECT):latest .
	docker tag $(PROJECT):latest $(ECR_URI)

.PHONY: push
push: docker-login
	docker push $(ECR_URI)

.PHONY: tf-init
tf-init:
	cd terraform && terraform init

.PHONY: tf-apply
tf-apply:
	cd terraform && terraform apply -auto-approve -var="lambda_image_uri=$(ECR_URI)" -var="region=$(REGION)" -var="project_name=$(PROJECT)"

.PHONY: deploy
deploy: model ecr image push tf-init tf-apply
