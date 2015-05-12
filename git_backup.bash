
# bash/zsh
repo_path=/d/Code/xx
file_list=null
__git_backup()
{
    if [ -n "$1" ]; then
    cd $repo_path
    target="$2/$1_backup"
    mkdir -p "$target" 
    git branch --no-track backup "$1" 
    git checkout backup
    git reset  --hard "$1"~
    for i in $file_list
    do 
        if [ -f "$i" ]; then
        # First create the target directory, if it doesn't exist.
        mkdir -p "$target/$(dirname $i)"
        # Then copy over the file.
        cp "$i" "$target/$i"
        fi
    done
    git checkout master
    git branch -d backup
     return 1
    else
     return 0
    fi
}
__git_export ()
{	
    if [ -n "$1" ]; then
     mkdir -p "$2/$1"
     cp -pv --parents $file_list "$2/$1"
     return 1
    else
     return 0
    fi
}


    path=`pwd`
    #echo $path
    cd $repo_path 
    echo "please input commit hash:"
    read -r commit_id
    file_list=`git diff-tree -r --no-commit-id --name-only --diff-filter=ACMRT "$commit_id"`
    __git_export "$commit_id" "$path"
    __git_backup "$commit_id" "$path"
    exit 0;
   

