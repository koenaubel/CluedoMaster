"""
Created on Fri Mar  1 17:03:42 2019

@authors: Jochem & Koen
"""
import sqlite3
import pandas as pd

def NextPlayer(CurrentPlayerNumber , NumberOfPlayers):
    return 1 if CurrentPlayerNumber == NumberOfPlayers else CurrentPlayerNumber + 1

def NextTurn():
    print('')
    print(Player)
    print('')
    PlayerTurn = int(input("Whose turn is it? Give the Player's number: "))
    Location = input('Which location? ')
    Suspect = input('Which suspect? ')
    Weapon = input('Which weapon? ')
    TurnCards = [Location.upper(), Suspect.upper(), Weapon.upper()]

    #Turn.loc[]

    #Show card
    print('')
    PlayerNumber = PlayerTurn
    ShowCard = 'N'
    CardShowed = []
    while ShowCard.upper() == 'N':
        PlayerNumber = NextPlayer(PlayerNumber,NumberOfPlayers)
        PlayerName = Player.loc[PlayerNumber,'Name']
        if PlayerNumber == PlayerTurn:
            print("")
            print('Niemand heeft iets laten zien')
            ShowCard = 'Y'
        else:
            if PlayerNumber == 1:
                CardsToShow = MyCards.intersection(TurnCards)
                if len(CardsToShow) == 0:
                    print("You don't have cards to show")
                elif len(CardsToShow) == 1:
                    print("Please show this card: " + Cards.loc[Cards.Id.isin(CardsToShow)]['Name'].to_string(index=False, header=False))
                    ShowCard = 'Y'
                else:
                    print("Choose one of these cards to show:")
                    print(Cards.loc[Cards.Id.isin(CardsToShow)][['Id', 'Name']].to_string(index=False, header=False))
                    print("")
                    CardShowed = input("Which card did you show? Please enter the code. ")
                    ShowCard = 'Y'
            else:
                ShowCard = input('Does ' + PlayerName + ' show a card (Y/N)? ').upper()

    if PlayerTurn == 1:
        CardShowed = input('which card did you see?')
    return PlayerTurn, TurnCards, ShowCard, PlayerNumber, CardShowed


db = sqlite3.connect('CluedoMaster.db')
cur = db.cursor()

#Load cards

Cards = pd.read_sql('SELECT * FROM Location', db)
Cards = Cards.append(pd.read_sql('SELECT * FROM Suspect', db), ignore_index=True)
Cards = Cards.append(pd.read_sql('SELECT * FROM Weapon', db), ignore_index=True)
Cards = Cards.drop('index', axis=1)

db.close()

Player = []

PlayerCards = pd.DataFrame({'PlayerName': [],
                            'Card':[]})

Turn = pd.DataFrame({'PlayerId': [],
                     'Cards': []})

#Start game

#Input players
NumberOfPlayers = int(input('How many players? '))
print('')
print('Start with your own name.')
for i in range(NumberOfPlayers):
    PlayerName = input('Name of player ' + str(i+1) + ': ')
    Player.loc[i,'Name'] = PlayerName
Player.index += 1

#Input cards
print('')
print(Cards.to_string(index=False, header=False))
MyCards = ''
i = 0
while MyCards.upper() != 'R':
    MyCards = input("Which of these cards do you have? Type 'R' if ready.  ")
    if MyCards.upper() != 'R':
        PlayerCards.loc[i,'PlayerName'] = Player.loc[1,'Name']
        PlayerCards.loc[i,'Card'] = MyCards.upper()
        i = i+1
MyCards = set(PlayerCards.Card)

print('')
print('You have these cards:')
print(Cards.loc[Cards.Id.isin(PlayerCards.Card)].to_string(index = False, header = False))

#Next Turn
EndOfGame = 'N'
while EndOfGame.upper() != 'Y':
    NextTurn()
    EndOfGame = input("Has the game ended (Y/N)? ")

print('')
print('Oke! ik hoop je snel terug te zien bij een volgend potje!')

'''
Hints:
    welke kaarten zijn bekend
    welke kaarten zijn het niet
    Wie heeft welke kaarten
    Wie heeft welke kaarten niet
    welke kaart kun je het beste tonen (al eerder getoond)
    vraag geen kaarten die je al gekregen hebt
    --
    welke kaarten moet ik vragen (AlphaZero)


    --- Hoe bijhouden
    Elke kaart heeft een status: bekend (wie heeft hem), onbekend (wie heeft hem niet), oplossing
    Owner (0 of 1 NameId), NotOwner (list of nameIds), PossibleOwnersCount, Probability

'''
