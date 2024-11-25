#!/bin/bash

# Configuration: Default file paths
VC_FILE="./vc.yaml"
LOG_FILE="./temp.log"

# Display usage instructions
usage() {
    echo "Usage: $0 [-f|--file <file_path>] '<convention>(<app>):<message>'"
    echo "Options:"
    echo "  -h, --help           Show this help message and exit"
    echo "  -f, --file <path>    Specify the vc.yaml file path (default: ./vc.yaml)"
    echo ""
    echo "Examples:"
    echo "  $0 '!feat(api):Introduce breaking API change'"
    echo "  $0 -f custom_vc.yaml 'feat(app):Add a new feature'"
    exit $1
}

# Parse command-line arguments and return parsed inputs
# Outputs: INPUT_STRING
parse_args() {
    local input_string=""
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage 0
            ;;
            -f|--file)
                VC_FILE="$2"
                shift 2
            ;;
            -*)
                echo "Unknown option: $1"
                usage 0
            ;;
            *)
                input_string="$input_string $1"
                shift 1
            ;;
        esac
    done
    if [ -z "$input_string" ]; then
        echo "Error: No input string provided."
        usage 1
    fi

    echo "$input_string"
}


parse_input() {
    local input_string="$@"
    local convention app message
    convention=$(echo "$input_string" | sed -n 's/^\([^()]*\)(.*):.*/\1/p')
    app=$(echo "$input_string" | sed -n 's/^[^(]*(\([^)]*\)):.*$/\1/p')
    if [ -z "$convention" ] || [ -z "$app" ]; then
        echo "Invalid input format."
        usage
    fi

    echo "$convention $app"
}

# Load versions from the specified vc.yaml file
# Outputs: API_VERSION, APP_VERSION
load_versions() {
    if [ ! -f "$VC_FILE" ]; then
        echo "Error: File not found - $VC_FILE"
        exit 1
    fi

    local api_version app_version
    api_version=$(yq -e '.API_VERSION' "$VC_FILE")
    app_version=$(yq -e '.APP_VERSION' "$VC_FILE")

    if [ -z "$api_version" ] || [ -z "$app_version" ]; then
        echo "Failed to load versions from $VC_FILE. Ensure the file is valid."
        exit 1
    fi

    echo $api_version $app_version
}

# Increment version based on convention
# Input: Version, Convention
# Outputs: New Version
increment_version() {
    local version=$1
    local convention=$2
    convention=$(echo $convention | tr -d '\\')
    version=$(echo $version | tr -d '"')
    IFS='.' read -r major minor patch <<<$version
    case "$convention" in
    !feat|!fix|!refactor)
        major=$((major + 1))
        minor=0
        patch=0
        ;;
    feat)
        major=$major
        minor=$((minor + 1))
        patch=0
        ;;
    fix|refactor)
        major=$major
        minor=$minor
        patch=$((patch + 1))
        ;;
    esac
    echo $major.$minor.$patch
}

# Update the version in vc.yaml based on app and convention
# Input: APP, VERSION, CONVENTION
update_version() {
    local app=$1
    local version=$2
    local convention=$3

    case "$app" in
    api)
        yq -i -y ".API_VERSION = \"$(increment_version "$version" "$convention")\"" "$VC_FILE"
        ;;
    app)
        yq -i -y ".APP_VERSION = \"$(increment_version "$version" "$convention")\"" $VC_FILE
        ;;
    *)
        # trace this line number
        echo "Error: Invalid app - $app"
        usage 1
        exit 1
        ;;
    esac
}

# Main function
main() {
    # Parse arguments
    read -r input_string <<<"$(parse_args $@)"
    # Parse input string
    read -r convention app <<<$(parse_input $input_string)
    # Load versions from the file
    read -r api_version app_version <<<$(load_versions)

    update_version "$app" "$app_version" "$convention"
    # replace `\!` with `!` in the input string
    input_string=$(echo "$input_string" | tr -d '\\')
    echo "Commit message: $input_string" > $LOG_FILE
    git add .
    git commit -m "$input_string"
}

# Call the main function
main "$@"
