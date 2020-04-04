# venvctl bash completion start
_venvctl_completion()
{
    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   VENVCTL_AUTO_COMPLETE=1 $1 2>/dev/null ) )
}
complete -o default -F _venvctl_completion venvctl
# venvctl bash completion end