***Tento repozitár nemá nijak poškodzovať spoločnosť Slovak Telekom a ani ich oficiálnu aplikáciu z ktorej bolo spracované toto API.***

**Použitie API z tohoto dokumentu nemusí byť povolené Telekomom pre neoficiálne aplikácie!** *Nezodpovedám za akékoľvek problémy ktoré môžu nastať.*

# Slovak Telekom App API
Zreverseengineerované API z oficiálnej aplikácie slovenského Telekomu. Na GitHube naschvál aby sa dalo jednoducho nájsť a pokiaľ možno aj pochopiť.

* Pôvodne na využitie v rôznych neoficiálnych Telekom aplikáciach pre UWP Windows, SailfishOS a iné rôzne platformy na ktoré neexistuje žiadna oficiálna aplikácia.
* Všetky popísané requesty fungujú dokedy ich Telekom neprešteluje a nepokazí. *(čož dúfajme že sa ani nestane)*

Zároveň je v tomto repozitári aj **[funkčný pythonový príklad využitia tohoto API](https://github.com/TheMorc/telekom-api/blob/main/telekom.py)**.

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
