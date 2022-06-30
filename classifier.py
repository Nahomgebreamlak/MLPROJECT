import os
import numpy as np
from androguard.core.bytecodes.apk import APK 
import numpy as np
import joblib
from androguard.misc import AnalyzeAPK



permissions = []
with open('./static/permissions.txt', 'r') as f:
    content = f.readlines()
    for line in content:
        cur_perm = line[:-1]
        permissions.append(cur_perm)
            
multifeature = []
with open('./static/multifeaturelist.txt', 'r') as f:
    content = f.readlines()
    for line in content:
        cur_perm = line[:-1]
        multifeature.append(cur_perm)





def predict(apk,ch):
    if ch == 0 and os.path.exists(apk):
        input,perm,name, sdk, size=ExtractFeatures(apk)
        SVC = joblib.load(open('static/models/multifeaturemodel', 'rb'))
        result = SVC.predict([input])
        if result == "B":
            result = 'Benign(safe)'
        else :
            result = "Malware"    
            
    elif ch == 1 and os.path.exists(apk) :
        input,perm,name, sdk, size=use_permissions(apk)
        SVC = joblib.load(open('static/models/permissionmodel', 'rb'))
        result = SVC.predict([input])
        if result == 'benign':
            result = 'Benign(safe)'
        else:
            result = 'Malware'
        
    return result, name, sdk, size , perm


def ExtractFeatures(apk):
    vector = {}    
    perm,methods,classnames,intents,name, sdk, size=EXTRACT_METHOD_CALLS(apk)
    for d in multifeature:
        if d in perm:
         vector[d]=1
        elif d in methods:
            vector[d]=1
        elif d in classnames:
            vector[d]=1
        elif d in intents:
            vector[d]=1
        else:
         vector[d]=0
    input = [ v for v in vector.values() ]
    return input,perm,name, sdk, size

def use_permissions(file):
    vector={}
    app = APK(file)
    perm = app.get_permissions()
    name, sdk, size = meta_fetch(app,file)
    for p in permissions:
        if p in perm:
            vector[p] = 1
        else:
            vector[p] = 0
    data = [v for v in vector.values()]
    return data,perm,name,sdk,size


def EXTRACT_METHOD_CALLS(a):
    app, list_of_dex, dx = AnalyzeAPK(a)
    perm = app.get_permissions()
    intents = getIntents(app)
    name, sdk, size =meta_fetch(app,a)
    methods =[]
    classnames=[]
    for method in dx.get_methods():
        methods.append(method.name) 
    for classname in dx.get_classes():
        classnames.append(classname.name)
    return perm,methods ,classnames,intents,name, sdk, size    
    


def getIntents(app):
     a =app 
     activities = a.get_activities()
     receivers = a.get_receivers()
     services = a.get_services()
     filter_list = []
     for i in activities:
         filters = a.get_intent_filters("activity", i)
         if len(filters) > 0:
             flist =list(filters.values())
             for lists in flist:
                 for intentname in lists:
                     filter_list.append(intentname)

     for i in receivers:
         filters = a.get_intent_filters("receiver", i)
         if len(filters) > 0:
             flist =list(filters.values())
             for lists in flist:
                 for intentname in lists:
                     filter_list.append(intentname)
     for i in services:
         filters = a.get_intent_filters("service", i)
    
         if len(filters) > 0:
             flist =list(filters.values())
             for lists in flist:
                 for intentname in lists:
                     filter_list.append(intentname)
     return filter_list        

    
def meta_fetch(app,apk):
    return app.get_app_name(), app.get_target_sdk_version(), str(round(os.stat(apk).st_size / (1024 * 1024), 2)) + ' MB'


