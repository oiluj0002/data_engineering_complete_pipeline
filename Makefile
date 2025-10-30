# Makefile helpers for unified docker-compose (LocalStack, tools, and ELT job)
# Usage examples:
#   make localstack                 # start LocalStack
#   make localstack-down            # stop all compose services
#   make localstack-logs            # tail LocalStack logs
#   make aws AWS_ARGS='s3 ls'       # run AWS CLI in tools container
#   make terraform                  # terraform init + apply (LocalStack)
#   make terraform-destroy          # terraform destroy
#   make tools-shell                # interactive shell inside tools container
#   make elt-run                    # run the ELT job container once

COMPOSE_FILE := docker-compose.yml
DC := docker compose -f $(COMPOSE_FILE)

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  localstack           - Start LocalStack service"
	@echo "  localstack-down      - Stop all services (compose down)"
	@echo "  localstack-logs      - Tail LocalStack logs"
	@echo "  aws                  - Run AWS CLI in tools container (use AWS_ARGS='...')"
	@echo "  terraform            - Terraform init + apply against LocalStack"
	@echo "  terraform-init       - Terraform init (-upgrade)"
	@echo "  terraform-plan       - Terraform plan"
	@echo "  terraform-apply      - Terraform apply (-auto-approve)"
	@echo "  terraform-destroy    - Terraform destroy (-auto-approve)"
	@echo "  tools-shell          - Interactive shell in tools container"
	@echo "  elt-run              - Run ELT job container once"

.PHONY: localstack
localstack:
	$(DC) up -d localstack

.PHONY: localstack-down
localstack-down:
	$(DC) down

.PHONY: localstack-logs
localstack-logs:
	$(DC) logs -f localstack

# Run AWS CLI; pass command via AWS_ARGS, e.g.: make aws AWS_ARGS='s3 ls'
.PHONY: aws
aws:
	@[ -n "$(AWS_ARGS)" ] || (echo "Usage: make aws AWS_ARGS='s3 ls'" && exit 2)
	$(DC) run --rm localstack-tools aws $$AWS_ARGS

# Terraform helpers (working dir is the mounted /terraform)
.PHONY: terraform
terraform: terraform-apply

.PHONY: terraform-init
terraform-init:
	$(DC) run --rm localstack-tools sh -lc "cd /terraform && terraform init -upgrade"

.PHONY: terraform-plan
terraform-plan:
	$(DC) run --rm localstack-tools sh -lc "cd /terraform && terraform plan"

.PHONY: terraform-apply
terraform-apply:
	$(DC) run --rm localstack-tools sh -lc "cd /terraform && terraform init -upgrade && terraform apply -auto-approve"

.PHONY: terraform-destroy
terraform-destroy:
	$(DC) run --rm localstack-tools sh -lc "cd /terraform && terraform destroy -auto-approve"

.PHONY: tools-shell
tools-shell:
	$(DC) run --rm -it localstack-tools bash

.PHONY: elt-run
elt-run:
	$(DC) run --rm elt-job
