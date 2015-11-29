fup
===

test: show per-friends updates on 500px

--- example use ---

-- create a virtual environment and install reqs  
$ virtualenv virt  
$ virt/bin/pip install request discover requests-oauth  
$ virt/bin/pip install PxMagic  
$ virt/bin/pip install https://github.com/500px/PxMagic.git  
$ # or clone the git repo  

-- exec  
$ virt/bin/python test.py USERNAME > OUTFILE  
$ virt/bin/python test.py -h # read the help  
