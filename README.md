# httpdwn

### What can it do:
+ [x] Mulit threading with parallel - Install GNU Parallel
+ [x] Random User-agent for each request
+ [x] It takes screenshots too :)

### Read input
+ This script can read from `stdin` and `argv[1]`

### Run the script in parallel
+ `cat probed.txt | parallel --pipe -N1 -j10 python httpdwn.py`
+ Use maximum 2 threads per core

### Usefull strings to grep for
+ Titles
+ Server headers
+ Known subdomain takeovers
+ URLS
+ Sectrets
+ Error messages
+ fileupload forms
+ Interesting Base64 encoded strings
