# WEB-CRAWLER

## Running (Instructions of MacOS and Linux)
**The application require Python 3 installed**
Install dependencies with `make install` command.  
Run the app with `python main.py` command.  
During the run, the application should output logs to the console and `tmp\main.log`.  
After successfull completion, the results can be found in `site_map` directory.  

### Running with Docker
The application can be run as a Docker container.  
Build Docker image using command like:
```
docker build -t web-crawler .
```
Next, you can run the app using command like:
```
docker run --rm -v $PWD/site_map:app/site_map/ web-crawler
```

## Development
The development dependencies can be installed using following command: 
```
make install-dev
```
To run tests, please use the following command:
```
make test
```

### Updating dependencies
Please don't update the `requirements.txt` file manualy.  
In order to add/update dependency, please use `make freeze` command.


## Description
The web-crawler application extract links for each sub-page for given URL.  
To improve the performance, the application use concurrency. The current presentation of the results  
is very basic.

### Improvements
- [ ] recognise sub-page link with absolute and relative page address
- [ ] match different protocols for the same page
- [ ] add more tests
- [ ] improve presentation of results
