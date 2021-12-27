Carbon Calculator
================

The Carbon Calculator tool aims to calculate the CO2 emissions of any website. The tool is the porting in python of the WholeGrain Agency [Carbon Calculator tool](<https://www.websitecarbon.com/>), but it is faster and with more metrics.


How it works
------------
The tool uses the same [algorithm](https://www.websitecarbon.com/how-does-it-work/) of the original tool but it is faster because it doesn't call external APIs.
Soon more infos in a Medium post.

<img src="https://github.com/gpirrotta/carbon-calculator/raw/main/docs/images/py-carbon-calculator.png">



Requirements
------------
* Python >=3.6
* [The Green Web Foundation Dataset](https://www.thegreenwebfoundation.org/)
* [LightHouse Tool](https://github.com/GoogleChrome/lighthouse)


Installation
-------------


##### Install the Green Web Foundation Dataset

Go to the [Green Web Foundation](https://admin.thegreenwebfoundation.org/admin/green-urls), get the most updated link and substitute it in the following command:

```
mkdir data && cd data
curl https://tgwf-green-domains-live.s3.nl-ams.scw.cloud/green_urls_2021-12-08.db.gz | gunzip -c > green_urls.db
```

##### Install the Lighthouse tool 

```nodejs
npm install -g lighthouse
```

##### Install the Carbon Calculator tool 

```py
pip install carbon-calculator
```


Using the tool
--------------
##### As Python Library
  
```py
from carbon.calculator import CarbonCalculator
from carbon.services import LighthouseService, GreenWebService

# If lighthouse tool is installed globally the following row can be omitted
lighthouse = LighthouseService(lighthouse = PATH_OF_LIGHTHOUSE_TOOL)

# It loads the Green Web Dataset DB (must be a SQL3Lite file)
greenweb = GreenWebService(greenweb = PATH_URL_OF_GREEN_DB)

# It calculates CO2 emissions
carbon = CarbonCalculator(lighthouse=lighthouse, greenweb=greenweb)
carbon.footprint("https://www.unime.it")

print(carbon.co2_grams)

//0.29566587414592505

```

##### As Python Library from INI File
Example of **config.ini** file:
```
[GREENWEB]
GREENWEB_PATH = /Users/giovanni/projects/carbon-calculator/data/green_urls.db

[LIGHTHOUSE]
LIGHTHOUSE_PATH = /Users/giovanni/.nvm/versions/node/v14.17.6/bin/lighthouse
```
If Lighthouse tool is installed globally set the LIGHTHOUSE_PATH empty


```py
from carbon.calculator import CarbonCalculator

carbon = CarbonCalculator.from_ini_file('config.ini')
carbon.footprint("https://www.unime.it")

print(carbon.co2_grams)

//0.29566587414592505

```

##### As Command Line Interface (CLI)

```
carbon-cli -h

usage: carbon-cli [-h] -db GREENWEB [-lh LIGHTHOUSE] website

Carbon Calculator - the tool calculates the carbon emissions (CO2) and green infos of any website

positional arguments:
  website               The URL to analyze

optional arguments:
  -h, --help            show this help message and exit
  -db GREENWEB, --greenweb GREENWEB
                        (Mandatory) - The path of the Green Web Foundation DB (SQL3Lite DB file)
  -lh LIGHTHOUSE, --lighthouse LIGHTHOUSE
                        (Optional) - The path of the Lighthouse tool
```


```
carbon-cli --greenweb=/Users/giovanni/projects/carbon-calculator/data/green_urls_2021-12-01.db  --lighthouse=/Users/giovanni/.nvm/versions/node/v14.17.6/bin/lighthouse https://www.unime.it
```

Output
------
```
{
    "date": "2021-12-10T16:07:20.881173+01:00",
    "url": "https://www.unime.it",
    "hosting_green": false,
    "co2_grams": 2.3048954692203547,
    "energy_kWh": 0.004852411514148116,
    "water_litres": 1.2819828599803613,
    "resources": {
        "transfer_size_bytes": {
            "total": 3823256,
            "total_weighted": 2886558,
            "html": 18332,
            "css": 220144,
            "javascript": 573821,
            "image": 2962769,
            "font": 1613,
            "audio": 0,
            "video": 0,
            "other": 46577
        },
        "resources_size_bytes": {
            "total": 8375362,
            "html": 278333,
            "css": 3448588,
            "javascript": 1645906,
            "image": 2955453,
            "font": 1268,
            "audio": 0,
            "video": 0,
            "other": 45814
        }
    }
}

```

###### Fields available

| Name              | Format                                 | Detail                                                                                  | Example                          |
| ----------------- | -------------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------- |
| **co2_grams**     | float                                  | The CO2 Emissions in grams                                                              | 2.3048954692203547               |
| **date**          | YYYY-MM-DDThh:mm:ss.sTZD (**ISO8601**) | Date and time of the measurement                                                        | 2021-12-10T16:07:20.881173+01:00 |
| **energy_kWh**    | float                                  | The power energy consumed in kWh (**kiloWatt-hour**)                                    | 0.004852411514148116             |
| **hosting_green** | boolean                                | boolean - true if the hosting is present in the Green Web Foundation DB otherwise false | True                             |
| **resources**     | array                                  | Info Resources (See table below)                                                        |                                  |
| **url**           | string                                 | The website to analyze                                                                  | https://www.unime.it             |
| **water_litres**  | float                                  | The amount of water to boil to emit the same amount of CO2 in the air                   | 1.2819828599803613               |




###### Info Resources

| Array key names                            | Format     | Detail                                                               | Example      |
|--------------------------------------------|------------|----------------------------------------------------------------------|--------------|
| transfer_size_bytes[**total**]             |   int      |  The data traffic total in bytes  (compressed)                       | 3823256      |
| transfer_size_bytes[**total_weighted**]    |   int      | The weighted data traffic total in bytes (considering caches)        | 2886558      |
| transfer_size_bytes[**html**]              |   int      | The HTML data traffic total in bytes                                 | 18332        |
| transfer_size_bytes[**css**]               |   int      | The CSS data traffic total in bytes                                  | 220144       |
| transfer_size_bytes[**javascript**]        |   int      | The JAVASCRIPT data traffic total in bytes                           | 573821       |
| transfer_size_bytes[**image**]             |   int      | The IMAGE data traffic total in bytes                                | 2962769      |
| transfer_size_bytes[**font**]              |   int      | The FONT data traffic total in bytes                                 | 1613         |
| transfer_size_bytes[**audio**]             |   int      | The AUDIO data traffic total in bytes                                | 0            |
| transfer_size_bytes[**video**]             |   int      | The VIDEO data traffic total in bytes                                | 0            |
| transfer_size_bytes[**other**]             |   int      | The OTHER data traffic total in bytes                                | 46577        |
| resources_size_bytes[**total**]            |   int      | The Web resources total size in bytes                                | 8375362      |
| resources_size_bytes[**html**]             |   int      | The HTML resource size in bytes                                      | 278333       |
| resources_size_bytes[**css**]              |   int      | The CSS resources size in bytes                                      | 3448588      |
| resources_size_bytes[**javascript**]       |   int      | The JAVASCRIPT resources size in bytes                               | 1645906      |
| resources_size_bytes[**image**]            |   int      | The IMAGE resources size in bytes                                    | 2955453      |
| resources_size_bytes[**font**]             |   int      | The FONT resources size in bytes                                     | 1268         |
| resources_size_bytes[**audio**]            |   int      | The AUDIO resources size in bytes                                    | 0            |
| resources_size_bytes[**video**]            |   int      | The VIDEO resources size in bytes                                    | 0            |
| resources_size_bytes[**other**]            |   int      | The OTHER resources size in bytes                                    | 45814        |


Resources
---------
* **Lighthouse**: [github repo](https://github.com/GoogleChrome/lighthouse)
* **Green Web Dataset**: [website](https://www.thegreenwebfoundation.org/)



License
-------
* **Carbon Calculator**: [MIT license](https://spdx.org/licenses/MIT.html)
* **Green Web Dataset**: [Open Database License](https://opendatacommons.org/licenses/odbl/summary/index.html)


Credits
-------
[Giovanni Pirrotta](mailto:giovanni.pirrotta@gmail.com)