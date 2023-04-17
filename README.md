# ALEPH – log of users‘ remote access from OPAC

## Purpose, main info
ALEPH BIB records more and more link to various remote Internet resources, like online e-books, indigenous or distant repositories, e-content providers’ sites, publisher webs, TOCs etc. These are mostly linked using Marc21 field 856.
There is no default ALEPH service or possibility for monitoring which sites or URLs are visited from OPAC BIB records and how particular sources in the catalogue are used or no. Administrator can query z35 Oracle table in BIB base, however only total amount of access can be read from this table :   `select count(*)  from z35  where z35_event_date between 'yyyymmdd' and 'yyyymmdd' and z35_event_type='40';`
One possibility for this monitoring is application of external services like Google Analytics.
Another one is to monitor this by own, might using this instrument.

## Description
When OPAC user clicks on link of OPAC service to remote URL, new Javascript calls CGI script using AJAX sending parametrs of OPAC service. CGI bash script on server takes the system number and line number of link and queries RestFulAPI to get BIB record. It extracts URL from corresponding 856 field and logs it.

## Log format
`datetime – IP address – BIB record system number – URL`
This is common text file that sould be later used for analyses according to library requirements.

## Implementation
1.  Modify www template file include-window. In this file, in Javascript function 
`function open_window (loc)`
add following lines to the beginning of the function:
```
    <script language="Javascript">
    <!--
    function open_window (loc)
    {
       //remote access logging
       var path2log_remote_access_cgi='/cgi-bin/'
       if ( loc.indexOf('service_type=MEDIA') > -1) {
          var xhttpLoc = new XMLHttpRequest();
          xhttpLoc.open('GET', path2log_remote_access_cgi+'log_remote_access.cgi?loc='+encodeURIComponent(loc), true);
          xhttpLoc.send();
          }
       //remote access logging END
    … … …
```
Replace value in the variable `path2log_remote_access_cgi` to real location of CGI scripts according to your Apache configuration.


2. Download and save file  `log_remote_access.cgi `to your CGI direktory, might `$http_root/cgi-bin`

3. Edit this file and modify three variables – parameters at the beginning:
log_file ='…' #filesystem path to file, including filename, where to save the log file
restAPI_url='http://localhost:1891/' #protocol+URL+port to access Aleph RestFulAPI
bib_base='XXX01' #Aleph BIB base

4. restart Aleph WWW server (util w 3 1) to bring modified opac template include-window into production. The log file should now be filled.


**Requirements**: CGI at Apache, ALEPH RestfulAPI, , ALEPH version 18-23

**Languages**: Javascript, Bash

