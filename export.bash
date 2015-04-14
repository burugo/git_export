# bash/zsh
repo_path=/d/Code/bbc
__git_export ()
{	
    if [ -n "$1" ]; then
     cd $repo_path 
     git diff-tree -r --no-commit-id --name-only --diff-filter=ACMRT $1 | xargs tar -rf $2/$1.tar
     return 1
    else
     return 0
    fi
}


    path=`pwd`
    #echo $path
    echo "please input commit hash:"
    read -r commit_id
    __git_export "$commit_id" "$path"
   
    echo "need ftp down?(y/n)"
    read -r need_down
    cd $path
    python ./ftp_copy.py "$commit_id" "$need_down"
    exit 0;
   

