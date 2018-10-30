# Student Report Preparer
# Version 1.0 31 October 2018
# Created by Jeff Mitchell
# Takes in student report output files and prepares them for sending
# to management
   

import copy
import csv
import custtools.admintools as ad
import custtools.datetools as da
import custtools.filetools as ft
import datetime as dt
import pandas as pd
import re
import sys


def add_eid(tags_df, sd_df, sid_name, eid_name, tag_name):
    """Return DataFrame with Enrolment Code added to each student.
    
    Args:
        tags_df (DataFrame): Student ID, Tag.
        sd_df (DataFrame): eid_name, sid_name, fname_name, lname_name,
        tid_name, tag_name, sdate_name.
        sid_name (str): Student ID column name.
        eid_name (str): Enrolment Code column name.
        tag_name (str): Tag column name.
    
    Returns:
        updated_tags (DataFrame): tags_df with the Enrolment Code added.
    """
    students = []
    print('\nAdding Enrolment ID\'s')
    headings = [sid_name, eid_name, tag_name]
    num_students = len(tags_df) # For calculating % complete
    n = 0
    for index, row in tags_df.iterrows():
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        student = []
        # Get Student ID
        studentID = row[sid_name]
        student.append(studentID)
        # Find student in sd_data
        for index_s, row_s in sd_df.iterrows():
            if row_s[sid_name] == studentID:
                student.append(row_s[eid_name])
                student.append(row[tag_name])
                students.append(student)
                break
    updated_tags = pd.DataFrame(data = students, columns = headings)
    print('\rFinished adding Enrolment ID\'s')
    return updated_tags


def add_inactive(updated_tags, sd_df, sid_name, tag_name, sid_loc = 0):
    """Add inactive students to data.
    
    Takes students that are missing from updated_tags, and present in sd_df,
    and adds their Student ID and tag to the data.
    
    Args:
        updated_tags (list): List of Student ID and Tag.
        sd_df (DataFrame): Student Database data.
        sid_name (str): Name of Student ID column.
        tag_name (str): Name of Tag column.
        sid_loc (int): Location of Student ID in updated_tags.
        
    Returns:
        all_tags (list): updated_tags with inactive students added back.
    """
    all_tags = copy.deepcopy(updated_tags)
    print('\nAdding Inactive Students')
    for student in all_tags:
    # Get list of Student IDs in updated_tags
        existing_students = get_students_list(updated_tags, 0)
    # Add students not currently in existing_students
    num_students = len(sd_df) # For calculating % complete
    n = 0
    for index, row in sd_df.iterrows():
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        if row[sid_name] not in existing_students:
            student = [row[sid_name], row[tag_name]] # Add Student ID, Tag
            all_tags.append(student)
    print('\rFinished adding Inactive Students')
    return all_tags


def add_missing(lsd, sd, tutors, missing, fname, lname, tid_name, sid_name,
                c_name):
    """Add details of students missing from lsd_tags.
    
    Extracts and generates the required information for each student in
    missing so that they can be added to the lsd_tags data.
    First and Last name is combined from the Student Database data. Course is
    taken from the Student Database data. Tutor First and Last name is taken
    from the tutors data.
    
    # To Do: Send column names in a list and then get from list position
    
    Args:
        lsd (list): List of Student IDs, Name, Course Code, Tutor Name, Tag.
        sd (DataFrame): Student Database data.
        tutors (DataFrame): Tutor ID, First Name, Last Name.
        missing (list): Student ID of students not in lsd.
        fname (str): Column name for First Name.
        lname (str): Column name for Last Name.
        tid_name (str): Column name for Tutor ID.
        sid_name (str): Column name for Student ID.
        c_name (str): column name for Course
    
    Returns:
        updated_lsd (list): List with previous lsd data and missing students
        appended.
    """
    updated_lsd = copy.deepcopy(lsd)
    print('\nAdding missing students')
    num_students = len(missing) # For calculating % complete
    n = 0
    for student in missing:
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        new_student = []
        # Add Student ID
        new_student.append(student)
        # Add Name
        new_student.append(get_s_name(student, sd, fname, lname, sid_name))
        # Add Course Code
        new_student.append(get_s_course(student, sd, sid_name, c_name))
        # Add Tutor's name
        new_student.append(get_t_name(student, sd, tutors, fname, lname,
                                      tid_name, sid_name))
        # Add Black tag
        new_student.append('Black')
        updated_lsd.append(new_student)
    # print('Debugging add_missing()')
    # ad.debug_list(updated_lsd)
    print('\rFinished adding missing students')
    return updated_lsd


def add_stud(tags_df, sd_df, headings_t, headings_s):
    """Return DataFrame with Student details added.
    
    Adds Student Name, Course, Tutor Name to the tags_df DataFrame.
    
    Args:
      tags_df (DataFrame): sid_name, eid_name, stud_name, course_name,
      tutor_name, new_tags_name.   
      sd_df (list): eid_name, sid_name, fname_name, lname_name, cid_name,
      tid_name, status_name, tag_name, sdate_name
      headings_t (list): tags_df headings: See tags_df (list). 
      headings_s (list): sd_df headings: See sd_df (list). 
    
    Returns:
        updated_tags (DataFrame): tags_df with Student details added.
    """
    students = []
    print('\nAdding Student Details')
    num_students = len(tags_df) # For calculating % complete
    n = 0
    for index, row in tags_df.iterrows():
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        student = []
        # Get Student ID
        studentID = row[headings_t[0]]
        student.append(studentID)
        student.append(row[headings_t[1]])
        # Find student in sd_df
        for index_sd, row_sd in sd_df.iterrows():
            if row_sd[headings_s[1]] == studentID:
                name = '{} {}'.format(row_sd[headings_s[2]],
                        row_sd[headings_s[3]])
                student.append(name)
                student.append(row_sd[headings_s[4]])
                student.append(row_sd[headings_s[5]])
                student.append(row[headings_t[5]])
                students.append(student)
                break
    headings = [headings_t[0], headings_t[1], headings_t[2], headings_s[4],
                headings_s[5], headings_t[5]]
    updated_tags = pd.DataFrame(data = students, columns = headings)
    print('\rFinished adding Student Details')
    return updated_tags


def add_tutor(student_ids, sd_df, tutors, fname, lname, tid_name, sid_name):
    """Return Tutor name for each student.
    
    Args:
        student_ids (list): Student IDs
        sd (DataFrame): Student Database data.
        tutors (DataFrame): Tutors ID, First name and Last name.
        fname (str): Column name for First Name.
        lname (str): Column name for Last Name.
        tid_name (str): Column name for Tutor ID.
        sid_name (str): Column name for Student ID.
    
    Returns:
        updated_students (list): Each student with their tutor name.
    """
    updated_students = []
    print('\nAdding Tutor Details')
    num_students = len(student_ids) # For calculating % complete
    n = 0
    for student in student_ids:
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        tutor = get_t_name(student, sd_df, tutors, fname, lname, tid_name,
                           sid_name)
        updated_student = [student, tutor]
        updated_students.append(updated_student)
    print('\rFinished adding Tutor Details')
    return updated_students


def add_tutor_df(tags_df, tags_df_students, headings, sid_loc=0, t_loc=1):
    """Add tutor name to tags_df DataFrame.
    
    Args:
        tags_df (DataFrame): Student information.
        tags_df_students (list): Student ID and Tutor name.
        headings (list): sid_name, stud_name, tutor_name, new_tags_name.
        sid_loc (int): Location of Student ID in tags_df_students.
        t_loc (int): Location of Tutor name in tags_df_students.
        
    Returns:
        updated_tags_df (DataFrame) tags_df with Tutor column added.
    """
    students = []
    print('\nAdding Tutor Name')
    num_students = len(tags_df.index) # For calculating % complete
    n = 0
    for index, row in tags_df.iterrows():
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        student = []
        # Get Student ID
        studentID = row[headings[0]]
        student.append(studentID)
        student.append(row[headings[1]])
        # Get tutor name
        for student_tutor in tags_df_students:
            if student_tutor[sid_loc] == studentID:
                student.append(student_tutor[t_loc])
                break
        student.append(row[headings[3]])        
        students.append(student)
    updated_tags_df = pd.DataFrame(data = students, columns = headings)
    print('\rFinished adding Tutor Name')
    return updated_tags_df


def check_active_students(report_data):
    """Return list of warnings for information in Active Students file.

    Checks the Active Students file data to see if the required information is
    present. Missing or incorrect information that is non-fatal is appended
    to a warnings list and returned.

    Args:
        report_data (list): Active Students File data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (report_data):
        Student ID, Student, Course
    
    File Source (report_data):
        Active students in a course
    """
    errors = []
    warnings = ['\nActive Students File Warnings:\n']
    for student in report_data:
        if student[1] in (None, ''):
            warnings.append('Name is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[2] in (None, ''):
            warnings.append('Course is missing for student with Student '
                            'ID {}'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Students File')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_add(address_data):
    """Return list of warnings for information in Addresses data file.
    
    Checks the Addresses data to see if the required information is present.
    Missing or incorrect information that is non-fatal is appended to a
    warnings list and returned.
    
    Args:
        address_data (list): Address data for all students in database.
        
    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.
    
    File Structure (Addresses):
        StudentPK, AddressNumber, AddressStreet, AddressSuburb, AddressCity,
        AddressPostcode, AddressCountry
        
    File Source (Addresses):
        Student Database (Students Table)
    """
    errors = []
    warnings = ['\nAddresses Data File Warnings:'
                '\n']
    for student in address_data:
        if student[1] in (None, ''):
            warnings.append('Address Number is missing for student with the '
                            'Student ID {}'.format(student[0]))
        if student[2] in (None, ''):
            warnings.append('Address Street is missing for student with the '
                            'Student ID {}'.format(student[0]))
        if student[3] in (None, ''):
            warnings.append('Address Suburb is missing for student with the '
                            'Student ID {}'.format(student[0]))
        if student[4] in (None, ''):
            warnings.append('Address City is missing for student with the '
                            'Student ID {}'.format(student[0]))
        if student[5] in (None, ''):
            warnings.append('Address Postcode is missing for student with the '
                            'Student ID {}'.format(student[0]))
        if student[6] in (None, ''):
            warnings.append('Address Country is missing for student with the '
                            'Student ID {}'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Adresses Data File')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_ccr(report_data):
    """Return list of warnings for information in Count completion report file.

    Checks the Count completion by tutor and group in courses report data to
    see if the required information is present. Missing or incorrect
    information that is non-fatal is appended to a warnings list and returned.

    Args:
        report_data (list): Count completion by tutor and group in courses
        report data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (report_data):
        Course, Tutor, Completions

    File Source (report_data):
        Count of completions by tutor and group in courses
    """
    errors = []
    warnings = ['\nCount of completions by tutor and group Report Warnings:'
                '\n']
    for student in report_data:
        if student[1] in (None, ''):
            warnings.append('Tutor group is missing for an entry')
        if student[2] in (None, ''):
            warnings.append('Completions missing for an entry')
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Count Completion Report')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_cst(report_data):
    """Return warnings for information in Count students per tutor report file.

    Checks the Count of students per tutor group report data to see if the
    required information is present. Missing or incorrect information that is
    non-fatal is appended to a warnings list and returned.

    Args:
        report_data (list): Count of students per tutor group report data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (report_data):
        Course, Tutor Group, Number Students

    File Source (report_data):
        Count of students per tutor groups
    """
    errors = []
    warnings = ['\nCount of students per tutor groups Report Warnings:\n']
    for student in report_data:
        if student[1] in (None, ''):
            warnings.append('Tutor group is missing for an entry')
        if student[2] in (None, ''):
            warnings.append('Number students missing for an entry')
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Count Students Tutor Groups Report')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_expiry_report(report_data):
    """Return list of warnings for information in Expiry report file.

    Checks the Expiry report data to see if the required information is
    present. Missing or incorrect information that is non-fatal is appended
    to a warnings list and returned.

    Args:
        report_data (list): Expiry report data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (report_data):
        StudentID, Student, Email, Course, Expiry date
        
    File Source (report_data):
        Students expiring X months
    """
    errors = []
    warnings = ['\nExpiry Report Warnings:\n']
    for student in report_data:
        if student[1] in (None, ''):
            warnings.append('Name is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[2] in (None, ''):
            warnings.append('Email is missing for student with Student '
                            'ID {}'.format(student[0]))
        if student[3] in (None, ''):
            warnings.append('Course is missing for student with Student '
                            'ID {}'.format(student[0]))
        if student[4] in (None, ''):
            errors.append('Expiry is missing for student with '
                            'Student ID {}'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Expiry Report')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_insightly(report_data):
    """Return list of warnings for information in Insightly data.

    Checks the Insightly data to see if the required information is present.
    Missing or incorrect information that is non-fatal is appended to a
    warnings list and returned.

    Args:
        report_data (list): Insightly report data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (report_data):
        StudentID, First Name, Last Name, Tags.

    File source (report_data):
        Insightly Data Dump (using columns listed in File structure).
    """
    errors = []
    warnings = ['\nInsightly Data File Warnings:\n']
    for student in report_data:
        if student[1] in (None, ''):
            errors.append('First Name is missing for student with the '
                          'Student ID {}'.format(student[0]))
        if student[2] in (None, ''):
            errors.append('Last Name is missing for student with the '
                          'Student ID {}'.format(student[0]))
        if student[3] in (None, ''):
            warnings.append('Tags is missing for student with the '
                          'Student ID {}'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Insightly Data File')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_last_login(report_data):
    """Return list of warnings for information in Last Login Date report file.

    Checks the Last Login Date report data to see if the required information
    is present. Missing or incorrect information that is non-fatal is appended
    to a warnings list and returned.

    Args:
        report_data (list): Last Login Date report data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (report_data):
        StudentID, Student, Tutor, Course, Last Access, Email
    
    File Source (report_data):
        Last Login Date
    """
    errors = []
    warnings = ['\nLast Login Date Report Warnings:\n']
    for student in report_data:
        if student[1] in (None, ''):
            warnings.append('Name is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[2] in (None, ''):
            warnings.append('Tutor is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[3] in (None, ''):
            warnings.append('Course is missing for student with Student '
                            'ID {}'.format(student[0]))
        if student[4] in (None, ''):
            warnings.append('Last Access is missing for student with '
                            'Student ID {}'.format(student[0]))
        if student[5] in (None, ''):
            warnings.append('Email is missing for student with Student '
                            'ID {}'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Last Login Date Report')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_last_sub_date(report_data):
    """Return list of warnings for information in Last Submission Made data.

    Checks the Last Submission Made report data to see if the required 
    information is present. Missing or incorrect information that is non-fatal
    is appended to a warnings list and returned.

    Args:
        report_data (list): Last Submissions Date report data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (report_data):
        StudentID, Student, Course, Tutor, Last submission date
        
    File Source (report_data):
        Last submission date (all courses)
    """
    errors = []
    warnings = ['\nLast Submission Date Report Warnings:\n']
    for student in report_data:
        if student[1] in (None, ''):
            warnings.append('Name is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[2] in (None, ''):
            warnings.append('Course is missing for student with Student '
                            'ID {}'.format(student[0]))
        if student[3] in (None, ''):
            warnings.append('Tutor is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[4] in (None, ''):
            warnings.append('Last submission date is missing for student '
                            'with Student ID {}'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Last_submissions_date_')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_never_logged_in(report_data):
    """Return list of warnings for information in Never Logged In report file.

    Checks the Never Logged In report data to see if the required information
    is present. Missing or incorrect information that is non-fatal is appended
    to a warnings list and returned.

    Args:
        report_data (list): Never Logged In report data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (report_data):
        StudentID, Student, Tutor, Course, Account Created, Report Date, Email
    
    File Source (report_data):
        Students never logged in
    """
    errors = []
    warnings = ['\nNever Logged In Report Warnings:\n']
    for student in report_data:
        if student[1] in (None, ''):
            warnings.append('Name is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[2] in (None, ''):
            warnings.append('Tutor is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[3] in (None, ''):
            warnings.append('Course is missing for student with Student '
                            'ID {}'.format(student[0]))
        if student[4] in (None, ''):
            errors.append('Account Created is missing for student with '
                            'Student ID {}'.format(student[0]))
        if student[5] in (None, ''):
            errors.append('Report Date is missing for student with '
                            'Student ID {}'.format(student[0]))
        if student[6] in (None, ''):
            warnings.append('Email is missing for student with '
                            'Student ID {}'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Never Logged In Report')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_not_logged_in(report_data):
    """Return list of warnings for information in Not Logged In report file.

    Checks the Not Logged In report data to see if the required infornation
    is present. Missing or incorrect information that is non-fatal is appended
    to a warnings list and returned.

    Args:
        report_data (list): Not Logged In report data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (report_data):
        StudentID, Student, Tutor, Course, Last Access, Email
    
    File Source (report_data):
        Students have not logged in last X weeks
    """
    errors = []
    warnings = ['\nNot Logged In Report Warnings:\n']
    for student in report_data:
        if student[1] in (None, ''):
            warnings.append('Name is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[2] in (None, ''):
            warnings.append('Tutor is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[3] in (None, ''):
            warnings.append('Course is missing for student with Student '
                            'ID {}'.format(student[0]))
        if student[4] in (None, ''):
            warnings.append('Last Access is missing for student with '
                            'Student ID {}'.format(student[0]))
        if student[5] in (None, ''):
            warnings.append('Email is missing for student with '
                            'Student ID {}'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Not Logged In Report')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_prev_data(read_data):
    """Return list of warnings for information in Previous Months Tags file.

    Checks the Previous Months Tags data to see if the required infornation
    is present. Missing or incorrect information that is non-fatal is appended
    to a warnings list and returned.

    Args:
        read_data (list): Previous Months Tags data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (read_data):
        StudentID, EnrolmentID, Student, Course, Tutor, Updated_Tags
    
    File Source (read_data):
        Previous Months Updated Tags File.
    """
    errors = []
    warnings = ['\nPrevious Months Tags Warnings:\n']
    for student in read_data:
        if student[1] in (None, ''):
            errors.append('Enrolment ID is missing for student with '
                          'Student ID {}'.format(student[0]))
        if student[2] in (None, ''):
            warnings.append('Name is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[3] in (None, ''):
            warnings.append('Course is missing for student with Student '
                            'ID {}'.format(student[0]))
        if student[4] in (None, ''):
            warnings.append('Tutor is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[5] in (None, ''):
            errors.append('Tag is missing for student with Student ID '
                            '{}'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Previous Months Tags data')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_review_warnings():
    """Return True or False for reviewing warning messages.

    Returns:
        True if user wants to review warning messages, False otherwise.
    """
    review = ''
    while review == '':
        review = input('\nDo you want to view the warning messages? y/n --> ')
        if review not in ('y', 'n'):
            print('\nThat is not a valid answer! Please try again.')
            review = ''
        elif review == 'y':
            return True
        else:
            return False


def check_students_file(report_data):
    """Return list of warnings for information in Students file.

    Checks the Students file data to see if the required information is
    present. Missing or incorrect information that is non-fatal is appended
    to a warnings list and returned.

    Args:
        report_data (list): Students File data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (report_data):
        Course, Tutor, Student ID, Student
    
    File Source (report_data):
        Students in tutor group
    """
    errors = []
    warnings = ['\nStudent File Warnings:\n']
    for student in report_data:
        for item in student:
            if item[1] in (None, ''):
                warnings.append('Tutor is missing for student with Student ID '
                                '{}'.format(item[2]))
            if item[2] in (None, ''):
                warnings.append('Student ID is missing for student with Student '
                                'Name {}}'.format(item[3]))
            if item[3] in (None, ''):
                warnings.append('Student Name is missing for student with '
                                'Student ID {}'.format(item[2]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Students File')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_subs_made(report_data, period):
    """Return list of warnings for information in Submissions Made report file.

    Checks the Submissions Made report data to see if the required information
    is present. Missing or incorrect information that is non-fatal is appended
    to a warnings list and returned.

    Args:
        report_data (list): Submissions Made report data.
        period (str): The period the data covers.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (report_data):
        StudentID, Student, Course, Tutor, Assignment name,
        Last submission date
        
    File Source (report_data):
        Students submitted work in previous X weeks
    """
    errors = []
    warnings = ['\nSubmissions Made Report Warnings:\n']
    for student in report_data:               
        if student[1] in (None, ''):
            warnings.append('Name is missing for student with Student ID '
                            '{}'.format(student[0]))
        if student[2] in (None, ''):
            warnings.append('Course is missing for student with Student '
                            'ID {}'.format(student[0]))
        if student[3] in (None, ''):
            warnings.append('Tutor is missing for student with Student '
                            'ID {}'.format(student[0]))
        if student[4] in (None, ''):
            warnings.append('Assignment name is missing for student with '
                            'Student ID {}'.format(student[0]))
        if student[5] in (None, ''):
            errors.append('Last submission date is missing for student '
                            'with Student ID {}'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    name = 'Submissions_Made_{}'.format(period)
    if len(errors) > 0:
        ft.process_error_log(errors, name)
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_tags_data(report_data):
    """Return warnings for information in Enrolment Tags data file.

    Checks the Enrolment Tags report data to see if the required information is
    present. Missing or incorrect information that is non-fatal is appended to
    a warnings list and returned.
    
    Args:
         report_data (list): Enrolment Tags report data.
         
    File Structure (report_data):
        EnrolmentPK, StudentID, NameGiven, NameSurname, CourseFK, TutorFK,
        Status, Tag, StartDate.
        
    File Source (report_data):
        qryEnrolmentTags query from Student Database.
    """
    errors = []
    warnings = ['\nEnrolment Tags Report Warnings:\n']
    for student in report_data:
        if student[1] in (None, ''):
            errors.append('Student ID is missing for student with the '
                            'enrolment ID {}.'.format(student[0]))
        if student[2] in (None, ''):
            warnings.append('First Name is missing for student with the '
                            'Student ID {}'.format(student[1]))
        if student[3] in (None, ''):
            warnings.append('Last Name is missing for student with the '
                            'Student ID {}'.format(student[1]))
        if student[4] in (None, ''):
            warnings.append('Course Code is missing for student with the '
                            'Student ID {}'.format(student[1]))
        if student[6] in (None, ''):
            warnings.append('Status is missing for student with the Student '
                            'ID {}'.format(student[1]))
        if student[7] in (None, ''):
            errors.append('Tag is missing for student with the Student ID '
                            '{}'.format(student[1]))
        if student[8] in (None, ''):
            errors.append('Start Date is missing for student with the Student '
                          'ID {}'.format(student[1]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Enrolment Tags Report')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_tu(tu_data):
    """Return list of warnings for information in Tutor_IDs.csv file.

    Checks the Tutor ID list data for the required information.
    Required information that is missing causes an error file to be saved
    and the program to exit.
    Missing or incorrect information that is non-fatal is appended to a
    warnings list and returned.

    Args:
        tu_data (list): A list with the ID number and name for each tutor.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (tu_data):
        TutorID, First Name, Last Name.
    """
    i = 0
    errors = []
    warnings = ['\nTutor File Warnings:\n']
    while i < len(tu_data):
        tutor = extract_tutor(tu_data, i)
        # print('check_tu Tutor: ' + str(tutor))
        if tutor[0] in (None, ''):
            continue
        if len(tutor[0].strip()) != 6:
            errors.append('Tutor ID number is not the required length '
                          'for tutor in position {} in the list.'.format
                          (i))
        if tutor[1] in (None, ''):
            warnings.append('First Name for tutor with Tutor ID Number {} is '
                            'missing.'.format(tutor[0]))
        if tutor[2] in (None, ''):
            warnings.append('Last Name for tutor with Tutor ID Number {} is '
                            'missing.'.format(tutor[0]))
        i += 1
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Tutor_ID_Numbers')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_tutor_ids(tutors, students):
    """Check Tutor IDs in student data are in Tutor ID list.
    
    Checks that the Tutor ID for each student is contained in the list of valid
    Tutor IDs. If invalid Tutor IDs are found they students concerned are
    printed to the screen, an error file is created and the program exits.
    
    Args:
        tutors (list): List of valid Tutor IDs.
        students (list): List of lists of data for each student.
    """
    errors = []
    for student in students:
        if student[5] not in tutors:
            errors.append('Tutor ID {} appears for the Student with the '
                          'Student ID number of {}. This Tutor ID does not '
                          'appear in the list of valid Tutor IDs.'.format(
                                  student[5], student[1]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Tutor_ID_Numbers')


def check_ua(report_data):
    """Return warnings for information in Count unmarked assess report file.

    Checks the Count of unmarked assessments by tutor report data to see if the
    required information is present. Missing or incorrect information that is
    non-fatal is appended to a warnings list and returned.

    Args:
        report_data (list): Count of unmarked assessments by tutor report data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (report_data):
        Course, Tutor, Number assessments

    File Source (report_data):
        Count of unmarked assessments by tutor
    """
    errors = []
    warnings = ['\nCount of unmarked assessments Report Warnings:\n']
    for student in report_data:
        if student[1] in (None, ''):
            warnings.append('Tutor group is missing for an entry')
        if student[2] in (None, ''):
            warnings.append('Number students missing for an entry')
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Count Unmarked Assessments Report')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_ucm(report_data):
    """Return list of warnings for information in User completion report file.

    Checks the User completion mark by course and group report data to see if
    the required information is present. Missing or incorrect information that
    is non-fatal is appended to a warnings list and returned.

    Args:
        report_data (list): User completion mark by course and group report
        data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (report_data):
        Course, Tutor group, Student ID, Student, Tutor, Head Tutor, Manager

    File Source (report_data):
        Users completion mark by course and group
    """
    errors = []
    warnings = ['\nUser completion mark Report Warnings:\n']
    # print('Length of report data: ' + str(len(report_data)))
    # ad.debug_list(report_data)
    for student in report_data:
        if student[1] in (None, ''):
            warnings.append('Tutor group is missing for student with '
                            'Student ID {}'.format(student[2]))
        if student[2] in (None, ''):
            warnings.append('Student ID is missing for student with Name '
                            '{}'.format(student[3]))
        if student[3] in (None, ''):
            warnings.append('Name is missing for student with Student '
                            'ID {}'.format(student[2]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'User Completion Mark Report')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_umt(report_data):
    """Return list of warnings for information in User Mark T only report file.

    Checks the Users marked by tutor only report data to see if the required
    information is present. Missing or incorrect information that is non-fatal
    is appended to a warnings list and returned.

    Args:
        report_data (list): Users marked by tutor only report data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File Structure (Users marked by tutor only):
        Course, Tutor group, Student ID, Student, Tutor, Head Tutor, Manager
        
    File Source(Users marked by tutor):
        Users marked by tutor but not head tutor or manager
    """
    errors = []
    warnings = ['\nUsers marked complete tutor only Report Warnings:\n']
    for student in report_data:
        if student[1] in (None, ''):
            warnings.append('Tutor group is missing for student with '
                            'Student ID {}'.format(student[2]))
        if student[2] in (None, ''):
            warnings.append('Student ID is missing for student with Name '
                            '{}'.format(student[3]))
        if student[3] in (None, ''):
            warnings.append('Name is missing for student with Student '
                            'ID {}'.format(student[2]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Users marked by tutor only Report')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def clean_insightly(raw_data):
    """Clean data in the Insightly data.
    
    Extracts the desired columns from the Insightly data and cleans the raw
    data.
    
    Args:
        raw_data (list): Raw insightly data.
        
    Returns:
        cleaned_data (list): Insightly data that has been cleaned.
    
    File structure (report_data):
        StudentID, First Name, Last Name, Tags.

    File source (report_data):
        Insightly Data Dump (using columns listed in File structure).
    """
    cleaned_data = []
    for student in raw_data:
        cleaned_student = []
        # Extract and clean desired columns
        cleaned_student.append(student[0].strip())
        cleaned_student.append(student[1].strip())
        cleaned_student.append(student[2].strip())
        cleaned_student.append(student[3].strip())
        cleaned_data.append(cleaned_student)
    return cleaned_data


def clean_last_subs_date(report_data):
    """Clean data in Last submissions date data.
    
    Extracts the course code and formats the Last submission date into 
    'DD/MM/YYYY'.
    
    Args:
        report_data (list): Raw Last submission date data.
        
    Returns:
        cleaned_data (list): Last submission date data that has been cleaned.
    
    File Structure (report_data):
        StudentID, Student, Course, Tutor, Last submission date
        
    File Source (report_data):
        Last submission date (all courses)
    """
    cleaned_data = []
    print('\nCleaning Last Sub Date')
    num_students = len(report_data) # For calculating % complete
    n = 0
    for student in report_data:
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        cleaned_student = []
        cleaned_student.append(student[0].strip())
        cleaned_student.append(student[1].strip())
        cleaned_student.append(extract_course_code(student[2].strip()))
        cleaned_student.append(student[3].strip())
        # Extract desired date portion _ TO BE WRITTEN
        # Can this be fixed using the check on separator function?
        cleaned_student.append(extract_last_submission_date_3
                               (student[4].strip()))
        cleaned_data.append(cleaned_student)
    
    print('\nDebugging clean_last_subs_date')
    ad.debug_list(cleaned_data)
    
    print('\rFinished cleaning Last Sub Date')
    return cleaned_data


def convert_e_date(students, sd_df_students):
    """Return student list with tag based on last submission date.
    
    Calculates the appropriate tag based on the last submission date.
    
    Args:
        students (list): Student data.
        sd_df_students (list): List of active students.
        
    Returns:
        updated_students (list): Students list returned with the Last 
        submission date replaced by the appropriate tag based on the last
        submission date.
    
    List structure:
        Student ID, Student, Course, Tutor, Last submission date.
    """
    updated_students = []
    black_day = 139
    red_day = 83
    orange_day = 55
    print('\nConverting Enrolment Dates')
    for student in students:
        if student[0] not in sd_df_students: # Skip non-active students
            continue
        updated_student = []
        # Get number of days enrolled for
        # print('Student passed to get_days_passed: {}'.format(student))
        days_passed = da.get_days_past(student[4], '/', '/')
        # print('\n\n\nDays past for {}: {}\n'.format(student[0], days_passed))
        if days_passed == None:
            tag = 'Green'
        elif days_passed > black_day:
            tag = 'Black'
        elif days_passed > red_day:
            tag = 'Red'
        elif days_passed > orange_day:
            tag = 'Orange'
        else:
            tag = 'Green'
        updated_student.append(student[0])
        updated_student.append(student[1])
        updated_student.append(student[2])
        updated_student.append(student[3])
        updated_student.append(tag)
        updated_students.append(updated_student)
    print('\rFinished converting Enrolment Dates')
    return updated_students
        

def convert_purple(students, purple):
    """Overwrite status of Purple students.
    
    Students that are contained in the Purple list have their status
    overwritten to Purple.
    
    Args:
        students (list): Student tag list.
        purple (list): Student ID's of students with Purple tag.
    
    Returns:
        updated_students (list): Student ID and Tag.
    """
    updated_students = []
    print('\nConverting Purple Tags')
    num_students = len(students) # For calculating % complete
    n = 0
    for student in students:
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        updated_student = []
        updated_student.append(student[0])
        if student[0] in purple:
            updated_student.append('Purple')
        else:
            updated_student.append(student[1])
        updated_students.append(updated_student)
    print('\rFinished Converting Purple Tags')
    return updated_students            


def extract_course_code(course):
    """Extract the course code.
    
    Looks for the course code in a course string (XXX-XX-XXX). If it is present
    it returns the course code. If it is not present it returns 'Skip'.
    
    Args:
        course (str): Full course name to be searched.
    
    Returns:
        Either the course code or 'Skip' if a course code cannot be found.
    """
    if re.search('.+\(.+-.+-.+\)', course):
        # Extract the course code and return it
        start = course.index('(')
        return course[start+1:-1]
    else:
        return 'Skip'


def extract_last_submission_date(date):
    """Return the date in the format DD-MM-YYYY.
    
    Replaces the provided date with one in the format DD-MM-YYYY. The separator
    that is used is a '/'. Input date should be in the format 
    YYYY-MM-DD hh:mm...
    
    Args:
        date (str): Date to be processed.
        
    Returns:
        new_date (str): Date in the format DD-MM-YYYY.
    """
    # Find location of the first separator and extract DD
    # print(date)
    sep = ('-')
    first_sep = date.find(sep)
    years = date[:first_sep]
    #print(years)
    # Find location of the second seperator and extract MM
    remaining = date[first_sep + 1:]
    second_sep = remaining.find(sep)
    months = remaining[:second_sep]
    # Extract DD
    date_end = second_sep + 3
    days = remaining[second_sep + 1:date_end]
    # Return up to the end of the date (DD/MM/YYYY)
    new_date = days + sep + months + sep + years
    #print(new_date)
    return new_date


def extract_last_submission_date_2(date):
    """Return the date in the format DD/MM/YYYY.
    
    Replaces the provided date with one in the format DD/MM/YYYY. Finds the
    first empty character and returns from the start of the string to one 
    character prior to the empty charachter. Input date should be in the format 
    DD/MM/YYYY hh:mm... A leading 0 is added to the day if one is missing.
     
    Args:
        date (str): Date to be processed.
        
    Returns:
        new_date (str): Date in the format DD-MM-YYYY.
    """
    space = date.index(' ')
    date = date[:space]
    if len(date) == 10:
        new_date = date
    elif len(date) == 9:
        new_date = '0' + date
    else:
        return date
    return new_date


def extract_last_submission_date_3(date):
    """Return the date in the format DD/MM/YYYY.
    
    Replaces the provided date with one in the format DD/MM/YYYY. The separator
    that is used is a '-'. Input date should be in the format 
    YYYY-MM-DD hh:mm...
    
    Args:
        date (str): Date to be processed.
        
    Returns:
        new_date (str): Date in the format DD-MM-YYYY.
    """
    # Find location of the first separator and extract DD
    # print(date)
    sep = '-'
    new_sep = '/'
    first_sep = date.find(sep)
    years = date[:first_sep]
    #print(years)
    # Find location of the second seperator and extract MM
    remaining = date[first_sep + 1:]
    second_sep = remaining.find(sep)
    months = remaining[:second_sep]
    # Extract DD
    date_end = second_sep + 3
    days = remaining[second_sep + 1:date_end]
    # Return up to the end of the date (DD/MM/YYYY)
    new_date = days + new_sep + months + new_sep + years
    #print(new_date)
    return new_date


def extract_last_submission_date_4(date):
    """Return the date in the format DD/MM/YYYY.
    
    Replaces the provided date with one in the format DD/MM/YYYY. The separator
    that is used is a '/'. Input date should be in the format 
    DD/MM/YYYY hh:mm...
    
    Args:
        date (str): Date to be processed.
        
    Returns:
        new_date (str): Date in the format DD-MM-YYYY.
    """
    # Find location of the first separator and extract DD
    # print(date)
    sep = '/'
    new_sep = '/'
    first_sep = date.find(sep)
    days = date[:first_sep]
    #print(years)
    # Find location of the second seperator and extract MM
    remaining = date[first_sep + 1:]
    second_sep = remaining.find(sep)
    months = remaining[:second_sep]
    # Extract DD
    date_end = second_sep + 5
    years = remaining[second_sep + 1:date_end]
    # Return up to the end of the date (DD/MM/YYYY)
    new_date = days + new_sep + months + new_sep + years
    #print(new_date)
    return new_date


def extract_tag(raw_data):
    """Replace Contact tag with Status tag.
    
    Replaces the Tags field with the tag for their status, extracted
    from the Tags list.
    
    Args:
        raw_data (str): String containing Contact tag data.
        
    Returns:
        The colour of their status tag if found, 'N/A' otherwise.
    """
    if re.search('suspended', raw_data.lower()):
        return 'Suspended'
    elif re.search('withdrawn', raw_data.lower()):
        return 'Withdrawn'
    elif re.search('graduated', raw_data.lower()):
        return 'Graduated'
    elif re.search('expired', raw_data.lower()):
        return 'Expired'
    elif re.search('on hold', raw_data.lower()):
        return 'On Hold'
    elif re.search('cancelled', raw_data.lower()):
        return 'Cancelled'
    elif re.search('green', raw_data.lower()):
        return 'Green'
    elif re.search('orange', raw_data.lower()):
        return 'Orange'
    elif re.search('red', raw_data.lower()):
        return 'Red'
    elif re.search('black', raw_data.lower()):
        return 'Black'
    elif re.search('purple', raw_data.lower()):
        return 'Purple'
    else:
        return 'N/A'


def extract_tutor(tutor_data, tutor_pos):
    """Extract a single tutor.

    Args:
        tutor_data (list): List containing tutor data.
        tutor_pos (int): Location of the tutor to be extracted.

    Returns:
        tutor (list): A single tutor in a list.
    """
    tutor = tutor_data[tutor_pos]
    return tutor


def find_missing(sd_df_s, lsd_tags_s):
    """Return students missing from lsd_tags_s.
    
    Find students that are in the sd_df but not in the lsd_tags list. These
    will be students that have not submitted anything to the platform.
    
    Args:
        sd_df_s (list): Students in the sd_df data.
        lsd_tags_s (list): Students in the lsd_tags_s data. 
    
    Returns:
        missing (list): Students that are missing from lsd_tags_s.
    """
    missing = []
    print('\nFinding missing students')
    num_students = len(sd_df_s) # For calculating % complete
    n = 0
    for student in sd_df_s:
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        if student not in lsd_tags_s:
            missing.append(student)
    print('\rFinished finding missing students')
    return missing    


def get_active(sd_data, lsd_data, sid_name):
    """Return only students that are active.
    
    Gets the list of Active students from the Student Database data. Returns
    only the lsd_data students that area listed Active in the database.
    
    Args:
        sd_data (DataFrame): Student database information.
        lsd_data (list): Student enrolment data from the Learning Platform.
        sid_name (str): Name of Student ID column.
        
    Returns:
        updated_lsd (list): Only Active students from lsd_data.
    
    List Structure (lsd_data):
        Student ID, Student, Course, Tutor, Last submission date.
    """
    # Create a list with active students from sd_data
    active = []
    for index, row in sd_data.iterrows():
        active.append(row[sid_name])     
    # Check if each student from lsd_data is in active list
    updated_lsd = []
    for student in lsd_data:
        if student[0] in active:
            updated_lsd.append(student)
    # Return list with just the active lsd_data students
    return updated_lsd


def get_changes(students):
    """Count number of tags progressed and regressed per tutor.
    
    Returns a dictionary with each tutor and a count of students progressed
    and regressed for them. COmpares the value for Current Tag and Previous
    Tag to determine if a student has progressed or regressed.
    
    Args:
        students (list): Student Tags data
        
    Returns:
        tutor_dict (dict): Dictionary with changes count by tutor.
        results (list): List of possible changes.
    """
    # Create a list of tutors from students
    tutors = []
    for student in students:
        if student[4] not in tutors:
            tutors.append(student[4])
    # Create a dictionary with tutor names
    # Create a list with the results
    results = ['Progressed', 'Regressed', 'Maintained']
    tutor_dict = {}
    for tutor in tutors:
        tutor_dict[tutor] = {}
        for result in results:
            tutor_dict[tutor][result] = 0
    # Update dictionary by going through students
    for student in students:
        tutor = student[4]
        if student[7] < student[8]: # Student has regressed
            tutor_dict[tutor]['Regressed'] += 1
        elif student[7] > student[8]: # Student has progressed
            tutor_dict[tutor]['Progressed'] += 1
        else: # Student has maintained tag
            tutor_dict[tutor]['Maintained'] += 1       
    return tutor_dict, results


def get_colour(en_dates):
    """Return the max colour tag for each student.
    
    Separates the students into four lists depending on what colour tag they
    are able to qualify for, based on their enrolment date. For instance, a
    student that has only been enrolled for 2 months can only be green. A
    student that has been enrolled for over 140 days can be black.
    
    Args:
        en_dates (list): List of lists with Student ID and Enrolment Date.
        
    Returns:
        black, red, orange, green (list): List for each colour with the
        students in that colour group (max).
    """
    black, red, orange, green = ([] for i in range(4))
    black_day = 139
    red_day = 83
    orange_day = 55
    print('\nGetting Colour Tags')
    num_students = len(en_dates) # For calculating % complete
    n = 0
    for student in en_dates:
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        # Get number of days enrolled for
        enrolled_days = da.get_days_past(student[1])
        if enrolled_days in (None, ''):
            green.append(student[0])
        elif enrolled_days > black_day:
            black.append(student[0])
        elif enrolled_days > red_day:
            red.append(student[0])
        elif enrolled_days > orange_day:
            orange.append(student[0])
        else:
            green.append(student[0])
    '''
    print('\nBlack zone students:')
    ad.debug_list(black)
    print('\nRed zone students:')
    ad.debug_list(red)
    print('\nOrange zone students:')
    ad.debug_list(orange)
    print('\nGreen zone students:')
    ad.debug_list(green)
    '''
    print('\rFinished getting Colour Tags')
    '''
    print('Orange Tags: {}'.format(len(orange)))
    print('{}'.format(orange))
    print('Red Tags: {}'.format(len(red)))
    print('{}'.format(red))
    '''
    return black, red, orange, green        


def get_enrol_dates(sd_data, s_id, e_date, sd_df_students):
    """Return list of enrolment dates.
    
    Extracts the Student ID number and Enrolment date for each student and
    returns in a list of lists.
    
    Args:
        sd_data (DataFrame): Student database tag information.
        s_id (str): Name for Student ID column.
        e_date (str): Name for Enrolment date column.
        sd_df_students (list): Student ID for active students
        
    Returns:
        colours (list): List of Student ID  and Enrolment date for each
        student.
    """
    colours = []
    print('\nGetting Enrolment Dates')
    num_students = len(sd_data) # For calculating % complete
    n = 0
    for index, row in sd_data.iterrows():
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        if row[s_id] in sd_df_students: # Only get active students
            student = []
            student.append(row[s_id])
            student.append(row[e_date])
            colours.append(student)
    print('\rFinished getting Enrolment Dates')
    return colours


def get_id_changes(tags_df, id_df, headings, tag_name):
    """Return students that have had their tag changed from Insightly Data.
    
    Merges id_df and tags_df. Compares Tags and Updated_Tags columns and if
    they are different the student is added to the returned DataFrame.
    
    Args:
        tags_df (DataFrame): sid_name, eid_name, stud_name, course_name,
        tutor_name, new_tags_name.
        id_df (DataFrame): sid_name, tag_name.
        headings (list): sid_name, stud_name, tutor_name, new_tags_name.
        tag_name (str): Column name for Tag.
    
    Returns:
        changed_students (DataFrame): Students that have changed tags.
    """
    changed = []
    print('\nGetting Changes')
    # Merge DataFrames
    combined = pd.merge(id_df, tags_df, on = headings[0], how = 'inner')
    new_headings = [headings[0], headings[1], headings[2], tag_name,
                    headings[3]]
    combined = combined[new_headings]
    num_students = len(combined.index) # For calculating % complete
    n = 0
    # Extract students that have had their tag changed
    for index, row in combined.iterrows():
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        if row[tag_name] != row[headings[3]]:
            student = []
            student.append(row[headings[0]])
            student.append(row[headings[1]])
            student.append(row[headings[2]])
            student.append(row[headings[3]])
            changed.append(student)
    changed_students = pd.DataFrame(data = changed, columns = headings)
    changed_students = changed_students.rename(columns={headings[3]:tag_name})
    print('\rFinished getting Changes')
    return changed_students


def get_lsd_tags_students(students, valid_students, location):
    """Return list of Student IDs from data.
    
    Args:
        students (list): Student Data.
        valid_students (list): Students that are to be included.
        location (int): Location of Student ID in string.
    
    Returns:
        student_ids (list): List of Student ID numbers.
    """
    student_ids = []
    print('\nGetting Student ID\'s')
    num_students = len(students) # For calculating % complete
    n = 0
    for student in students:
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        if student[location] in valid_students:
            student_ids.append(student[location])
    print('\rFinished getting Student ID\'s')
    return student_ids


def get_purple(id_df, sid_name, tag_name):
    """Return a list of students with Purple for status.
    
    Checks the status column for each student and extracts the Student ID's for
    students that are Purple.
    
    Args:
        id_df (DataFrame): Data from Insightly.
        tag_name (str): Name of tag column.
    
    Returns:
        purple_students (list): Students with Purple status.
    """
    purple_students = []
    print('\nGetting Purple Tags')
    num_students = len(id_df) # For calculating % complete
    n = 0
    for index, row in id_df.iterrows():
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        if row[tag_name] == 'Purple':
            purple_students.append(row[sid_name])
    print('\rFinished getting Purple Tags')
    return purple_students


def get_sd_changes(sd_df, tags_df, headings, tag_name):
    """Return students that have had their tag changed from Student Database.
    
    Merges sd_df and tags_df. Compares Tags and Updated_Tags columns and if
    they are different the student is added to the returned DataFrame.
    
    Args:
        tags_df (DataFrame): sid_name, eid_name, stud_name, course_name,
        tutor_name, new_tags_name
        sd_df (DataFrame): eid_name, sid_name, fname_name, lname_name,
        tid_name, tag_name, sdate_name.
        headings (list): sid_name, eid_name, stud_name, new_tags_name.
        tag_name (str): Column name for Tag.
    
    Returns:
        changed_students (DataFrame): Students that have changed tags.
    """
    changed = []
    print('\nGetting Changes')
    # Merge DataFrames
    combined = pd.merge(sd_df, tags_df, on = headings[0], how = 'inner')
    combined = combined.rename(columns={'EnrolmentID_x':'EnrolmentID'})
    new_headings = [headings[0], headings[1], headings[2], tag_name,
                    headings[3]]
    combined = combined[new_headings]
    # Extract students that have had their tag changed
    num_students = len(combined.index) # For calculating % complete
    n = 0
    for index, row in combined.iterrows():
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        if row[tag_name] != row[headings[3]]:
            student = []
            student.append(row[headings[0]])
            student.append(row[headings[1]])
            student.append(row[headings[2]])
            student.append(row[headings[3]])
            changed.append(student)
    changed_students = pd.DataFrame(data = changed, columns = headings)
    changed_students = changed_students.rename(columns={headings[3]:tag_name})
    print('\rFinished getting Changes')
    return changed_students


def get_sd_df_students(students, sid_name, tag_name):
    """Return list of Student IDs from data.
    
    Filters out students that are not Active (have a status that is in the
    reserved list). Returns only Student ID numbers of Active students.
    
    Args:
        students (DataFrame): Student Data.
        sid_name (str): Name of Student ID column.
        tag_name (str): Name of tag column.
    
    Returns:
        student_ids (list): List of Student ID numbers.
    """
    student_ids = []
    print('\nGetting Student ID\'s')
    reserved = ['withdrawn', 'graduated', 'expired', 'suspended', 'on hold',
                'cancelled', 'transferred']
    num_students = len(students) # For calculating % complete
    n = 0
    for index, row in students.iterrows():
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        if row[tag_name].lower() not in reserved: # filter non-active students
            student_ids.append(row[sid_name])
    print('\rFinished getting Student ID\'s')
    return student_ids


def get_students(students, col_name):
    """Return list of Student IDs.
    
    Args:
      students (DataFrame): Student data to be processed.
      col_name (str): Name of column to be collected.
      
    Returns:
        student_ids (list): List of Student IDs.
    """
    student_ids = []
    print('\nGetting Student ID\'s')
    num_students = len(students) # For calculating % complete
    n = 0
    for index, row in students.iterrows():
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        student_ids.append(row[col_name])
    print('\rFinished getting Student ID\'s')
    return student_ids


def get_students_list(students, location):
    """Return list of Student IDs.
    
    Args:
      students (list): Student data to be processed.
      location (int): Location of column to be collected.
      
    Returns:
        student_ids (list): List of Student IDs.
    """
    student_ids = []
    for student in students:
        student_ids.append(student[location])
    return student_ids
    

def get_s_course(student, sd, sid_name, c_name):
    """Return student course.
      
    Args:
        student (str): Student ID Number.
        sd (DataFrame): Student Database data.
        sid_name (str): Column name for Student ID.
        c_name (str): Column name for Course name.
    
    Returns:
        course (str): Student's course.
    """
    for index, row in sd.iterrows():
        if row[sid_name] == student:
            course = '{}'.format(row[c_name])
            return course
    return ''


def get_s_name(student, sd, fname, lname, sid_name):
    """Return student name.
    
    Finds the student's First name and Last name in the Student Data and
    returns a formatted string.
    
    Args:
        student (str): Student ID Number.
        sd (DataFrame): Student Database data.
        fname (str): Column name for First Name.
        lname (str): Column name for Last Name.
        sid_name (str): Column name for Student ID.
    
    Returns:
        name (str): First name + Last name
    """
    for index, row in sd.iterrows():
        if row[sid_name] == student:
            name = '{} {}'.format(row[fname], row[lname])
            return name
    return ''


def get_tags(students, black, red, orange, green):
    """Return list of udpated tags.
    
    Creates a list with StudentID, Start_Tag and Zone.
    
    Args:
        students (list): StudentID and Tag_start
        black, red, orange, green (lists): Zone lists.
    
    Returns:
        updated_students (list): Students with Tag_start and Zone.
    """
    updated_students = []
    print('\nGetting Student Tags')
    num_students = len(students) # For calculating % complete
    n = 0
    for student in students:
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        updated_student = []
        if student[0] in black:
            zone = 'Black'
        elif student[0] in red:
            zone = 'Red'
        elif student[0] in orange:
            zone = 'Orange'
        elif student[0] in green:
            zone = 'Green'
        else:
            zone = 'N/A'
        updated_student.append(student[0])
        updated_student.append(student[4])
        updated_student.append(zone)
        updated_students.append(updated_student)
    print('\rFinished getting Student Tags')
    return updated_students


def get_tags_values(students):
    """Return list with tag values added.
    
    For each student the tag value for old tag and new tag is appended to the
    student's data and returned as a list. This can be used to determine
    whether the student has progressed or regressed.
    
    Args:
        students (list): StudentID, EnrolmentID, Name, Course, Tutor,
        Current_Tag, Previous_Tag.
    
    Returns:
        updated_students (list): Tag values added.
    """
    # Allocated values to tags
    green_val = 4
    orange_val = 3
    red_val = 2
    black_val = 1
    updated_students = []
    for student in students:
        this_student = []
        # Add existing student data
        i = 0
        while i < 7:
            this_student.append(student[i])
            i += 1
        # Add value for Current_tag
        if student[5] == 'Green':
            this_student.append(green_val)
        elif student[5] == 'Orange':
            this_student.append(orange_val)
        elif student[5] == 'Red':
            this_student.append(red_val)
        else:
            this_student.append(black_val)
        # Add value for Previous_tag
        if student[6] == 'Green':
            this_student.append(green_val)
        elif student[6] == 'Orange':
            this_student.append(orange_val)
        elif student[6] == 'Red':
            this_student.append(red_val)
        else:
            this_student.append(black_val)
        updated_students.append(this_student)
    return updated_students              


def get_tutor_changes(changes_tutor, changes_list):
    """Create list with Tutor changes counts.
    
    Extracts the data from the nested Dictionaries and returns it as a list.
    
    Args:
        changes_tutor (dict): Nested dictionary of tutor changes counts.
        changes_list (list): 'Progressed', 'Regressed', 'Maintained'
    
    Returns:
        change_count (list): Change counts as a list
    """
    change_count = []
    for tutor, values in changes_tutor.items():
        this_tutor = []
        this_tutor.append(tutor)
        i = 0
        while i < 3:
            this_tutor.append(changes_tutor[tutor][changes_list[i]])
            i += 1
        change_count.append(this_tutor)
    return change_count


def get_tutor_stats(prev_month, this_month, a_loc = 0, b_loc = 0):
    """Return number of students progressing and regressing per tutor.
    
    Regressed students are those that have drop down a tag colour, e.g. from
    Green to Orange. Progressed students have bone up a tag colour, usually by
    submitting work and going to Green. If a student is Purple or N/A they are
    ignored for this analysis.
    
    Args:
        prev_month (list): Tag data from previous month.
        this_month (list): Tag data from current month.
        a_loc (int) Location of Student ID in this_month
        b_loc (int) Location of Student ID in prev_month
    
    Returns:
        tutor_data (dict): Tutor data stored in a dictionary.
        
    Data format:
        StudentID, EnrolmentID, Student, Course, Tutor, Updated_Tags
    """
    # Get list of students in each group
    a_students = get_students_list(this_month, a_loc)
    b_students = get_students_list(prev_month, b_loc)
    # Get list of students in both lists
    common = ad.get_common(a_students, b_students)
    # Get tag information for desired sudents from both lists
    tag_merge = merge_tags(this_month, prev_month, common)
    # Analyse number of progressed and regressed for each tutor
    tutor_data, change_list = get_changes(tag_merge)
    return tutor_data, change_list


def get_tutor_tags(tags_tutor, tag_list):
    """Cretae list with Tutor Tag counts.
    
    Extracts the data from the nested Dictionaries and returns it as a list.
    
    Args:
        tags_tutor (dict): Nested dictionary of tutor tag counts.
        tag_list (list): 'Green', 'Orange', 'Red', 'Black', 'Purple'
    
    Returns:
        tag_count (list): List with tag counts per tutor.
    """
    tag_count = []
    for tutor, values in tags_tutor.items():
        this_tutor = []
        this_tutor.append(tutor)
        i = 0
        while i < 5:
            this_tutor.append(tags_tutor[tutor][tag_list[i]])
            i += 1
        tag_count.append(this_tutor)
    return tag_count


def get_t_name(student, sd, tutors, fname, lname, tid_name, sid_name):
    """Return tutor name.
    
    Finds the student's tutor's First name and Last name in the Tutors Data and
    returns a formatted string.
    
    Args:
        student (str): Student ID Number.
        sd (DataFrame): Student Database data.
        tutors (DataFrame): Tutors ID, First name and Last name.
        fname (str): Column name for First Name.
        lname (str): Column name for Last Name.
        tid_name (str): Column name for Tutor ID.
        sid_name (str): Column name for Student ID.
    
    Returns:
        name (str): First name + Last name
    """
    # Find Student ID data in sd and identify Tutor ID
    for index, row in sd.iterrows():
        if row[sid_name] == student:
            tutor_id = row[tid_name]
            # Find Tutor ID and return formatted name
            for index_t, row_t in tutors.iterrows():
                if row_t[tid_name] == tutor_id:
                    name = '{} {}'.format(row_t[fname], row_t[lname])
                    return name
    return ''


def list_expired(expiry):
    """Replaces the timestamps of students that have expired with 'Expired'.
    
    Converts the timestamp information into datetime and then compares to the
    current date. Those that are expired are overwritten with 'Expired'.
    
    Args:
        expiry (str): Timestamp information for student expiry.
        
    Returns:
        'Expired' if the student has expired, the input timestamp otherwise.
    """
    current_date = dt.datetime.now()
    expired_date = pd.to_datetime(expiry, errors='coerce')
    if expired_date < current_date:
        return 'Expired'
    else:
        return expiry


def list_non_active(status):
    """Replaces the status of non-active students with 'Skip'.
    
    Checks for active students by looking for 'Active' in the status. Those
    without 'Active' are overwritten with 'Skip'.
    
    Args:
        status (str): Information for status.
        
    Returns:
        'Skip' if the status is not active, the passed status otherwise.
    """
    if re.search('active', status.lower().strip()):
        return status
    else:
        return 'Skip'


def list_non_on(course):
    """Replaces the course name of non-online courses with 'Skip'.
    
    Checks for online courses by looking for 'ON' in the course name. Those
    without 'ON' are overwritten with 'Skip'.
    
    Args:
        course (str): Information for course name.
        
    Returns:
        'Skip' if the course is not online, the passed course otherwise.
    """
    if re.search('.+\(.+-ON-.+\)', course):
        return course
    else:
        return 'Skip'


def list_non_on_code(course):
    """Replaces the course name of non-online courses with 'Skip'.
    
    Checks for online courses by looking for 'ON' in the course code. Those
    without 'ON' are overwritten with 'Skip'.
    
    Args:
        course (str): Information for course name.
        
    Returns:
        'Skip' if the course is not online, the passed course otherwise.
    """
    if re.search('.+-ON-.+', course):
        return course
    else:
        return 'Skip'


def list_non_pt(course):
    """Replaces the course name of non-part-time courses with 'Skip'.
    
    Checks for part-time courses by looking for 'PT' in the course name. Those
    without 'PT' are overwritten with 'Skip'.
    
    Args:
        course (str): Information for course name.
        
    Returns:
        'Skip' if the course is not part-time, the passed course otherwise.
    """
    if re.search('.+\(.+-PT-.+\)', course):
        return course
    else:
        return 'Skip'


def list_non_pt_code(course):
    """Replaces the course name of non-part-time courses with 'Skip'.
    
    Checks for part-time courses by looking for 'PT' in the course code. Those
    without 'PT' are overwritten with 'Skip'.
    
    Args:
        course (str): Information for course name.
        
    Returns:
        'Skip' if the course is not part-time, the passed course otherwise.
    """
    if re.search('.+-PT-.+', course):
        return course
    else:
        return 'Skip'


def list_non_st(course):
    """Replaces the course name of non-student courses with 'Skip'.
    
    Checks for student courses by looking for '(..-..-..)' in the course name.
    Those without this are overwritten with 'Skip'.
    
    Args:
        course (str): Information for course name.
        
    Returns:
        'Skip' if the course is not for students, the passed course otherwise.
    """
    if re.search('.+\(.+-.+-.+\)', course):
        return course
    else:
        return 'Skip'


def load_data(source, f_name=''):
    """Read data from a file.

    Args:
        source (str): The code for the table that the source data belongs to.
        f_name (str): (Optional) File name to be loaded. If not provided, user
        will be prompted to provide a file name.

    Returns:
        read_data (list): A list containing the data read from the file.
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.
    """
    warnings = []
    # Load file
    if f_name in (None, ''): # Get from user
        read_data = ft.get_csv_fname_load(source)
    else:
        read_data = ft.load_csv(f_name, 'e')
    # Check that data has entries for each required column
    if source == 'Active_Students_File_':
        to_add, items_to_add = check_active_students(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Addresses_':
        to_add, items_to_add = check_add(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Count_Completions_Report_':
        to_add, items_to_add = check_ccr(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Count_Students_Tutors_Report_':
        to_add, items_to_add = check_cst(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Count_Unmarked_Assess_Report_':
        to_add, items_to_add = check_ua(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Expiry_Report_':
        to_add, items_to_add = check_expiry_report(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Insightly Tag Data':
        to_add, items_to_add = check_insightly(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Last_Login_':
        to_add, items_to_add = check_last_login(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Last Submission Data':
        to_add, items_to_add = check_last_sub_date(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Never_Logged_In_':
        to_add, items_to_add = check_never_logged_in(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Not_Logged_In_':
        to_add, items_to_add = check_not_logged_in(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Previous Tag Data':
        to_add, items_to_add = check_prev_data(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)           
    elif source == 'Student Database Tags':
        to_add, items_to_add = check_tags_data(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Students_File_':
        to_add, items_to_add = check_students_file(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Submissions_Made_':
        to_add, items_to_add = check_subs_made(read_data, source)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Tutor_IDs_':
        to_add, items_to_add = check_tu(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'User_Completions_Mark_Report_':
        to_add, items_to_add = check_ucm(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'User_Mark_Tutor_Only_':
        to_add, items_to_add = check_umt(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    if len(warnings) > 0:
        return read_data, True, warnings
    else:
        return read_data, False, warnings


def main():
    repeat = True
    low = 1
    high = 18
    while repeat:
        try_again = False
        main_message()
        try:
            action = int(input('\nPlease enter the number for your '
                               'selection --> '))
        except ValueError:
            print('Please enter a number between {} and {}.'.format(low, high))
            try_again = True
        else:
            if int(action) < low or int(action) > high:
                print('\nPlease select from the available options ({} - {})'
                      .format(low, high))
                try_again = True
            elif action == 1:
                process_expiry('10_Days_')
            elif action == 2:
                process_expiry('1_Month_')
            elif action == 3:
                process_expiry('3_Months_')
            elif action == 4:
                process_submissions_made_pt('2_Weeks_')
            elif action == 5:
                process_submissions_made_on('4_Weeks_')  
            elif action == 6:
                process_not_submitted_pt('2_Weeks_')                
            elif action == 7:
                process_not_submitted_on('4_Weeks_') 
            elif action == 8:
                process_last_login()
            elif action == 9:
                process_never_logged_in()
            elif action == 10:
                process_not_logged_in_pt('1_Week_')
            elif action == 11:
                process_not_logged_in_on('4_Weeks_')
            elif action == 12:
                process_completion_mcg()
            elif action == 13:
                process_complete_tut()
            elif action == 14:
                process_completions_tut()
            elif action == 15:
                process_count_ass_unmarked()
            elif action == 16:
                process_count_students_tut()
            elif action == 17:
                process_insightly_tags()
            elif action == high:
                print('\nIf you have generated any files, please find them '
                      'saved to disk. Goodbye.')
                sys.exit()
        if not try_again:
            repeat = ad.check_repeat()
    print('\nPlease find your files saved to disk. Goodbye.')


def main_message():
    """Print the menu of options."""
    print('\n\n*************==========================*****************')
    print('\nStudent Report Preparer version 1.0')
    print('Created by Jeff Mitchell, 2018')
    print('\nOptions:')
    print('\n1 Prepare Student Expiry Report - 10 Days')
    print('2 Prepare Student Expiry Report - 1 Month')
    print('3 Prepare Student Expiry Report - 3 Months')
    print('4 Prepare Submissions Made Report - 2 Weeks')
    print('5 Prepare Submissions Made Report - 4 Weeks')
    print('6 Prepare Students Not Submitted Report - 2 Weeks')
    print('7 Prepare Students Not Submitted Report - 4 Weeks')
    print('8 Prepare Last Login Report')
    print('9 Prepare Never Logged In Report')
    print('10 Prepare Not Logged In Report - 1 Week')
    print('11 Prepare Not Logged In Report - 4 Weeks')
    print('12 Prepare Completion Mark Course Group Report')
    print('13 Prepare Complete Tutor Only Report')
    print('14 Prepare Count of Completions Tutor Group Report')
    print('15 Prepare Count of Unmarked Assessments Report')
    print('16 Prepare Count of Students Per Tutor Report')
    print('17 Prepare Insightly Tags Updates Report')
    print('18 Exit')


def merge_tags(list_a, list_b, common):
    """Return students with tag info for further analysis.
    
    Returns a list with each student that appears in both lists. Appends the
    tag for each student from each list to the student. Also appends a value
    based on each tag which is used in a later function to determine if the
    student has progressed or regressed.
    
    Args:
        list_a (list): Current month student data.
        list_b (list): Previous month student data.
        common (list): Student IDs appearing in both lists.
    
    Returns:
        students (list): Updated student tags information.
        
    File structure (list_x):
        StudentID, EnrolmentID, Student, Course, Tutor, Updated_Tags.
    """
    allowed = ['Green', 'Orange', 'Red', 'Black']
    students = []
    for student in common:
        this_student = []
        this_student.append(student)
        for student_a in list_a:
            # print('Student a: {}'.format(student_a[0]))
            if student == student_a[0]:
                # print('Student found')
                # Add data from list_a
                i = 1
                while i < 6:
                    this_student.append(student_a[i])
                    i += 1
                # Add tag from list_b
                for student_b in list_b:
                    if student == student_b[0]:
                        this_student.append(student_b[5])
                        break
                break
        students.append(this_student)
    # Remove students that do not have an allowed tag
    for student in students:
        if student[5] not in allowed or student[6] not in allowed:
            students.remove(student)      
    # Add values for tags
    students = get_tags_values(students)
    return students    


def process_complete_tut():
    """Prepares Users marked by tutor only report.
    
    Checks the source file and then saves it as an .xls file.
    
    File Structure (Users marked by tutor only):
        Course, Tutor group, Student ID, Student, Tutor, Head Tutor, Manager
        
    File Source(Users marked by tutor):
        Users marked by tutor but not head tutor or manager
    """
    warnings = ['\nProcessing Users marked tutor only Report data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Users marked tutor only Report data.')
    # Confirm the required files are in place
    required_files = ['Users marked tutor only Report']
    ad.confirm_files('Users marked tutor only Report', required_files)
    # Get name for 'Users marked tutor only' Report data file and then load
    report_data, to_add, warnings_to_add = load_data('User_Mark_Tutor_Only_'
                                                     'Report_')
    # print('Check loaded data:')
    # ad.debug_list(report_data)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe with the data
    headings = ['Course', 'Tutor group', 'Student ID', 'Student', 'Tutor',
                'Head Tutor', 'Manager']
    comp = pd.DataFrame(data = report_data, columns = headings)
    f_name = 'Users_Mark_Tutor_Only_All_{}.xls'.format(
            ft.generate_time_string())
    comp.to_excel(f_name, index=False)
    print('\nUsers_Mark_Tutor_Only_All_ has been saved to {}'.format(f_name))
    ft.process_warning_log(warnings, warnings_to_process)
    

def process_completion_mcg():
    """Prepare Users completion mark by course and group report.
    
    Filters out courses that are not for students by looking for *(*-*-*)* in
    course name.
    
    File Structure (Completion mark group report):
        Course, Tutor group, Student ID, Student, Tutor, Head Tutor, Manager
        
    File Source (Completion mark group report):
        Users completion mark by course and group
    """
    warnings = ['\nProcessing User completions mark Report data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing User completions mark Report data.')
    # Confirm the required files are in place
    required_files = ['User completions mark Report']
    ad.confirm_files('User completions mark Report', required_files)
    # Get name for 'User completions mark Report' Report data file and then load
    report_data, to_add, warnings_to_add = load_data('User_Completions_Mark_'
                                                     'Report_')
    # print('Check loaded data:')
    # ad.debug_list(report_data)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe with the data
    headings = ['Course', 'Tutor group', 'Student ID', 'Student', 'Tutor',
                'Head Tutor', 'Manager']
    comp = pd.DataFrame(data = report_data, columns = headings)
    # Change value in Course column to 'Skip' if not a student course
    comp['Course'] = comp['Course'].apply(list_non_st)
    # Remove courses that are not Part-time ('Skip' in 'Course')
    comp = comp.drop(comp.index[comp['Course'] == 'Skip'])   
    # Save Master file
    f_name = 'User_Completions_Mark_All_{}.xls'.format(
            ft.generate_time_string())
    comp.to_excel(f_name, index=False)
    print('\nUser_Completions_Mark_All_ has been saved to {}'.format(f_name))
    ft.process_warning_log(warnings, warnings_to_process)


def process_completions_tut():
    """Prepare Count of completions by tutor and group in courses report.
    
    Filters out courses that are not Part-time by looking for *(*-PT-*)* in
    course name.
    
    File Structure (Count of completions report):
        Course, Tutor, Completions
        
    File Source (Count of completions report):
        Count of completions by tutor and group in courses
    """
    warnings = ['\nProcessing Count of completions Report data Warnings:\n']
    warnings_to_process = False
    print('\nCount of completions Report data.')
    # Confirm the required files are in place
    required_files = ['Count of completions Report']
    ad.confirm_files('Count of completions Report', required_files)
    # Get name for 'Count of completions Report' Report data file and then load
    report_data, to_add, warnings_to_add = load_data('Count_Completions_'
                                                     'Report_')
    # print('Check loaded data:')
    # ad.debug_list(report_data)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe with the data
    headings = ['Course', 'Tutor', 'Completions']
    comp = pd.DataFrame(data = report_data, columns = headings)
    # Change value in Course column to 'Skip' if not a Part-time course
    comp['Course'] = comp['Course'].apply(list_non_pt)
    # Remove courses that are not Part-time ('Skip' in 'Course')
    comp = comp.drop(comp.index[comp['Course'] == 'Skip'])
    # Convert the Completions column to integers
    comp['Completions'] = comp['Completions'].apply(ad.convert_to_int)
    # Save Master file
    f_name = 'Count_Completions_Report_All_{}.xls'.format(
            ft.generate_time_string())
    comp.to_excel(f_name, index=False)
    print('\nCount_Completions_Report_ has been saved to {}'.format(f_name))
    ft.process_warning_log(warnings, warnings_to_process)


def process_count_ass_marked():
    """Still to be written
    """
    pass


def process_count_ass_unmarked():
    """Prepare Count of unmarked assessments per tutor report.
    
    File Structure (Count of unmarked assessments per tutor report):
        Course, Tutor, Number assessments
        
    File Source (Count of unmarked assessments per tutor report):
        Count of unmarked assessments per tutor report
    """
    warnings = ['\nProcessing Count of unmarked assessments per tutor Report '
                'data Warnings:\n']
    warnings_to_process = False
    print('\nCount of unmarked assessments per tutor Report data.')
    # Confirm the required files are in place
    required_files = ['Count of unmarked assessments per tutor Report']
    ad.confirm_files('Count of unmarked assessments per tutor Report',
                  required_files)
    # Get name for 'Count of umarked... Report' Report data file and then load
    report_data, to_add, warnings_to_add = load_data('Count_Unmarked_Asses_'
                                                     'Report_')
    # print('Check loaded data:')
    # ad.debug_list(report_data)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe with the data
    headings = ['Course', 'Tutor', 'Number assessments']
    comp = pd.DataFrame(data = report_data, columns = headings)
    # Convert the Number Students column to integers
    comp['Number assessments'] = comp['Number assessments'].apply(
            ad.convert_to_int)
    # Save Master file
    f_name_1 = 'Count_Unmarked_Assessments_Report_All_'
    f_name = '{}{}.xls'.format(f_name_1, ft.generate_time_string())
    comp.to_excel(f_name, index=False)
    print('\n{} has been saved to {}'.format(f_name_1, f_name))
    ft.process_warning_log(warnings, warnings_to_process)


def process_count_students_tut():
    """Prepare Count of students per tutor group report.
    
    File Structure (Count of students per tutor group report):
        Course, Tutor, Completions
        
    File Source (Count of students per tutor group report):
        Count of students per tutor group
    """
    warnings = ['\nProcessing Count of students in tutor group Report data'
                ' Warnings:\n']
    warnings_to_process = False
    print('\nCount of students in tutor group Report data.')
    # Confirm the required files are in place
    required_files = ['Count of students in tutor group Report']
    ad.confirm_files('Count of students in tutor group Report', required_files)
    # Get name for 'Count of students... Report' Report data file and then load
    report_data, to_add, warnings_to_add = load_data('Count_Students_Tutors_'
                                                     'Report_')
    # print('Check loaded data:')
    # ad.debug_list(report_data)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe with the data
    headings = ['Course', 'Tutor', 'Number Students']
    comp = pd.DataFrame(data = report_data, columns = headings)
    # Convert the Number Students column to integers
    comp['Number Students'] = comp['Number Students'].apply(ad.convert_to_int)
    # Save Master file
    f_name_1 = 'Count_Students_Tutor_Report_All_'
    f_name = '{}{}.xls'.format(f_name_1, ft.generate_time_string())
    comp.to_excel(f_name, index=False)
    print('\n{} has been saved to {}'.format(f_name_1, f_name))
    ft.process_warning_log(warnings, warnings_to_process)


def process_expiry(period):
    """Process expiry report.

    Process a report for the students that are expiring. Adds to the report the
    student's address details from the student database.
    
    Args:
        period (str): Period report covers. Used for save file name.
    
    File Structure (Expiry report):
        Student ID, Student, Email, Course, Expiry Date
        
    File Structure (Addresses):
        StudentPK, AddressNumber, AddressStreet, AddressSuburb, AddressCity,
        AddressPostcode, AddressCountry
        
    File Source (Expiry report):
        Students expiring X months
        
    File Source (Addresses):
        Student Database (Students Table)
    """
    warnings = ['\nProcessing Expiry Report data Warnings:\n']
    warnings_to_process = False
    print('\nExpiry Report data.')
    # Confirm the required files are in place
    required_files = ['Expiry Report', 'Addresses']
    ad.confirm_files('Expiry Report', required_files)
    # Get name for Expiry Report data file and then load
    report_data, to_add, warnings_to_add = load_data('Expiry_Report_')
    # print('Check loaded data:')
    # ad.debug_list(report_data)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Get name for Addresses data file and then load
    address_data, to_add, warnings_to_add = load_data('Addresses_')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe with the address data
    headings = ['Student ID', 'Number', 'Street', 'Suburb', 'City', 'Postcode',
                'Country']
    addresses = pd.DataFrame(data = address_data, columns = headings)
    # Create a dataframe with the report data
    headings = ['Student ID', 'Student', 'Email', 'Course',
                'Expiry Date']
    expiry = pd.DataFrame(data = report_data, columns = headings)
    # Change value in 'Expiry Date' if student has expired
    expiry['Expiry Date'] = expiry['Expiry Date'].apply(list_expired)
    # Remove students that have already expired ('Expired' in 'Expiry Date')
    expiry = expiry.drop(expiry.index[expiry['Expiry Date'] == 'Expired'])
    # Convert Expiry date to DD-MM-YYYY
    expiry['Expiry Date'] = expiry['Expiry Date'].apply(da.clean_date,
          args=('-','-',''))
    # Merge the two dataframes so that address information is incorporated
    updated_expiry = pd.merge(expiry, addresses, on = 'Student ID',
                              how = 'left')
    # Save Master file
    f_name = 'Expiry_Report_{}{}.xls'.format(period, ft.generate_time_string())
    updated_expiry.to_excel(f_name, index=False)
    print('\nExpiry_Report_ has been saved to {}'.format(f_name))
    ft.process_warning_log(warnings, warnings_to_process)


def process_insightly_tags():
    """Process Insightly Tags updates report.
    
    Process the Insightly Tags based on student submission reports. Generates
    a report of all active student's status tags and a second report that lists
    all of the tags that need to be changed.
    
    File Structure (Student Database Tags):
        EnrolmentPK, StudentID, NameGiven, NameSurname, CourseFK, TutorFK,
        Status, Tag, StartDate.
    
    File Structure (Insightly Tags Data):
        Student ID Number, First Name, Last Name, Contact Tag List
        
    File Structure (Submissions):
        Student ID, Student, Course, Tutor, Last submission date.
    
    File Structure (Tutor_IDs.csv):
        TutorID, First Name, Last Name.
        
    File Structure (Last Month Tags):
        StudentID, EnrolmentID, Student, Course, Tutor, Updated_Tags.
        
    File Source (Student Database Tags):
        qryEnrolmentTags query from Student Database.
    
    File Source (Insightly Tags):
        Insightly Data Dump (using columns listed in File structure).    
    
    File Source (Submissions):
        Learning Platform reports - Last submission date (all courses)
    
    File Source (Tutor_IDs.csv):
        Tutors sheet of Enrolments Google Sheet or Student Database.
        
    File Source (Last Month Tags):
        Updated_Tags report from the previous month.
    """
    warnings = ['\nProcessing Insightly Tags data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Insightly Tags data.')
    # Confirm the required files are in place
    required_files = ['Student Database Tags', 'Tutor IDs File', 'Submissions',
                      'Insightly Tags Data', 'Last Month Tags']
    ad.confirm_files('Insightly Tags Report', required_files)
    # Variables for column names
    cid_name  = 'Course ID'
    course_name = 'Course'
    eid_name = 'EnrolmentID'
    fname_name  = 'First Name'
    lname_name  = 'Last Name'
    sdate_name = 'Start Date'
    sid_name  = 'StudentID'
    status_name  = 'Status'
    stud_name = 'Student'
    tag_name = 'Tag'
    tid_name  = 'Tutor ID'
    tutor_name = 'Tutor'
    # Load Tutor_Id.csv
    tutors_data, to_add, warnings_to_add = load_data('Tutor_IDs_', 'Tutor_IDs')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a DataFrame for the Tutor IDs data
    headings = [tid_name, fname_name, lname_name]
    tutors = pd.DataFrame(data = tutors_data, columns = headings)
    # Create a list of Tutor ID's
    tutor_ids = tutors[tid_name].unique()
    # Get name for the Student Database Tags data file and then load
    sd_data, to_add, warnings_to_add = load_data('Student Database Tags')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Go through tutor ids in database data and make sure present in tutor data
    check_tutor_ids(tutor_ids, sd_data)
    # Create a DataFrame for the Student Database Tags data
    headings = [eid_name, sid_name, fname_name, lname_name, cid_name, tid_name,
                status_name, tag_name, sdate_name]
    sd_df = pd.DataFrame(data = sd_data, columns = headings)
    # Convert Start Dates to "DD/MM/YYYY"
    sd_df[sdate_name] = sd_df[sdate_name].apply(da.clean_date)
    # Get name for the Insightly Tags data file and then load
    id_data, to_add, warnings_to_add = load_data('Insightly Tag Data')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean Insightly Tag data
    id_clean = clean_insightly(id_data)
    # Create DataFrame for Insightly Data
    headings = [sid_name, fname_name, lname_name, tag_name]
    id_df = pd.DataFrame(data = id_clean, columns = headings)
    # Extract Insightly Tag info (status tag)
    # Find status tag and save to column
    id_df[tag_name] = id_df[tag_name].apply(extract_tag)
    headings = [sid_name, tag_name]
    id_df = id_df[headings]
    # Load Tutor_Id.csv
    tutors_data, to_add, warnings_to_add = load_data('Tutor_IDs_', 'Tutor_IDs')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a DataFrame for the Tutor IDs data
    headings = [tid_name, fname_name, lname_name]
    tutors = pd.DataFrame(data = tutors_data, columns = headings)
    # Load Last submission date information
    lsd_data, to_add, warnings_to_add = load_data('Last Submission Data')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # ad.debug_list(lsd_data)
    print('\nNow processing the data. Please wait...')
    # Clean Last submissions data
    lsd_clean = clean_last_subs_date(lsd_data)
    # ----------------------------------------------------------------------
    # Filter out inactive students so not included in enrolment date check
    # ----------------------------------------------------------------------
    # Get a list of the Student ID's in sd_df (minus inactive)
    sd_df_students = get_sd_df_students(sd_df, sid_name, tag_name)
    # Convert Enrolment Date to a Status Tag - only for Active students
    lsd_tags = convert_e_date(lsd_clean, sd_df_students)    
    # Get a list of students in lsd_tags
    lsd_tags_students = get_lsd_tags_students(lsd_tags, sd_df_students, 0)
    # Get list of students missing from lsd_tags
    missing_students = find_missing(sd_df_students, lsd_tags_students)
    # Add missing active students and their details to the lsd_tags data
    # Set tag to 'Black' as have not submitted and zones will correct
    lsd_tags = add_missing(lsd_tags, sd_df, tutors, missing_students,
                           fname_name, lname_name, tid_name, sid_name,
                           cid_name)
    # Create Tag Zone lists (Max tag a student can have based on enrolment)
    en_dates = get_enrol_dates(sd_df, sid_name, sdate_name, sd_df_students)
    black, red, orange, green = get_colour(en_dates)
    # Create a list to hold StudentID, sub_tag, zone
    student_tags = get_tags(lsd_tags, black, red, orange, green)
    # Determine Tag for each student
    updated_tags = update_tags(student_tags)
    # print('Updated: tags:')
    # print(updated_tags)
    # Create a list of Student ID's for students with Purple Tags
    purple = get_purple(id_df, sid_name, tag_name)
    # Overwrite purple students
    updated_tags = convert_purple(updated_tags, purple)
    # -----------------------------------------------------------------------
    # Inactive students returned to Updated_tags
    # -----------------------------------------------------------------------
    new_tags = add_inactive(updated_tags, sd_df, sid_name, tag_name)
    # Create a DataFrame with the updated tags info
    new_tags_name = 'Updated_Tags'
    headings = [sid_name, new_tags_name]
    tags_df = pd.DataFrame(data = new_tags, columns = headings)
    # Add Enrolment ID
    tags_df = add_eid(tags_df, sd_df, sid_name, eid_name, new_tags_name)
    # Add Student Details
    headings = [sid_name, eid_name, stud_name, course_name, tutor_name,
                new_tags_name]
    headings_sd_df = [eid_name, sid_name, fname_name, lname_name, cid_name,
                      tid_name, status_name, tag_name, sdate_name]
    tags_df = add_stud(tags_df, sd_df, headings, headings_sd_df)
    # Replace Tutor ID with Tutor Name
    headings = [tid_name, fname_name, lname_name]
    tags_df[tid_name] = tags_df[tid_name].apply(replace_single_tutor_name,
           args=(tutors, headings))
    # Rename Tutor ID column to Tutor
    tags_df = tags_df.rename(columns={tid_name:tutor_name})
    # Sort by Tutor and then Student
    tags_df = tags_df.sort_values([tutor_name, stud_name])
    # Save the updated tags information - record of current tags
    f_name = 'Updated_Tags_{}.xls'.format(ft.generate_time_string())
    tags_df.to_excel(f_name, index=False)
    # Save as CSV to be opened for comparison analysis
    ut_name = 'Updated_Tags_{}.csv'.format(ft.generate_time_string())
    tags_df.to_csv(ut_name, index=False)
    print('\nUpdated_Tags has been saved to {}'.format(f_name))
    print('\nAnalysing changes to tags in Student Database.')
    # Check for changes made to tags from sd_data
    headings = [sid_name, eid_name, stud_name, new_tags_name]
    sd_changed = get_sd_changes(sd_df, tags_df, headings, tag_name)
    sd_changed = sd_changed.sort_values(sid_name)
    # print(sd_changed)
    # Save the changed tags information - Student Database tags to update
    f_name = 'Changed_Tags_Student_Database_{}.xls'.format(
            ft.generate_time_string())
    sd_changed.to_excel(f_name, index=False)
    print('\nChanged_Tags_Student_Database_ has been saved to {}'.format(
            f_name))
    print('\nAnalysing changes to tags in Insightly.')
    # Check for changes made to tags from insightly data
    headings = [sid_name, stud_name, tutor_name, new_tags_name]
    # Get a list of student ID in tags_df
    tags_df_students = get_students(tags_df, sid_name)
    # Get tutor name for each student in list and add it
    tags_df_students = add_tutor(tags_df_students, sd_df, tutors, fname_name,
                                 lname_name, tid_name, sid_name)
    # Add Tutor column to tags_df and add the tutor name for each student
    tags_df = add_tutor_df(tags_df, tags_df_students, headings)
    id_changed = get_id_changes(tags_df, id_df, headings, tag_name)
    id_changed = id_changed.sort_values([tutor_name, stud_name])
    # print(id_changed)
    # Save the changed tags information - Insightly tags to update
    f_name = 'Changed_Tags_Insightly_{}.xls'.format(ft.generate_time_string())
    id_changed.to_excel(f_name, index=False)
    print('\nChanged_Tags_Insightly_ has been saved to {}'.format(f_name))
    print('\nCounting number of tags per tutor.')
    # Count the number of tags per colour per tutor
    headings = [sid_name, eid_name, stud_name, course_name, tutor_name,
                new_tags_name]
    # Get Dictionary with the tags count information
    tags_tutor, tags_list = tags_count(tags_df, headings)
    # Extract Dictionary items into a list
    tag_count = get_tutor_tags(tags_tutor, tags_list)
    headings = ['Tutor', tags_list[0], tags_list[1], tags_list[2], 
                tags_list[3], tags_list[4]]
    # Create a DataFrame for Tutor tags count
    tags_tutor_df = pd.DataFrame(data=tag_count, columns = headings)
    # Rename empty Tutor cell
    tags_tutor_df['Tutor'] = tags_tutor_df['Tutor'].apply(rename_tutor)
    # Add a Total row
    tags_tutor_df = tags_tutor_df.append(tags_tutor_df.sum(numeric_only=True),
                         ignore_index=True)
    num_rows = tags_tutor_df.shape[0] - 1
    tags_tutor_df.loc[num_rows, 'Tutor'] = 'Total'
    # Save the Count of Tags by Tutor
    f_name = 'Tags_Count_{}.xls'.format(ft.generate_time_string())
    tags_tutor_df.to_excel(f_name, index=False)
    print('\nTags_Count_ has been saved to {}'.format(f_name))
    print('\nAnalysing Student changes.')
    # Get count of students that have regressed and progressed
    # Load previous month's tags
    prev_data, to_add, warnings_to_add = load_data('Previous Tag Data')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Load Updated Tags for this month (processed earlier) into a list
    ut_name = ut_name[:-4] # Remove .csv from file name
    print('\nLoading {}...'.format(ut_name))
    this_data, to_add, warnings_to_add = load_data('Previous Tag Data',
                                                   ut_name)
    print('\nLoaded {}.'.format(ut_name))
    # ad.debug_list(this_data)
    # Get Dictionary with counts for each tutor
    tutor_stats, change_list = get_tutor_stats(prev_data, this_data)
    # Extract Dictionary items into a list
    change_count = get_tutor_changes(tutor_stats, change_list)
    # Create a DataFrame
    headings = ['Tutor', 'Progressed', 'Regressed', 'Maintained']
    change_count_df = pd.DataFrame(data = change_count, columns = headings)
    change_count_df = change_count_df.append(
            change_count_df.sum(numeric_only=True), ignore_index=True)
    change_count_df['Tutor'] = change_count_df['Tutor'].apply(rename_tutor)
    num_rows = change_count_df.shape[0] - 1
    change_count_df.loc[num_rows, 'Tutor'] = 'Total'
    f_name = 'Tags_Changes_{}.xls'.format(ft.generate_time_string())
    change_count_df.to_excel(f_name, index=False)
    print('\nTags_Changes has been saved to {}'.format(f_name))
    ft.process_warning_log(warnings, warnings_to_process)


def process_last_login():
    """Process Last Login In report.
    
    Process the report of the last time students accessed a course.
        
    File Structure (Last login):
        Student ID, Student, Tutor, Course, Last Access
        
    File Source (Last login):
        Last login date
    """
    warnings = ['\nProcessing Last Login data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Last Login data.')
    # Confirm the required files are in place
    required_files = ['Last Login Report']
    ad.confirm_files('Last Login Report', required_files)
    # Get name for Last Login Report data file and then load
    report_data, to_add, warnings_to_add = load_data('Last_Login_')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe with the data
    headings = ['Student ID', 'Student', 'Tutor', 'Course', 'Last Access',
                'Email']
    last_logged = pd.DataFrame(data = report_data, columns = headings)
    last_col = 'Last Access'
    # Convert timestamps to dates (strings)
    last_logged[last_col] = last_logged[last_col].apply(da.clean_date,
               args=('-','-',''))
    # Replace 01-01-1970 with an empty string in date column Last Submission
    last_logged[last_col] = last_logged[last_col].apply(da.replace_nil_date)
    # Save Master file
    f_name = 'Last_Login_All_{}.xls'.format(ft.generate_time_string())
    last_logged.to_excel(f_name, index=False)
    print('\nLast_Login_All_ has been saved to {}'.format(f_name))
    ft.process_warning_log(warnings, warnings_to_process)


def process_never_logged_in():
    """Process a Never Logged In report.

    Loads the report data file and processes it.
    Saves the processed data to a file for distributing to management and
    individual files for each tutor.
    
    File Structure (Never Logged In Report):
        Student ID, Student, Tutor, Course, Account Created, Report Date, Email
        
    File Source (Never Logged In Report):
        Students never logged in
    """
    warnings = ['\nProcessing Never Logged In data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Never Logged In data.')
    # Confirm the required files are in place
    required_files = ['Never Logged In Report']
    ad.confirm_files('Never Logged In Report', required_files)
    # Get name for Never Logged In Report data file and then load
    report_data, to_add, warnings_to_add = load_data('Never_Logged_In_')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe with the data
    headings = ['Student ID', 'Student', 'Tutor', 'Course', 'Account Created',
                'Report Date', 'Email']
    not_logged = pd.DataFrame(data = report_data, columns = headings)
    # Convert timestamps to dates (strings)
    not_logged['Account Created'] = not_logged['Account Created'].apply(
            da.clean_date, args=('-','-',''))
    not_logged['Report Date'] = not_logged['Report Date'].apply(da.clean_date,
              args=('-','-',''))
    # Save Master file
    f_name = 'Never_Logged_In_All_{}.xls'.format(ft.generate_time_string())
    not_logged.to_excel(f_name, index=False)
    print('\nNever_Logged_In_All_ has been saved to {}'.format(f_name))
    ft.process_warning_log(warnings, warnings_to_process)
    

def process_not_logged_in_on(period):
    """Process Not Logged In report for online courses.
    
    Process the report of students who have not accessed an online course
    during the reporting timeframe.
    
    Args:
        period (str): Period the report covers.
        
    File Structure (Not logged in):
        Student ID, Student, Tutor, Course, Last Access
        
    File Source (Not logged in):
        Students have not logged in last 4 weeks
    """
    warnings = ['\nProcessing Not Logged In data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Not Logged In data.')
    # Confirm the required files are in place
    required_files = ['Not Logged In Report']
    ad.confirm_files('Not Logged In Report', required_files)
    # Get name for Not Logged In Report data file and then load
    report_data, to_add, warnings_to_add = load_data('Not_Logged_In_')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe with the data
    headings = ['Student ID', 'Student', 'Tutor', 'Course', 'Last Access',
                'Email']
    r_data = pd.DataFrame(data = report_data, columns = headings)
    # Change value in Course column to 'Skip' if not an online course
    r_data['Course'] = r_data['Course'].apply(list_non_on)
    # Remove courses that are not Online ('Skip' in 'Course')
    r_data = r_data.drop(r_data.index[r_data['Course'] == 'Skip'])
    last_col = 'Last Access'
    # Convert timestamps to dates (strings)
    r_data[last_col] = r_data[last_col].apply(da.clean_date, args=('-','-',''))
    # Replace 01-01-1970 with an empty string in date column Last Submission
    r_data[last_col] = r_data[last_col].apply(da.replace_nil_date)
    # Save Master file
    f_name = 'Not_Logged_In_ON_{}{}.xls'.format(period,
                               ft.generate_time_string())
    r_data.to_excel(f_name, index=False)
    print('\nNot_Logged_In_ON_{} has been saved to {}'.format(period, f_name))
    ft.process_warning_log(warnings, warnings_to_process)


def process_not_logged_in_pt(period):
    """Process Not Logged In report for part-time courses.
    
    Process the report of students who have not accessed a part-time course
    during the reporting timeframe.
    
    Args:
        period (str): Period the report covers.
        
    File Structure (Not logged in):
        Student ID, Student, Tutor, Course, Last Access, Email
        
    File Source (Not logged in):
        Students have not logged in last week
    """
    warnings = ['\nProcessing Not Logged In data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Not Logged In data.')
    # Confirm the required files are in place
    required_files = ['Not Logged In Report']
    ad.confirm_files('Not Logged In Report', required_files)
    # Get name for Not Logged In Report data file and then load
    report_data, to_add, warnings_to_add = load_data('Not_Logged_In_')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe with the data
    headings = ['Student ID', 'Student', 'Tutor', 'Course', 'Last Access',
                'Email']
    r_data = pd.DataFrame(data = report_data, columns = headings)
    # Change value in Course column to 'Skip' if not a Part-time course
    r_data['Course'] = r_data['Course'].apply(list_non_pt)
    # Remove courses that are not Part-time ('Skip' in 'Course')
    r_data = r_data.drop(r_data.index[r_data['Course'] == 'Skip'])
    last_col = 'Last Access'
    # Convert timestamps to dates (strings)
    r_data[last_col] = r_data[last_col].apply(da.clean_date, args=('-','-',''))
    # Replace 01-01-1970 with an empty string in date column Last Submission
    r_data[last_col] = r_data[last_col].apply(da.replace_nil_date)
    # Save Master file
    f_name = 'Not_Logged_In_PT_{}{}.xls'.format(period,
                               ft.generate_time_string())
    r_data.to_excel(f_name, index=False)
    print('\nNot_Logged_In_PT_{} has been saved to {}'.format(period, f_name))
    ft.process_warning_log(warnings, warnings_to_process)
    

def process_not_submitted_on(period):
    """Process a report of students that have not submitted for online courses.
    
    Takes the data of the students that have submitted and compares to the list
    of students on the course. Returns a list of students that do not appear in
    the submission report (and therefore have not submitted in the report time
    frame).
    
    Args:
        period (str): Period the report covers.
    
    File Structure (Submissions Made Report):
        Student ID,Student,Course,Tutor,Assignment name,Last submission date
    
    File Source (Submissions Made Report):
        Students submitted work in previous X weeks
        
    File Structure (Students File):
        Course, Tutor, Student ID, Student
        
    File Source (Students File):
        Students in Tutor Group
        
    File Structure (Active Students):
        Student ID, Student, Course
    
    File Source (Active Students):
        Active students in a course
    """
    warnings = ['\nProcessing Not Submitted data Warnings:\n']
    warnings_to_process = False
    print('\nNot Submitted data.')
    # Confirm the required files are in place
    required_files = ['Submissions Made report', 'Student File',
                      'Active Students File']
    ad.confirm_files('Not Submitted Report', required_files)
    # Get name for Submissions Made Report data file and then load
    report_data, to_add, warnings_to_add = load_data('Submissions_Made_')
    # print('Check loaded data:')
    # ad.debug_list(report_data)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Get the name for the Students File
    student_data, to_add, warnings_to_add = load_data('Students_File_')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Get the name for the Active Students File
    active_students, to_add, warnings_to_add = load_data(
            'Active_Students_File_')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe for Submissions Made report data
    headings = ['Student ID', 'Student', 'Course', 'Tutor', 'Assignment name',
                'Last submission date']
    subs = pd.DataFrame(data = report_data, columns = headings)
    # Change value in Course column to 'Skip' if not an online course
    subs['Course'] = subs['Course'].apply(list_non_on)
    # Remove courses that are not Online ('Skip' in 'Course')
    subs = subs.drop(subs.index[subs['Course'] == 'Skip'])
    # Clean the Last submission date
    last_col = 'Last submission date'
    subs[last_col] = subs[last_col].apply(extract_last_submission_date)
    # Replace 01-01-1970 with an empty string in date column Last Submission
    subs[last_col] = subs[last_col].apply(da.replace_nil_date)
    # Create a dataframe for the students in the course
    headings = ['Course', 'Tutor', 'Student ID', 'Student']
    students = pd.DataFrame(data = student_data, columns = headings)
     # Change value in Course column to 'Skip' if not an Online course
    students['Course'] = students['Course'].apply(list_non_on)
    # Remove courses that are not Online ('Skip' in 'Course')
    students = students.drop(students.index[students['Course'] == 'Skip'])
    # Create a dataframe for active students
    headings = ['Student ID', 'Student', 'Course']
    active = pd.DataFrame(data = active_students, columns = headings)
    # Change value in Course column to 'Skip' if not an Online course
    active['Course'] = active['Course'].apply(list_non_on)
    # Remove courses that are not Online ('Skip' in 'Course')
    active = active.drop(active.index[active['Course'] == 'Skip'])
    # Remove students that aren't active in the course from students dataframe
    active_students = []
    # Get the Student ID for each student in active
    for index, row in active.iterrows():
        active_students.append(row['Student ID'])
    # Remove inactive students
    students = students[students['Student ID'].isin(active_students)]
    # Find students that have not submitted
    submitted_students = []
    # Get the Student ID for each student that has submitted
    for index, row in subs.iterrows():
        submitted_students.append(row['Student ID'])
    # Remove from Students those that have submitted
    sid_col = 'Student ID'
    non_sub_students = students[~students[sid_col].isin(submitted_students)]
    # Sort on the Student ID column
    non_sub_students =  non_sub_students.sort_values(['Tutor', 'Student ID'])
    # Save a master file ordered by Tutor and Student ID
    f_name = 'Not_Submitted_All_{}{}.xls'.format(period,
                                ft.generate_time_string())
    non_sub_students.to_excel(f_name, index=False)
    print('\nNot_Submitted_All_ has been saved to {}'.format(f_name))
    ft.process_warning_log(warnings, warnings_to_process)
    

def process_not_submitted_pt(period):
    """Process a report of students that have not submitted for pt courses.
    
    Takes the data of the students that have submitted and compares to the list
    of students on the course. Returns a list of students that do not appear in
    the submission report (and therefore have not submitted in the report time
    frame).
    
    Args:
        period (str): Period the report covers.
    
    File Structure (Submissions Made Report):
        Student ID,Student,Course,Tutor,Assignment name,Last submission date
    
    File Source (Submissions Made Report):
        Students submitted work in previous X weeks
        
    File Structure (Students File):
        Course, Tutor, Student ID, Student
        
    File Source (Students File):
        Students in Tutor Group
        
    File Structure (Active Students):
        Student ID, Student, Course
    
    File Source (Active Students):
        Active students in a course
    """
    warnings = ['\nProcessing Not Submitted data Warnings:\n']
    warnings_to_process = False
    print('\nNot Submitted data.')
    # Confirm the required files are in place
    required_files = ['Submissions Made report', 'Student File',
                      'Active Students File']
    ad.confirm_files('Not Submitted Report', required_files)
    # Get name for Submissions Made Report data file and then load
    report_data, to_add, warnings_to_add = load_data('Submissions_Made_')
    # print('Check loaded data:')
    # ad.debug_list(report_data)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Get the name for the Students File
    student_data, to_add, warnings_to_add = load_data('Students_File_')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Get the name for the Active Students File
    active_students, to_add, warnings_to_add = load_data('Active_Students_File_')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe for Submissions Made report data
    headings = ['Student ID', 'Student', 'Course', 'Tutor', 'Assignment name',
                'Last submission date']
    subs = pd.DataFrame(data = report_data, columns = headings)
    # Change value in Course column to 'Skip' if not a Part-time course
    subs['Course'] = subs['Course'].apply(list_non_pt)
    # Remove courses that are not Part-time ('Skip' in 'Course')
    subs = subs.drop(subs.index[subs['Course'] == 'Skip'])
    # Clean the Last submission date
    last_col = 'Last submission date'
    subs[last_col] = subs[last_col].apply(extract_last_submission_date)
    # Replace 01-01-1970 with an empty string in date column Last Submission
    subs[last_col] = subs[last_col].apply(da.replace_nil_date)
    # Create a dataframe for the students in the course
    headings = ['Course', 'Tutor', 'Student ID', 'Student']
    students = pd.DataFrame(data = student_data, columns = headings)
    # Change value in Course column to 'Skip' if not a Part-time course
    students['Course'] = students['Course'].apply(list_non_pt)
    # Remove courses that are not Part-time ('Skip' in 'Course')
    students = students.drop(students.index[students['Course'] == 'Skip'])
    # Create a dataframe for active students
    headings = ['Student ID', 'Student', 'Course']
    active = pd.DataFrame(data = active_students, columns = headings)
    # Change value in Course column to 'Skip' if not a Part-time course
    active['Course'] = active['Course'].apply(list_non_pt)
    # Remove courses that are not Part-time ('Skip' in 'Course')
    active = active.drop(active.index[active['Course'] == 'Skip'])
    # Remove students that aren't active in the course from students dataframe
    active_students = []
    # Get the Student ID for each student in active
    for index, row in active.iterrows():
        active_students.append(row['Student ID'])
    # Remove inactive students
    students = students[students['Student ID'].isin(active_students)]
    # Find students that have not submitted
    submitted_students = []
    # Get the Student ID for each student that has submitted
    for index, row in subs.iterrows():
        submitted_students.append(row['Student ID'])
    # Remove from Students those that have submitted
    sid_col = 'Student ID'
    non_sub_students = students[~students[sid_col].isin(submitted_students)]
    # Sort on the Student ID column
    non_sub_students =  non_sub_students.sort_values(['Tutor', 'Student ID'])
    # Save a master file ordered by Tutor and Student ID
    f_name = 'Not_Submitted_All_{}{}.xls'.format(period,
                                ft.generate_time_string())
    non_sub_students.to_excel(f_name, index=False)
    print('\nNot_Submitted_All_ has been saved to {}'.format(f_name))
    ft.process_warning_log(warnings, warnings_to_process)


def process_submissions_made_on(period):
    """Process a Submissions Made report for Online courses.

    Loads the report data file and processes it.
    Saves the processed data to a file for distributing to management and
    individual files for each tutor.
    
    Args:
        period (str) Period the report covers.
    
    File Structure (Submissions Made Report):
        Student ID,Student,Course,Tutor,Assignment name,Last submission date
    
    File Source (Submissions Made Report):
        Students submitted work in previous X weeks
    """
    warnings = ['\nProcessing Submissions Made data Warnings:\n']
    warnings_to_process = False
    print('\nSubmissions Made data.')
    # Confirm the required files are in place
    required_files = ['Submissions Made report']
    ad.confirm_files('Submissions Made Report', required_files)
    # Get name for Submissions Made Report data file and then load
    report_data, to_add, warnings_to_add = load_data('Submissions_Made_')
    # print('Check loaded data:')
    # ad.debug_list(report_data)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe for Submissions Made report data
    headings = ['Student ID', 'Student', 'Course', 'Tutor', 'Assignment name',
                'Last submission date']
    subs = pd.DataFrame(data = report_data, columns = headings)
    # Change value in Course column to 'Skip' if not an online course
    subs['Course'] = subs['Course'].apply(list_non_on)
    # Remove courses that are not Online ('Skip' in 'Course')
    subs = subs.drop(subs.index[subs['Course'] == 'Skip'])
    # Clean the Last submission date
    last_col = 'Last submission date'
    # print(subs)
    subs[last_col] = subs[last_col].apply(da.clean_date, args=('-','-',''))
    # Replace 01-01-1970 with an empty string in date column Last Submission
    subs[last_col] = subs[last_col].apply(da.replace_nil_date)
    # Remove Assessment name column
    headings = ['Student ID', 'Student', 'Course', 'Tutor',
                'Last submission date']
    subs = subs[headings]
    # Sort by Last submission date
    subs =  subs.sort_values(['Tutor', 'Last submission date'])
    # Save a master file
    f_name = 'Submitted_All_{}{}.xls'.format(period, ft.generate_time_string())
    subs.to_excel(f_name, index=False)
    print('\nSubmitted_All_ has been saved to {}'.format(f_name))
    ft.process_warning_log(warnings, warnings_to_process)


def process_submissions_made_pt(period):
    """Process a Submissions Made report for Part-time courses.

    Loads the report data file and processes it.
    Saves the processed data to a file for distributing to management and
    individual files for each tutor.
    
    Args:
        period (str) Period the report covers.
    
    File Structure (Submissions Made Report):
        Student ID,Student,Course,Tutor,Assignment name,Last submission date
    
    File Source (Submissions Made Report):
        Students submitted work in previous X weeks
    """
    warnings = ['\nProcessing Submissions Made data Warnings:\n']
    warnings_to_process = False
    print('\nSubmissions Made data.')
    # Confirm the required files are in place
    required_files = ['Submissions Made report']
    ad.confirm_files('Submissions Made Report', required_files)
    # Get name for Submissions Made Report data file and then load
    report_data, to_add, warnings_to_add = load_data('Submissions_Made_')
    # ad.debug_list(report_data)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create a dataframe for Submissions Made report data
    headings = ['Student ID', 'Student', 'Course', 'Tutor', 'Assignment name',
                'Last submission date']
    subs = pd.DataFrame(data = report_data, columns = headings)
    # Change value in Course column to 'Skip' if not a Part-time course
    subs['Course'] = subs['Course'].apply(list_non_pt)
    # Remove courses that are not Part-time ('Skip' in 'Course')
    subs = subs.drop(subs.index[subs['Course'] == 'Skip'])
    # Clean the Last submission date
    last_col = 'Last submission date'
    subs[last_col] = subs[last_col].apply(da.clean_date, args=('-','-',''))
    # Replace 01-01-1970 with an empty string in date column Last Submission
    subs[last_col] = subs[last_col].apply(da.replace_nil_date)
    # Remove Assessment name column
    headings = ['Student ID', 'Student', 'Course', 'Tutor',
                'Last submission date']
    subs = subs[headings]
    # Sort by Last submission date
    subs =  subs.sort_values(['Tutor', 'Last submission date'])
    # Save a master file
    f_name = 'Submitted_All_{}{}.xls'.format(period, ft.generate_time_string())
    subs.to_excel(f_name, index=False)
    print('\nSubmitted_All_ has been saved to {}'.format(f_name))
    ft.process_warning_log(warnings, warnings_to_process)


def removal(raw_data):
    """Replace Contact tag for unwanted students.
    
    Replaces the Tags field with 'Remove' if the student contains
    the tag 'Withdrawn', 'Graduated', 'Expired', 'Suspended', 'On Hold',
    'Cancelled' or 'Transferred'. This allows the students to be dropped from
    the data in a later step.
    
    Args:
        raw_data (str): String containing Contact tag data.
        
    Returns:
        'Remove' if a tag  in the list for removal is found, the passed Tags
        otherwise.
    """
    to_remove = ['withdrawn', 'graduated', 'expired', 'suspended', 'on hold',
                 'cancelled', 'transferred']
    for item in to_remove:
        if re.search(item, raw_data.lower()):
            return 'Remove'
    else:
        return raw_data


def rename_tutor(tutor):
    """Rename empty tutor in tags_count DataFrame.
    
    Args:
        tutor (str): Name of Tutor.
    
    Returns:
        'Combined or Unknown' if Tutor name is blank.
    """
    if tutor in (None, ''):
        return 'Combined or Unknown'
    else:
        return tutor


def replace_single_tutor_name(tutor_id, tutors, headings):
    """Replace Tutor ID with Tutor Name.
    
    Args:
        tutor (str): Tutor ID.
        tutors (DataFrame): TutorIDs.csv information. 
        headings (list): tid_name, fname_name, lname_name.
    
    Returns:
        tutor_name (str): Name of Tutor.
    """
    # Skip students without a tutor
    if tutor_id in (None, ''):
        return tutor_id
    # Create a dictionary with Tutor ID's and Tutor
    tutor_dict = {}
    for index, row in tutors.iterrows():
        # Create key value TutorID: First + Last Name
        tutor_dict[row[headings[0]]] = '{} {}'.format(row[headings[1]],
                  row[headings[2]])
    updated_tutor = tutor_dict[tutor_id]
    return updated_tutor


def replace_tutor_name(tutor_count, tutors, headings):
    """Replace Tutor ID with Tutor Name.
    
    Args:
        tutor_count (list): Tutor count information with Tutor ID.
        tutors (DataFrame): TutorIDs.csv information. 
        headings (list): tid_name, fname_name, lname_name.
    
    Returns:
        updated_tutors (list): Data with Tutor names replacing Tutor IDs.
    """
    updated_tutors = []
    # Create a dictionary with Tutor ID's and Tutor
    tutor_dict = {}
    for index, row in tutors.iterrows():
        # Create key value TutorID: First + Last Name
        tutor_dict[row[headings[0]]] = '{} {}'.format(row[headings[1]],
                  row[headings[2]])
    # Update Tutor names in tutor_count
    for tutor in tutor_count:
        updated_tutor = []
        updated_tutor.append(tutor_dict[tutor[0]])
        updated_tutor.append(tutor[1])
        updated_tutor.append(tutor[2])
        updated_tutor.append(tutor[3])
        updated_tutors.append(updated_tutor)
    return updated_tutors


def save_tags_count(count_data, headings, f_name):
    """Save tags count data to a CSV file.
    
    Note: Not currently used.
    
    Args:
        count_data (dict): Tutors and their tag counts.
        headings (list): Column headings.
        f_name (str): File name.
    """
    print('Data:')
    with open(f_name, 'w', newline='') as f:
        csvwriter = csv.writer(f, delimiter=',', quotechar='|',
                               lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        # Write data
        for tutor in count_data:
            for item in count_data[tutor]:
                csvwriter.writerow([tutor, item, count_data[tutor][item]])


def save_tutor_df(all_data, d_name, tut_col):
    """Save data for each tutor into separate csv files.
    
    Args:
        all_Data (DataFrame): The data to be saved.
        d_name (str): Name of the file to save to.
        tut_col (str): Name of the column holding tutor data.
    """
    tutor_grp = all_data.groupby(tut_col)
    # print(tutor_grp.groups.keys())
    for tutor in tutor_grp.groups.keys():
        # print(tutor_grp.get_group(tutor))
        tutor_students = tutor_grp.get_group(tutor)
        tutor_name = '{}_'.format(tutor.replace(' ', '_'))
        f_name = '{}{}{}.xls'.format(d_name, tutor_name,
                  ft.generate_time_string())
        tutor_students.to_excel(f_name, index = False)
        print('{} has been saved to {}'.format(tutor, f_name))


def tags_count(tags_data, headings):
    """Count number of tags per colour per tutor.
    
    Returns a dictionary with each tutor and a count of each tag colour for
    them. Skips tags that are not in the list of tags to include.
    
    Args:
        tags_data (DataFrame): Student Tags data
        headings (list): sid_name, eid_name, stud_name, course_name,
        tutor_name, new_tags_name.
        
    Returns:
        tags_count (dict): Dictionary with tag count be colour for each tutor.
    """
    # Create a list of tutors from tags_data
    tutors = tags_data[headings[4]].unique()
    tags = ['Green', 'Orange', 'Red', 'Black', 'Purple']
    tags_count = {}
    print('\nCounting Tags per Colour')
    # Create and populate dictionary to hold tags per tutor
    for tutor in tutors:
        tags_count[tutor] = {}
        for tag in tags:
            tags_count[tutor][tag] = 0
    # Update dictionary by going through tags_data
    num_students = len(tags_data.index) # For calculating % complete
    n = 0
    for index, row in tags_data.iterrows():
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        # Get tutor name
        tutor = row[headings[4]]
        # Get tag colour
        tag = row[headings[5]]
        # Update tag count
        if tag in tags:
            tags_count[tutor][tag] += 1
    # ad.debug_dict(tags_count)    
    # Return dictionary
    print('\rFinished counting Tags per Colour')
    return tags_count, tags


def update_tags(tag_list):
    """Return student tags.
    
    Compares the student's tag to their tag zone and determines the correct
    tag for the student. If the tag is Green it stays Green. For Orange, Red
    and Black tags, the tag is not allowed to exceed the student's zone. E.g.
    if a student is tagged Red but can only be in the Orange zone, their tag
    will be set to Orange.
    
    Args:
        tag_list(list): StudentID, tag_start and zone.
    
    Returns:
        updated_students (list): StudentID, Tag.
    """
    updated_students = []
    reserved = ['withdrawn', 'graduated', 'expired', 'suspended', 'on hold',
                'cancelled', 'transferred']
    print('\nUpdating Student Tags')
    num_students = len(tag_list) # For calculating % complete
    n = 0
    for student in tag_list:
        updated_student = []
        # Display progress
        n += 1
        progress = round((n/num_students) * 100)
        print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
        updated_student.append(student[0])
        '''
        print('Debugging: Student ID: {} Tag_Start: {} Zone: {}'.format
              (student[0], student[1], student[2]))
        '''
        if student[1] in reserved:
            tag = student[1]
        elif student[1] == 'Green' or student[2] == 'Green':
            tag = 'Green'
        elif student[1] == 'Orange' or student[2] == 'Orange':
            tag = 'Orange'
        elif student[1] == 'Red' or student[2] == 'Red':
            tag = 'Red'
        else:
            tag = 'Black'
        updated_student.append(tag)
        updated_students.append(updated_student)
    print('\rFinished Updating Student Tags')
    return updated_students


if __name__ == '__main__':
    main()
