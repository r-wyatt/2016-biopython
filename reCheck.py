import os, re, sys

test = re.match(r'\>([A-Z|a-z]{2,3}_[0-9]*.[0-9]*) .*',">XP_102904901.1 spinach")
print  test.group(1)