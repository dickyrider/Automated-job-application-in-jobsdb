Introduction

Jobsdb_data is an process-accelerated tool designed to shorten the job application process, allowing users to apply for jobs automatically by combining the scheduling tool in window or mac. Finding a new job is not easy in today’s environment. The job market is competitive, and people are busy with their own lives. Most people don’t realize that they deserve a better job. By leveraging the power of automation, users can save time in their job searching and even receive interview invitations without any effort.

Features

Now:
1.	List all the job title and company name from specific page in dataframe format
2.	Account log-in
3.	Open the job description website directly
4.	Apply job rapidly

Future upgrade:
1.	Show the requirement and job description


Usage

•	Search the job

jobsdb_data(job, page = 1, function = None)

#job: Input the requirement to search (for example, business analyst, python and etc.)
#function: Defaulted to none, input the classification which can be found in jobsdb

•	Log in the JobsDB account

jobsdb_data.log_in(account_id,account_pw)

•	Turn the searching result to DataFrame

jobsdb_data.information()

•	Apply Job automatically

jobsdb_data.apply(apply_link, resume = None, expected_salary = None)
#resume: The resume name in your account
#expected_salary: check the employer question
#If the application can not be processed due to unfilled employer question, the result will return to 'Submission fail'
#If the application redirects to the employer's website, the program will not submit the application, and it will return as 'Non-jobsDB application'.





