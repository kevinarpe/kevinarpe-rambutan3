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

PYPI_PACKAGE_NAME='kevinarpe-rambutan3'
PYTHON_PACKAGE_NAME='rambutan3'

BASE_PYPI_SERVER_NAME='pypi'

RELEASE_MODE_TEST='test'
RELEASE_MODE_PROD='prod'

PYPI_URL_TEST='https://testpypi.python.org/pypi'
PYPI_URL_PROD='https://pypi.python.org/pypi'

VERSION_FILE_NAME='version.txt'

main()
{
    if [ $# != 1 ]
    then
        echo_usage_and_exit_on_error 'ERROR: Expected exactly one argument: RELEASE_MODE'
    fi

    # Example: 'test' or 'prod'
    local release_mode="$1" ; shift
    check_release_mode "$release_mode"

    local cwd="$(dirname "$(readlink -f "$0")")"
    local server_name="$(echo_server_name "$release_mode")"
    local orig_virtualenv_dir_path="$VIRTUAL_ENV"
    local test_virtualenv_dir_path="$(readlink -f "$VIRTUAL_ENV/../rambutan3-test-release")"
    local pypi_url="$(echo_pypi_url "$release_mode")"

    check_which_python3_matches_virtualenv
    pushd "$cwd"
    check_zero_git_uncommitted_changes
    update_version
    git_commit_changes
    check_zero_git_uncommitted_changes
    git_tag_version
    pypi_register_new_package "$server_name"
    create_source_dist
    gpg_sign_release
    upload_package_to_pypi "$server_name"
    create_virtualenv "$test_virtualenv_dir_path"
    activate_virtualenv "$test_virtualenv_dir_path"
    check_which_python3_matches_virtualenv
    pip_install_package "$pypi_url"
    remove_virtualenv "$test_virtualenv_dir_path"
    activate_virtualenv "$orig_virtualenv_dir_path"
#    git_push_plus_tags
    popd
}

echo_usage_and_exit_on_error()
{
    local error="$1" ; shift

    printf -- '%s\n\n' "$error"
    printf -- 'Usage: "%s" {%s,%s}\n\n' "$0" "$RELEASE_MODE_TEST" "$RELEASE_MODE_PROD"
    printf -- 'Example setup.py version for %s: 1.0.2a0\n' "$RELEASE_MODE_TEST"
    printf -- 'Example setup.py version for %s: 1.0.2\n' "$RELEASE_MODE_PROD"
    exit 1
}

check_release_mode()
{
    # Example: 'test' or 'prod'
    local release_mode="$1" ; shift

    if [ "$release_mode" != "$RELEASE_MODE_TEST" ] \
    && [ "$release_mode" != "$RELEASE_MODE_PROD" ]
    then
        echo_usage_and_exit_on_error \
            "$(printf -- "ERROR: Argument RELEASE_MODE: Expected '%s' or '%s', but found '%s'" \
                      "$RELEASE_MODE_TEST" "$RELEASE_MODE_PROD")"
    fi
}

echo_server_name()
{
    # Example: 'test' or 'prod'
    local release_mode="$1" ; shift

    local server_name="$BASE_PYPI_SERVER_NAME"
    if [ "$release_mode" = "$RELEASE_MODE_TEST" ]
    then
        # 'pypi' -> 'testpypi'
        server_name="$release_mode$server_name"
    fi
    printf -- '%s' "$server_name"
}

check_zero_git_uncommitted_changes()
{
    # Ref: http://stackoverflow.com/a/3879077/257299
    if ! git diff-index --quiet HEAD
    then
        printf -- '\nERROR: Uncommited Git changes\n\n'
        git status
        git diff-index --quiet HEAD
    fi
}

update_version()
{
    cat "$VERSION_FILE_NAME" 1> /dev/null 2>&1
    local current_version="$(cat "$VERSION_FILE_NAME")"

    while true
    do
        printf -- 'Current version: [%s]\n' "$current_version"
        local next_version=''
        read -p 'Next version: ' next_version

        # Intentional: Do not anchor with '$'.  Allow trailing non-digits, e.g., 'a' (for alpha)
        if [[ "$next_version" =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]
        then
            break
        else
            printf -- 'ERROR: Invalid version format.  Please try again.\n\n'
        fi
    done

    printf -- '%s\n' "$next_version" > "$VERSION_FILE_NAME"
}

git_commit_changes()
{
    local next_version="$(cat "$VERSION_FILE_NAME")"
    git add --all
    git commit --message="$0: Next version: [$next_version]"
}

git_tag_version()
{
    local next_version="$(cat "$VERSION_FILE_NAME")"
    git tag --message="$0: Next version: [$next_version]" "$next_version"
}

check_which_python3_matches_virtualenv()
{
    [ "$VIRTUAL_ENV/bin/python3" = "$(which python3)" ]
}

pypi_register_new_package()
{
    local server_name="$1" ; shift

    python3 setup.py register -r "$server_name"
}

create_source_dist()
{
    /bin/rm -Rf dist
    python3 setup.py sdist
}

gpg_sign_release()
{
    echo "$GPG_PASSWORD" | gpg --passphrase-fd 0 --detach-sign --armor dist/*.tar.gz
}

upload_package_to_pypi()
{
    local server_name="$1" ; shift

    twine upload -r "$server_name" dist/*
}

create_virtualenv()
{
    local virtualenv_dir_path="$1"

    /bin/rm -Rf "$virtualenv_dir_path"
    /usr/bin/python3 $VIRTUALENV_HOME/virtualenv.py --python /usr/bin/python3 "$virtualenv_dir_path"
    # Re-enable python2 from /usr/bin, but do not touch python3
    /bin/rm -f "$virtualenv_dir_path/bin/python"
}

activate_virtualenv()
{
    local virtualenv_dir_path="$1"

    # DISABLE: Treat unset variables as an error when substituting.
    set +u
    source "$virtualenv_dir_path/bin/activate"
    # ENABLE: Treat unset variables as an error when substituting.
    set -u
}

echo_pypi_url()
{
    # Example: 'test' or 'prod'
    local release_mode="$1" ; shift

    if [ "$release_mode" = "$RELEASE_MODE_TEST" ]
    then
        printf -- '%s' "$PYPI_URL_TEST"
    else
        printf -- '%s' "$PYPI_URL_PROD"
    fi
}

pip_install_package()
{
    local pypi_url="$1" ; shift

    pip install -i "$pypi_url" --pre "$PYPI_PACKAGE_NAME"

    # Check package can be imported
    printf -- 'import %s ; quit()\n' "$PYTHON_PACKAGE_NAME" | python3
}

remove_virtualenv()
{
    local virtualenv_dir_path="$1"

    /bin/rm -Rf "$virtualenv_dir_path"
}

git_push_plus_tags()
{
    git push --tags
}

main "$@"

