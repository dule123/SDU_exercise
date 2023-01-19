import csv
import pandas as pd
import numpy as np

from django.utils import timezone
import datetime
import pytz
from django.utils.timezone import make_aware


from django.core.management.base import BaseCommand, CommandError
from EC_funding.models import Projects 
from EC_funding.models import Organisations

# ams_dt = loc_dt.astimezone(amsterdam)
# ams_dt.strftime(fmt)

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
        df["contentUpdateDate"].replace("nan", None, inplace=True)


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
        print ('Loaded Projects csv')

        
        ########### load organisation cvs file into a dataframe
        # added low_memory=False to avoid error message about mixed types 
        df = pd.read_csv("/Users/dule/django/SDU_exercise/SDU_data/csv/organization.csv", sep=';', low_memory=False) 


        # print(df.loc[293:298, "organisationID"])
        # df["organisationID"] = df["organisationID"].astype(str)
        # df["organisationID"].replace("nan", None, inplace=True)
        # print(df.loc[293:298, "organisationID"])
        # df["organisationID"] = df["organisationID"].astype(float).round().astype(int)

        # df["organisationID"] = pd.to_numeric(df['organisationID'], errors='coerce').astype(float).round().astype(int)



        # df["organisationID"] = df["organisationID"].astype(str)
        # df.dropna(); 
        # df["organisationID"] = df["organisationID"].astype(int)
        # # df.replace("nan", 0, inplace=True)
        
        # do some data cleaning
        # 1. replace all , with . in two columns that hold financial information 
        df['ecContribution'] = df['ecContribution'].replace(',','.', regex=True)

        # 2. separate geolocation into latitude and longitude and convert into numeric
        # some values are enclosed in (), eliminate those firs
        df['geolocation'] = df['geolocation'].replace('\(','', regex=True)
        df['geolocation'] = df['geolocation'].replace('\)','', regex=True)
        # split the column into two new columns
        df[['latitude','longitude']] = df['geolocation'].str.split(',', expand=True)
        # change the type from string to float 
        df['latitude'] = df['latitude'].astype(float)
        df['longitude'] = df['longitude'].astype(float)

        # 3. convert date columns to strings and replace any empty values with None
        # this is done because DateFiled does not accept empty values. 
        df['contentUpdateDate'] = df['contentUpdateDate'].astype(str)
        df["contentUpdateDate"].replace("nan", None, inplace=True)
    
        # 4. convert boolean columns to strings and replace any empty values with None
        df['endOfParticipation'] = df['endOfParticipation'].astype(str)
        df["endOfParticipation"].replace("nan", None, inplace=True)
        df['active'] = df['active'].astype(str)
        df["active"].replace("nan", None, inplace=True) 

        # 5. converting a "xxxxxxx" to an empty filed, assuming this was a mistake/typo
        df["rcn"].replace("xxxxxxx", None, inplace=True) 
        df["ecContribution"].replace("xxxxx", None, inplace=True) 

        # getting error message, to be fixed later... 
        # /Users/dule/django/SDU_exercise/EC_funding/management/commands/import_data.py:63: DtypeWarning: Columns (17,20) have mixed types. Specify dtype option on import or set low_memory=False.
        #   df = pd.read_csv("/Users/dule/django/SDU_exercise/SDU_data/csv/organization.csv", sep=';')

        ######## some tools used for debugging 
        # column_names = list(df.columns.values)
        # print (column_names)
        # df.info()
        # string_cols = df.select_dtypes(include=['object'])
        # max_length = string_cols.apply(lambda x: x.str.len()).max()
        # print(max_length)
        ########


        #  go though all the rows of the data frame and create the instances of the model
        for index, row in df.iterrows():

            Organisations.objects.create(project=Projects.objects.get(id=row["projectID"]), 
            projectAcronym=row['projectAcronym'],
            organisationID=row['organisationID'], vatNumber=row['vatNumber'], name=row['name'],
            shortName=row['shortName'], SME=row['SME'], activityType=row['activityType'], 
            street=row['street'], postCode=row['postCode'], city=row['city'], country=row['country'],
            nutsCode=row['nutsCode'], latitude=row['latitude'], longitude=row['longitude'], 
            organizationURL=row['organizationURL'], contactForm=row['contactForm'], 
            contentUpdateDate=row['contentUpdateDate'], rcn=row['rcn'], order=row['order'],
            role=row['role'], ecContribution=row['ecContribution'], netEcContribution=row['netEcContribution'], 
            totalCost=row['totalCost'], endOfParticipation=row['endOfParticipation'])
