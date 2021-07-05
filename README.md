# Binusmaya

> For windows, you may need to run the executable file via **cmd**.

> You also need python installed on the device

## Description

This python script is a scraper tool for listing forums and assignments we haven't worked on yet. It also can output the forums and assignments into markdown file. Using this tool, i wish it can help to finished our forums and assignments on quicker time. For those who have not install python in their device, i also create an executable file for windows and linux. The python script will need your username and password to login your binusmaya account. And if your name is different on binus maya, you can insert your name in the third input. The latest code that I added is to scrape the enrichment program for us, it also shows us the status for our applied internship and also the available job on binus internship program.

## Running Requirement

To run this python3 script, you need to install some library. This can be achieve by running:
```
pip3 install -r requirements.txt
```

## Command

By this default running without arguments will getting **all of the assignments and forum** in your binus maya account and also **write into a markdown file**. But there is an arguments that can help you achieve quicker execution in this script. Below is the argument you can used on this script:

```
COMMAND:
 --all            : run all available command
 -h, --help       : help command
 -s               : set semester to persistent index
ASSIGNMENT:
 -a, --assignment : scraping on the assignment
 -w               : write into assignment.md
 -o               : write into assignment_notion.md
FORUM:
 -f, --forum      : scraping on the forum
 -w               : write into forum.md  with lecturer post and user post
 -o               : write into forum_notion.md
TODOLIST:
 -t, --todolist   : scraping on the todolist
 -w               : write into todolist.md
ENRICHMENT:
 --enrichment     : scraping enrichment page
 -e               : set enrichment semester (do not need --enrichment flag)
 -m               : for mobile view

 --progressbar    : print progressbar for each thread request
 --detailwrite    : output detail write on forum.md
```

The tag -a and -f is running on specific information, where tag -a only listing assignment and -f listing on the forum. Tag -s is use for automatic choosing the semester on the list. For example if you want to choose your current semester you can use **-s 0**. For the enrichment program, you can also specify the semester that you internship by using **-e** similar to the semester in assignment and forum (example: **-e 0** for the first semester that you internship).

