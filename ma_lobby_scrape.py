#!/usr/bin/env python
from __future__ import division
import string
import csv 
import urllib2  
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

print 'execfile("/Users/austinc/Desktop/ma_lobby_scrape.py")'

def pause(url):
	try:
		b=urllib2.urlopen(url)
	except:
		print 'except'
		time.sleep(60)
		pause(url)
	return(b)
	
	
def fetch_lobby_bills(yearo):
	writer=csv.writer(open('/Users/austinc/Desktop/lobbied_bills_%s.csv' % (yearo),'wb'),delimiter='*')
	header_row=['Year','Lobbyist_Name','Half','Bill','Position','Client','Spent']
	writer.writerow(header_row)
	browser=webdriver.Firefox()
	for year in range(int(yearo),int(yearo)+1):
		print year
		browser.get("http://www.sec.state.ma.us/LobbyistPublicSearch/")
		elem=browser.find_element_by_name("ctl00$ContentPlaceHolder1$ucSearchCriteriaByType$ddlYear")
		elem.send_keys(str(year))
		elem=browser.find_element_by_name("ctl00$ContentPlaceHolder1$ucSearchCriteriaByType$drpType")
		elem.send_keys("L")
		elem=browser.find_element_by_name("ctl00$ContentPlaceHolder1$btnSearch")
		elem.send_keys("Search" + Keys.RETURN)
		time.sleep(30)
		year_list=browser.page_source
		lobby_finder=re.compile('<tr class="GridItem">(?:.*?)UserType">(.*?)</span>(?:.*?)PeriodId=(.*?)&amp;RefId=(.*?)"(?:.*?)>(.*?)</a>',re.DOTALL)
		lobbyists=lobby_finder.findall(year_list)
		# print lobbyists[:30]
		for lobbyist in lobbyists:
			# print lobbyist
			if "(" in lobbyist[3]:
				edge=[]
				print("EXCLUDED:"),
				print lobbyist
			else:
				print("ACCEPTED:"),
				print lobbyist
				lobbyist_details=get_details(lobbyist)
				for bill in lobbyist_details:
					writer.writerow(bill)
		
		
def get_details(lobbyist):
	details=[]
	url='http://www.sec.state.ma.us/LobbyistPublicSearch/CompleteDisclosure.aspx?PeriodId=%s1&RefId=%s' % (lobbyist[1],lobbyist[2])
	url2='http://www.sec.state.ma.us/LobbyistPublicSearch/CompleteDisclosure.aspx?PeriodId=%s2&RefId=%s' % (lobbyist[1],lobbyist[2])
	detail_finder=re.compile('<tr class="GridItem">(?:.*?)lblBillNumber">(.*?)</span>(?:.*?)lblAgentPosition">(.{3,10})</span>(?:.*?)lblBusinessAssociation">(.*?)</span>\r\n                        </td><td>(.*?)</td>(?:.*?)\$(.*?)\r',re.DOTALL)
	try:
		lobby_page_h1=urllib2.urlopen(url).read()
		details1=detail_finder.findall(lobby_page_h1)
	except: 
		details1=[]
	try:
		lobby_page_h2=urllib2.urlopen(url2).read()
		details2=detail_finder.findall(lobby_page_h2)
	except:
		details2=[]	
	# print "DETAILS1"
	# print details1
	# print "DETAILS2"
	# print details2
	# bill_finder=re.compile('((?:s|b)[\.-:,]{0,1}b[\.-:,]{0,1}[0-9]{1,5}|sb [0-9]{1,5}|senate bill [0-9]{1,5}|house bill [0-9]{1,5}|h.b. [0-9]{1,5}|s.b. [0-9]{1,5}|h.b [0-9]{1,5}|s.b [0-9]{1,5}|h.[0-9]{1,5}|s.[0-9]{1,5}|h[0-9]{1,5}|s[0-9]{1,5}|house [0-9]{1,5}|house[0-9]{1,5}|senate [0-9]{1,5}|senate[0-9]{1,5}|h. [0-9]{1,5}|s. [0-9]{1,5}|hb [0-9]{1,5}|sb [0-9]{1,5})')
	bill_finder=re.compile(r'\b(s|h|senate|house|sen|hou)(?:[\.\-:, #	]{0,2})(?:b|bill|budget|bill number|bill no|number|no|r|resolution){0,1}(?:[\.\-:, #	]{0,2})([0-9]{1,5})')
	for detail in details1:
		bill_holder=bill_finder.findall(detail[0].lower())
		# print bill_holder
		# print detail[0]
		if len(bill_holder)==0:
			# print("NO BILLS H1:"),
			# print detail[0].lower()
			edge=[]
		for bill in bill_holder:
			# print bill
			billz=bill[0]+bill[1]
			# print billz
			billz=billz.replace("senate","s")
			billz=billz.replace("house","h")
			billz=billz.replace("sen","s")
			billz=billz.replace("hou","h")
			if len(billz)==2:
				billz=billz[0]+"0000"+billz[1]
			if len(billz)==3:
				billz=billz[0]+"000"+billz[1:]
			if len(billz)==4:
				billz=billz[0]+"00"+billz[1:]
			if len(billz)==5:
				billz=billz[0]+"0"+billz[1:]
			temp=[]
			temp.append(str(lobbyist[1])) # year
			temp.append(str(lobbyist[3])) # name
			temp.append("1") # half of year
			temp.append(billz) # bill number
			temp.append(detail[1]) # support/oppose/neutral
			temp.append(detail[3]) # Client
			temp.append(float(detail[4].replace(",",""))/len(bill_holder)) # Amount spent
			# temp.append(detail[2]) # legislative contacts
			details.append(temp)
	for detail in details2:
		bill_holder=bill_finder.findall(detail[0].lower())
		# print bill_holder
		# print detail[0]
		if len(bill_holder)==0:
			# print("NO BILLS H2:"),
			# print detail[0].lower()
			edge=[]
		for bill in bill_holder:
			# print bill
			billz=bill[0]+bill[1]
			# print billz
			billz=billz.replace("senate","s")
			billz=billz.replace("house","h")
			billz=billz.replace("sen","s")
			billz=billz.replace("hou","h")
			if len(billz)==2:
				billz=billz[0]+"0000"+billz[1]
			if len(billz)==3:
				billz=billz[0]+"000"+billz[1:]
			if len(billz)==4:
				billz=billz[0]+"00"+billz[1:]
			if len(billz)==5:
				billz=billz[0]+"0"+billz[1:]
			temp=[]
			temp.append(str(lobbyist[1])) # year
			temp.append(str(lobbyist[3])) # name
			temp.append("2") # half of year
			temp.append(billz) # bill number
			temp.append(detail[1]) # support/oppose/neutral
			temp.append(detail[3]) # Client
			temp.append(float(detail[4].replace(",",""))/len(bill_holder)) # Amount spent
			# temp.append(detail[2]) # legislative contacts
			details.append(temp)
	# for test in details:
		# print "TEST"
		# print test
		# for comparison in details:
			# print "COMPARISON"
			# print comparison
			# if test[3]==comparison[3] and test[5]==comparison[5] and test[4]==comparison[4]:
				# test[6]=test[6]+comparison[6]
				# details.remove(comparison)
	for case in details:
		if int(case[6])==0:
			details.remove(case)
	# print lobbyist[3]
	return details
	
def consolidate_year(file):
	# print "AT THE MOMENT, HHI INFO GENERATED BY THIS FUNCTION IS WRONG WRONG WRONG"
	print "BEFORE YOU USE THIS, MAKE SURE THERE ARE NO QUOTES IN THE INPUT FILE"
	reader=csv.reader(open(file),delimiter='*')
	writer=csv.writer(open('/Users/austinc/Desktop/total_lobby.csv','wb'),delimiter=',')
	writer.writerow(['bill','year','support_spent','oppose_spent','neutral_spent','support_hhi','oppose_hhi','neutral_hhi'])
	list=[row for row in reader if len(row)>1]
	# print list
	# print len(list)
	temp=[]
	year=list[1][0]
	for row in list[1:]:
		if float(row[6])>0:
			temp.append(row[3])
	# print temp
	# print set(temp)
	for bill in set(temp):
		bill_support=0
		bill_oppose=0
		bill_neutral=0
		for row in list:
			if row[3]==bill:
				# print row[6]
				if row[4].lower()=="neutral":
					bill_neutral=bill_neutral+float(row[6])
				if row[4].lower()=="support":
					bill_support=bill_support+float(row[6])
				if row[4].lower()=="oppose":
					bill_oppose=bill_oppose+float(row[6])
		# print "SUPPORT"
		# print bill_support
		clients_support_dic={}
		clients_oppose_dic={}
		clients_neutral_dic={}
		for row in list:
			if row[3]==bill and row[4].lower()=="neutral":
				if row[5] in clients_neutral_dic:
					clients_neutral_dic[row[5]]=clients_neutral_dic[row[5]]+float(row[6])
				else:
					clients_neutral_dic[row[5]]=float(row[6])
			if row[3]==bill and row[4].lower()=="support":
				if row[5] in clients_support_dic:
					clients_support_dic[row[5]]=clients_support_dic[row[5]]+float(row[6])
				else:
					clients_support_dic[row[5]]=float(row[6])
			if row[3]==bill and row[4].lower()=="oppose":
				if row[5] in clients_oppose_dic:
					clients_oppose_dic[row[5]]=clients_oppose_dic[row[5]]+float(row[6])
				else:
					clients_oppose_dic[row[5]]=float(row[6])
		print clients_support_dic
		sq_support_shares=0
		sq_oppose_shares=0
		sq_neutral_shares=0
		for client in clients_support_dic:
			if bill_support>0:
				sq_share=(clients_support_dic[client]/bill_support)**2
				sq_support_shares=sq_support_shares+sq_share
		for client in clients_oppose_dic:
			if bill_oppose>0:
				sq_share=(clients_oppose_dic[client]/bill_oppose)**2
				sq_oppose_shares=sq_oppose_shares+sq_share
		for client in clients_neutral_dic:
			if bill_neutral>0:
				sq_share=(clients_neutral_dic[client]/bill_neutral)**2
				sq_neutral_shares=sq_neutral_shares+sq_share
		if sq_support_shares==0:
			sq_support_shares=''
		if sq_oppose_shares==0:
			sq_oppose_shares=''
		if sq_neutral_shares==0:
			sq_neutral_shares=''
		bill_row=[]
		bill_row.append(bill)
		bill_row.append(year)
		bill_row.append(bill_support)
		bill_row.append(bill_oppose)
		bill_row.append(bill_neutral)
		bill_row.append(sq_support_shares)
		bill_row.append(sq_oppose_shares)
		bill_row.append(sq_neutral_shares)
		writer.writerow(bill_row)
			

def fetch_success(file):
	print "THIS NEEDS TO BE REWRITTEN TO GET VOTE DATA"
	reader=csv.reader(open(file,'rU'),delimiter=',')
	writer=csv.writer(open('/Users/austinc/Desktop/ma_lobby_w_results.csv','wb'),delimiter=',')
	writer.writerow(['bill','year','session','support','oppose','neutral','support_hhi','oppose_hhi','neutral_hhi','passed','passed_in_part','substitution_passed','new_draft_passed','republished_passed','study_order_passed','reported_in_part_passed','house_ayes','house_nays','senate_ayes','senate_nays'])
	list=[row for row in reader]
	list=list[1:]
	for bill in list:
		print bill[0]
		if bill[0][0]=='h':
			chamber='House'
		if bill[0][0]=='s':
			chamber='Senate'
		bill_no=int(bill[0][1:])
		url='https://malegislature.gov/Bills/%s/%s/%s%s' % (bill[2],chamber,bill[0][0],bill_no)
		print url
		bill_page=urllib2.urlopen(url).read()
		status=[0,0,0,0,0,0,0,0,0,0,0]
		status_final=iterated_success(bill_page,status)
		print 'result of iterated_success=%s' % (status_final)
		status=[0,0,0,0,0,0,0,0,0,0,0]
		if status_final[0]>0 and status_final[2]==0 and status_final[3]==0 and status_final[4]==0 and status_final[5]==0 and status_final[6]==0:
			if status_final[1]>0:
				status[1]=1
			else:
				status[0]=1
		if status_final[0]>0 and status_final[1]>0:
			status[1]=1
		if status_final[0]>0 and status_final[2]>0:
			status[2]=1
		if status_final[0]>0 and status_final[3]>0:
			status[3]=1
		if status_final[0]>0 and status_final[4]>0:
			status[4]=1
		if status_final[0]>0 and status_final[5]>0:
			status[5]=1
		if status_final[0]>0 and status_final[6]>0:
			status[6]=1
		bill.append(status[0])
		bill.append(status[1])
		bill.append(status[2])
		bill.append(status[3])
		bill.append(status[4])
		bill.append(status[5])
		bill.append(status[6])
		bill.append(status_final[7])
		bill.append(status_final[8])
		bill.append(status_final[9])
		bill.append(status_final[10])
		writer.writerow(bill)
		print bill
		
		
		
def iterated_success(bill,status):
	# print bill
	print status
	if status[0]+status[1]+status[2]+status[3]+status[4]+status[5]+status[6]>20:
		return status
	signed_in_part=re.compile('(Signed (in part) by the Governor)')
	passed=re.compile('(>Chapter [0-9]{1,3} of the Acts of [0-9]{4}<)')
	substitution=re.compile('substituting therefor a bill with the same title, see <a href="/Bills/(.*?)">')
	substitution2=re.compile('New draft substituted, see <a href="/Bills/(.*?)">')
	new_draft=re.compile('Accompanied a new draft, see <a href="/Bills/(.*?)">')
	republished=re.compile('Republished as amended, see <a href="/Bills/(.*?)">')
	study_order=re.compile('Accompanied a study order, see <a href="/Bills/(.*?)">')
	reported_in_part=re.compile('Reported, in part, by <a href="/Bills/(.*?)">')
	vote_taken=re.compile('<td headers="bBranch">(.*?)</td>\r\n                                <td headers="bAction">Enacted - (.*?) YEAS to (.*?) NAYS')
	# print len(passed.findall(bill))
	# print len(substitution.findall(bill))
	# print len(substitution2.findall(bill))
	# print len(new_draft.findall(bill))
	# print len(republished.findall(bill))
	# print len(study_order.findall(bill))
	# print len(reported_in_part.findall(bill))
	if len(passed.findall(bill))>0:
		if len(signed_in_part.findall(bill))>0:
			status[1]=status[1]+1
		else:
			status[0]=status[0]+1
		if len(vote_taken.findall(bill))>0:
			for vote in vote_taken.findall(bill):
				if vote[0]=="House":
					status[7]==vote[1]
					status[8]==vote[2]
				if vote[0]=="House":
					status[9]==vote[1]
					status[10]==vote[2]
		# print 'passed'
		# print status
		return status
	if len(substitution.findall(bill))>0 or len(substitution2.findall(bill))>0:
		status[2]=status[2]+1
		if len(substitution.findall(bill))>0:
			url='https://malegislature.gov/Bills/%s' % (substitution.findall(bill)[0])
		if len(substitution2.findall(bill))>0:
			url='https://malegislature.gov/Bills/%s' % (substitution2.findall(bill)[0])
		bill_page=urllib2.urlopen(url).read()
		# print 'substitution'
		return iterated_success(bill_page,status)
	if len(new_draft.findall(bill))>0:
		status[3]=status[3]+1
		url='https://malegislature.gov/Bills/%s' % (new_draft.findall(bill)[0])
		bill_page=urllib2.urlopen(url).read()
		# print 'new draft'
		return iterated_success(bill_page,status)
	if len(republished.findall(bill))>0:
		status[4]=status[4]+1
		url='https://malegislature.gov/Bills/%s' % (republished.findall(bill)[0])
		bill_page=urllib2.urlopen(url).read()
		# print 'republished'
		return iterated_success(bill_page,status)
	if len(reported_in_part.findall(bill))>0:
		status[6]=status[6]+1
		url='https://malegislature.gov/Bills/%s' % (reported_in_part.findall(bill)[0])
		bill_page=urllib2.urlopen(url).read()
		# print 'reported in part'
		return iterated_success(bill_page,status)
	if len(study_order.findall(bill))>0:
		status[5]=status[5]+1
		url='https://malegislature.gov/Bills/%s' % (study_order.findall(bill)[0])
		bill_page=urllib2.urlopen(url).read()
		# print 'study order'
		return iterated_success(bill_page,status)
	if len(passed.findall(bill))==0 and len(substitution.findall(bill))==0 and len(substitution2.findall(bill))==0 and len(new_draft.findall(bill))==0 and len(republished.findall(bill))==0 and len(study_order.findall(bill))==0 and len(reported_in_part.findall(bill))==0:
		status=[0,0,0,0,0,0,0,0,0,0,0]
		return status
		
		
