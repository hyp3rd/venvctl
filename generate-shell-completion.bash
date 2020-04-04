#!/bin/bash

# bash
_VENVCTL_COMPLETE=source_bash venvctl > $(pwd)/module/cli/completion.d/venvctl-bash-complete.sh

# zsh || fish
_VENVCTL_COMPLETE=source_zsh venvctl > $(pwd)/module/cli/completion.d/venvctl-shell-complete.sh
