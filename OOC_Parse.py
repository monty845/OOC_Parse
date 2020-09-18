# -*- coding: utf-8 -*-
"""
@author: Monty
Created for Casuality of Kurinnaxx
Log Parser - Allows parsing combat log to catch OOC Activity that WCL Misses
Currently Checks:
    Greater Nature Protection Potions
    Nature Protection Potions
    Greater Arcane Protection Potions
    Brilliant Wizzard and Mana Oil usage
    Sapper Usage
    Dynamite Usage
    Resurrections
    Major Mana Potions
    Superior Mana Potions
    Greater Mana Potions
    Dark/Demonic Runes (combined)
    Greater Nature Protection Potions from the end of Sartura to End of Viscidus
    Sappers/Dynamite use during Viscidus
    
Limitations:
    Assumes Viscidus right after Sartura for pre-fight GNPP Tracking
    Assumes C'Thun is last boss, and stops parsing
    No more than 96 players in combat log
"""
import sys

#Combat Log location
f = open('G:\Blizzard\World of Warcraft\_classic_\Logs\WoWCombatLog.txt')
#f = open('G:\Log.txt')
#Location for output
outf = open(G:\Blizzard\World of Warcraft\_classic_\Logs\Parse.csv, "w")
#outf = open('G:\Potion.txt', "w")

#spells to look for
spellIdList = ["7254", "17546", "17549", "25122", "25123", "13241", "23063", "2893", "4987", "21954", "7932", "23786", "20594", "26677", "20770", "20773", "20748", "17531", "17530", "11903", "27869", "16666", "3169", "17534"]
#lip , 17546
#What type of combat log actions to look for
activityList = ["SPELL_CAST_SUCCESS"]

#Allows easy conversion between text and csv
delimiter = ","

#Store players found in log
playerNameList = []

#Arrays to track potion usage per player, mapped to player name list
#should be good up to 96 players, if you have more than that, trim your log
GNPPCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
VGNPPCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
GAPPCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
NPPCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
OilCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
SapperCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
VSapperCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Dynamite = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
VDynamite = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
VPoisonCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Res = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
MMana = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
SMana = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
GMana = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Rune = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIP = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
MHealth = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#Track whether we are in the Viscidus encounter
Visc = 0
ViscG = 0


#Start Parsing Logs
for line in f:

    #Split combat log entry from timestamp
    split = line.split(" ",3)
    entry = split[3]
    entryList = entry.split(",")

    #Log combat start, for reference on pre-pots
    if entryList[0] == "ENCOUNTER_START":
        #outf.write(split[1] + " " + entryList[2] + " - Start" + "\n")    
        if entryList[2].strip('/"') == "Viscidus":
            Visc = 1
    #Log combat end, to split up from next round of pre-potting
    if entryList[0] == "ENCOUNTER_END":
        #outf.write(split[1] + " " + entryList[2] + " - End" + "\n")
        if entryList[2].strip('/"') == "C'thun":
            #ViscG = 1
            #Stop parsing when C'Thun is killed
            break
        if entryList[2].strip('/"') == "Viscidus":
            Visc = 0
            ViscG = 0
            #break
        if entryList[2].strip('/"') == "Battleguard Sartura":
            ViscG = 1

    #Look for all activites defined above
    if entryList[0] in activityList:

        #Check if activity was spell we are interested in
        if entryList[9] in spellIdList:
            
            #Format player name
            source = entryList[2].split("-")
            name = source[0].strip('/"')
            
            #Spell Name Initialization
            spell = "Error"
            
            #Check if player in player array, if not add
            if name not in playerNameList:
                playerNameList.append(name)

            #Find index for player, to use in cast arrays, if new
            #player, would have just been added above
            index = playerNameList.index(name)
        
            #Determine which spell, log and increment counters
            if entryList[9] == "17546":
                spell = "Greater Nature Protection"
                GNPPCount[index] = GNPPCount[index] + 1
                if ViscG == 1:
                    VGNPPCount[index] = VGNPPCount[index] +1
            if entryList[9] == "7254":
                spell = "Nature Protection"
                NPPCount[index] = NPPCount[index] + 1
            if entryList[9] == "17549":
                spell = "Greater Arcane Protection"
                GAPPCount[index] = GAPPCount[index] + 1
            if entryList[9] == "25122":
                spell = "Brilliant Wizard Oil"
                OilCount[index] = OilCount[index] + 1
            if entryList[9] == "25123":
                spell = "Brilliant Mana Oil"
                OilCount[index] = OilCount[index] + 1
            if entryList[9] == "13241":
                spell = "Sapper"
                SapperCount[index] = SapperCount[index] + 1
                if Visc == 1:
                   VSapperCount[index] = VSapperCount[index] + 1            
            if entryList[9] == "23063":
                spell = "Dynamite"
                Dynamite[index] = Dynamite[index] + 1
                if Visc == 1:
                   VDynamite[index] = VDynamite[index] + 1
            #Check for all Spell Id that count as Poison removal
            if entryList[9] in ["2893", "4987", "21954", "7932", "23786", "20594", "26677"]:
                spell = "Misc Posion Removal"
                if Visc == 1:
                    VPoisonCount[index] = VPoisonCount[index] + 1
            if entryList[9] in ["20770", "20773", "20748"]:
                spell = "Rez"
                Res[index] = Res[index] + 1
            if entryList[9] == "17531":
                spell = "Major Mana"
                MMana[index] = MMana[index] + 1
            if entryList[9] == "17530":
                spell = "Superior Mana"
                SMana[index] = SMana[index] + 1
            if entryList[9] == "11903":
                spell = "Greater Mana"
                GMana[index] = GMana[index] + 1
            if entryList[9] in ["27869", "16666"]:
                spell = "Dark/Demonic Rune"
                Rune[index] = Rune[index] + 1
            if entryList[9] in ["3169"]:
                spell = "LIP"
                LIP[index] = LIP[index] + 1
            if entryList[9] in ["17534"]:
                spell = "Mhealth"
                MHealth[index] = MHealth[index] + 1
            
            #Log events in order
            #outf.write(split[1] + " " + name.ljust(14) + " " + spell + "\n")
            

#Summary Header
#outf.write("\n"+"\n")
width = 8
output = "Name".ljust(14) + delimiter
output = output + "GNPP    " + delimiter
output = output + "NPP     " + delimiter
output = output + "GAPP    " + delimiter
output = output + "Oils    " + delimiter
output = output + "Sappper " + delimiter
output = output + "Dynamite" + delimiter
output = output + "VSappper" + delimiter
output = output + "VDynamit" + delimiter
output = output + "VGNP    " + delimiter
output = output + "VCleanse" + delimiter
output = output + "Ress    " + delimiter
output = output + "Maj Mana" + delimiter
output = output + "Sup Mana" + delimiter
output = output + "Gre Mana" + delimiter
output = output + "D/D Rune" + delimiter
output = output + "LIP     " + delimiter
output = output + "MHealth " + "\n"
outf.write(output)

#Loop through player list for cas counts, and output to log
for name in playerNameList:
    index = playerNameList.index(name)
    output = name.ljust(14) + delimiter
    output = output + str(GNPPCount[index]).ljust(width) + delimiter
    output = output + str(NPPCount[index]).ljust(width) + delimiter
    output = output + str(GAPPCount[index]).ljust(width) + delimiter
    output = output + str(OilCount[index]).ljust(width) + delimiter
    output = output + str(SapperCount[index]).ljust(width) + delimiter
    output = output + str(Dynamite[index]).ljust(width) + delimiter
    output = output + str(VSapperCount[index]).ljust(width) + delimiter
    output = output + str(VDynamite[index]).ljust(width) + delimiter
    output = output + str(VGNPPCount[index]).ljust(width) + delimiter
    output = output + str(VPoisonCount[index]).ljust(width) + delimiter
    output = output + str(Res[index]).ljust(width) + delimiter
    output = output + str(MMana[index]).ljust(width) + delimiter
    output = output + str(SMana[index]).ljust(width) + delimiter
    output = output + str(GMana[index]).ljust(width) + delimiter
    output = output + str(Rune[index]).ljust(width) + delimiter
    output = output + str(LIP[index]).ljust(width) + delimiter
    output = output + str(MHealth[index]).ljust(width) + "\n"
    outf.write(output)

outf.close()