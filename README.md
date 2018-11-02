# Overview

The Student Reports Preparer app takes in raw student data and returns reports
based off this data.

## Inputs

The app takes in csv files containing raw data to be analysed for the generation
of the required reports.

## Outputs

The app outputs xls files containing the report data.

## Version

Version Number 1.0  
App last updated 31 October 2018  
Readme last updated 2 November 2018

# Operation

- Place the required, updated data files into the same directory as the app file
- Run the Student_Reports_Preparer.py file from within Spyder or from the command
line
- Select the desired function from the menu
- Provide the names for any required files or press enter to open the Open file 
dialog.

# Functions

Note: Where a required file has text in brackets following it, this text is the
name of the report in the Learning Platform that the data is pulled from.

## Prepare Complete Tutor Only Report

Prepares a report showing the students that have been marked complete by their
tutor but not by the Head Tutor or Manager.

### Required Files

- Users Marked Tutor Only Report (Users marked by tutor but not head tutor or 
manager)

## Prepare Completion Mark Course Group Report

Prepares a report showing the completion status for each student for the columns
of Tutor, Head Tutor and Manager.

### Required Files

- User Completion Mark Report (Users completion mark by course and group)

## Prepare Count of Completions Tutor Group Report

Prepares a report showing the number of students for each tutor group that have
been marked as complete. It only shows students in the Part-time courses.

### Required Files

- Count of Completions Report (Count of completions by tutor and group in courses)

## Prepare Count of Students Per Tutor Report

Prepares a report showing the number of students for each tutor group.

### Required Files

- Count of Students in Tutor Group Report (Count of students per tutor group)

## Prepare Count of Unmarked Assessments Report

Prepares a report showing the number of unmarked assessments for each tutor group.

### Required Files

- Count of Unmarked Assessments per Tutor Report (Count of unmarked assessments
by tutor)

## Prepare Insightly Tags Updates Report

Prepares a number of reports showing the changes that need to be made to Insightly
tags and statistics on the number of students allocated each tag.


## Prepare Last Login Report

Prepares a report stating the last time each student logged into the Learning
Platform.

### Required Files

- Last Login Report (Last login date)

## Prepare Never Logged In Report

Prepares a report showing all of the students that have never logged into the
Learning Platform.

### Required Files

- Never Logged In Report (Students never logged in)

## Prepare Not Logged In Report - 1 Week

Prepares a report showing all of the students that have not logged into the
Learning Platform during the past week. Used to track part-time students.

### Required Files

- Not Logged In Report (Students have not logged in last week)

## Prepare Not Logged In Report - 4 Weeks

Prepares a report showing all of the students that have not logged into the
Learning Platform during the past 4 weeks. Used to track online students.

### Required Files

- Not Logged In Report (Students have not logged in previous 4 weeks)

## Prepare Student Expiry Report - 1 Month

Prepares a report of students that expire from a course in the next month.

### Required Files

- addresses.csv
- Expiry Report (Students expiring this month)

## Prepare Student Expiry Report - 3 Months

Prepares a report of students that expire from a course in the next three months.

### Required Files

- addresses.csv
- Expiry Report (Students expiring next 3 months)

## Prepare Students Not Submitted Report - 2 Weeks

Prepares a report of students that have not made a submission in the last 2 weeks.
Used for tracking part-time student submissions.

### Required Files

- Active Students File
- Student File
- Submissions Made Report (Students submitted work in previous 2 weeks)

## Prepare Students Not Submitted Report - 4 Weeks

Prepares a report of students that have not made a submission in the last 4 weeks.
Used for tracking online student submissions.

### Required Files

- Active Students File
- Student File
- Submissions Made Report (Students submitted work in previous 4 weeks)

## Prepare Submissions Made Report - 2 Weeks

Prepares a report of students that have made a submission in the last 2 weeks.
Used for tracking part-time student submissions.

### Required Files

- Submissions Made Report (Students submitted work in previous 2 weeks)

## Prepare Submissions Made Report - 4 Weeks

Prepares a report of students that have made a submission in the last 4 weeks.
Used for tracking online student submissions.

### Required Files

- Submissions Made Report (Students submitted work in previous 4 weeks)

### Required Files

- Insightly Tags Data (Contact Tag List report from Insightly)
- Last Month Tags (Updated_Tags...csv file from the previous month)
- Student Database Tags
- Submissions (Last submission date (all courses))
- Tutor_IDs.csv

# Files used

## Active Students File

### File Name

active.csv

### Contents

Each student that is active in the Learning Platform (active in a course).

### Structure

CSV file with the StudentID, Student full name and Course. 

### Source

Active students in a course query from the Learning Platform.

## Addresses File

### File Name

addresses.csv

### Contents

Address details of each student in the Student Database.

### Structure

CSV file with the StudentID and Address details for each student. 

### Source

Students table in the Student Database.

## Count of Completions Report

### File Name

countcomp.csv

### Contents

Count of completions for each tutor group in the Learning Platform.

### Structure

CSV file with the Course, Tutor and Completions for each Tutor group in the
Learning Platform.

### Source

Count of completions by tutor and group in courses report from the Learning
Platform.

## Count of Students in Tutor Group Report

### File Name

countstudents.csv

### Contents

Count of students for each tutor group in the Learning Platform.

### Structure

CSV file with the Course, Tutor Group and Number Students for each Tutor group in
the Learning Platform.

### Source

Count of students per tutor group report from the Learning Platform.

## Count of Unmarked Assessments per Tutor Report

### File Name

countunmarked.csv

### Contents

Count of unmarked assessments for each tutor group in the Learning Platform.

### Structure

CSV file with the Course, Tutor and Number assessments for each Tutor group in the
Learning Platform.

### Source

Count of unmarked assessments by tutor report from the Learning Platform.

## Expiry Report

### File Name

1month.csv or 3months.csv

### Contents

Student Expiry Dates from the Learning Platform.

### Structure

CSV file with the StudentID, Student full name, Email, Course and Expiry Date. 

### Source

Expiry report from the Learning Platform. Either 'Students expiring this month'
or 'Students expiring next 3 months'.

## Insightly Tags Data

### File Name

insightly.csv

### Contents

Contact Tag details for each student in Insightly.

### Structure

CSV file with the StudentID, First name, Last name and Contact Tag List. 

### Source

Contact Tag List report from Insightly.

## Last Login Report

### File Name

lastlogin.csv

### Contents

Last login date for students on the Learning Platform.

### Structure

CSV file with the StudentID, Student full name, Tutor, Course, Last Access and
Email. 

### Source

Last login date report from the Learning Platform.

## Last Month Tags

Updated_Tags_xxx.csv where xxx is the timestamp from the previous month's file.

### Contents

Updated Tags for Insightly from the previous month's analysis.

### Structure

CSV file with the StudentID, EnrolmentID, Student full name, CourseID, Tutor and
Updated_Tags. 

### Source

Updated_Tags...csv file from the previous month.

## Never Logged In Report

### File Name

neverlogin.csv

### Contents

Details of students that have never logged into the Learning Platform.

### Structure

CSV file with the StudentID, Student full name, Tutor, Course, Account created,
Report date and Email. 

### Source

Students never logged in report from the Learning Platform.

## Not Logged In Report

### File Name

notlog1.csv or notlog4.csv

### Contents

Details of students that have not logged into the Learning Platform during the
relevant period of weeks.

### Structure

CSV file with the StudentID, Student full name, Tutor, Course, Last access and
Email. 

### Source

Students have not logged in last week report from the Learning Platform.
Alternatively, it could be the Students have not logged in previous 4 weeks report.

## Student Database Tags

### File Name

database.csv

### Contents

Enrolment details for students in the Student Database.

### Structure

CSV file with the EnrolmentPK, StudentID, NameGiven, NameSurname, CourseFK,
TutorFK, Status, Tag, StartDate. 

### Source

qryEnrolmentTags query from the Student Database.

### Notes

Make sure the StartDate column is in the format DD/MM/YYYY.

## Student File

### File Name

students.csv

### Contents

Students and the Tutor group they are in on the Learning Platform.

### Structure

CSV file with the Course, Tutor, StudentID and Student full name. 

### Source

Students in Tutor Group report from the Learning Platform.

## Submissions

### File Name

lastsub.csv

### Contents

Last submission date for each student in the Learning Platform for all courses.

### Structure

CSV file with the StudentID, Student full name, Course, Tutor and Last submission
date. 

### Source

Last submission date (all courses) report from the Learning Platform.

### Notes

Make sure the Last submission date column is in the format DD/MM/YYYY.

## Submissions Made Report

### File Name

sub2weeks.csv or sub4weeks.csv

### Contents

Last submission date for each student in the Learning Platform.

### Structure

CSV file with the StudentID, Student full name, Email, Course, Tutor, Assignment
name and Last submission date. 

### Source

Last submission report from the Learning Platform. Either 'Students submitted work
in previous 2 weeks' or 'Students submitted work in previous 4 weeks'.

### Notes

Make sure the Last submission date column is in the format DD/MM/YYYY.

## Tutor IDs File

### File Name

Tutor_IDs.csv

### Contents

Tutor details for tutors currently in the Student Database (Tutors table).

### Structure

CSV file with the Tutor ID, First Name, Last Name.

### Source

Tutors table of the Student Database.

## User Completion Mark Report

### File Name

cmcg.csv

### Contents

Completion status (Tutor, Head Tutor, Manager) for each student in the Learning
Platform.

### Structure

CSV file with the Course, Tutor group, StudentID, Student full name, Tutor,
Head Tutor and Manager. 

### Source

Users completion mark by course and group report from the Learning Platform.

## Users Marked Tutor Only Report

tutoronly.csv

### Contents

Completion status (Tutor, Head Tutor, Manager) for each student in the Learning
Platform that has been marked complete by their tutor but not by the Head Tutor
or Manager.

### Structure

CSV file with the Course, Tutor group, StudentID, Student full name, Tutor,
Head Tutor and Manager. 

### Source

Users marked by tutor but not head tutor or manager report from the Learning
Platform.

# Dependencies

- admintools from custtools
- datetools from custtools
- filetools from custtools
- pandas

# Development

## Known bugs

- If a file name is changed the loading and loaded messages will use the old name.
- Tutors that have been removed from the Learning Platform will be missing from
the lastsub data for the affected students.

## Items to fix

- 

## Current development step

- Update file names

## Required development steps

\<TBC>

## Future additions

- Order Updated_tags report on Student ID number.
- Add a help menu.
- Make Completion Mark Course Group filter automatically (look at lambda).
- Sort Insightly Changed_Tags report on EnrolmentID.
- Update file names (e.g. addresses.csv to be called Addresses File).
- Automatically load source files that don't need to be specifically selected.
- Add required file name to print out for files automatically loaded.
