# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3 as lite
import sys

con = None

class AutodataPipeline(object):

	def __init__(self):
		self.setupDBCon()
		self.createTables()
		

	def process_item(self, item, spider):
		self.storeInDb(item)

		return item

	def storeInDb(self, item):
		self.storePromoterInfoInDb(item)

	def storePromoterInfoInDb(self, item):
		self.cur.execute("INSERT INTO Promoters(\
			company_name , \
			city , \
			company_type , \
			contact_number , \
			company_website \
			) \
		VALUES( ?, ?, ?, ?, ?)", \
		( \
			item.get('companyName', ''),
			item.get('city', ''), 
			item.get('companyType','-'), 
			item.get('contactNumber','-'),
			item.get('companyWebsite', '-')
		))
		self.con.commit()  

	def setupDBCon(self):
		self.con = lite.connect('autoAncillary151to218.db')
		self.cur = self.con.cursor()
  			

	# def stripHTML(self, string):
	# 	tagStripper = MLStripper()
	# 	tagStripper.feed(string)
	# 	return tagStripper.get_data()

	# this is the class destructor. It will get called automaticly by python's garbage collecter once this class is no longer used. 
	def __del__(self):
		self.closeDB()

	# I'm currently droping the tables if they exist before I run the script each time, so that
	# I don't get duplicate info. 
	def createTables(self):
		self.dropPromotersTable()

		self.createPromotersTable()


	def createPromotersTable(self):
		self.cur.execute("CREATE TABLE IF NOT EXISTS Promoters(id INTEGER PRIMARY KEY NOT NULL, \
			company_name TEXT, \
			city TEXT, \
			company_type TEXT, \
			contact_number TEXT, \
			company_website TEXT \
			)")

	def dropPromotersTable(self):
		self.cur.execute("DROP TABLE IF EXISTS Promoters")

	def closeDB(self):
		self.con.close()



# from HTMLParser import HTMLParser

# class MLStripper(HTMLParser):
#     def __init__(self):
#         self.reset()
#         self.fed = []
#     def handle_data(self, d):
#         self.fed.append(d)
#     def get_data(self):
#         return ''.join(self.fed)
