# Blog Entries

## Title: Security system not implemented (entry 1)

#### By Conor Tilley

Initially we had wanted to include a security system to our project that would provide security for a number of the systems we would intend to use such as the database on MySQL, Unity (the game engine, that got changed to Pygame) and for the User and AI. We thought this was a good idea to have as sensitive user information would be stored on the database such as passwords and we wanted to protect this information. At the start we thought we would have enough time to be able to implement this as our deadline came up, it was always going to be one of the last things we incorporated into the project as we needed a working system first to provide security to but we were delayed with implementing the security features getting caught up in other aspects of the project.

Our initial idea was to have at least a week to try and implement security features to the systems so we would have time to work out bugs or parts that were not being secured. This would prevent security breaches to our systems and stop peoples sensitive information being stolen and initially we were going to try implement this with each system setup but then saw that at the end would be for the best as it was not the main goal of the project. 

The only challenge we faced for this was the time constrain we were under and so unable to add the security feature. Should be have more time it would possibly be added after we were entirely happy with the setup of the rest of the system. 

From this I feel me and Sam learned to have better time management and to not set too many expectations for ourselves in the project otherwise we would become overwhelmed with work to try and get done in the time frame we made for ourselves and in the long run this would not be beneficial to us.



## Title: AI model (entry 2)

#### By Conor Tilley and Samuel Barnett

Sam can talk about the AI base strategy here (talk about what learned from this)

The AI model can be talked about here, Conor (talk about what learned from this)


## Title: MySQL Database (entry 3)

#### By Conor Tilley

The database in MySQL has undergone many changes since it was made around the time the functional specification was submitted. Originally I created one table and then moved onto six tables.

When I first sourced the data files that are used for the project, I thought about how I would add this information to a table in the database. I tried a few ideas and wrote a script to convert the information into the format of the table I created but it did not capture all the information in the way I wanted and I did not add all the information I wanted also. Then I tried to create several tables each one storing some parts of information from the data files, this worked well being able to capture all the information I wanted to use but then I had problems when I tried to join these tables together to use for the AI model which I wanted to just use one table for. Each table had a different amount of rows so they could not be joined together without the data getting confusing to read and understand. Then I found a public github repository that converted the same files that I was using to a formatted table, but they were adding it to .csv files and using the pandas library import as their database, so I used some of their code to format the information and then was able to add it to my table in MySQL successfully. 

Now that I had one table and in a form I wanted to use I had to convert the rest of the information into numerical values for the AI to be able to read the table, this involved some tweaking of the file I used to convert the information from the .txt file to the sql table. 

Overall the table displays the actions of each person row by row now for each hand in numerical values that the AI can read and understand from now. I believe I improved my SQL skills greatly by doing all this work with the database, tables and scripts to convert the information for the AI. 

## Title: Poker Dataset (entry 4)

#### By Conor Tilley

At the start of the project I was tasked with finding a suitable dataset we could use for our project. At first I thought it would be easy as poker is a massive game on online platforms and in real life. I knew there would be datasets out there, i searched on kaggle, google dataset and github for a suitable dataset but none were ideal as our project is to make a heads up poker AI that is a one on one game and all the datasets that were online were that of tournaments or 6-8 player tables.

Eventually I decided on the pluribus dataset which is a 6 player dataset that actually used another AI that was trained and was playing players live at the time and all the actions were stored to be used by the AI after. The dataset is publicly available so I downloaded it and started working on a script to convert it to a suitable format for the AI as I mentioned in my 3rd data entry. I had to alter the dataset slightly after i checked it to make sure it was clean and not missing any values, I only added the hands to the database where at least 4 players folded before the flop, so that way for the rest of the game it is essentially heads up play against the other player. This was not ideal as it will make the AI weaker but hopefully it can be altered to account for this and wont become too weak. This was the best trade off I could think off as there is no publicly available heads up poker datasets available publicly at the time of making this project

Working with this dataset was interesting to me as I had to learn how to write the script in the way that the information extracted would be put into the correct form to be inserted into the table, I had to learn how to convert values to numerical values from strings or characters as it was taken from the .txt files and then load them into the table once complete.



