# Dianping_Crawler

This crawler is able to help me crawl the publicly viewable information of a user or a venue in Dazhong Dianping (http://www.dianping.com/aboutus). 

## Before Installation

We have tested our crawler on Ubuntu (version: 14.04). Please make sure that you have installed Python2.7 and Selenium Webdriver.

## User Crawler 

Usage:

- Change directory to User_Crawler.

- Run 'bash install.sh' (no sudo please) to set everything ready for user crawler to run.

- Edit 'begin_ID', 'end_ID', and 'step' in 'dianping_u_script.py'.

- Manually set the content of status.txt to begin_ID (important).

- Run crawler using bash command 'xvfb-run python dianping_u_script.py'.

- When it is done, you can collect your data in 'User_Crawler/Data' folder.

## Venue Crawler

Will be released soon.


## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).

