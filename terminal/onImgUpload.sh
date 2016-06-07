    #/bin/bash  
    ################################################################  
    #  automatically run a script(action.sh) when the contents  
    #     of a directory (${EVENTPATH}) changed.  
    #  pls. install the inotify-tools-3.13-1.el4.rf.i386.rpm module  
    #       before use this scripts  
    #  Aborn Jiang (aborn.jiang@gmail.com)  
    #  Sep.8, 2013  
    ################################################################  
      
    EVENTPATH="/home/uftp/TOBACCO_ZUNYI_CAMERA/"  
    STATICPATH="/home/sonic513/cam_survilliance_server/static/img/captured/"
    MSG="./.inotifymsg"  
    RES="./.res"
    PATTERN=".jpg$"          # only when the rpm files changed.  
    while inotifywait -e create -e delete -r ${EVENTPATH} 1>${MSG} 2>/dev/null; do  
        FILE=`cat ${MSG} |egrep ${PATTERN} | awk '{print $3}' `  
        ACTION=`cat ${MSG} |egrep ${PATTERN} | awk '{print $2}' `  
        [ ! -z ${FILE} ] && \  
        cp "${EVENTPATH}/${FILE}" "${STATICPATH}/${FILE}" && \  
        ./action.sh ${FILE}
    done  
