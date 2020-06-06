@echo off
doskey clear=cls
doskey cp=copy $*
doskey emacs=emacs -nw $*
doskey head=more $*
doskey less=more $*
doskey ls=dir
doskey ls=dir $*
doskey man=help $*
doskey mv=move $*
doskey pwd=cd
doskey rm=del $*
doskey tail=type $*
doskey wc-l=find /c /v "" $*
doskey wc-l=find /c /v ""
