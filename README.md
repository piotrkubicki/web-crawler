# WEB-CRAWLER

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


**Crawler must:**

- [x] create map of each visited page
    - [x] get page content
    - [x] get all links
    - [x] create page map
- [x] know which sub-pages are already mapped
- [x] recognise external links and don't follow
    - [x] filter external links
- [x] reconginse and ignore links to other entities like email
- [ ] recognise sub-page link with absolute and relative page address
- [x] map each identified sub-page

Improvements:
- [ ] map each sub-page in new thread
- [ ] match different protocols for the same page
- [ ] add more tests
