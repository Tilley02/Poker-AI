<a name="br1"></a> 

**Functional Specification**

COMSCI - CA326 - Heads-up Poker Game

Due Date: 1/12/23

**Student Name**

**Student ID**

21342951

21307283

Sam Barnett

Conor Tilley

**Table of Contents**

Page Number

(2)

1\. Introduction

1\.1. Overview

1\.2. Business Context

1\.3. Glossary

2\. General Description

2\.1. Product/System functions

(3)

2\.2. User Characteristics and Objectives

2\.3. Operational Scenarios

2\.4. Constraints

3\. Functional Requirements

4\. System Architecture

5\. High-Level Design

6\. Preliminary Schedule

4\. Appendix

(6)

(9)

(11)

(12)

(14)

1



<a name="br2"></a> 

1\. Introduction

1\.1 Overview

The system is a poker AI that will play against a human player in a head-on-head style

progressively getting better the more hands are played until ultimately it can beat the player in a

game. The blinds increase as the game goes on, the AI starts off with a general playing method then

the AI understands how the player plays as the game goes on and adjusts how it plays then. This is

useful for players of all levels in poker as they can learn how the AI played and how it made its

reading on a player or if someone just wants to play poker to pass some time. The AI will be able to

play poker like normal, e.g. check, call, raise or fold and play based on the cards shown to both

players. Unity will be used for the user interface (UI) of the AI and this will then work with the

poker game we create.

1\.2 Business Context

Many online poker sites are interested in AI poker to be used to detect cheaters or fraud. Some of

these would be the World Series of Poker or America’s card room. The World Series of Poker

(WSOP) is a series of poker games held annually in Las Vegas. It has been on since 1970 where

only a limited amount could enter but now is open to anyone who pays the entry fee. There is one

overall winner at the end of the tournament who is given the title of World Champion of Poker. It

became popular over time from players winning from spectacular scenarios such as a player who

entered online, made it to the main event as an underdog and ended up winning the title, this helped

online poker massively as many people heard about this and signed up to WSOP’s online poker site.

WSOP would use AI to help in many aspects such as recreating scenarios for players to analyse, AI

to help players improve, be used to help plan the WSOP such as dates, tables and the prize pool.

1\.3 Glossary

●

●

●

●

User Interface - UI

Structured Query Language - SQL

Artificial Intelligence - AI

Random Number Generation - RNG

2



<a name="br3"></a> 

2\. General Description

2\.1 Product / System Functions

The general functionality of the system is shown as functions here that can be talked about more in

section 3. More may be added should we see fit.

●

●

●

●

Sign up, then add to the database

Log in

Edit profile

View past stats (i.e if won or lost money in the game, how long the game was, amount

started with)

●

●

●

●

●

●

Main page

Contact page

Help page

Continue game

New game (set constraints i.e difficulty, time limit, starting amount)

End game

2\.2 User Characteristics and Objectives

The user community for a poker site is available to anyone who has a computer/ laptop and

internet access. Generally, a person who can access a poker site is familiar with a computer

and using general software systems so for them to operate on this site would be easy to pick

up. The site will still be made in a user-friendly fashion making it easy for a person to

navigate through it and know what they are doing. The user when they first go onto the site

will be asked to sign up and create a profile, after which they will be sent to our main page,

from there they will be able to go into a game against our AI which will be clearly visible

from the main page they get sent to.

**Wish list:**

A possible tutorial of how the page works and where everything is might be added should we have

time, for when a new user first joins. Informs the user how the AI works as you play it.

We hope to have the site laid out very clearly so a user knows where everything is and how the site

works within a few minutes of joining. This will be achieved only at the end when we are polishing

up everything to make the site user-friendly.

3



<a name="br4"></a> 

2\.3 Operational Scenarios

●

Unregistered user:

○

If it is the user’s first time on the site they will have to sign up and create a

profile before they can access anything, they will have to enter info to create

their profile and get them setup into the database

○

They will have limit functionality on the site if they do not sign up first, such

as not being able to play or go onto the help page

●

Registered user (not logged in):

○

If a registered user is not logged in yet when they enter the site again they

will also have limited functionality on the site as the unregistered user

would.

○

The registered user will only have to log in to the site by entering either their

username or email and their password.

●

●

Registered user (logged in):

When a user is then logged in they have access to the site and what it offers,

○

they will be able to play a game, go onto the help page or contact us page

etc.

Contact us page:

When a user experiences a problem such as not being able to enter a game

○

due to not being logged in even if they are, they will be able to enter the

contact us page or the help page and view/ enter an inquiry about their

problem. The user will either be able to look up their problem and solve it

themselves or contact us about what the problem is and send an email to let

us know.

●

Playing a game:

○

When a user clicks on to play a game they will first be asked about the

constraints (rules) they would like to play with and their starting amount.

From there they can click to start a game where they will enter a poker table

in a head-on-head against our poker AI.

○

4



<a name="br5"></a> 

2\.4 Constraints

**Time Constraint:**

●

The project is due on the 23rd of February where it should ideally be complete and

functional. The deadline for the Function Specification is also due on the 1st of December.

Will we be able to understand and implement everything we must do for the overall project

such as user requirements.

●

**Database Storage:**

Limit storage on mySQL account, unsure how many people will be able to sign up to the

●

site until we run out of storage as info will also be saved about the person such as their

games played and win/loss etc.

**Fair play on site (Industry protocol):**

●

We must ensure that our site is fair to the user i.e. RNG for the deck of cards, will inform

the user we are fair when they first join.

●

●

We must follow the rules of the country we are in for online gambling

Have customer support should a user feel they are treated unfairly

**Training and Testing:**

To train and test our AI will be timely and potentially trained incorrectly, we must have a

●

large enough data set available to be able to train the model we create and test it after to

ensure we get the results we require. This could also be costly if we must do this over a

period of time.

5



<a name="br6"></a> 

3\. Functional Requirements

**Game Logic**

This will be the core functionality of the game. The rules of Heads-Up Poker will have to be

implemented, including increasing blinds, betting rounds, hand rankings, card shuffling, card

dealing etc.

This requirement is essential, as it forms the foundation for our project. Its implementation is

imperative for our other requirements to function correctly.

One potential technical issue with this requirement could be game logic not functioning as intended.

For example, an issue in the card ranking mechanism could lead to an incorrect outcome in a poker

round. Issues may also arise from ineffective error handling, which could lead to severe issues in

the gameplay.

This requirement is central to our entire project, as every other aspect hinges on its precise

implementation. It acts as the string that holds our game together, with all subsequent requirements

depending on its accuracy and reliability.

**AI Opponent**

The AI opponent requirement involves the integration of an intelligent computer-controlled

opponent in our game. This AI should possess the ability to analyse player behaviour, and make

strategic decisions, all while evolving its playstyle over time. The overall objective of it is to

provide each player with a dynamic experience in response to their own unique playstyle.

The AI opponent is a pivotal component of our game. Without it, the player won’t be able to engage

in our poker game. Its adaptive nature helps to ensure the game remains engaging, and introduces a

level of difficulty, no matter the skill level of the player. It must strike a balance between being

challenging, while not compromising the overall enjoyment of the player.

Many technical issues could arise from the implementation of our AI, such as its decision-making

algorithm making sub-optimal decisions. It may also come up with an inaccurate representation of a

player’s playstyle, leading to an unsuitable adaptation. Optimisation of our AI may also produce its

own difficulties. We must ensure its real-time responsiveness doesn’t compromise the overall

efficiency of the game. The player shouldn't have to wait for the AI to make decisions. Due to the

possible complexity of the AI, this may prove to be problematic.

The AI opponent is intricately connected with the Game Logic requirement. It relies on an accurate

implementation of the rules of Heads-Up Poker, to make informed decisions. Therefore, the

successful implementation of our AI is dependent on a well-established game logic implementation.

Additionally, the AI will interact closely with the User Interface requirement, as the player needs

clear and informative feedback on the AI’s actions for a satisfying experience in our game.

6



<a name="br7"></a> 

**User Interface**

The User Interface requirement is centred on crafting an intuitive and visually appealing interaction

platform for players to interact within the Heads-Up Poker game. This will involve designing game

elements such as chip count, player hand, betting options and community cards, which all must be

presented in a way that enhances player experience. The UI should support easy navigation and

provide clear communication of game information.

The User Interface is a major factor of our game as it's directly responsible for how players will

interact with and perceive the game. A well-designed UI will contribute significantly to the

satisfaction of users and ease of the gameplay. It serves as the bridge between player and game

mechanics.

Implementing an effective UI could spawn a host of technical challenges, such as unclear visual

elements, difficult navigation and potential performance optimization issues. Providing effective

real-time updates may also prove to be difficult, particularly during phases such as betting rounds

and card shuffling.

The User Interface is closely intertwined with the Game Logic requirement. It relies on accurate and

timely information from the Game Logic to present relevant and correct game elements. The UI will

also support the AI Opponent requirement by providing a medium for players to understand and

respond to the AI’s actions.

**Player Profile**

The Player Profile requirement involves creating individual profiles for players within our Heads-up

Poker game. This profile will be a personalised space that will offer an overview of a user's

statistics and playstyle.

A Player’s Profile will be critical for enhancing a player’s experience, as they will be able to review

their performances and potentially adapt their playstyle based on historical data,

Technical issues may arise from implementing player profiles, We will have to take careful

consideration in how we approach data storage and our information retrieval mechanisms.

We will have to ensure that we have an efficient algorithm in place, as failure to achieve this may

result in poor performance of our game. Getting our system to handle profile updates and

synchronisation may also prove to be a significant hurdle for us.

This requirement is paramount for our AI opponent to function correctly. The AI will analyse player

behaviour which will be stored in their profile to tailor its strategy, so it is imperative for our player

profile implementation to be both accurate and efficient. Additionally, the User Interface

requirement will depend on the Player Profile for it to be able to display relevant information about

a user.

7



<a name="br8"></a> 

**Security**

The Security requirement is essential for ensuring the secure storage of player data. It involves the

encryption of data transfer, as well as protecting against potential exploits in our game.

Security is critical for maintaining the integrity of player profiles, and upholding the overall

credibility of the game.

Security implementations could cause many technical issues. One such issue could arise from the

handling of player data. We will have to continuously monitor our security implementations to

ensure data transfer is completely encrypted. Failure to create an effective method of storing and

retrieving player data will corrupt both our game’s integrity and safety.

The Security Requirement is closely linked with the Game Logic and AI opponent requirements. It

requires our Game Logic to be sound in order to ensure fairness in our game by preventing any

attempts at cheating. It is also imperative for our Player Profile requirement, as it safeguards the

secure storage and retrieval of player data. Furthermore, it contributes to the stability of the User

Interface by preventing any security-related disruptions.

**Audio and Visuals**

The Audio and Visuals requirement is focused on enhancing the engaging/immersive nature of our

Heads-Up Poker game. It involves designing visually appealing graphics, animations and

incorporating audio elements to give our game more personality.

The Audio and Visual requirement, while not nearly as critical as some of the previous

requirements, still serves an important role in enhancing player engagement, and improving the

overall enjoyability of the game. Well-designed visuals will create an immersive environment, with

audio elements providing an element of feedback for the player.

A technical issue that could potentially arise from implementing visuals and animations, could be in

the efficiency of the game. If these elements are not optimised suitably, it could inadvertently lessen

the enjoyment of the game through lag, so it is essential we implement these elements competently.

The Audio and visuals requirements are connected heavily with the User Interface, Game Logic and

AI Opponent requirements. For the User Interface, well-designed visual and audio elements

contribute to the clarity and aesthetic appeal of the gaming environment. The Game Logic

requirement is crucial for ensuring the visual elements accurately represent the state of the game.

Additionally, we can use visual elements to represent the AI Opponent’s actions.

8



<a name="br9"></a> 

4\. System Architecture

The system architecture diagram demonstrates how different modules interact with each other.

Components that are third party or use third party software are highlighted such as the security

module which will use third party software for email verification. The comments beside the arrows

show what can be done or what is done between two modules such as Unity updates AI this means

it tells the AI what the user’s move was and other info such as amount bet etc to help it get a read on

the player

4\.1 Unity:

Interacts with the User and the Poker AI. Will be the UI for the game and how the user and AI will

interact with each other and the game. Will show the poker game, and how the user will log in, edit

their profile and start, continue or end a game. Is also the game engine so it will run the game as

well. It informs the AI when the user does something with information such as how long the user

took, the amount bet etc. The AI then does its move and tells Unity which in turn tells the user

9



<a name="br10"></a> 

4\.2 Poker AI:

Interacts with the Unity game engine, the database and the Security Module. Is loaded into the game

when a user starts a new game and waits for the user to move first. Over time as Unity provides

information on how the user plays it builds a profile on the user to see what type of player they are

and will use this to try to beat the user. It uses to database to train and test itself based on the dataset

from the database

4\.3 Security Module:

Interacts with the Poker AI, the User and the database. Provides security for the database protecting

users’ information, provides security for people signing up to the sight with validity checks,

provides security to the user such as keeping them safe from malware or viruses and provides

security for the Poker AI code and information

4\.4 MySQL database:

Interacts with Unity game engine, the user and the Poker AI. This is where all the data will be

stored in relation to our poker AI, the users on our site and information on games they played, their

profile information and the current game(s) they are playing in currently. It stores the data for the

Poker AI also.

4\.5 User:

Is who will interact with the database and the Unity game engine to start the game and play against

the AI. They are essentially the testers for the Poker AI as the AI will improve the more players it

plays against but will start with basic poker moves as it gets a read on the player.

10



<a name="br11"></a> 

5\. High-Level Design

Object model

Here is a high-level object model diagram of how our system will work with the Poker AI. The

diagram shows how the system interacts with each component in it and the relation between each

component i.e. is it a one-way relation noted by the arrow in only one direction and if it is a

two-way relation shown by the arrow in both directions. Small text boxes are also added to give a

small bit of information on what is happening in the relation or the component itself.

11



<a name="br12"></a> 

6\. Preliminary Schedule

**1. Set up Game Logic using Unity**

The game serves as the base for our project. We must first set up this foundation in order to

be able to create our AI model, User Interface and Security Requirements. This will require

a suitable Graphics Processing Unit (GPU) and Central Processing Unit (CPU).

**2. Set up SQL database**

We will have to establish a MySQL database to store critical information such as player

profiles, game states and all other relevant data. We will also use MySQL to define

relationships within our database and retrieve information during gameplay.

**3. Implement a User Interface**

We will require a suitable user interface in order to be able to interact effectively with our

game. This can be rather basic at first to allow us to work on other implementations such as

the AI model. The interface should be able to facilitate communication between the AI and

game logic.

**4. Create a Base AI with a Set Playstyle**

Our first implementation of an AI will have a predefined playstyle. This initial AI will act

as a starting point for training. It’s strategy should be simple, making it simpler to observe

and understand its decisions during the training process

**5. Collect Data**

We will allow the AI to play against itself in the game environment. We will then collect

data on the actions taken by the AI, and the outcome of each of those decisions. We can

then use this dataset for training the machine learning model.

**6. Tensorflow**

We will then implement TensorFlow into our project. We will use it to design and train our

model using the data we collected previously. The model should then be able to learn from

gameplay data to improve its decision-making abilities over time. We should eventually

introduce an iterative training process to allow the AI to continually play against itself, and

refine its ability.

**7. Implement Security Features**

We will have to implement security features to safeguard player data, game integrity and

system resources. This includes encryption mechanisms for protecting data during transfer.

12



<a name="br13"></a> 

**8. Testing/evaluation**

We must ensure the AI is able to adapt its behaviour based on unique player playstyles. In

order to train the AI to do this, we must have it play against different human players. These

players must ensure they are using different strategies and play styles each time. We can use

this testing environment to assess the AI performance and refine the model if necessary.

13



<a name="br14"></a> 

7\. Appendices

●

System Architecture introduction -

<https://www.edrawsoft.com/article/system-architecture-diagram.html>

MySQL - <https://www.mysql.com/>

How poker works - <https://www.pokernews.com/poker-rules/>

Train and test AI -

●

●

●

[https://www.transcribeme.com/blog/what-is-ai-training-data/#:~:text=First%20and%20forem](https://www.transcribeme.com/blog/what-is-ai-training-data/#:~:text=First%20and%20foremost%2C%20training%20data,when%20faced%20with%20new%20data.)

[ost%2C%20training%20data,when%20faced%20with%20new%20data](https://www.transcribeme.com/blog/what-is-ai-training-data/#:~:text=First%20and%20foremost%2C%20training%20data,when%20faced%20with%20new%20data.)[.](https://www.transcribeme.com/blog/what-is-ai-training-data/#:~:text=First%20and%20foremost%2C%20training%20data,when%20faced%20with%20new%20data.)

14

