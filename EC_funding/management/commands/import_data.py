import csv
import pandas as pd
import numpy as np

# from django.utils import timezone
# import datetime
# import pytz


from django.core.management.base import BaseCommand, CommandError
from EC_funding.models import Projects

class Command(BaseCommand):
    help = 'Imports two cvs files'

    def handle(self, *args, **options):

        # load project cvs file into a dataframe
        df = pd.read_csv("/Users/dule/django/SDU_exercise/SDU_data/csv/project.csv", sep=';', quotechar='"')

        # do some data cleaning
        # 1. replace all , with . in two columns that hold financial information 
        df['totalCost'] = df['totalCost'].replace(',','.', regex=True)
        df['ecMaxContribution'] = df['ecMaxContribution'].replace(',','.', regex=True)

        # 2. replace CLOSED with CLO in the colum "status"
        df["status"].replace(to_replace={"CLOSED": "CLO"}, inplace=True)

        # 3. convert date columns to strings and replace any empty values with None
        # this is done because DateFiled does not accept empty values. 
        df['startDate'] = df['startDate'].astype(str)
        df['endDate'] = df['endDate'].astype(str)
        df['contentUpdateDate'] = df['contentUpdateDate'].astype(str)
        df["startDate"].replace("nan", None, inplace=True)
        df["endDate"].replace("nan", None, inplace=True)
        df["contentUpdateDate"].replace("contentUpdateDate", None, inplace=True)


        ######## some tools used for debugging 
        # check column_names 
        # column_names = list(df.columns.values)
        # print (column_names)

        # Find the maximum string length of all string columns
        # string_cols = df.select_dtypes(include=['object'])
        # max_length = string_cols.apply(lambda x: x.str.len()).max()
        # print(max_length)
        #########
        
        #  go though all the rows of the data frame and create the instances of the model
        for index, row in df.iterrows():
            Projects.objects.create(id=row['id'], acronym=row['acronym'], status=row['status'],
            title=row['title'], startDate=row['startDate'], endDate=row['endDate'], totalCost=row['totalCost'],
            ecMaxContribution=row['ecMaxContribution'], legalBasis=row['legalBasis'], topics=row['topics'],
            ecSignatureDate=row['ecSignatureDate'], frameworkProgramme=row['frameworkProgramme'],
            masterCall=row['masterCall'], subCall=row['subCall'],  fundingScheme=row['fundingScheme'],
            nature=row['nature'], objective=row['objective'], 
            rcn=row['rcn'], grantDoi=row['grantDoi'])

        
        # load organisation cvs file into a dataframe
        df = pd.read_csv("/Users/dule/django/SDU_exercise/SDU_data/csv/organization.csv", sep=';') 

        # do some data cleaning
        # 1. replace all , with . in two columns that hold financial information 
        df['ecContribution'] = df['ecContribution'].replace(',','.', regex=True)

        # 2. separate geolocation into latitude and longitude
        df[['latitude','longitude']] = df['geolocation'].str.split(',', expand=True)



