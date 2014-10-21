#!/bin/sh

# download OpenSubtitles2012 with the 2013 extension

wget "http://opus.lingfil.uu.se/download.php?f=OpenSubtitles2012/en.tar.gz" -O "OpenSubtitles2012.tar.gz"
wget "http://opus.lingfil.uu.se/download.php?f=OpenSubtitles2013/en.tar.gz" -O "OpenSubtitles2013.tar.gz"

# untar them both

tar -xvzf "OpenSubtitles2012.tar.gz"
tar -xvzf "OpenSubtitles2013.tar.gz"

# save symfix.sh script to ~/symfix.sh for later use
# replace symbolic links with target
# source: http://superuser.com/questions/303559/replace-symbolic-links-with-files/303593#303593

cat > ~/symfix.sh <<- EOM
#!/bin/sh
set -e
for link; do
    test -h "$link" || continue

    dir=$(dirname "$link")
    reltarget=$(readlink "$link")
    case $reltarget in
        /*) abstarget=$reltarget;;
        *)  abstarget=$dir/$reltarget;;
    esac

    rm -fv "$link"
    cp -afv "$abstarget" "$link" || {
        # on failure, restore the symlink
        rm -rfv "$link"
        ln -sfv "$reltarget" "$link"
    }
done
EOM

# fix directory structure to match that which the symlinks expect

cd "OpenSubtitles2012"
mkdir xml
mv en xml/
cd ..

# run above script to replace all symlinks with the target file

cd "OpenSubtitles2013"
find . -type l -exec ~/symfix.sh {} +

# unzip all subtitles

find . -name '*.gz' -print -exec gunzip '{}' \;