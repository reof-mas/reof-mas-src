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

Our multi-agent system attempts to first generate musical themes and then the most contrasting ones among the best ones are used to
generate songs with structure resembling that of compositions devised by human composers.


Summary
=======

In our multi-agent system we have composer agents which have different musical backgrounds. Some of them get their inspiration in known themes from Mozart or Bach.
Each one of them generates a set of themes and they compare them with each other, while also asking an opinion to audience agents who do not generate any kind
of music.

Over time, the composer agents modify their theme generation function based on what was deemed good-sounding by the whole society.
At the end of the simulation, the most and the least complex themes of the best ones at each iteration are fed into a song creation algorithm that is in the environment, which in turn will transform the both themes in many ways to produce
a single song.


Terminology
===========

- **Note** A note is a basic building block of music. It has at least two attributes: a pitch (a frequency in Hz) and duration (see below).

- **Duration** Duration of a note is the time interval it takes to play the note relatively to the actual rythm. For instance, a note may take an entire bar, half of it, a quarter, and so on.

- **Pitch** Pitch is measured in Hz and defines how high or low it is perceived.

- **Theme** The material, usually a recognizable melody, upon which part or all of a composition is based. A theme can be seen as the combination and transformation of one or several motifs. [1]

- **Motif** A short succession of notes that is the smallest analyzable element or phrase within a theme. [2]

- **Inversion** the inverted form of a motif or theme, in which every ascending movement in the motif is transformed into a equally great descending movement and vice-versa. Check [3]

- **Retrograde** the retrograde form of a motif or theme, in which the last note of the motif/theme becomes the first, the second last becomes the second, etc. Check [4]

- **Transposition** refers to the process of moving a collection of notes up or down in pitch by a constant interval [5]


Installing and running the program
==================================

Warning: This guide is for linux. Other operating systems may require manual installation of the packages.

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

After this there should be generated artefacts in py_env/src/outputs. Vote winner themes are named artefact_[id].mid and created songs are called song_[id].mid.


Agent overview
==============

We have two types of agents: composer agents and an audience agent. 

Composer agents are experts in music. They create short themes and evaluate each other's creations. Composer agents also have a memory and they remember a certain amount of their own creations and artefacts from the domain.

The audience agent emulates a normal person who doesn't have musical expertise. It provides an uneducated evaluation for the composers' creations.


Inspiring sets
==============

Every agent has a Markov chain of note transitions. The Markov chain is initially created from a set of real songs, for example the works of Bach. During the execution of the program, agents add melodies created by themselves and other agents to their Markov chain. Currently, we opted to using a second order Markov chain. The problem of the first order is that the artefacts may sound too random. On the other hand, if we were to choose an order at least three, our system will start plagiarize too much the compositions in the corpus used for constructing the Markov chains.


Generating artefacts
====================

A composer agent creates a short theme using its Markov chain. The starting note is selected randomly and from there the next note is selected using the Markov chain transition probabilities. The generated themes are filtered using the composer agent's own evaluation and the audience agent's opinion.

TODO: Song creation


Artefact evaluation
=========================

Composer agents evaluate themes using three measures: value, novelty and surprise.

Value is calculated using Zipf's law, which states that in natural text, the second most frequent word appears 1/2 times as often as the most frequent word, the third most frequent word appears 1/3 times as often as the most frequent one, and so on. Whenever evaluating a theme, we measure how well it obeys the law, and return a value denoting that value.

In order to determine the novelty of a theme ``A``, we compare the Levenshtein distance between ``A`` and ``B`` for every artefact ``B`` in the agents memory, and choose the minimum distance over all ``B`` as the novelty. Instead of using the alphabet notes, a melody is transformed into an array containing the steps between consecutive notes. We do this because what the notes are doesn't really matter to the human ear. What matters is the change in pitch between the notes.

For surprise evaluation the agents use their Markov chain probabilities. The more unlikely the transitions in the melody are, the more surprising it is.

Audience agent is supposed to give a layman's evaluation to themes in contrast to the expert opinion of a composer. Currently it only uses Zipf's law, because we didn't have enough time to implement more evaluation methods for it.

TODO: Song evaluation


Source code layout
==================

(All the files are in the directory ``py_env/src`` of our repository.)

* ``audience_agent.py`` - gives a layman's evaluation for artefacts.
* ``composer.py`` - implements the agent responsible for generating artefacts, computing the value, novelty and surprise of each artefact, and finally voting for artefacts in the environment.
* ``list_memory.py`` - a FIFO (first in, first out) queue for holding at most ``c`` artefacts, where ``c`` is the maximum allowed capacity of the memory queue.
* ``markov_chain.py`` - implements the Markov chain. The algorithm returns absolute transitions counts, yet the function ``get_transition_probs_for_state`` can convert those to transition probabilities.
* ``melodic_chains.py`` - contains the entry point to our CC software.
* ``music_environment.py`` - inherits the environment from Creamas providing the voting function required by Creamas.
* ``serializers.py`` - contains artefact serialization.
* ``utility.py`` - contains miscellaneous utility functions.


Source code documentation
==================

* :ref:`modindex`


Examples
========

The songs here have been created by our system.

Created by the latest version:

| Created by old versions:
| :download:`duke.mid <downloadables/duke.mid>`
| :download:`preliminary <downloadables/preliminary.midi>`
| :download:`horror.midi <downloadables/horror.midi>`


References
==========

- [1] https://en.wikipedia.org/wiki/Subject_(music) Retreived 1 Dec 2016, 14:53
- [2] https://en.wikipedia.org/wiki/Motif_(music) Retreived 1 Dec 2016, 14:54
- [3] https://en.wikipedia.org/wiki/Inversion_(music) Retrieved 13 Dec 2016, 16:57
- [4] https://en.wikipedia.org/wiki/Retrograde_(music) Retrieved 13 Dec 2016, 16:59
- [5] https://en.wikipedia.org/wiki/Transposition_(music) Retrieved 13 Dec 2016, 16:59



