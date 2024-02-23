# Table of Contents

1. [Introduction](#introduction)
   1. [Overview](#overview)
   2. [Glossary](#glossary)
2. [System Architecture](#system-architecture)
   1. [Pygame](#pygame)
   2. [Poker-AI](#poker-ai)
   3. [Poker-data-files](#poker-data-files)
   4. [MySQL-database](#mysql-database)
   5. [User](#user)
3. [High-Level Design](#high-level-design)
4. [Problems and Resolution](#problems-and-resolution)
5. [Installation Guide](#installation-guide)
  	1. [Steps to install the software](#steps-to-install-the-software)
  	2. [Required software](#required-software)
  	3. [Required hardware](#required-hardware)
6. [Future Work](#future-work)
7. [References](#references)

## Introduction <a name="introduction"></a>

### Overview <a name="overview"></a>

Heads up poker AI and the poker game is  the system that was developed by us. The game interactions including the user interface was created with pygame as compared to our original idea of using Unity, which had a high learning curve to it. We created the game logic using several different .py files, all working together within the same directory. Our main.py file orchestrated all the logic and ran the actual game itself, blitting different assets onto the screen depending on which particular gamestate the game was in. 

The Poker AI was created in python. We used a combination of a base AI strategy alongside a model. The base strategy was coded to produce different responses, depending on different factors in the game, such as the strength of their hand, if the player has raised, as well as how high the blinds are. Probabilities were assigned to these different scenarios to ensure the AI was thoughtful most of the time, but could simultaneously bluff a hand. E.g. The AI might check off a weak pair 95% of the time, but for the other 5% they might do a large raise.The poker AI Model uses data that is stored in a database in SQL on a local server, MySQL was used to create the database, the tables and to insert the data to the tables used for both the AI and poker game. The data had to be cleaned, formatted and converted to numerical values for the AI so a script was created to extract the relevant data from the poker hands in the data files and inserted into the sql tables, with help from Joseph’s public repo who converts the data in a different format but parts still used from this repo for game data processing [1].

The AI use's machine learning to learn from the extracted data and data extracted from the game that a player is currently playing in. Each hand is added to the database which the AI then reads, with the goal to adjust to the players play style and ultimately  beat them. 


(talk more about AI here from work that gets done before Friday deadline).  

### Glossary <a name="glossary"></a>

Define any technical terms used in this document. Only include those with which the reader may not be familiar.


## System Architecture <a name="system-architecture"></a>


System Architecture Diagram
![system architecture diagram](System_architecture_diagram(tech_manual).drawio-2.pdf "System architecture diagram")

Diagram shows how different modules interact with each other. The comments beside the arrows show what can be done or what is done between two modules. It is different to our initial design in a few ways. The database is setup different to how we originally though it would be, we use Pygame instead of Unity due to the high learning curve of Unity and the time constraints we had and we did not implement a security module/ system also due to time constraints. These changes are reflected in the diagram and showcase how the system modules now interact with each other now in our current design.

### Pygame <a name="pygame"></a>
Interacts with the user, AI and poker data files modules. It is the game engine and user interface for the game and is how the user and AI interacts with the game and each other. Also how the data is received from the user and inputted to the database. It's where the data is entered into essentially and then outputted.
Pygame’s graphic libraries allowed us to blit assets onto a screen. We used these assets alongside coded logic to create our playable 2d poker game.

### Poker AI <a name="poker-ai"></a>
The Poker AI module only interacts with the Pygame module. It is loaded into the game when the user starts a new game using Pygame and waits for the user to start then calculates what its action should be based off the user’s. It adjusts its play style over the course of the game using player information stored in the database

### Poker data files <a name="poker-data-files"></a>
This is where all the raw data of previous poker hands is stored from the player to be used by the AI and where all the data files are that the AI is trained and tested on originally. These are then inserted into the database after being formatted

### MySQL database <a name="mysql-database"></a>
Where all the formatted data is held and given to the AI. The database interacts with the AI module giving it the data formatted. Also holds the data for the game that the user and AI are in, constantly giving the received inputs/ data to the AI allowing it to adjust its play style.

### User <a name="user"></a>
The user module interacts with the Pygame module. Interacting with the UI and inputting data to the game. They are still essentially the testers for the AI still as the AI improves as it players the user.



## High-Level Design <a name="high-level-design"></a>

This section should set out the high-level design of the system. It should include system models showing the relationship between system components and the systems and its environment. These might be object-models, DFD, etc. Unlike the design in the Functional Specification, this description must reflect the design of the system as it is demonstrated.

Object Model Diagram
![object model diagram](object_model_diagram(tech_manual).drawio.pdf "Object Model diagram")

This high level model diagram shows how our different systems interact with each other and their relationships to each other. They create a cycle as information is constantly exchanged as it is in inputted it goes to the AI as it develops its strategy. Each system contains attributes which show what they do in the system and better explaining the system in turn.


## Problems and Resolution <a name="problems-and-resolution"></a>

  * One problem we encountered was trying to source a good dataset, many available datasets online were not of professional quality meaning it was just normal poker players. For the AI to be able to play good it had to learn from good players who play according to the maths of the game. We discovered the ‘pluribus’ dataset which was an AI created and played against strong poker players. This dataset would yield the best results when training the AI.
Another problem encountered was setting up that data. That is cleaning the data, formatting the data and converting the information into numerical values so the AI can use it. We had to learn how to convert the poker data to numerical value and then was able to insert it into mySQL database tables we had created.  


  * **Another problem (talk about AI here issues that occurred in training and testing)**


  * An early problem we encountered was the difficulty in using Unity. We thought switching over to Unreal Engine might make things easier, but we found that we were having to constantly look at tutorials to perform the simplest of tasks. After trying to code in a blueprint, we quickly discovered that it would be way too complicated to have to learn so much while under such a time constraint. After doing some research, we discovered Pygame would be a simple solution. There are many reasons why pygame was such a great solution. The main one being its ease of use, as we only had to watch one thirty minute tutorial and the rest figured itself out. Python is such a simple coding language to use with its vast array of libraries. It was essential that our model was created using Python, so its bizarre we overlooked Pygame initially when creating our Functional Specification


## Installation Guide <a name="installation-guide"></a>

### Steps to install the software <a name="steps-to-install-the-software"></a>

1. MySQL Workbench: 
  * The MySQL workbench can be downloaded from here - [here](https://dev.mysql.com/downloads/workbench/)
  * When on the page click the operating system for your device
  * Then select the operating system version for your device
  * Follow the on-screen instructions provided by the SQL software next to complete installation
  * MySQL version 8.0 was used for this project


2. Visual Studio Code (VSCO):
  * VSCO or an IDE can be used for the project just as long as one is installed
  * Link to download VSCO here - [here](https://code.visualstudio.com/download)
  * When on the page select the option for your operating system
  * The on-screen instructions will take you through the rest of the installation after it has been downloaded


3. Python:
  * Python can be installed from here - [here](https://www.python.org/downloads/)
  * When on the site, hover over the downloads and then select the version for your operating system
  * When downloaded follow the on-screen instructions to complete the download
  * Click the option to add Python to your path when installing when asked


4. Pygame:
  * Pygame is a very simple installation that can be done with VSCO
  * Once python is installed open up VSCO or your IDE and in a terminal window type ‘pip install pygame’
  * Then wait for the download to complete and then you can import pygame at the top of your files for use


5. Git:
  * To clone the project repository from our gitlab, git is required on your system first
  * To install Git go here - [here](https://github.com/git-guides/install-git)
  * Follow the on-screen steps and when the download is complete follow the steps that show up

### Required software <a name="required-software"></a>

  * **Pygame** - Pygame’s functionality for handling graphics, sound, input devices, and other game-related tasks, is essential for our Heads Up Poker Game.

  * **MySQL workbench** - Is needed to store the dataset created from the data files,  It is needed for creating the tables that format the dataset and make the data readable and it is also needed for the AI model so it can access the dataset to train and test on. The latest version of the workbench can be downloaded. 
 
  * **Import Libraries** - To create, train and test the AI model different libraries have to be imported that contain different software that is used. They will all be imported for the user as they are in the files so no installation is required just that they remain in the files

  * **Python** -  Is required as the code is written using python and libraries in python are imported and used. Python 3.11 was used during this project

  * **GitHub/ GitLab** - It is used to copy the project repository from our gitlab, you will need it on your device to be able to do this first.

### Required hardware <a name="required-hardware"></a>

  * A single somewhat model laptop or computer is all that is required. If it is an older version of hardware it might not be able to download the required software for this project.
  
## Future Work <a name="future-work"></a>

1. Security considerations were always on our minds for when doing this project but implementing the features would be time consuming and with the time constraints we had due to unaccounted for problems and work taking longer than expected we had to forgo implementing these features. We would like to have the database information secured as it stores important player information that would be both sensitive and private. We would have have sensitive data encrypted and backup our data regularly. We would also have to comply with data privacy laws by making user sensitive information and game data anonymous where is appropriate.

2. Scalability features - As the systems and the player count possibly grow with more gameplay and user information to hold the MySQL database will face storage issues and we will also require more computational resources. We will have to look at solutions such as moving to cloud based services as a means to store all the new incoming information such as AWS. 

3. Bug fixes - There will always be bug fixes that we will want to fix in the future in our code as the more we work on the project the more we would uncover. We would ideally prioritise these and then work on them when works best. We would do tests on different parts of our system over time as we work on them and note the bug(s) that occur from them if any. Git would be used here for version control to track changes and bug fixes and to be able to revert back to a previous version of the project should a bug fix cause sever problems. User feedback would also be taken into account for problems users say they had, this helps us fix bugs we may have missed

4. AI improvement - More complex AI models would be used as we would have more time to train and test them on the available dataset that could possibly be bigger also should we increase the database storage. We would also have time to tweak the parameters of the model, longer to test it and to review the training process by examining graphs and statistics of the model. This more complex model would have more factors than the current model and would be able to adapt quicker to the player’s play style. Data would be collected from players playing our game that would then be further used to test the AI further constantly improving it.

5. User improvement - We would like to further improve the user interface to make it even easier and simpler for the user to interact with the system. This would improve the experience of the user and improve the chances of them returning. Possible tutorials can be implemented and having more setting for the user to allow them to adjust the game to their needs. 



## References <a name="references"></a>

Section will include links to sourced information (i.e. code, text, diagrams etc)

Used to process data files to format for the AI model.
-- [Poker Texas Holdem Bot - Game Data Preprocessing](https://github.com/JosephCottingham/poker-texas-holdem-bot/tree/dev/Game-Data-Preprocessing)

