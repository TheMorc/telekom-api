***Tento repozitár nemá nijak poškodzovať spoločnosť Slovak Telekom a ani ich oficiálnu aplikáciu z ktorej bolo spracované toto API.***

**Použitie API z tohoto dokumentu nemusí byť povolené Telekomom pre neoficiálne aplikácie!** *Nezodpovedám za akékoľvek problémy ktoré môžu nastať.*

# Slovak Telekom App API
Zreverseengineerované API z oficiálnej aplikácie slovenského Telekomu. Na GitHube naschvál aby sa dalo jednoducho nájsť a pokiaľ možno aj pochopiť.

* Pôvodne na využitie v rôznych neoficiálnych Telekom aplikáciach pre UWP Windows, SailfishOS a iné rôzne platformy na ktoré neexistuje žiadna oficiálna aplikácia.
* Všetky popísané requesty fungujú dokedy ich Telekom neprešteluje a nepokazí. *(čož dúfajme že sa ani nestane)*

Funkčné príklady využitia tohto API:
* **[Pythonový bastl v tomto repozitári](https://github.com/TheMorc/telekom-api/blob/main/telekom.py)**
* **[UWP aplikácia pre Windows](https://github.com/TheMorc/telekom-uwp)**

## Prispievanie do repozitára
Keď vám nejaká podstatná vec chýba, chcete niečo doplniť tak kľudne do toho, potom môžete poslať pull request s novými informáciami.
Každá doplnená vec sa ráta.

## Autor
V prípade záujmu môžete poslať otázku/dopyt/čokoľvek do Issues sekcie tu v tomto repozitári.

**Richard Gráčik - Morc** ([@TheMorc](https://github.com/TheMorc))

## Popis API *(možno moc nečítateľný)*
* curl príkazy povačšine čisté
* response možno nie pri všetkých krokoch dostupný ale väčšinou s popisom čo obsahuje 
* kopa vecí je plná otáznikov a netuším čo a ako

**postup pri prvom pustení:** pýtať pin, verifikuvať, prihlásiť a vytlačiť dashboard

**postup pri pustení do 10 minút:** prihlásiť a vytlačiť dashboard

**postup pri pustení od 10 minút hore:** popýtať nový token, prihlásiť a vytlačiť dashboard
## 

### pýtaní pinu na číslo
* pýta číslo, typ, zariadenie a dôvod
```shell
curl  -H 'Authorization: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' \
-H 'X-Request-Session-Id: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' \
-H 'X-Request-Tracking-Id: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' \
-H 'Content-Type: application/json' -X POST https://t-app.telekom.sk/pin/ -d '{"serviceId":<TU JE TEL. ČÍSLO VO FORMÁTE +4219xxXXXxxx>"","serviceType":"phoneNumber","device":{"os":"ios"},"context":"login"}'
```
* response má nonce ktorý sa potom používa na verifikáciu pinom
```json
{
  "serviceId" : "<SEM DÁ TEL. ČÍSLO>",
  "nonce" : "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF",
  "enableProfilePin" : false,
  "isPinSet" : false,
  "enableAlphaNumericServiceId" : false,
  "rememberMe" : false
}
```

##

### verifikácia
* pýta device id (asi generované lokálne na zariadení) ktoré sa potom používa aj pri prihlasovaní
* pýta nonce ktorý je z prvého POST requestu na PIN
```shell
curl -H 'Accept: */*' -H 'Authorization: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' \
-H 'X-Request-Session-Id: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' \
-H 'X-Request-Tracking-Id: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' -H 'Content-Type: application/json' \
-X PUT https://t-app.telekom.sk/pin/ -d '{"device":{"id":"FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF","os":"ios"},"enableProfilePin":false,"serviceId":"<TU JE TEL. ČÍSLO>","serviceType":"phoneNumber","context":"login","PIN":"123456","nonce":"FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"}'
```
* response má tokeny ktoré sa používajú pri prihlasovaní a používaní aplikácie

##

### prihlásení a prvý dump údajov z telekomu
* pýta accessToken, deviceId z verifikácie, sub je MSISDN_ a číslo 421xxxxxx
```shell
curl -H 'Accept: */*' -H 'Authorization: Bearer <TU JE accessToken' \
-H 'X-Client-Version: 18.8.2 (887) 2-78c3ec0 (HEAD)' -H 'X-Request-Session-Id: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' \
-H 'X-Request-Tracking-Id: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' -H 'os: iOS/13.5.1' -H 'Accept-Language: sk' \
--compressed -H 'Content-Type: application/json' -H 'User-Agent: OneApp/887 CFNetwork/1126 Darwin/19.5.0' \
-H 'Connection: keep-alive' -H 'app-widget: false' 'https://t-app.telekom.sk/profiles/?deviceId=FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF&devicesWithEMI=false&genCenToken=true&hybridEnabled=true&loyaltyEnabled=false&sub=<TU JE MSISDN S ČÍSLOM>&subscriptionServiceEnabled=false'
```
* response má centralToken, MSISDN id, email, číslo, status, meno účtu, typ karty jej číslo custom meno, špeciálne ID (SIEBEL-PRD-PRODUCT) ktoré je potom ďalej používané 

##

### regen tokenu na yo-digital
* pýta token na dvoch místach jednaký kerý je v prvom dumpe údajov z telekomu
```shell
curl -H 'content-type: application/json' -H 'accept: */*' \
-H 'authorization: Bearer <TU JE accessToken>' \
-H 'x-client-version: 18.8.2 (887) 2-78c3ec0 (HEAD)' -H 'x-request-session-id: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' \
-H 'x-request-tracking-id: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' -H 'os: iOS/13.5.1' --compressed -H 'accept-language: sk' \
-H 'user-agent: OneApp/887 CFNetwork/1126 Darwin/19.5.0' \
-H 'central_token: <TU JE centralToken z profilov>' \
-X POST https://external-gateway.oa.yo-digital.com/centralauth-prod/token/generate -d null
```
* response má voláky access_token ktorý netuším kde sa používa, potom refreshToken ktorý je asi potom na ďalšie regeny cez t-app.telekom.sk/token stránku, ostatok netuším                

##

### telekom dashboard (ukazuje dáta)
* pýta prvý accessToken
```shell
curl -H 'Accept: */*' -H 'Authorization: Bearer <TU JE accessToken>' \
-H 'X-Client-Version: 18.8.2 (887) 2-78c3ec0 (HEAD)' -H 'X-Request-Session-Id: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' -H 'X-Request-Tracking-Id: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' \
-H 'os: iOS/13.5.1' -H 'Accept-Language: sk' --compressed -H 'Content-Type: application/json' -H 'User-Agent: OneApp/887 CFNetwork/1126 Darwin/19.5.0' -H 'Connection: keep-alive' \
-H 'app-widget: false' 'https://t-app.telekom.sk/dashboard/product/<TU JE SIEBEL PRODUCT ID>?enableFreeUnit=true&priority=primary&profileId=<TU JE MSISDN S ČÍSLOM>&serviceOnboarding=false&serviceOutageEnabled=false&showTotalCreditBalance=true&showUnlimited=true'
```
* názorná ukážka responsu, má veci kolo SIMky ako napríklad dáta z mesačného programu
```json
{
    "campaignPlanDetail": {
        "id": "RP1014",
        "name": "ÁNO S"
    },
    "consumption": {
        "boostAction": "inactive",
        "consumptionGroupType": "data",
        "id": "aggregated",
        "level": "low",
        "max": {
            "unit": "GB",
            "value": 4.5
        },
        "name": "Zostávajúce dáta z vášho mesačného programu - zostatok",
        "priority": 0,
        "remaining": {
            "unit": "MB",
            "value": 0
        },
        "remainingPercentage": 0,
        "type": "line",
        "unlimitedDataBackup": false,
        "updatedTime": "2021-09-16T13:29:58.000Z",
        "used": {
            "unit": "GB",
            "value": 4.5
        }
    },
    "consumptionSummaries": [
        {
            "key": "extra_cost",
            "level": "normal",
            "unit": "EUR",
            "value": 0.0
        }
    ],
    "isRoamingEnabled": false,
    "newStatus": "Active",
    "status": "active",
    "tariffChangeStatus": "Active",
    "unlimitedDataBackup": false
}
```

##

### popýtavaní nového tokenu
* pýta refreshToken
```shell
curl -H 'Accept: */*' -H 'Authorization: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' -H 'X-Client-Version: 18.8.2 (887) 2-78c3ec0 (HEAD)' -H 'X-Request-Session-Id: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' \
-H 'X-Request-Tracking-Id: FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF' -H 'os: iOS/13.5.1' -H 'Accept-Language: sk' --compressed -H 'Content-Type: application/json' -H 'User-Agent: OneApp/887 CFNetwork/1126 Darwin/19.5.0' \
-H 'Connection: keep-alive' \
-X POST https://t-app.telekom.sk/token/ -d '{"genCenToken":false,"refreshToken":"<TU JE refreshToken>","deviceId":"0D3BF2CC-AD00-4881-B815-D159BFDAC1E7"}'
```
* response má nový accessToken kerý sa používa potom v apke, asi aj nový refreshToken na potomajšé refreshuvaní

##

### "Akcie a súťaže" webview
* pýta accessToken
```
http://m.telekom.sk/api/app-sutaze-akcie/ver2/?zdroj=oneapp_menu
```

##

### "Magenta1 Skupina" webview 
* pýta accessToken - ako Authorization: Bearer
```
https://m.telekom.sk/api/app-sutaze-akcie/ver2/magenta1/?zdroj=oneapp_menu
```

##

### "Eshop" webview
```
https://www.telekom.sk/eshop-telekom?traffic_source=app_webview
```

##

### Nezaplatené faktúry (v aplikácií nad dashboardom tuším)
* pýta accessToken
```
https://t-app.telekom.sk/customerBills/unpaid/summary/
```
* response má počet, cenu a faktúru

##

### aktualizovať SIM label
* pýta accessToken a json s novým menom
```
PATCH https://t-app.telekom.sk/profiles/MSISDN_<MSISDN s číslom>/manageableAssets/<ŠPECIFICKÝ SIEBEL PRD PRODUKT>?fields=label
```
* json príklad
```json
{
    "label": "SIMka"
}
```
* response má SIEBEL PRD PRODUKT id a nové meno

##

### aktualizovať profil (meno, email, číslo atď)
* pýta accessToken a json s novými údajmi
```
PATCH https://t-app.telekom.sk/profiles/MSISDN_<MSISDN s číslom>?fields=individual%2Ccharacteristics%2CcontactMediums
```
* json príklad
```json
{
    "contactMediums": [
        {
            "medium": {
                "number": "+4219XXxxxXXX"
            },
            "role": {
                "name": "contact"
            },
            "type": "mobile"
        },
        {
            "medium": {
                "emailAddress": "mail@Example.com"
            },
            "role": {
                "name": "contact"
            },
            "type": "email"
        }
    ],
    "individual": {
        "familyName": "Priezvisko",
        "givenName": "Meno"
    }
}
```
* response má characteristics s telekom_username, contactMediums s číslom a mailom, detailedStatus, id, individual s menom a prievziskom a status

##

### Faktúruvačky
* bere accessToken
```
GET https://t-app.telekom.sk/billingMonths?monthCount=24
```
* skrátený response
```json
[
    {
        "month": 9,
        "year": 2021
    },
    {
        "month": 8,
        "year": 2021
    },
    {
        "month": 7,
        "year": 2021
    },
    {
        "month": 11,
        "year": 2019
    }
]
```

##

### Špecifické fakturačné období
* bere accessToken
```
GET https://t-app.telekom.sk/customerBills/paid/2021/9
```
* response má údaje a veci naokolo
```
[
    {
        "appliedPayment": [],
        "billDate": "2021-09-01",
        "billDocument": [],
        "billingAccount": {
            "businessId": "xxxxxxxxxx",
            "id": "SIEBEL-PRD-BILLING_PROFILE-xxxxxxxxxxxx",
            "name": "xxxxxxxxxx"
        },
        "id": "SIEBEL-PRD-BILLING_PROFILE-xxxxxxxxxxxx__RMCA-PRD-INVOICE-xxxxxxxxxxxx",
        "isBillUnpayable": false,
        "relatedParty": [],
        "taxItem": [],
        "type": "Pravidelná faktúra"
    }
]
```

##

### Detaily špecifického fakturačného obdobia
* bere accessToken
```
GET https://t-app.telekom.sk/customerBills/SIEBEL-PRD-BILLING_PROFILE-xxxxxxxxxxxx__RMCA-PRD-INVOICE-xxxxxxxxxxxx
```
* response má všetky sprostosti naokolo od odkazu na faktúru v PDFku, ceny, dátumy a tak.

##

### Aktuálny výpis pre kartu
* bere accessToken
```
GET https://t-app.telekom.sk/manageServices/product/SIEBEL-PRD-PRODUCT-xxxxxxxxxxxxxxxxxxxxxx/details?checkCancelEligibility=false&devicesWithEMI=false&disableDocumentManagement=true&enableExtraData=false&enableFreeUnit=true&enableVasCategories=false&profileId=MSISDN_<tu je MSISDN s číslom>&serviceOnboarding=false&serviceOutageEnabled=false&subscriptionServiceEnabled=false&swapEnabled=false&tariffOfferEnable=true&transferUnitsEnabled=false&vasDelay=true
```
* response má všetky údaje o paušáli, zostávajúce dáta, SMSky, MMSky, prevolané a neprevolané minúty, dátumy, IDčká atď

##

### Vypíš dostupné data/roam balíčkové skupiny
* bere accessToken
```
GET https://t-app.telekom.sk/v2/manageServices/product/SIEBEL-PRD-PRODUCT-xxxxxxxxxxxxxxxxxxxxxx/addons/?customCategory=true&enableAddonBenefitVisualization=false&enableAdvancedAddon=true&loyaltyEnabled=false&planEnabled=true
```
* response
```json
{
    "addonGroups": [],
    "categories": [
        {
            "id": "data",
            "name": "Dátové balíčky",
            "priority": 10000
        },
        {
            "id": "roaming",
            "name": "Roamingové balíčky",
            "priority": 9500
        }
    ]
}
```

##

### Vypíš dostupné dátové balíčky pre kartu
* bere accessToken
```
GET https://t-app.telekom.sk/v2/manageServices/product/SIEBEL-PRD-PRODUCT-xxxxxxxxxxxxxxxxxxxxxx/addons/?categoryId=data&enableAddonBenefitVisualization=false&enableAdvancedAddon=true&loyaltyEnabled=false&planEnabled=true
```
* response
```json
{
    "categories": [
        {
            "id": "POSTPAID_DATA_ONE_DAY",
            "name": "Denné - jednorazové",
            "offers": [
                {
                    "description": "Dátový balíček <b>Denné dáta pre prenos plnou rýchlosťou. <br><b>Objem dát: neobmedzené </b><br>Aktivácia balíčka vám bude účtovaná v najbližšej faktúre.",
                    "group": "addon",
                    "id": "DATA DEN NEOB",
                    "name": "Denné dáta neobmedzené",
                    "price": {
                        "amount": 3,
                        "currencyCode": "EUR"
                    },
                    "priceType": "activationFee",
                    "priority": 80,
                    "shortDescription": "Dátový balíček <b>Denné dáta pre prenos plnou rýchlosťou. <br><b>Objem dát: neobmedzené </b><br>Aktivácia balíčka vám bude účtovaná v najbližšej faktúre.",
                    "subscriptionPlanCharacteristics": false,
                    "validUntil": "2021-09-22T13:22:20.177Z",
                    "warningMessage": "Dátový balíček <b>Denné dáta pre prenos plnou rýchlosťou. <br><b>Objem dát: neobmedzené </b><br>Aktivácia balíčka vám bude účtovaná v najbližšej faktúre."
                },
                {
                    "description": "Dátový balíček <b>Denné dáta 1  GB</b> pre prenos plnou rýchlosťou. <br><b>Objem dát: 1 GB</b><br>Aktivácia balíčka vám bude účtovaná v najbližšej faktúre.",
                    "group": "addon",
                    "id": "DATA_DEN_1_GB",
                    "name": "Denné dáta 1 GB",
                    "price": {
                        "amount": 1.5,
                        "currencyCode": "EUR"
                    },
                    "priceType": "activationFee",
                    "priority": 70,
                    "shortDescription": "Dátový balíček <b>Denné dáta 1 GB</b> pre prenos plnou rýchlosťou. <br><b>Objem dát: 1 GB</b><br>Aktivácia balíčka vám bude účtovaná v najbližšej faktúre.",
                    "subscriptionPlanCharacteristics": false,
                    "validUntil": "2021-09-22T13:22:20.177Z",
                    "warningMessage": "Dátový balíček <b>Denné dáta 1  GB</b> pre prenos plnou rýchlosťou. <br><b>Objem dát: 1 GB</b><br>Aktivácia balíčka vám bude účtovaná v najbližšej faktúre."
                }
            ],
            "priority": 6800
        },
        {
            "id": "POSTPAID_DATA_BILL_CYCLE",
            "name": "Mesačné - jednorazové",
            "offers": [
                {
                    "description": "Dátový balíček <b>DATA 1 GB</b> pre prenos plnou rýchlosťou. <br><b>Objem dát: 1 GB</b><br>Aktivácia balíčka vám bude účtovaná v najbližšej faktúre.",
                    "group": "addon",
                    "id": "DATA_1_GB_PREN",
                    "name": "DATA 1 GB",
                    "price": {
                        "amount": 3,
                        "currencyCode": "EUR"
                    },
                    "priceType": "activationFee",
                    "priority": 60,
                    "shortDescription": "Dátový balíček <b>DATA 1 GB</b> pre prenos plnou rýchlosťou. <br><b>Objem dát: 1 GB</b><br>Aktivácia balíčka vám bude účtovaná v najbližšej faktúre.",
                    "subscriptionPlanCharacteristics": false,
                    "validUntil": "2021-10-31T22:59:59.999Z",
                    "warningMessage": "Dátový balíček <b>DATA 1 GB</b> pre prenos plnou rýchlosťou. <br><b>Objem dát: 1 GB</b><br>Aktivácia balíčka vám bude účtovaná v najbližšej faktúre."
                }
            ],
            "priority": 6700
        },
        {
            "id": "POSTPAID_DATA_ADR",
            "name": "Mesačné - automaticky dokupované",
            "offers": [
                {
                    "description": "Dátový balíček <b>DATA 1 GB - Automatické dokupovanie</b> pre prenos plnou rýchlosťou. <br><b>Objem dát: 1 GB</b><br>Dáta z tohto balíčka čerpáte iba v prípade, ak už nemáte dáta z paušálu a nemáte aktivovaný žiaden iný dátový balíček. Po jeho vyčerpaní sa automaticky obnoví a môžete dáta znova využívať. Spoplatnené je každé obnovenie balíka a bude účtované v najbližšej faktúre. Automatické dokupovanie prebieha až do deaktivácie tohto balíčka.",
                    "group": "addon",
                    "id": "SC1708",
                    "name": "DATA 1 GB - Automatické dokupovanie",
                    "price": {
                        "amount": 3,
                        "currencyCode": "EUR"
                    },
                    "priceType": "recurringFee",
                    "priority": 30,
                    "recurringChargeDuration": 1,
                    "recurringChargePeriod": "day",
                    "shortDescription": "Dátový balíček <b>DATA 1 GB - Automatické dokupovanie</b> pre prenos plnou rýchlosťou. <br><b>Objem dát: 1 GB</b><br>Dáta z tohto balíčka čerpáte iba v prípade, ak už nemáte dáta z paušálu a nemáte aktivovaný žiaden iný dátový balíček. Po jeho vyčerpaní sa automaticky obnoví a môžete dáta znova využívať. Spoplatnené je každé obnovenie balíka a bude účtované v najbližšej faktúre. Automatické dokupovanie prebieha až do deaktivácie tohto balíčka.",
                    "subscriptionPlanCharacteristics": false,
                    "validUntil": "2021-10-31T22:59:59.999Z",
                    "warningMessage": "Dátový balíček <b>DATA 1 GB - Automatické dokupovanie</b> pre prenos plnou rýchlosťou. <br><b>Objem dát: 1 GB</b><br>Dáta z tohto balíčka čerpáte iba v prípade, ak už nemáte dáta z paušálu a nemáte aktivovaný žiaden iný dátový balíček. Po jeho vyčerpaní sa automaticky obnoví a môžete dáta znova využívať. Spoplatnené je každé obnovenie balíka a bude účtované v najbližšej faktúre. Automatické dokupovanie prebieha až do deaktivácie tohto balíčka."
                }
            ],
            "priority": 6600
        },
        {
            "id": "POSTPAID_DATA_RECURRING",
            "name": "S mesačným poplatkom",
            "offers": [
                {
                    "description": "S balíkom <b>StreamOn</b> počúvate hudbu a pozeráte videá cez podporované mobilné aplikácie neobmedzene a bez obáv, že si miniete svoje dáta.<br><b>Cena balíka: 10,00€ s DPH /mesiac<br>Za balík <b>StreamOn</b> platíte mesačný poplatok až do deaktivácie balíka.",
                    "group": "addon",
                    "id": "SC1571",
                    "name": "StreamOn – s automatickým obnovením",
                    "price": {
                        "amount": 10,
                        "currencyCode": "EUR"
                    },
                    "priceType": "recurringFee",
                    "priority": 65,
                    "recurringChargeDuration": 1,
                    "recurringChargePeriod": "month",
                    "shortDescription": "S balíkom <b>StreamOn</b> počúvate hudbu a pozeráte videá cez podporované mobilné aplikácie neobmedzene a bez obáv, že si miniete svoje dáta. Podporované aplikácie nájdete na linke nižšie.<br><b>Cena balíka: 10,00€ s DPH /mesiac<br>Za balík <b>StreamOn</b> platíte mesačný poplatok až do deaktivácie balíka.",
                    "subscriptionPlanCharacteristics": false,
                    "termsAndConditionsUrl": "https://www.telekom.sk/streamon",
                    "warningMessage": "S balíkom <b>StreamOn</b> počúvate hudbu a pozeráte videá cez podporované mobilné aplikácie neobmedzene a bez obáv, že si miniete svoje dáta.<br><b>Cena balíka: 10,00€ s DPH /mesiac<br>Za balík <b>StreamOn</b> platíte mesačný poplatok až do deaktivácie balíka."
                }
            ],
            "priority": 6500
        }
    ]
}
```
