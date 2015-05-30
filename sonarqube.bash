#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e
# Treat unset variables as an error when substituting.
set -u
# the return value of a pipeline is the status of
# the last command to exit with a non-zero status,
# or zero if no command exited with a non-zero status
set -o pipefail
# Print commands and their arguments as they are executed.
# set -x

main()
{
    local cwd="$(readlink -f "$(dirname "$0")")"
    local maven_settings_file_path="$cwd/maven_settings.xml"
    printf -- "\n$ mvn --settings \"$maven_settings_file_path\" sonar:sonar\n\n"
    mvn --settings "$maven_settings_file_path" --define "sonar.host.url=$SONARQUBE_URL" sonar:sonar
}

main "$@"

