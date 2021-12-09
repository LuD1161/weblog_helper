# Weblog Helper

**weblog_helper** is a python script that helps in parsing `NCSA Common (access log)` files and filtering the output on the basis of IP address or CIDR range.

## Usage

```posix-shell
usage: weblog_helper.py [-h] [--ip IP] [--log-file LOG_FILE]

weblog_helper is a python script that parses NCSA Common (access log) log
files and filters the output on the basis of IP address or CIDR range.

optional arguments:
  -h, --help           show this help message and exit
  --ip IP              Filter logs with this IP
  --log-file LOG_FILE  Log file path

❯ ./weblog_helper.py --log-file /Users/aseemshrey/Downloads/public_access.log.txt --ip 180.76.15.0/24
180.76.15.135 - - [02/Jun/2015:17:05:23 -0700] "GET /logs/access_140730.log HTTP/1.1" 200 979626 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "www.redlug.com"
180.76.15.137 - - [02/Jun/2015:17:05:28 -0700] "GET /logs/access_140730.log HTTP/1.1" 200 7849856 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "www.redlug.com"
180.76.15.17 - - [02/Jun/2015:17:20:23 -0700] "GET /logs/access_141026.log HTTP/1.1" 200 45768 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)" "www.redlug.com"
~~~~ SNIP FOR BREVITY ~~~~
```

## Tests
```posix-shell
make test
```

## TO Do 
- Create class based implementation in `overengineered.py` so as to add functionality easily and ignore errors in log lines.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)