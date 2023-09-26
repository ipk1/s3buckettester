# s3buckettester
This python script takes input in the form of a text files with all s3buckets and check for pubic access, writes paths in a file, tries to read all the files present in it by enumerating and also checks for any sensitive info like api keys,db cerds  and passwords and writes all the files that have this info in them in a file called juicy_info.txt

install boto3 using pip
configure awscli with your accesskey, secret and region 


check usage for commands
