#/usr/bin/env bash
# https://web.archive.org/web/20200507173259/https://debian-administration.org/article/317/An_introduction_to_bash_completion_part_2

_rtv()
{
    local cur prev opts base
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    #
    #  The basic options we'll complete.
    #
    opts="predvajaj shrani"

    #
    #  Complete the arguments to some of the basic commands.
    #
    case "${prev}" in
        predvajaj)
            local running="$(wl-paste) --id"
            COMPREPLY=( $(compgen -W "${running}" -- ${cur}) )
            return 0
            ;;
        shrani)
            local names="$(wl-paste) --id"
            COMPREPLY=( $(compgen -W "${names}" -- ${cur}) )
            return 0
            ;;
        *)
        ;;
    esac

   COMPREPLY=($(compgen -W "${opts}" -- ${cur}))  
   return 0

}
complete -F _rtv rtv
