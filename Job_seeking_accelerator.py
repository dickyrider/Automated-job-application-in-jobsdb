#!/usr/bin/env python
# coding: utf-8

# In[616]:


import urllib
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os
import webbrowser


# In[645]:


# Purpose 1. Applying job automation
# Purpose 2. Gathering the 'key words' from recruitment adverisement

# Still in progress.....

# In[642]:


class jobsdb_auto:
    def __init__(self, job, page_range = (1,1), function=0):
        self.job = job
        self.function = function
        
        #Setting url
        if function:
            self.var = (job +' jobs in '+ function).replace(" ", "-")
        else:
            self.var = (job +' jobs').replace(" ", "-")
            
        self.start_page = page_range[0]
        self.end_page = page_range[1] + 1
        self.jobsdb_url = 'https://hk.jobsdb.com/'
        
        #Finding job title, company and website link
        for page in range(self.start_page,self.end_page):
            self.url = (self.jobsdb_url + self.var + f"?page={page}")
            self.page = requests.get(self.url)
            self.soup = BeautifulSoup(self.page.content, "html.parser")
            self.job_titles = self.soup.find_all('article')
            self.companies = self.soup.find_all('a', {'data-automation': 'jobCompany'})
            self.links = self.soup.find_all('a', href=lambda href: href and href.endswith('search-standalone'))
    
    #Listing all the job title and total quantity of job title
    def title(self):
        count = 0
        for job in self.job_titles:
            title = job['aria-label']
            print(title)
            count +=1
        return count
    
    #Listing all the company and total quantity of company
    def com(self):
        count = 0
        
        for job_title in self.job_titles:
            job_company = job_title.find_next('a', {'data-automation': "jobCompany"})
            if job_company:
                print(job_company.text.strip())
                count +=1
            else:
                print('No company name')
                count +=1

        return count
        
    #Listing all the link and total quantity of link
    def web(self):
        count = 0
        for link in self.links:
            print(link['href'])
            count +=1
        return count
    
    # Building a dataframe for job titles, company and link      
    def information(self):
        title_lst = []
        company_lst = []
        link_lst = []
        
        for page in range(self.start_page,self.end_page):
            self.url = (self.jobsdb_url + self.var + f"?page={page}")
            self.page = requests.get(self.url)
            self.soup = BeautifulSoup(self.page.content, "html.parser")
            self.job_titles = self.soup.find_all('a', {'data-automation': "jobTitle"})
            self.companies = self.soup.find_all('a', {'data-automation': 'jobCompany'})
            self.links = self.soup.find_all('a', href=lambda href: href and href.endswith('search-standalone'))
            
            #Using find_next to distingusih which position have no company information
            for job in self.job_titles:
                title_lst.append(job.text.strip())
                job_company = job.find_next('a', {'data-automation': "jobCompany"})
                if job_company:
                    company_lst.append(job_company.text.strip())
                else:
                    company_lst.append('No company information')
            
            for link in self.links:
                jobsdb_url = 'https://hk.jobsdb.com'
                website = jobsdb_url + link['href']
                link_lst.append(website)
            
        self.df = pd.DataFrame({'Job_title':title_lst, 'Company':company_lst, 'Website':link_lst})
        return self.df
    
    #Opening link directly by index from dataframe
    def open_link(self, index):
        
        if not hasattr(self, 'df') or self.df.empty:
                self.information()
                
        
            
        web = 'Website'
        title = 'Job_title'
        com = 'Company'
        link = self.df[web][index]
        webbrowser.open(link)
        print(f'Opening link - {df[web][index]}')
        print(f'Job title: {df[title][index]}')
        print(f'Company: {df[com][index]}')
                


# In[643]:


# Searching 'business analysis' for 1 page
# Building dataframe for page 1 information

job = jobsdb_auto('python， operation',(1,1), function = 'banking-financial-services')
df = job.information()

