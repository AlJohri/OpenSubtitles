OpenSubtitles
=============

This repository is a collection of scripts that help download and parse the OpenSubtitles corpus.

- opensubtitles.sh: downloads, extracts, and merges the 2012/2013 corpora from http://opus.lingfil.uu.se
- opensubtitles.py: naieve attempt at trying to download a single english subtitle for each imdb id. rate limits at 200 downloads per day

----------------------------------------------------------------------

- analyze.py: tries to cluster a single year of movie transcripts
- explore.py: prints a list of all genres for the given year
- load.py: loads all subtitles into memory for a given year, used by all other scripts
- xml.py: parse xml file into subtitle.txt file
- parse.py: find corresponding imdb id from opensubtitles id and get json of metadata

Citations
----------

OpenSubtitles: http://www.opensubtitles.org/

Jörg Tiedemann, 2012, Parallel Data, Tools and Interfaces in OPUS. In Proceedings of the 8th International Conference on Language Resources and Evaluation (LREC 2012)
