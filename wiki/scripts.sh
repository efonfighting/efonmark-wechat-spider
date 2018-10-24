# 利用mencoder 和 命令行 批量修改视频信息
ls *.mp4 | while read line ;do mencoder $line -o output.mp4 -ovc copy -oac twolame;mv output.mp4 $line;done
