# Online Library
Script for downloading books from tululu website and their images.
Also, it is parsing books data as name, author, genre, comments

## Setup
First of all need to install packages.
Python3 should be already installed. 
Use `pip` to install requirements:
```
pip install -r requirements.txt
```

## Usage
Use bash command to run script: 


```
python3 online_library.py
```
You can change number of books manual, script has 2 options:

* start_id
* end_id

So, if you want to download 30 books and images, you can use for example:
```commandline
python3 online_library.py --start_id 20 --end_id 50
```

