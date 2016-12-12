.. REOF-MAS: CCMAS 2016 Project documentation master file, created by
   sphinx-quickstart on Mon Nov 21 20:35:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to REOF-MAS: CCMAS 2016 Project's documentation!
********************************************************

Source code documentation
==================

* :ref:`modindex`

Project objective
=================

Our multi-agent system attempts to generate monophonic songs with structure resembling that of compositions devised by human composers.

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


Running the demonstration
=========================

In order to download the program and run its demonstration, use the following commands:
::
        git clone git@github.com:reof-mas/reof-mas-src.git
        cd reof-mas-src/
        pyvenv-3.5 py_env
        . py_env/bin/activate
        pip3 install -r requirements.txt
        cd py_env/src
        python melodic_chains.py
        deactivate
        cd outputs
        open *



Generating artifacts
====================

We treat all possible notes as an alphabet, which allows us to use Markov chains for generating sequences of notes, a composition. Currently, we opted to using a second order Markov chain. The problem of the first order is that the artifacts may sound too random. On the other hand, if we were to choose an order at least three, our system will start plagiarize too much the compositions in the corpus used for constructing the Markov chains. (TODO: more content)

Source code layout
==================

(All the files are in the directory ``py_env/src`` of our repository.)

* ``composer.py`` - implements the actual agent responsible for generating artifacts, computing the value and novelty of each artifact, and finally reporting the best one to the environment.
* ``list_memory.py`` - a FIFO (first in, first out) queue for holding at most ``c`` artifacts, where ``c`` is the maximum allowed capacity of the memory queue.
* ``markov_chain.py`` - implements the actual Markov chain. The actual algorithm returns absolute transitions counts, yet the function ``get_transition_probs_for_state`` can convert those to actual transition probabilities. Also, we chose to reinforce the sequences generated from the Markov chain by adding those sequences to the Markov chain itself, thus reinforcing "good" compositions.
* ``melodic_chains.py`` - contains the actual entry point to our CC software.
* ``music_environment.py`` - subclasses the environment from Creamas providing the voting function required by Creamas.
* ``utility.py`` - contains miscellaneous utility functions.


Artefact value evaluation
=========================

The Zipf's law states that in natural text, the second most frequent word appears 1/2 times as often as the most frequent word, the third most frequent word appears 1/3 times as often as the most frequent one, and so on. Whenever evaluating an artefact, we measure how well it obeys the law, and return a value denoting that value.

Artefact novelty evaluation
===========================

In order to determine the novelty of an artefact ``A``, we compare the Levenshtein distance between ``A`` and ``B`` for every artefact ``B`` in the agents memory, and choose the minimum distance over all ``B`` as the novelty.


Agent overview
==============

Add text


References
==========

- [1] https://en.wikipedia.org/wiki/Subject_(music) Retreived 1 Dec 2016, 14:53
- [2] https://en.wikipedia.org/wiki/Motif_(music) Retreived 1 Dec 2016, 14:54



