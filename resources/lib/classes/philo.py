from resources.lib.globals import *

FUNCTION = ""

class Philo(object):

    Token_Code = ""
    User_ID = ""
    Session = None
    CookieJar = None
    Headers = {
        "Host": "www.philo.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.philo.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
    Verify = False

    def __init__(self):
        global FUNCTION, COOKIE_PATH
        FUNCTION = "Philo::__init__"
        self.log("Initializing the Philo class")

        if DEVICE_ID == "":
            self.getDeviceID()
                
        self.CookieJar = MozillaCookieJar(COOKIE_PATH)
        if os.path.exists(COOKIE_PATH):
            self.log("Found cookie file, restoring sesion.")
            self.CookieJar.load(ignore_discard=True, ignore_expires=True)
        
        self.Session = requests.Session()
        self.Session.headers = self.Headers
        self.Session.cookies = self.CookieJar        
    
    def getDeviceID(self):
        global FUNCTION, DEVICE_ID, SETTINGS
        FUNCTION = "Philo:getDeviceID"
        self.log("Generating new Device ID")
        # web-3971f560-9db9-4686-89b6-59eebe03ab21
        DEVICE_ID = "web-%s" % uuid.uuid4()
        SETTINGS.setSetting('Device_ID', DEVICE_ID)        
    
    def logIn(self):
        global FUNCTION, STRINGS, EMAIL, DEVICE_ID, SETTINGS
        FUNCTION = "Philo::login"        
        logged_in = False

        if self.User_ID != "":
            self.log("User already logged in.")
            logged_in = True
        else:
            self.log("Attempting login")

            if EMAIL == "":
                EMAIL = inputDialog(STRINGS(30100))
                self.log("Received Email: %s" % EMAIL)

                if EMAIL is None:
                    self.log("User failed to provide an email, exiting")
                    notificationDialog(STRINGS(30102))
                    sys.exit()
                else:
                    SETTINGS.setSetting('Email', EMAIL)        

            token_url = "https://www.philo.com/auth/init/login_code"
            payload = '{"ident":"%s","device":"web","device_ident":"%s","location":"erie","send_token":true,"send_confirm_link":false}' % (EMAIL, DEVICE_ID)

            code_sent = False
            response = self.Session.post(url=token_url, headers=self.Headers, data=payload, verify=self.Verify)
            self.CookieJar.save(ignore_discard=True, ignore_expires=True)
            if response.status_code != 200:
                self.log("Code: %i -> %s" % (response.status_code, response.text))
            else:
                self.log(json.dumps(response.json(), indent=4))

                response = response.json()
                if 'error_code' in response:
                    """
                     0 - Success
                     3 - Sign-in failed. Please try again.
                    50 - A sign-in code has already been sent.
                    62 - A sign-in code is pending for a different device. Please wait a few minutes.
                    """
                    if response['error_code'] == 0:
                        code_sent = True
                        if 'analytics' in response:
                            if 'userId' in response['analytics']:
                                self.User_ID = response['analytics']['userId']
                                self.log("Already logged in, retrieved User ID: %s" % self.User_ID)
                                logged_in = True
                        if not logged_in:
                            self.log("Login code sent")
                    elif response['error_code'] == 50:
                        self.log("A sign-in code has already been sent.")
                        code_sent = True
                    else:
                        self.log('Error %i: %s' % (response['error_code'], response['description']))

            if code_sent and not logged_in:
                self.Token_Code = inputDialog(STRINGS(30101))
                self.log("Received code: %s" % self.Token_Code)
                if self.Token_Code == "None":
                    notificationDialog(STRINGS(30102))
                    sys.exit()

                code_url = "https://www.philo.com/auth/update/login_code"
                payload = '{"token":"%s"}' % self.Token_Code
                response = self.Session.post(url=code_url, headers=self.Headers, data=payload, verify=self.Verify)
                self.CookieJar.save(ignore_discard=True, ignore_expires=True)
                if response.status_code != 200:
                    self.log("Code: %i -> %s" % (response.status_code, response.text))
                else:
                    self.log(json.dumps(response.json(), indent=4))

                    response = response.json()
                    if 'error_code' in response:
                        if response['error_code'] == 0:
                            self.log("Successfully logged in.")
                            if 'analytics' in response:
                                if 'userId' in response['analytics']:
                                    self.User_ID = response['analytics']['userId']
                                    self.log("Retrieved User ID: %s" % self.User_ID)
                                    logged_in = True
        
        return logged_in
            
    def getProfiles(self):
        global FUNCTION
        FUNCTION = "Philo::getProfiles"
        profiles = []

        profile_url = "https://www.philo.com/user/profiles/list.json"
        response = self.Session.get(url=profile_url, headers=self.Headers, verify=self.Verify)
        if response.status_code != 200:
            self.log("Code: %i -> %s" % (response.status_code, response.text))
        else:
            response = response.json()
            self.log(json.dumps(response, indent=4))
            if 'status' in response:
                if response['status'] == 'SUCCESS':
                    if 'profiles' in response:
                        profiles = response['profiles']
                        count = 0
                        for profile in profiles:
                            new_profile = {
                                'ID': profile['id'],
                                'Name': profile['name'],
                                'Primary': profile['primary'],
                                'Mobile_Number': profile['mobileNumber'],
                                'Logged_In': profile['loggedIn'],
                                'Avatar': {
                                    'Small': profile['avatar']['s'],
                                    'Medium': profile['avatar']['m'],
                                    'Large': profile['avatar']['l']
                                }
                            }
                            profiles[count] = new_profile
                            count += 1

        return profiles

    def log(self, message):
        log(message=message, function=FUNCTION)
