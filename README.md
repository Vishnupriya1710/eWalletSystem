# eWalletSystem
## Goals of the Project
### 2.1 Phase I
Create an Enhanced Entity-Relationship Model representing the Entities, the attributes
and its various types. Highlight the structural constraints, participation and whatever
notations required post skimming the description of the Project we are working on.
Moreover, enlist the considerations we adopted to construct the ER diagram.
### 2.2 Phase II
Create the logical design of the WALLET Payment Network by mapping the EER diagram
into the relational schema. Analyze the ER diagram and indicate the entities, their
relationships and attributes.Identify the Primary Keys and Foreign Keys on the Relational
Database schema. Determine the constraints for the relational model.
### 2.3 Phase III
Work on deploying the Application Design of the Wallet Payment Network that
collaborates the end products of Phase I and Phase II. Creation and Population of the
Database Relations is to be ensured, provided that no error or violations of constraints or
properties is encountered. Integration of SQL Querying with the Application Framework,
displaying the development of instances for the functionalities and menus of the Wallet
payment network.

## ER Diagram
![image](https://github.com/Vishnupriya1710/eWalletSystem/assets/41684141/639f91c0-115b-4c78-bda9-e6268b8f17c8)

## Relational Schema
![image](https://github.com/Vishnupriya1710/eWalletSystem/assets/41684141/48ce5fe1-902e-455f-9bb8-5e4aea8b042b)

## Use Cases
* A Beginner Login - Registration Window is ensured to activate new customers to register using the Wallet Application and current customers to perform necessary actions through Login.
* The Wallet User is enabled to the plethora of basic and related options as part of the Main Menu, where he or she can look into their profile (MyWallet Account), Actions to perform (SEND to and REQUEST from), (MyWallet Statements), Search Transactions. If the user has reached task completion, he or she can logout via Sign out option.
* MyWallet Account is expanded to various functionalities where the user can view and modify their account information, their mode of transaction via phone number or email address. Moreover, the user can add or remove bank accounts, keeping an account as primary or default.
* Send to and Request From actions are enabled as options of Main Menu that allow the user to send amount to a user on a phone number or email_address linked to the account where the money can be transferred. If transferred, we enabled a special functionality that ensures the status of receiving money within 15 days. If the destination account user fails to accept the transaction, the transaction will be cancelled and the amount will be credited back to the source account.
* MyWallet Statement Window enables the user to look into variousinteresting functionalities that can display the total amount of money they sent or received in a range of dates or in a specific month with a basic numeric value. Also, the maximum amount transactions that go out or come in per month. Wallet Application can also show the maximum total amount of money sent or received referred to as the BEST USERS from all our Wallet Users.
