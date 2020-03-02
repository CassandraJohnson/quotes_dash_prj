from django.db import models
import re
import bcrypt

emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

class UserManager(models.Manager):
    def register(self, first_name, last_name, email, password, confirm_password):   
        validation_result = self.validate(first_name, last_name, email, password, confirm_password)  # Result: result = {'status': True, 'errors': "Validation successful"}
        if validation_result['status'] == True:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            created_user = self.create(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
            validation_result = {'status': validation_result['status'], 'created_user': created_user}
            return validation_result
        return validation_result
    
    def validate_edit(self, first_name, last_name, email):
        errors = []
        result = {}
            #  Validate First Name
        if first_name == '':
            msg = "First name is REQUIRED"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(first_name) < 2:
            msg = "First Name should have at least two characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif any(char.isdigit() for char in first_name) == True:
            msg = "Name cannot contain numbers"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
            #  Validate Last Name
        if last_name == '':
            msg = "Last name is REQUIRED"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(last_name) < 2:
            msg = "Last Name should have at least two characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif any(char.isdigit() for char in last_name) == True:
            msg = "Name cannot contain numbers"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
            # Validate Email
        if email == '':
            msg = "Email is REQUIRED"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif not emailRegex.match(email):
            msg = "The email provided is not formatted correctly"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(self.filter(email = email)) > 0:
            msg = "The Email provided already exists in our database"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        #current_user = User.objects.get(id = user_id)
        self.create(first_name=first_name, last_name=last_name, email=email)
        msg = "Account updated."
        errors.append(msg)
        result = {'status' : True, 'errors' : errors[0]}
        return result


    def validate(self, first_name, last_name, email, password, confirm_password):
        errors = []
        result = {}
            #  Validate First Name
        if first_name == '':
            msg = "First name is REQUIRED"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(first_name) < 2:
            msg = "First Name should have at least two characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif any(char.isdigit() for char in first_name) == True:
            msg = "Name cannot contain numbers"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
            #  Validate Last Name
        if last_name == '':
            msg = "Last name is REQUIRED"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(last_name) < 2:
            msg = "Last Name should have at least two characters"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif any(char.isdigit() for char in last_name) == True:
            msg = "Name cannot contain numbers"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
            # Validate Email
        if email == '':
            msg = "Email is REQUIRED"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif not emailRegex.match(email):
            msg = "The email provided is invalid"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(self.filter(email = email)) > 0:
            msg = "The Email provided already exists in our database"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
            # Password Validation
        if password == '':
            msg = "Password is REQUIRED"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(password) < 8:
            msg = "Password must be greater than 8 characters"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif not passwordRegex.match(password):
            msg = "Password must contain at least one lowercase letter, one uppercase letter, and one digit"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
                # Confirm Password
        elif confirm_password != password:
            msg = "Passwords do not match"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
           
        else:
            result = {'status': True, 'errors': "Validation successful"}
            return result

    def login_validate(self, email, password):
        errors = []
        try:
            found_user = self.get(email = email)
            if bcrypt.checkpw(password.encode(), found_user.password.encode()):
                result = {'status' : True, 'found_user' : found_user}
                return result
            else:
                msg = "Email and Password do not match"
                errors.append(msg)
                result = {'status' : False, 'errors' : errors[0]}
                return result
        except:
            msg = "Email is not in our database"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result

class QuoteManager(models.Manager):
    def validate_quote(self, quote_text, user_id, quoted_by):
        errors = []
        if len(quoted_by) < 4:
            msg = "'Quoted by' should be more than 4 characters."
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(quote_text) < 10:
            msg = "Quote is too short to be a quote!"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        current_user = User.objects.get(id = user_id)
        self.create(quote_text = quote_text, author = current_user, quoted_by = quoted_by)
        msg = "Quote created."
        errors.append(msg)
        result = {'status' : True, 'errors' : errors[0]}
        return result

    
class User(models.Model):
    first_name = models.CharField (max_length=255, null = True)
    last_name = models.CharField (max_length=45, null = True)
    email = models.CharField (max_length = 45, null = True)
    password = models.CharField (max_length=100, null = True)
    remove = models.CharField(max_length=25, null = True)
    
    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

class Quote(models.Model):
    quote_text = models.TextField (max_length = 1000, null = True)
    author = models.ForeignKey(User, related_name="quotes_posted")
    created_at = models.DateTimeField (auto_now_add = True)
    favorites = models.ManyToManyField(User, related_name='movies_favorited')
    quoted_by = models.CharField (max_length=255, null = True)
    objects = QuoteManager()

# Create your models here.