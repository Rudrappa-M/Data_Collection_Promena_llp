from django.test import TestCase

# Create your tests here.
def Designationid(userid,assignid):
    three = '000'
    two='00'
    one='0'
    length = len(str(userid))
    if length == 1:
        ids = str(assignid)+three+str(userid)
        desgid = int(ids)
        print(desgid)
        return(desgid)
    elif length == 2:
        ids = str(assignid)+two+str(userid)
        desgid = int(ids)
        print(desgid)
        return(desgid)
    elif length == 3:
        ids = str(assignid)+one+str(userid)
        desgid = int(ids)
        print(desgid)
        return(desgid)
    else:
        ids = str(assignid)+str(userid)
        desgid = int(ids)
        print(desgid)
        return(desgid)
