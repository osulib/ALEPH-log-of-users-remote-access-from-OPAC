#!/bin/sh
#Creates log with information about access to remote websites, including
#ebooks, repositories etc.
#
#The log has following structure?
#  datetime - IP_address - aleph_record_sysNo - URL
#
#CONFIGURATION - fine three variables in the beginning of this script:
#        log_file  restAPI_url  bib_base
#
#created by Matyas Bajger www.svkos.cz 20181002
# updated 20200130 by Matyas Bajger (RC1)
#
#RC1 - variable $WWW_loc does not always contain "loc" URL argument
#      changed to more safe way - parsing URL arg. from $QUERY_STRING


#CONFIGURATION parameters
log_file='/exlibris/aleph/matyas/opac_remote_access.log' #filesystem path to save the log
restAPI_url='http://localhost:1891/' #protocol+URL+port to access Aleph RestFulAPI
bib_base='MVK01' #Aleph BIB base
#CONFIGURATION parameters END


echo 'Content-type: text/plain'
echo ''
echo 'loc is '$WWW_loc
echo 'xQUERY_STRING is '$QUERY_STRING

#RC1
#if [[ `echo "$WWW_loc" | grep -c 'http' | bc` == 0]]; then
   WWW_loc=`echo "$QUERY_STRING" | sed 's/^.*loc=//' | sed 's/&.*$//'`
#fi
echo '2loc is '$WWW_loc

if [[ `echo "$WWW_loc" | grep -c 'service_type.\{1,4\}MEDIA' | bc` == 1 ]]; then
   sysno=`echo "$WWW_loc" | grep -o 'doc_number=[0-9]\+' | sed 's/doc_number=//'`
   line_number=`echo "$WWW_loc" | grep -o 'line_number=[0-9]\+' | sed 's/line_number=//'`
   curl "$restAPI_url/rest-dlf/record/$bib_base""$sysno?view=full" >log_remote_access.tmp
   targetURL=`grep '<datafield tag="856.*</datafield>' -o log_remote_access.tmp | sed 's/<\/datafield>/<\/datafield>\\\n/g' | grep -o 'http[^<]\+' | sed $line_number'q;d'`

   echo "`date '+%Y-%m-%d %H:%M:%S'` - $REMOTE_ADDR - $sysno - $targetURL" >>$log_file
   echo "`date '+%Y-%m-%d %H:%M:%S'` - $REMOTE_ADDR - $sysno - $targetURL"

   echo 'OK'

else

   echo 'something went wrong - log has not been written'

fi

rm -f log_remote_access.tmp
