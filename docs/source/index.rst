.. REOF-MAS: CCMAS 2016 Project documentation master file, created by
   sphinx-quickstart on Mon Nov 21 20:35:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to REOF-MAS: CCMAS 2016 Project's documentation!
********************************************************

Terminology
===========

- **Note** A note is a basic building block of music. It has at least two attributes: a pitch (a frequency in Hz) and duration (see below).

- **Duration** Duration of a note is the time interval it takes to play the note relatively to the actual rythm. For instance, a note may take an entire bar, half of it, a quarter, and so on.

- **Pitch** Pitch is measured in Hz and defines how high or low it is perceived.

- **Theme** The material, usually a recognizable melody, upon which part or all of a composition is based. A theme can be seen as the combination and transformation of one or several motifs. [1]

- **Motif** A short succession of notes that is the smallest analyzable element or phrase within a theme. [2]

Contents:

.. toctree::
   :maxdepth: 2

Sample text
===========

Running the demonstration
=========================

In order to download the program and run its demonstration, use the following commands:
::
        git clone git@github.com:reof-mas/reof-mas-src.git
        cd reof-mas-src/py_env/
        . bin/activate
        cd ..
        ./run_all
        deactivate


References
==========

- [1] https://en.wikipedia.org/wiki/Subject_(music) Retreived 1 Dec 2016, 14:53
- [2] https://en.wikipedia.org/wiki/Motif_(music) Retreived 1 Dec 2016, 14:54



