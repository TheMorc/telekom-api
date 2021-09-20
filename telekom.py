#telekom veštení, pythonová verzia
#Morc, výmysel vznikol medzi 19.9.2021 - 20.9.2021

import requests, json, os, configparser
config = configparser.ConfigParser()
config['telekom'] = {}
nastavenia = config['telekom']
common_headers = {
    'Authorization': '7d06dd59-687c-454e-ade8-3520ff79a00d',
    'X-Request-Session-Id': 'FC4DF625-01D0-4ACC-A8E5-5260A3F9AC7F',
    'X-Request-Tracking-Id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF',
    'Content-Type': 'application/json',
}

def cfg_save():
	with open('telekom.cfg', 'w') as cfgfile:
		config.write(cfgfile)


def pin_verif_request():	#pin + verif sekcia, popýtaní SMSky na PIN do telekomu
	input_ciselko = input("Zadaj Telekom číslo (+4219xxXXXxxx formát): ")
	pin_request = requests.post('https://t-app.telekom.sk/pin/', headers=common_headers, data='{"serviceId":"' + input_ciselko + '","serviceType":"phoneNumber","device":{"os":"ios"},"context":"login"}')
	pin_response = json.loads(pin_request.text)
	
	if "errorType" in pin_request.text: #nonce nesmí chýbať, asi nastala chyba, vypíš čo sa stalo
		print("Nastala chyba pri pýtaní PINu")
		print(pin_response["code"])
		os._exit(os.EX_OK)
	
	pin_nonce = pin_response["nonce"]
	nastavenia['serviceId'] = input_ciselko
	#koniec pin sekcie	

	input_pin = input("Zadaj PIN z Telekom SMSky: ")
	verif_data = '{"device":{"id":"FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF","os":"ios"},"enableProfilePin":false,"serviceId":"' + input_ciselko + '","serviceType":"phoneNumber","context":"login","PIN":"' + input_pin + '","nonce":"' + pin_nonce + '"}'
	verif_request = requests.put('https://t-app.telekom.sk/pin/', headers=common_headers, data=verif_data)
	verif_response = json.loads(verif_request.text)
	
	if "errorType" in verif_request.text: #bez accessTokenu to nejde, asi nastala chyba, vypíš čo sa stalo
		print("Nastala chyba pri verifikácií PINu")
		print(verif_response["code"])
		os._exit(os.EX_OK)
	
	nastavenia['accessToken'] = verif_response["accessToken"]
	nastavenia['refreshToken'] = verif_response["refreshToken"]  


def regen_token():
	regen_data = '{"genCenToken":false,"refreshToken":"' + nastavenia['refreshToken'] + '","deviceId":"FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"}'
	regen_request = requests.post('https://t-app.telekom.sk/token/', headers=common_headers, data=regen_data)
	regen_response = json.loads(regen_request.text)
	
	if "errorType" in regen_request.text:
		print("Nastala chyba pri regene tokenu")
		print(regen_request.text)
	
	nastavenia['accessToken'] = regen_response["accessToken"]
	nastavenia['refreshToken'] = regen_response["refreshToken"]
	cfg_save()
	print("Regen tokenu úspešný")

def login():	#prihlasuvaní a pýtaní informácií z telekomu
	login_headers = {
	    'Accept': '*/*',
	    'Authorization': 'Bearer ' + nastavenia['accessToken'],
	    'X-Request-Session-Id': 'FC4DF625-01D0-4ACC-A8E5-5260A3F9AC7F',
	    'X-Request-Tracking-Id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF',
	    'Content-Type': 'application/json',
	}
	
	login_params = (
	    ('deviceId', 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'),
	    ('devicesWithEMI', 'false'),
	    ('genCenToken', 'true'),
	    ('hybridEnabled', 'true'),
	    ('loyaltyEnabled', 'false'),
	    ('sub', 'MSISDN_' + nastavenia['serviceId'][1:]),
	    ('subscriptionServiceEnabled', 'false'),
	)
	
	login_request = requests.get('https://t-app.telekom.sk/profiles/', headers=login_headers, params=login_params)
	login_response = json.loads(login_request.text)
	
	if "errorType" in login_request.text: #bez accessTokenu to nejde, asi nastala chyba, vypíš čo sa stalo
		print("Nastala chyba pri prihlasuvaní")
		print(login_response["code"])
		print("Pokus o regen tokenu")
		regen_token()
		print("Pokus o druhé prihlásení")
		login()
		dashboard()
		os._exit(os.EX_OK)
	
	print("Prihlásenie úspešné")
	nastavenia['productId'] = login_response[0]["manageableAssets"][0]["id"]
	
	login_meno = ""
	if "givenName" in login_request.text:
		login_meno = login_response[0]["individual"]["givenName"] + " " + login_response[0]["individual"]["familyName"] + " - "
	
	print(login_meno + login_response[0]["manageableAssets"][0]["label"] + " (" + nastavenia['serviceId'] + ")")
	
def dashboard():
	dash_headers = {
	    'Accept': '*/*',
	    'Authorization': 'Bearer ' + nastavenia['accessToken'],
	    'X-Request-Session-Id': 'FC4DF625-01D0-4ACC-A8E5-5260A3F9AC7F',
	    'X-Request-Tracking-Id': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF',
	    'Content-Type': 'application/json',
	}
	
	dash_params = (
	    ('enableFreeUnit', 'true'),
	    ('priority', 'primary'),
	    ('profileId', 'MSISDN_' + nastavenia['serviceId'][1:]),
	    ('serviceOnboarding', 'false'),
	    ('serviceOutageEnabled', 'false'),
	    ('showTotalCreditBalance', 'true'),
	    ('showUnlimited', 'true'),
	)
	
	dash_request = requests.get('https://t-app.telekom.sk/dashboard/product/' + nastavenia['productId'], headers=dash_headers, params=dash_params)
	dash_response = json.loads(dash_request.text)
	
	if "errorType" in dash_request.text:
		print("Nastala chyba pri vyťahuvaní dashboardu")
		print(dash_response["code"])
		os._exit(os.EX_OK)
	
	print(dash_response["campaignPlanDetail"]["name"] + " - Zostávajúce dáta: " + str(dash_response["consumption"]["remaining"]["value"]) + "GB/" + str(dash_response["consumption"]["max"]["value"]) + "GB")
		
if not os.path.isfile('telekom.cfg'): #je šanca že apka sa pustila prvý raz
	print('Prvé spustení pythonovej Telekom "apky", zahajujem prvý štelung účtu')
	pin_verif_request()

config.read('telekom.cfg')
login()
dashboard()
cfg_save()