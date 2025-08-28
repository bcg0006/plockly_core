#!/bin/bash

# Environment Setup Script for Plockly v2
# This script helps set up environment variables for different environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to generate secure secret key
generate_secret_key() {
    python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
}

# Function to setup environment
setup_environment() {
    local env_name=$1
    local env_file=".env.${env_name}"

    print_status "Setting up ${env_name} environment..."

    if [ -f "$env_file" ]; then
        print_warning "Environment file $env_file already exists!"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Skipping $env_name environment setup."
            return
        fi
    fi

    # Copy example file
    cp "env.${env_name}.example" "$env_file"

    # Generate secret key if needed
    if grep -q "your-${env_name}-secret-key" "$env_file"; then
        local secret_key=$(generate_secret_key)
        sed -i.bak "s/your-${env_name}-secret-key-change-this-in-production/$secret_key/g" "$env_file"
        rm "${env_file}.bak"
        print_success "Generated secure SECRET_KEY for $env_name"
    fi

    print_success "Environment file $env_file created successfully!"
    print_warning "Please review and update the values in $env_file before deployment."
}

# Function to setup GitHub secrets
setup_github_secrets() {
    print_status "Setting up GitHub repository secrets..."
    echo
    echo "To complete the CI/CD setup, you need to add the following secrets to your GitHub repository:"
    echo
    echo "Go to: https://github.com/bcg0006/plockly_core/settings/secrets/actions"
    echo
    echo "Add these secrets:"
    echo
    echo "STAGING_SECRET_KEY: $(generate_secret_key)"
    echo "STAGING_DATABASE_URL: postgresql://staging_user:staging_password@staging-db:5432/plockly_staging"
    echo "STAGING_ALLOWED_HOSTS: staging.plockly.com,localhost,127.0.0.1"
    echo
    echo "PRODUCTION_SECRET_KEY: $(generate_secret_key)"
    echo "PRODUCTION_DATABASE_URL: postgresql://prod_user:prod_password@prod-db:5432/plockly_production"
    echo "PRODUCTION_ALLOWED_HOSTS: plockly.com,www.plockly.com,api.plockly.com"
    echo
    echo "Optional secrets:"
    echo "SENTRY_DSN: Your Sentry DSN for error tracking"
    echo "GOOGLE_ANALYTICS_ID: Your Google Analytics ID"
    echo "EMAIL_HOST_USER: Your email username"
    echo "EMAIL_HOST_PASSWORD: Your email app-specific password"
}

# Function to validate environment file
validate_env_file() {
    local env_file=$1
    local env_name=$2

    print_status "Validating $env_name environment file..."

    if [ ! -f "$env_file" ]; then
        print_error "Environment file $env_file not found!"
        return 1
    fi

    # Check for required variables
    local required_vars=("SECRET_KEY" "DATABASE_URL" "ALLOWED_HOSTS")
    local missing_vars=()

    for var in "${required_vars[@]}"; do
        if ! grep -q "^${var}=" "$env_file" || grep -q "^${var}=your-" "$env_file"; then
            missing_vars+=("$var")
        fi
    done

    if [ ${#missing_vars[@]} -eq 0 ]; then
        print_success "$env_name environment file is properly configured!"
    else
        print_warning "The following variables need to be updated in $env_file:"
        for var in "${missing_vars[@]}"; do
            echo "  - $var"
        done
    fi
}

# Main script
main() {
    echo "🚀 Plockly v2 Environment Setup Script"
    echo "======================================"
    echo

    # Check if we're in the right directory
    if [ ! -f "docker-compose.yml" ]; then
        print_error "Please run this script from the project root directory!"
        exit 1
    fi

    # Create deploy directory if it doesn't exist
    if [ ! -d "deploy" ]; then
        print_error "Deploy directory not found! Please run this script from the project root."
        exit 1
    fi

    cd deploy

    # Setup environments
    setup_environment "staging"
    setup_environment "production"

    echo
    print_status "Environment files created successfully!"
    echo

    # Validate environment files
    validate_env_file ".env.staging" "staging"
    validate_env_file ".env.production" "production"

    echo
    print_status "Next steps:"
    echo "1. Review and update the values in .env.staging and .env.production"
    echo "2. Set up GitHub repository secrets for CI/CD"
    echo "3. Configure your staging and production servers"
    echo "4. Update the deployment scripts with your server details"

    echo
    setup_github_secrets

    print_success "Environment setup completed!"
}

# Run main function
main "$@"
