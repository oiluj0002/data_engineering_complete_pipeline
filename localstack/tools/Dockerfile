FROM debian:bookworm-slim

# Pin tool versions for reproducibility
ENV TERRAFORM_VERSION=1.13.4
ENV AWSCLI_VERSION=2.27.41

# Keep AWS CLI from using a pager by default
ENV AWS_PAGER=""

# Base dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       ca-certificates \
       curl \
       unzip \
       jq \
       less \
       groff \
       bash \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI v2 (version pinned)
RUN curl -fsSLo awscliv2.zip "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-${AWSCLI_VERSION}.zip" \
    && unzip -q awscliv2.zip \
    && ./aws/install \
    && ln -sf /usr/local/aws-cli/v2/current/bin/aws /usr/local/bin/aws \
    && rm -rf aws awscliv2.zip

# Install Terraform by downloading the static binary release
RUN curl -fsSLo terraform.zip "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" \
    && unzip -q terraform.zip -d /usr/local/bin \
    && chmod +x /usr/local/bin/terraform \
    && rm -f terraform.zip

# Basic sanity checks
RUN aws --version && terraform -version

WORKDIR /terraform