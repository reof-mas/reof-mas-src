.. REOF-MAS: CCMAS 2016 Project documentation master file, created by
   sphinx-quickstart on Mon Nov 21 20:35:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to REOF-MAS: CCMAS 2016 Project's documentation!
********************************************************

.. toctree::
   :maxdepth: 2

Project objective
=================

Our multi-agent system attempts to generate monophonic songs with structure resembling that of compositions devised by human composers.


Installing and running the program
==================================

Installing and using the program requires python 3.5, virtualenv and lilypond (http://lilypond.org/).
In order to download the program and run its demonstration, use the following commands:
::
        git clone git@github.com:reof-mas/reof-mas-src.git
        cd reof-mas-src/
        virtualenv -p python3 py_env/
        source py_env/bin/activate
        pip install -r requirements.txt
        cd py_env/src
        python melodic_chains.py

After this there should be generated artifacts in py_env/src/outputs. Vote winner themes are named artefact_[id].mid and created songs are called song_[id].mid.


Generating artifacts
====================

We treat all possible notes as an alphabet, which allows us to use Markov chains for generating sequences of notes, a composition. Currently, we opted to using a second order Markov chain. The problem of the first order is that the artifacts may sound too random. On the other hand, if we were to choose an order at least three, our system will start plagiarize too much the compositions in the corpus used for constructing the Markov chains. (TODO: more content)


Source code layout
==================

(All the files are in the directory ``py_env/src`` of our repository.)

* ``audience_agent.py`` - gives a layman's evaluation for artifacts.
* ``composer.py`` - implements the agent responsible for generating artifacts, computing the value, novelty and surprise of each artifact, and finally voting for artifacts in the environment.
* ``list_memory.py`` - a FIFO (first in, first out) queue for holding at most ``c`` artifacts, where ``c`` is the maximum allowed capacity of the memory queue.
* ``markov_chain.py`` - implements the Markov chain. The algorithm returns absolute transitions counts, yet the function ``get_transition_probs_for_state`` can convert those to transition probabilities.
* ``melodic_chains.py`` - contains the entry point to our CC software.
* ``music_environment.py`` - inherits the environment from Creamas providing the voting function required by Creamas.
* ``serializers.py`` - contains artifact serialization.
* ``utility.py`` - contains miscellaneous utility functions.

Source code documentation
==================

* :ref:`modindex`


Artefact value evaluation
=========================

The Zipf's law states that in natural text, the second most frequent word appears 1/2 times as often as the most frequent word, the third most frequent word appears 1/3 times as often as the most frequent one, and so on. Whenever evaluating an artefact, we measure how well it obeys the law, and return a value denoting that value.

Artefact novelty evaluation
===========================

In order to determine the novelty of an artefact ``A``, we compare the Levenshtein distance between ``A`` and ``B`` for every artefact ``B`` in the agents memory, and choose the minimum distance over all ``B`` as the novelty.


Agent overview
==============

Add text


Terminology
===========

- **Note** A note is a basic building block of music. It has at least two attributes: a pitch (a frequency in Hz) and duration (see below).

- **Duration** Duration of a note is the time interval it takes to play the note relatively to the actual rythm. For instance, a note may take an entire bar, half of it, a quarter, and so on.

- **Pitch** Pitch is measured in Hz and defines how high or low it is perceived.

- **Theme** The material, usually a recognizable melody, upon which part or all of a composition is based. A theme can be seen as the combination and transformation of one or several motifs. [1]

- **Motif** A short succession of notes that is the smallest analyzable element or phrase within a theme. [2]


References
==========

- [1] https://en.wikipedia.org/wiki/Subject_(music) Retreived 1 Dec 2016, 14:53
- [2] https://en.wikipedia.org/wiki/Motif_(music) Retreived 1 Dec 2016, 14:54



