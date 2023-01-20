
from django.db import models
from django.utils import timezone

# Create the model for projects table
# note: created fileds even for colums that are currently empty, 
# in case they are needed later in the project
class Projects(models.Model):
    id = models.IntegerField(primary_key=True)
    acronym = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    totalCost = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    ecMaxContribution = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    legalBasis= models.CharField(max_length=20, null=True, blank=True) 
    topics= models.CharField(max_length=60, null=True, blank=True) 
    ecSignatureDate = models.CharField(max_length=5, null=True, blank=True) 
    frameworkProgramme = models.CharField(max_length=50, null=True, blank=True)
    masterCall = models.CharField(max_length=5, null=True, blank=True)
    subCall = models.CharField(max_length=40, null=True, blank=True)
    fundingScheme = models.CharField(max_length=20, null=True, blank=True)
    nature = models.CharField(max_length=30, null=True, blank=True)
    objective = models.TextField(null=True, blank=True)
    contentUpdateDate = models.DateTimeField(null=True, blank=True)
    rcn = models.IntegerField(null=True, blank=True)
    grantDoi = models.CharField(max_length=255, null=True, blank=True)
    
    # this will help identify the model later, e.g. in error messages
    def __str__(self):
        return self.acronym


# Create the model for organisations table
# note: created fileds even for colums that are currently empty, 
# in case they are needed later in the project
class Organisations(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    projectAcronym = models.CharField(max_length=30, null=True, blank=True)
    organisationID = models.FloatField(null=True, blank=True)
    vatNumber = models.CharField(max_length=20, null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    shortName = models.TextField(null=True, blank=True)
    SME = models.CharField(max_length=3, null=True, blank=True); 
    activityType = models.CharField(max_length=3, null=True, blank=True)
    street = models.TextField(null=True, blank=True)
    postCode = models.CharField(max_length=30, null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    nutsCode = models.CharField(max_length=30, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    organizationURL = models.URLField()
    contactForm = models.URLField()
    contentUpdateDate = models.DateTimeField(null=True, blank=True)
    rcn = models.FloatField(null=True, blank=True)
    order = models.FloatField(null=True, blank=True)
    role = models.CharField(max_length=15, null=True, blank=True)
    ecContribution = models.FloatField(null=True, blank=True)
    netEcContribution = models.FloatField(null=True, blank=True)
    totalCost = models.FloatField( null=True, blank=True)
    endOfParticipation = models.BooleanField(null=True, blank=True)
    active = models.BooleanField(null=True, blank=True)
    
    # this will help identify the model later, e.g. in error messages
    def __str__(self):
        return self.shortName
