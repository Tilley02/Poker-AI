# Table of Contents

1. [Introduction](#introduction)
   1. [Overview](#overview)
   2. [Glossary](#glossary)
2. [System Architecture](#system-architecture)
3. [High-Level Design](#high-level-design)
4. [Problems and Resolution](#problems-and-resolution)
5. [Installation Guide](#installation-guide)
6. [Future Work](#future-work)
7. [References](#references)

## Introduction <a name="introduction"></a>

### Overview <a name="overview"></a>

Provides a brief (half page) overview of the system/product that was developed. Include a description of how it works with other systems (if appropriate).


The heads up poker AI and poker game is the system that was developed by us. The game interactions including the user interface was created with pygame as compared to our original idea of using Unity, which had a high learning curb to it.(Sam can talk more about game and user interface here, can remove this when done)

and the poker AI was created in python. The poker AI uses data that is stored in a database in SQL on a localserver, MySQL was used to create the database, the tables and to insert the data to the tables used for both the AI and poker game. The data had to be cleaned, formatted and converted to numerical values for the AI so a script was created to extract the relevent data from the poker hands in the data files and inserted into the sql tables. (see if can add more to this)

The AI use's machine learning to learn from the extracted data and data extracted from the game that a player is currently playing in. Each hand is added to the database which the AI then reads, with the goal to adjust to the players playstyle and beat them. (talk more about AI here from work that get done before Friday deadline). 

### Glossary <a name="glossary"></a>

Define any technical terms used in this document. Only include those with which the reader may not be familiar.

## System Architecture <a name="system-architecture"></a>

This section describes the high-level overview of the system architecture, showing the distribution functions across (potential) system modules. Architectural components that are reused or 3rd party should be highlighted. Unlike the architecture in the Functional Specification, this description must reflect the design components of the system as it is demonstrated.


![system architecture diagram](System_architecture_diagram(tech_manual).drawio-2.pdf "System architecture diagram")


## High-Level Design <a name="high-level-design"></a>

This section should set out the high-level design of the system. It should include system models showing the relationship between system components and the systems and its environment. These might be object-models, DFD, etc. Unlike the design in the Functional Specification, this description must reflect the design of the system as it is demonstrated.

## Problems and Resolution <a name="problems-and-resolution"></a>

This section should include a description of any major problems encountered during the design and implementation of the system and the actions that were taken to resolve them.

Talk about data preprocessing problems here i.e. the problems with getting data, setting up tables, formatting etc.

## Installation Guide <a name="installation-guide"></a>

This is a 1 to 2 page section which contains a step-by-step software installation guide. It should include a detailed description of the steps necessary to install the software, a list of all required software, components, versions, hardware, etc.

## Future Work <a name="future-work"></a>

Possible section to add in tbd

Discuss potential future enhancements or extensions to the poker AI system. This could include improving the AI's strategy, incorporating more advanced machine learning techniques, etc.


## References <a name="references"></a>

Section will include links to sourced information (i.e. code, text, diagrams etc)

Used to process data files to format for the AI model.
-- [Poker Texas Holdem Bot - Game Data Preprocessing](https://github.com/JosephCottingham/poker-texas-holdem-bot/tree/dev/Game-Data-Preprocessing)

