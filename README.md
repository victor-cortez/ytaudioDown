# ytaudioDown
Simple command line audio downloader script for youtube videos.

## Installation

Simply run the script using python and make sure you have youtube-dl installed.

## Commands

-h for help.

-f [path to folder] -> outputs to the specified folder (default: .)

-l -> set quality to low (192kbps) (default: 320kbps)

-c [codec] -> specifies the codec you want to download from youtube. Highly recommended to be set to "best" (default: best)

-q -> specifies the bitrate in kbps (default: 256)

--csv [path to .csv] -> if a csv file is passed here the code will download from the links in the csv. The csv has a format as follows:

tagName,url,startime,endtime

the times can be in fthe format of "0" for seconds, "0:0" for minutes:seconds and "0:0:0" for hours:minutes:seconds

--to-mp3 -> converts all the downloads to mp3 at the end

--to-m4a -> converts all the downloads to mp4 at the end

-a [link1] [link2] [link3]... downloads from the given urls separated by space

## Examples
To download audio files from a .csv and save them all in mp3 320kbps
```
python3 ytaudioDown.py -q 320 --to-mp3 -f outputFolder --csv test.csv
```

To download two audio files (one from each url) as m4a in 256 kbps
```
python3 ytaudioDown.py -q 256 --to-m4a -a https://www.youtube.com/watch?v=dQw4w9WgXcQ https://www.youtube.com/watch?v=YnopHCL1Jk8 -f outputFolder
```
To download audio files from a .csv and save them all in the best format youtube originally provides for each audio. (best is a default setting)
```
python3 ytaudioDown.py -c best -f outputFolder --csv test.csv
```

To download audio files from a .csv and save them all in the mp3 codec provided by youtube (not recommended since it can result in poor quality audio files).
```
python3 ytaudioDown.py -c mp3 -f outputFolder --csv test.csv
```
