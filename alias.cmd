@echo off

:: General purpose aliases:

DOSKEY ls=dir
DOSKEY np=notepad
DOSKEY gs=git status
DOSKEY gadd=git add --all
DOSKEY gm=git commit -m $*
DOSKEY npp=start notepad++ $*
DOSKEY home=cd "C:\Users\Rachael"
DOSKEY np+="C:\Program Files (x86)\Notepad++\notepad++.exe" $*
DOSKEY downloads=start C:\Users\Rachael\Downloads
DOSKEY c=cls
DOSKEY scripts=cd "C:\Users\Rachael\Scripts"

:: Bioinformatic aliases:

DOSKEY py=cd "C:\Users\Rachael\Python\2017-biopython"
DOSKEY usearch=usearch9.2.64_win32.exe $*
DOSKEY clone=cd "C:\Users\Rachael\Phd Research\Projects\Constructs"
DOSKEY trimal=trimal.exe $*
DOSKEY readall=readall.exe $*
DOSKEY muscle=muscle3.8.31_i86win32.exe $*
DOSKEY seqfrag=exciseDNAsection.py $*
DOSKEY Gblocks= Gblocks.exe $*
DOSKEY align=aliview



:: How to edit alias file:

DOSKEY aliases=start notepad++ "C:\Users\Rachael\Scripts\alias.cmd"

@echo on

