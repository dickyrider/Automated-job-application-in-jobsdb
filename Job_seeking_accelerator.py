#!/usr/bin/env python
# coding: utf-8

# In[616]:


import urllib
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pandas as pd
import os
import webbrowser
import time
import notion_df


class jobsdb_auto:
    def __init__(self, job, page = 1, function = None):
        self.job = job
        self.function = function
        self.driver = None
        
        #Setting url
        if function:
            self.var = (job +' jobs in '+ function).replace(" ", "-")
        else:
            self.var = (job +' jobs').replace(" ", "-")
            

        self.jobsdb_url = 'https://hk.jobsdb.com/'
        
        #Finding job title, company and website link

        self.url = (self.jobsdb_url + self.var + f"?page={page}")
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.job_titles = self.soup.find_all('article')
        self.companies = self.soup.find_all('a', {'data-automation': 'jobCompany'})
        self.links = self.soup.find_all('a', {'data-automation': "job-list-view-job-link"})
     
    #Log in the account
    
    def log_in(self,account_id,account_pw):
        
        #Find the log in page
        url = 'https://hk.jobsdb.com'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        find_log_in = soup.find_all('a', {'data-automation': 'dashboardSignIn'})
        link = [ url + i['href'] for i in find_log_in][0]
        


        #Open the automated browser
        self.driver = webdriver.Edge()
        self.driver.get(link)
    
        #Input the id and password to log in

        email_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'emailAddress')))
        email_input.send_keys(acc_id)
        
        pw_input = self.driver.find_element(By.ID, 'password')
        pw_input.send_keys(acc_pw) 
    
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-cy="login"]')
        login_button.click()

        try:
            WebDriverWait(self.driver, 10).until(EC.url_changes(self.driver.current_url))
            print ('Log-in completed' )
            
        #TimeoutException due to invaid email or password
        except TimeoutException:
            raise LogInFail()    
        
    # Building a dataframe for job titles, company and link      
    def information(self):
        title_lst = []
        company_lst = []
        link_lst = []
            
        #Using find_next to distingusih which position have no company information
        for job in self.job_titles:
            title_lst.append(job['aria-label'])
            job_company = None
            job_company = job.find_next('a', {'data-automation': "jobCompany"})
            if job_company != None:
                company_lst.append(job_company.text.strip())
                
            # if the company name cannot be found, it is hided in the job ad
            else:
                company_lst.append('confidential')
            
        for link in self.links:
            jobsdb_url = 'https://hk.jobsdb.com'
            website = jobsdb_url + link['href']
            link_lst.append(website)
            
        self.df = pd.DataFrame({'Job_title':title_lst, 'Company':company_lst, 'Website':link_lst})
        return self.df
        
    #Apply job automatively    
    def apply(self, apply_link, resume = None, expected_salary = None):
                
        url = apply_link
        
        apply_page = requests.get(url)
        apply_soup = BeautifulSoup(apply_page.content, "html.parser")
        links = apply_soup.find_all('a', {'data-automation': 'job-detail-apply'})
        
        for link in links:
            link_detail = link['href']
            
        apply_url = self.jobsdb_url[:-1] + link_detail
        
        self.driver.get(apply_url)
        
        #Detect whether the application website is JobsDB or not
        try:
            if resume == None:
                pass
            
            elif resume != None and resume != False:
                resume_select_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, ":r3:"))
                )
                resume_select_button.click()
                resume_select = Select(select_element)
                resume_select.select_by_visible_text(resume)
            elif resume == False:
                resume_select_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "resume-method-:r8:_2"))
                )
                resume_select_button.click()
                
            no_cv_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "coverLetter-method-:r4:_2"))
            )
            no_cv_button.click()
            continue_button(self)
                
                
        except TimeoutException as e:
            print("The application is directed to the company's own website.")
            return("Non-jobsDB application")
            
        if expected_salary == None:
            pass
        else:
            select_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "question-HK_Q_3292_V_1"))
            )
            expected_salary_select = Select(select_element)
            expected_salary_select.select_by_visible_text(expected_salary)
            
        continue_button(self)
        try:
            continue_button(self)
        except TimeoutException:
            pass
        
        try:
            submit_button(self)
        except TimeoutException:
            return submittion_fail()

        return application_submitted()
    

            
                    

        
        
#define continue button function       
def continue_button(self):
    button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="continue-button"]'))
    )
    button.click()

#define submit button function 
def submit_button(self):
    button = WebDriverWait(self.
                            driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="review-submit-application"]'))
    )
    button.click()

class LogInFail(Exception):
    def __init__(self, message = 'Invaild account email or password'):
        super().__init__(message)    
    
def submittion_fail():
    print('Submittion fail')
    print('Employer question(s) is not yet anwsered')
    return('Submittion fail')

def application_submitted():
    print('Application submitted')
    return('Application submitted')
               

