from django.db.models.signals import post_save
from .models import Profile
from django.contrib.auth.models import User
from django.dispatch import receiver

'''----------------------------------------------------------------------------'''

'''      ----------------     first method for Signal   -------------------   '''

'''----------------------------------------------------------------------------'''

# 1- create signal function 
def create_profile(sender , **kwargs):
    
    ''' 
     - print(kwargs) : 
    {
        'signal': <django.db.models.signals.ModelSignal object at 0x7f08348b2050>, 
        'instance': <User: certain_user>,
        'created': True,
        'update_fields': None, 
        'raw': False,
        'using': 'default'
     }
    '''
    if kwargs['created']:
         Profile.objects.create(user =kwargs['instance'])


# 2- execute signal function
post_save.connect(create_profile , sender =User)




'''----------------------------------------------------------------------------'''

'''      ----------------     second method for Signal   -------------------   '''

'''----------------------------------------------------------------------------'''

# @receiver(post_save, sender=User)
# def create_profile_another_method(sender, instance, created, **kwargs):
#     ''' 
#     - the sencod method need only one method 
#       - with APPConfig
#     '''
#     if created:
#         Profile.objects.create(user=instance)
  




'''----------------------------------------------------------------------------'''

'''      ----------------     Another shape to write method one -------------   '''

'''----------------------------------------------------------------------------'''

# def create_profile_method1_another_shape(sender , signal ,instance , created , update_fields ,raw , using ,**kwargs):
    
#     print("created = {}".format(created))
#     print("username = {}".format(instance.username))
#     print("update_fields = {}".format(update_fields))
#     print("raw = {}".format(raw))
#     print("using = {}".format(using))
#     print("signal = {}".format(signal))
#     print("sender = {}".format(sender))
#     print(kwargs)

#     if created == True:
#          Profile.objects.create(user = instance)
    

# post_save.connect(create_profile_method1_another_shape , sender =User)



'''----------------------------------------------------------------------------'''

'''        ----------------            Explaination            -------------   '''
 
'''----------------------------------------------------------------------------'''


'''
 - SIGNAL STEPS :
    - 1 - create signal function  .
    - 2 - execute signal function .
    - if (1 and 2) at the bottom of the page in a (uth_user_app.model.py) : 
         Not use 3
    - else :
         use 3     
    - 3 - IN (AppConfig) # call signal function to execute when listening for the creation of a User model.
 
 - INFO  : 
    post_save.connect(my_function_post_save, sender=MyModel)
 
 - arguments :    
    receiver  :   The function who receives the signal and does something.
    sender    :   Sends the signal
    created   :   Checks whether the model is created or not
    instance  :   created model instance
    **kwargs  :   wildcard keyword arguments
'''


