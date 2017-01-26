# RoAS - Rosei Automation System.
# Requires Selenium and Chrome Webdriver.
# Copyright (c) 2017 Ravi Teja Gannavarapu.
# Distributed under MIT License.

"""
Inspired from Hibiscus Automation by Ankit Choudhary (B216008) (b216008@iiit-bh.ac.in).
Contact Ravi Teja Gannavarapu (b216023@iiit-bh.ac.in) for further help/information.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os #For os.path.exists, 

#Food codes data. Please note that these codes are no way related to the Roseighara platform and are useful only in this module itself.
titles = ["", "BRF", "LUN", "DIN"]
mon1 = ["MON", "111", "112", "113"]
tue1 = ["TUE", "121", "122", "123"]
wed1 = ["WED", "131", "132", "133"]
thu1 = ["THU", "141", "142", "143"]
fri1 = ["FRI", "151", "152", "153"]
sat1 = ["SAT", "161", "162", "163"]
sun1 = ["SUN", "171", "172", "173"]
mon2 = ["MON", "211", "212", "213"]
tue2 = ["TUE", "221", "222", "223"]
wed2 = ["WED", "231", "232", "233"]
thu2 = ["THU", "241", "242", "243"]
fri2 = ["FRI", "251", "252", "253"]
sat2 = ["SAT", "261", "262", "263"]
sun2 = ["SUN", "271", "272", "273"]
foodcodes1 = [titles, mon1, tue1, wed1, thu1, fri1, sat1, sun1]
foodcodes2 = [titles, mon2, tue2, wed2, thu2, fri2, sat2, sun2]

#The dictionary below (d1) is Roseighara HTML ID's for the selenium webdriver.
d1 = {111:"mess1b1", 121:"mess1b2", 131:"mess1b3", 141:"mess1b4", 151:"mess1b5", 161:"mess1b6", 171:"mess1b7"\
	,112:"mess1l1", 122:"mess1l2", 132:"mess1l3", 142:"mess1l4", 152:"mess1l5", 162:"mess1l6", 172:"mess1l7"\
	,113:"mess1d1", 123:"mess1d2", 133:"mess1d3", 143:"mess1d4", 153:"mess1d5", 163:"mess1d6", 173:"mess1d7"}

#For printing the food codes.
def fcodes():
	print ("Roseighara-1 Food Codes\n")
	for i in foodcodes1:
		for j in i:
			print j + "\t",
		print "\n"
	print ("\nRoseighara-2 Food Codes\n")
	for i in foodcodes2:
		for j in i:
			print j + "\t",
		print "\n"

#For changing the user preferences.
def setprefs():
	uname = raw_input("Enter your username: ")
	pwd = raw_input("\nEnter your password: ")
	fcodes()
	print ("NOTE: Please prefix your food code with V for Veg and N for Non-Veg.\n")
	k = raw_input ("\nEnter your Roseighara 1 food codes in the correct format separated by space in a single line: ")
	g = raw_input ("\nEnter your Roseighara 2 food codes in the correct format separated by space in a single line: ")
	f = open("roseidata.dat", "w")
	f.write(uname)
	f.write("\n")
	f.write(pwd)
	f.write("\n")
	f.write(k)
	f.write("\n")
	f.write(g)
	f.write("\n")
	f.close()
	print ("\n\nPreferences updated!")
	main()

#For calculating the cost.
def cost():
	with open("roseidata.dat", "r") as f:
		b = f.readlines() #Reads from the files and stores each line as list item.
	b = [x.strip() for x in b] #Removes any whitespace characters from the list.
	f.close()
	a = []
	count1 = count2 = 0
	uc1 = b[2].split()
	uc2 = b[3].split()
	for i in uc1:
		if (i[3] == '1'):
			count1+=10
		elif (i[3] == '2' or i[3] == '3'):
			count1+=25
	for j in uc2:
		if (j[3] == '1'):
			count2+=10
		elif (j[3] == '2' or j[3] == '3'):
			count2+=25
	a.append(count1)
	a.append(count2)
	return a

#The main function. Does almost everything.
def main():
	if (os.path.exists("roseidata.dat") == False):
		print ("Preferences/Data file wasn't found. Please set preferences.\n")
		setprefs()
	else:
		with open("roseidata.dat", "r") as f:
			a = f.readlines() #Reads from the files and stores each line as list item.
		a = [x.strip() for x in a] #Removes any whitespace characters from the list.
		f.close()
		username = a[0]
		paword = a[1]
		ufc1 = a[2].split()
		ufc2 = a[3].split()
		ufc = [ufc1, ufc2]
		print ("Preferences file was found. Reading from file.\n")
		c = raw_input("1. Register coupons for the upcoming week.\n2. Change preferences.\n3. View present preferences.\n4. View amount to be paid.\n5. Exit.\n\nEnter your choice: ")
		if (int(c) == 1):
			browser = webdriver.Chrome("chromedriver.exe") #Set the path to the chromedriver executable folder.
			chromeOptions = webdriver.ChromeOptions()
			prefs = {"profile.managed_default_content_settings.images":2} #Prevents images from loading.
			chromeOptions.add_experimental_option("prefs", prefs) #Adds the 'prefs' in the above line to the chrome options.
			browser.get("http://172.16.2.200:8081/rosei/login.jsp")
			uname = browser.find_element_by_name('un')
			pword = browser.find_element_by_name('pw')
			uname.send_keys(username)
			pword.send_keys(paword)
			browser.find_element_by_name('submit').click()
			q = cost(ufc1, ufc2)
			for i in ufc:
				if (i == ufc1 and len(i) != 0):
					browser.get("http://172.16.2.200:8081/rosei/selectmess.jsp")
					browser.find_element_by_id('mess1').click()
					for j in ufc1:
						r = j[1:len(j)]
						g = int(r)
						if (j[0] == "V" or j[0] == "v"):
							for i in range(2):
								browser.find_element_by_id(d1[g]).click()
						elif (j[0] == "N" or j[0] == "n"):
							for i in range(1):
								browser.find_element_by_id (d1[g]).click()
					browser.find_element_by_id('submit').click()
					browser.sleep(5000)
					print ("Roseighara 1 Coupons Booked Successfully!")
				if (i == ufc2 and len(i) != 0):
					browser.get("http://172.16.2.200:8081/rosei/selectmess.jsp")
					browser.find_element_by_id('mess2').click()
					for j in ufc2:
						r = j[1:len(j)]
						g = int(r) - 100 #The goddamn HTML selectors used the same ID.
						if (j[0] == "V" or j[0] == "v"):
							for i in range(2):
								browser.find_element_by_id(d1[g]).click()
						elif (j[0] == "N" or j[0] == "n"):
							for i in range(1):
								browser.find_element_by_id (d1[g]).click()
					browser.find_element_by_id('submit').click()
					browser.sleep(5000)
					print ("Roseighara 2 Coupons Booked Successfully!")
			print ("\nRoseighara 1 Amount: " + str(q[0]))
			print ("\nRoseighara 2 Amount: " + str(q[1]))
			print ("\nTotal Roseighara Amount: " + str(q[0] + q[1]))
			
		elif (int(c) == 2):
			setprefs()
			main()

		elif (int(c) == 3):
			with open("roseidata.dat", "r") as f:
				a = f.readlines() #Reads from the files and stores each line as list item.
			a = [x.strip() for x in a] #Removes any whitespace characters from the list.
			f.close()
			username = a[0]
			paword = a[1]
			ufc1 = a[2].split()
			ufc2 = a[3].split()
			u = cost()
			print ("\nUsername: " + username)
			print ("Password: " + paword)
			print ("Roseighara 1 Food Preferences: " + ''.join(ufc1))
			print ("Roseighara 2 Food Preferences: " + ' '.join(ufc2))
			print ("Roseighara 1 Amount: " + str(u[0]))
			print ("Roseighara 2 Amount: " + str(u[1]))
			print ("Total Roseighara Amount: " + str(u[0] + u[1]))
			print ("\n\n")
			main()
			
		elif (int(c) == 4):
			u = cost()
			print ("Roseighara 1 Amount: " + str(u[0]))
			print ("Roseighara 2 Amount: " + str(u[1]))
			print ("Total Roseighara Amount: " + str(u[0] + u[1]))
			main()
			
		elif (int(c) == 5):
			exit()
			
		else:
			main()

#And finally the main function call.
print ("Welcome to Rosei Automation Tool\n")
main()
