# fastreader

This is a simple application that allows you to read plain text files with a
speed of 300 words per minute by default, but it can be configured to read at
any speed you want.

## Installation
You just have to clone this repository and run the `fastreader.py` file with
Python 3.6 or higher.

## Usage
You can run the application with the following command:

```bash
python fastreader.py
```

If you do not specify any file, the application will read the file `words.txt`
by default. You can specify a different file just by passing it as an
argument:

```bash
python fastreader.py path/to/file.txt
```

You can interact with the application by pressing the following keys:

* `Space`: Pause/resume the reading.
* `Left arrow`: Go back 1 word.
* `Right arrow`: Go forward 1 word.
* `Up arrow`: Increase the reading speed by 10 words per minute.
* `Down arrow`: Decrease the reading speed by 10 words per minute.
* `Escape`: Exit the application.

> **Note**: You have to pause the reading before word repositioning.