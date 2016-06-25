    #/bin/bash  
    ################################################################  
    #  automatically run a script(action.sh) when the contents  
    #     of a directory (${EVENTPATH}) changed.  
    #  pls. install the inotify-tools-3.13-1.el4.rf.i386.rpm module  
    #       before use this scripts  
    #  Aborn Jiang (aborn.jiang@gmail.com)  
    #  Sep.8, 2013  
    ################################################################  
    cd "/home/linaro/tobacco_monitor/terminal"
    ldconfig  
    EVENTPATH="/home/uftp/"  
    STATICPATH="/home/linaro/tobacco_monitor/terminal/img/captured/"
    MSG="./.inotifymsg"  
    RES="./.res"
    PATTERN=".jpg$"          # only when the rpm files changed.  
    while inotifywait -e close  -r ${EVENTPATH} 1>${MSG} 2>/dev/null; do  
        
        FILE=`cat ${MSG} |egrep ${PATTERN} | awk '{print $3}' `  
        ACTION=`cat ${MSG} |egrep ${PATTERN} | awk '{print $2}' `  
        [ ! -z ${FILE} ] && \  
        mv "${EVENTPATH}/${FILE}" "${STATICPATH}/${FILE}" && \  
        ./action.sh ${FILE}
        FILE_COUNT=`ls -l|grep "jpg"|wc -l`
        if [ $FILE_COUNT -gt 16*2*300];then
            FILE_NAME=`ls -rt ${STATICPATH}|head -1`
            rm -rf "${STATICPATH}/${FILE_NAME}" 
        fi
    done  
