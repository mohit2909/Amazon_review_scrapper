import urllib2
from bs4 import BeautifulSoup
import re
import json
import io
from time import sleep
import sys
def get_title(page):
	soup= BeautifulSoup(page, 'html.parser')
	title= soup.find('a', class_="a-link-normal").get_text()
	return title

def get_review(soup):
	review=[]
	data= soup.find_all('span', class_='a-size-base review-text')
	for row in data:
		cleanr = re.compile(r'<[^>]+>')
  		cleantext = cleanr.sub(" ", str(row))
		cleantext= cleanr.sub(" ",cleantext)
		review.append(cleantext)

	return review

def get_rating(soup):
	star=[]
	data= soup.find_all('span', class_='a-icon-alt')
	for row in data:
		cleanr = re.compile(r'<[^>]+>')
  		cleantext = cleanr.sub(" ", str(row))
		cleantext= cleanr.sub(" ",cleantext)
		star.append(cleantext)

	i=0;
	while(len(star)>i):
		if star[i]== ' | ':
			star.remove(star[i])
			i-=1	
		i+=1;
	stars=[]
	for row in star:
		words=row.split()
		stars.append(words[0])
	return stars
	
def create_dic(reviews,stars):
	leng=len(reviews)
	i=0
	dictionary=[];
	while(i<leng):
		dictionary.append(json.dumps({'rating': stars[i], 'review': reviews[i]}))
		i+=1;
	return dictionary


#wiki= "https://www.amazon.in/Moto-Plus-Lunar-Grey-64GB/product-reviews/B071HWTHPH/ref=cm_cr_othr_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
if(len(sys.argv)!=2):
	print("Give proper arguments")
	exit()
wiki=sys.argv[1];
wiki=wiki+"&pageNumber="
headers= headers = { 'User-Agent' : 'Mozilla/5.0' }
try:
	page= urllib2.urlopen(wiki+'1','html.parser')
	title= get_title(page)
except:
	print("Error")
	exit()

break_sentence="Sorry, no reviews match your current selections.Try clearing or changing some filters.Show all reviews"
file_obj= open(title,'w');
for i in range(1,6):
	pag=wiki+str(i)
	sleep(3);
	if(i%2==0):
		sleep(2)
	try:
		req= urllib2.Request(wiki+str(i), None, headers) 
		page= urllib2.urlopen(req).read()
		soup= BeautifulSoup(page, 'html.parser')
		br_point= BeautifulSoup(page,"html.parser").find("span" ,class_="a-size-medium");
		if(br_point):
			br_point=br_point.get_text()
			if(br_point==break_sentence):
				break
		
		reviews=get_review(soup)
		stars=get_rating(soup)
		stars= stars[3:3+len(reviews)]
		dictionary=create_dic(reviews,stars)
	
		for row in dictionary:
			file_obj.write(row)
			file_obj.write(',\n')
	except:
		print("Error")
		exit()
file_obj.close()
