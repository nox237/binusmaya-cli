# Binusmaya

> For windows, you may need to run the executable file via **cmd**.

## Description
This python script is a scraper tool for listing forums and assignments we haven't worked on yet. It also can output the forums and assignments into markdown file. Using this tool, i wish it can help to finished our forums and assignments on quicker time. For those who have not install python in their device, i also create an executable file for windows and linux.
The python script will need your username and password to login your binusmaya account. And if your name is different on binus maya, you can insert your name in the third input.

## File Checkum

### Windows
| - | Hash |
| --- | ----|
| sha1 | cdcf972eb8f23dd52f4d4023af1618d4d6d252e4 |
| md5 | 2513f15402e5ec38d9f3ac6f34649b74 |

### Linux
| - | Hash |
| --- | ----|
| sha1 | ab256316c0bd49753db49d0ef21e5205713ff065 |
| md5 | 521977cc3f1d141a3bba4618752a1c42 |

## Running Requirement
To run this python3 script, you need to install some library. This can be achieve by running:
```
pip3 install -r requirements.txt
```

## Command
By this default running without arguments will getting **all of the assignments and forum** in your binus maya account and also **write into a markdown file**. But there is an arguments that can help you achieve quicker execution in this script. Below is the argument you can used on this script:

```
COMMAND:
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
```

The tag -a and -f is running on specific information, where tag -a only listing assignment and -f listing on the forum. Tag -s is use for automatic choosing the semester on the list. For example if you want to choose your current semester you can use **-s 0**.

