from django import forms
from .models import UserProfileInfor,EventRegisterations
from django.contrib.auth.models import User
import re        
#from django import newforms as forms
import datetime
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
#from formValidationApp.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')
 
class UserProfileInforForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfor
        fields = ('university_name','age','profile_pic')
'''
class Subscribe(forms.Form):
    Email = forms.EmailField()
    def __str__(self):
        return self.Email
'''
'''
def ValidateLuhnChecksum(number_as_string):
    """ checks to make sure that the card passes a luhn mod-10 checksum """

    sum = 0
    num_digits = len(number_as_string)
    oddeven = num_digits & 1

    for i in range(0, num_digits):
        digit = int(number_as_string[i])

        if not (( i & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9

        sum = sum + digit
        
    return ( (sum % 10) == 0 )

# Regex for valid card numbers
CC_PATTERNS = {
    'mastercard':   '^5[12345]([0-9]{14})$',
    'visa':         '^4([0-9]{12,15})$',
}

def ValidateCharacters(number):
    """ Checks to make sure string only contains valid characters """
    return re.compile('^[0-9 ]*$').match(number) != None
        
def StripToNumbers(number):
    """ remove spaces from the number """
    if ValidateCharacters(number):
        result = ''
        rx = re.compile('^[0-9]$')
        for d in number:
            if rx.match(d):
                result += d
        return result
    else:
        raise Exception('Number has invalid digits')

def ValidateDigits(type, number):
    """ Checks to make sure that the Digits match the CC pattern """
    regex = CC_PATTERNS.get(type.lower(), False)
    if regex:
        return re.compile(regex).match(number) != None
    else:
        return False

def ValidateCreditCard(clean, number):
    """ Check that a credit card number matches the type and validates the Luhn Checksum """
    clean = clean.strip().lower()
    if ValidateCharacters(number):
        number = StripToNumbers(number)
        if CC_PATTERNS.has_key(clean):
            return ValidateDigits(clean, number)
            return ValidateLuhnChecksum(number)
    return False

class CardNumberField(forms.CharField):
    """ A newforms field for a creditcard number """
    def clean(self, value):
        
        value = forms.CharField.clean(self, value)
        if not ValidateCharacters(value):
            raise forms.ValidationError('Can only contain numbers and spaces.')
        value = StripToNumbers(value)
        if not ValidateLuhnChecksum(value):
            raise forms.ValidationError('Not a valid credit card number.')
        
        return value


class CardExpiryField(forms.CharField):
    """ A newforms field for a creditcard expiry date """
    def clean(self, value):     
        value = forms.CharField.clean(self, value.strip())
        
        # Just check MM/YY Pattern
        r = re.compile('^([0-9][0-9])/([0-9][0-9])$')
        m = r.match(value)
        if m == None:
            raise forms.ValidationError('Must be in the format MM/YY. i.e. "11/10" for Nov 2010.')
        
        # Check that the month is 1-12
        month = int(m.groups()[0])
        if month < 1 or month > 12:
            raise forms.ValidationError('Month must be in the range 1 - 12.')
        
        # Check that the year is not too far into the future
        year = int(m.groups()[1])
        curr_year = datetime.datetime.now().year % 100
        max_year = curr_year + 10
        if year > max_year or year < curr_year:
            raise forms.ValidationError('Year must be in the range %s - %s.' % (str(curr_year).zfill(2), str(max_year).zfill(2),))

        return value 

class PaymentForm(forms.ModelForm):    
    cc_number = CardNumberField(required=False)
    cc_expiry = CardExpiryField()
   
    #class Meta():
        #model = Payment 
    
    """
        This function checks that the card number matches the card type.  
        If you don't want to do this, comment out this function.
    """
    def clean(self):
        if self.cleaned_data:
            if len(self.cleaned_data.items()) == len(self.fields):      
                if self.cleaned_data['method'] == 'cc':
                    the_type = self.cleaned_data.get('cc_type', '')
                    number = self.cleaned_data.get('cc_number', '')
                    if not ValidateDigits(the_type, number):
                        raise forms.ValidationError('Card Number is not a valid ' + the_type.upper() + ' card number.')
                    if not self.instance.is_payment_valid():
                        raise forms.ValidationError('Credit card payment could not be processed.  Reason is %s.  Check that card details are correct and try again.  If you still receive this error, check with your financial institution.' % (self.instance.gateway_resptxt))
        return self.cleaned_data

'''

'''
class TelephoneInput(TextInput):

    # switch input type to type tel so that the numeric keyboard shows on mobile devices
    input_type = 'tel'


class CreditCardField(forms.CharField):

    # validates almost all of the example cards from PayPal
    # https://www.paypalobjects.com/en_US/vhelp/paypalmanager_help/credit_card_numbers.htm
    cards = [
        {
            'type': 'maestro',
            'patterns': [5018, 502, 503, 506, 56, 58, 639, 6220, 67],
            'length': [12, 13, 14, 15, 16, 17, 18, 19],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'forbrugsforeningen',
            'patterns': [600],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'dankort',
            'patterns': [5019],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'visa',
            'patterns': [4],
            'length': [13, 16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'mastercard',
            'patterns': [51, 52, 53, 54, 55, 22, 23, 24, 25, 26, 27],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'amex',
            'patterns': [34, 37],
            'length': [15],
            'cvvLength': [3, 4],
            'luhn': True
        }, {
            'type': 'dinersclub',
            'patterns': [30, 36, 38, 39],
            'length': [14],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'discover',
            'patterns': [60, 64, 65, 622],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'unionpay',
            'patterns': [62, 88],
            'length': [16, 17, 18, 19],
            'cvvLength': [3],
            'luhn': False
        }, {
            'type': 'jcb',
            'patterns': [35],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }
    ]

    def __init__(self, placeholder=None, *args, **kwargs):
        super(CreditCardField, self).__init__(
            # override default widget
            widget=TelephoneInput(attrs={
                'placeholder': placeholder
            })
        , *args, **kwargs)

    default_error_messages = {
        'invalid': _(u'The credit card number is invalid'),
    }

    def clean(self, value):

        # ensure no spaces or dashes
        value = value.replace(' ', '').replace('-', '')

        # get the card type and its specs
        card = self.card_from_number(value)

        # if no card found, invalid
        if not card:
            raise forms.ValidationError(self.error_messages['invalid'])

        # check the length
        if not len(value) in card['length']:
            raise forms.ValidationError(self.error_messages['invalid'])

        # test luhn if necessary
        if card['luhn']:
            if not self.validate_mod10(value):
                raise forms.ValidationError(self.error_messages['invalid'])

        return value

    def card_from_number(self, num):
        # find this card, based on the card number, in the defined set of cards
        for card in self.cards:
            for pattern in card['patterns']:
                if (str(pattern) == str(num)[:len(str(pattern))]):
                    return card

    def validate_mod10(self, num):
        # validate card number using the Luhn (mod 10) algorithm
        checksum, factor = 0, 1
        for c in reversed(num):
            for c in str(factor * int(c)):
                checksum += int(c)
            factor = 3 - factor
        return checksum % 10 == 0

class PaymentForm(forms.ModelForm):
    card_number = CreditCardField(placeholder=u'0000 0000 0000 0000', min_length=12, max_length=19)
'''

class PaymentForm(forms.Form):
    name_on_card=forms.CharField(required=True, label="Name on Card",max_length=100)
    number = CardNumberField(required=True, label="Card Number")
    expiration = CardExpiryField(required=True, label="Expiration Date")

    cvc = forms.CharField(required=True, label="CVV/CVC",widget=forms.TextInput(attrs={'size': '3','maxlength': '3',

                        'placeholder':''}))

    country = forms.CharField(required=False, max_length=255,label="City",widget=forms.TextInput())
    zip = forms.CharField(required=False, max_length=255,label=mark_safe("&nbsp;&nbsp;&nbsp;Zip"),widget=forms.TextInput())

 

class CardNumberField(forms.IntegerField):
    def get_cc_type(self, number):

        number = str(number)

        if len(number) == 13:

            if number[0] == "4":

                return "Visa"

        elif len(number) == 14:

            if number[:2] == "6":

                return "MasterCard"

        elif len(number) == 15:

            if number[:2] in ("34", "37"):

                return "American Express"

        elif len(number) == 16:

            if number[:4] == "6011":

                return "Discover"

        if number[:2] in ("51", "52", "53", "54", "55"):

            return "MasterCard"

        if number[0] == "4":

            return "Visa"

        return "Unknown"

 
    def clean(self, value):
        if value and (len(value) < 13 or len(value) > 16):

            raise forms.ValidationError("Please enter a valid credit card number.")

        elif self.get_cc_type(value) not in ('Visa', "MasterCard","American Express", "Discover"):
            raise forms.ValidationError("Please enter a Visa, Master Card, Discover, or American Express credit card number.")

        return super(CreditCardField, self).clean(value)

class EventRegisterationsForm(forms.ModelForm):
    class Meta():
        model = EventRegisterations
        fields = ('name', 'emailid' ,'gender' ,'college_name','phone_number','event','members', 'tshirt_size')
        widgets = {
            'event': forms.RadioSelect(attrs=( {'size': 20, 'title': 'Event' ,'backgroung-color':'white' })),
           
        }
        
        
        
        
        
        '''def clean(self): 
            super(EventRegisterationForm, self).clean() 
 
        emailid = self.cleaned_data.get('emailid') 
        text = self.cleaned_data.get('text') 
  
        # conditions to be met for the username length 
        if 
            self._errors['username'] = self.error_class([ 
                'Minimum 5 characters required']) 
        if len(text) <10: 
            self._errors['text'] = self.error_class([ 
                'Post Should Contain minimum 10 characters']) 
  
        # return any errors if found 
        return self.cleaned_data '''

