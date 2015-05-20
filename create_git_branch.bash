#!/usr/bin/env bash

main()
{
    if [ 1 != $# ]
    then
        printf -- 'ERROR: Expected new git branch name\n'
        exit 1
    fi
    local branch_name="$1" ; shift
    local final_branch_name="$branch_name""$(date '+_%Y%m%d_%H%M%S')"

    local cwd="$(readlink -f "$(dirname "$0")")"
    cd "$cwd"
    printf -- "git checkout -b '$final_branch_name'"
    git checkout -b "$final_branch_name"
}

main "$@"

