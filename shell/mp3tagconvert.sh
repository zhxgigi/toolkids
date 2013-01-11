find ~/Music/无能的力量/ -type f -name "*.mp3" -print0 | xargs -0 mid3iconv -e gbk -d -p
