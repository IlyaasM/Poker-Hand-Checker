#!/home/pi/software/bin/python3

import cgi, cgitb
import base64
import os
import subprocess
import re
import urllib.request

print("Content-type: text/html\n\n")
cgitb.enable()
form = cgi.FieldStorage()

def isOnePair(card):
    count = 0
    num = 0
    ranks = []
    removed = []
    if len(card) == 5:

        for i in card:
            for j in i:
                num = sum(x.isdigit() for x in i)
            if num == 2:
                rank = i[0:2]
            else:
                rank = i[0]
            ranks.append(rank)
        temp = set(ranks)
        count = list(temp)
        if len(count) == 4:
            return True
        else:
            return False

def isTwoPair(card):
    count = 0
    ranks = []
    removed = []
    if len(card) == 5:
        for i in card:
            for j in i:
                num = sum(x.isdigit() for x in i)
            if num == 2:
                rank = i[0:2]
            else:
                rank = i[0]
            ranks.append(rank)
        temp = set(ranks)
        count = list(temp)
        if len(count) == 3:
            return True
        else:
            return False

def isThreeOfAKind(card):
    count = []
    ranks = []
    removed = []
    if len(card) == 5:
        for i in card:
            for j in i:
                num = sum(x.isdigit() for x in i)
            if num == 2:
                rank = i[0:2]
            else:
                rank = i[0]
            ranks.append(rank)
        # temp = set(ranks)
        # count = list(temp)
        for k in ranks:
            new = ranks.count(k)
            count.append(new)
        if count.count(3) == 3 and len(count) == 5:
            return True
        else:
            return False

def isFourOfAKind(card):
    ranks = []
    if len(card) == 5:
        for i in card:
            for j in i:
                num = sum(x.isdigit() for x in i)
            if num == 2:
                rank = i[0:2]
            else:
                rank = i[0]
            ranks.append(rank)
        temp = set(ranks)
        count = list(temp)
        if ranks.count(count[0]) == 4 or ranks.count(count[1]) == 4:
            return True
        else:
            return False

def isStraight(card):
    ranks = []
    if len(card) == 5:
        for i in card:
            for j in i:
                num = sum(x.isdigit() for x in i)
            if num == 2:
                rank = int(i[0:2])
            else:
                rank = int(i[0])
            ranks.append(rank)
        temp = sorted(ranks)
        for i in range(1, len(temp)):
            if int(temp[i]) != int(temp[i - 1]) + 1:
                return False
        return True
    else:
        return False

def isFlush(card):
    if len(card) == 5:
        suits = []
        for i in card:
            if len(i) == 3:
                suits.append(i[2])
            else:
                suits.append(i[1])
        if suits.count(suits[0]) == 5:
            return True
        else:
            return False
    else:
        return False

def isFullHouse(card):
    if len(card) == 5:
        ranks = []
        cnts = []
        for i in card:
            for j in i:
                num = sum(x.isdigit() for x in i)
            if num == 2:
                rank = i[0:2]
            else:
                rank = i[0]
            ranks.append(rank)
        temp = set(ranks)
        new = list(temp)
        for j in new:
            if j in ranks:
                cnts.append(ranks.count(j))
        if len(cnts) == 2 and 2 in cnts and 3 in cnts:
            return True
        else:
            return False
    else:
        return False

def isStraightFlush(card):
    if len(card) == 5:
        if isFlush(card) and isStraight(card):
            return True
    else:
        return False

def isHighCard(card):
    if len(card) == 5:
        if isOnePair(card) and isTwoPair(card) and isThreeOfAKind(card) and isFourOfAKind(card) and isStraight(card) and isFlush(card) and isFullHouse(card) and isStraightFlush(card):
            print("fix here, and look at cards to see issue")
        else:
            return True
    else:
        return False

def findCategory(card):
    if isStraightFlush(card):
        return "SF"
    elif isFourOfAKind(card):
        return "4K"
    elif isFullHouse(card):
        return "FH"
    elif isFlush(card):
        return "FL"
    elif isStraight(card):
        return "ST"
    elif isThreeOfAKind(card):
        return "3K"
    elif isTwoPair(card):
        return "2P"
    elif isOnePair(card):
        return "1P"
    else:
        return "HC"

def isNumber(card):
    ten = {116: "10"}
    jack = {106: "11"}
    queen = {113: "12"}
    king = {107: "13"}
    ace = {97: "1"} # manual change ace to = low or high
    # letters = ["t","j","q","k","q"]
    newcards = []
    for i in card:
        if i[0].isnumeric():
            newcards.append(i)
        if i[0] == "t":
            new = re.sub(i,i.translate(ten),i)
            newcards.append(new)
        if i[0] == "j":
            new = re.sub(i, i.translate(jack), i)
            newcards.append(new)
        if i[0] == "q":
            new = re.sub(i, i.translate(queen), i)
            newcards.append(new)
        if i[0] == "k":
            new = re.sub(i, i.translate(king), i)
            newcards.append(new)
        if i[0] == "a":
            new = re.sub(i, i.translate(ace), i)
            newcards.append(new)

    return newcards

def display(cat):
    dict = {
        "HC": "HIGH CARD",
        "1P": "1 PAIR",
        "2P": "2 PAIR",
        "3K": "3 OF A KIND",
        "ST": "STRAIGHT",
        "FL": "FLUSH",
        "FH": "FULL HOUSE",
        "4K": "4 OF A KIND",
        "SF": "STRAIGHT FLUSH"
    }
    s = f"<h1>Your Poker Hand represents a {dict[cat]}</h1>"
    return s
def piInfo():
   print(subprocess.check_output("date", shell=True, text=True))
   print("<div>")
   print(subprocess.check_output("ps ax | grep nginx", shell=True, text=True))
   print("<div>")
   print(subprocess.check_output("uname -a", shell=True, text=True))
   print("<div>")
   print(subprocess.check_output("cat /sys/class/net/eth0/address", shell=True, text=True))
   print("<div>")
   print(subprocess.check_output("cat /proc/cpuinfo | tail -5", shell=True, text=True))
   print("<div>")
   print(subprocess.check_output("ifconfig | grep netmask", shell=True, text=True))
   print("<div>")
   print("<div>")
   print("<div>")
   print("<div>")


'''
#url = '../html/Prg550A2.html'
	# Tried to make the cards load onto the same page with code below
	# but it messes up the card image, because it points to a webpage
	#response = urllib.request.urlopen(url)
	#html = response.read().decode('utf-8')
	#print(html)	
	# print("<meta http-equiv='refresh' content='0'>")

'''    

def main():

	if form.getvalue("hand") == None:
		print(f"<h1>NOT ENOUGH CARDS TO CHECK HAND</h1>")
		print("<a href='../imohamed23_PRG550C.223.A2.html'><input type='button' value='GO BACK'></a>")
	else:
	
		deck = form.getvalue("hand")
		hand = isNumber(deck)

		if len(deck) == 5:
			for card in deck:
				print(f"<img src = \"../cards/{card}.png\" style = width = \"70\"height = \"100\">")
			print(display(findCategory(hand)))
			piInfo()
			print(f"<h1>CLICK THIS BUTTON TO SELECT A NEW HAND</h1>")
			print("<a href='../imohamed23_PRG550C.223.A2.html'><input type='button' value='Change Hand'></a>")
		else:
			# <a href = "imohamed23_PRG550C.223.A2.html" ><input type = "button" value = "Reset Cards" style="font-size: 20px;"> </a>
			if len(deck) < 5:
				print(f"<h1>NOT ENOUGH CARDS TO CHECK HAND</h1>")
			else:
				print(f"<h1>SELECTED TOO MANY CARDS</h1>")	
			print("<a href='../imohamed23_PRG550C.223.A2.html'><input type='button' value='GO BACK'></a>")

main()

