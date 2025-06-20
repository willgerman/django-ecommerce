
# Fountain Mugs LLC, E-Commerce Application

A digital storefront designed and developed for the Bridgewater College CSCI-400 Software Engineering course. The above company is fictional and any references or relation to existing businesses, places, people, entities, or objects is entirely coincidental and should not be considered an endorsement or imply any relationship between parties.


## Authors

- Will German ([@willgerman](https://github.com/willgerman))
- Daniel Shulgan ([@danielshulgan](https://github.com/danielshulgan))
- Chris Arnold ([@Carno2](https://github.com/Carno2))
- Jimmy Rosend ([@Jimbob432](https://github.com/Jimbob432))
- Cole Miller ([@colemiller12](https://github.com/colemiller12))
- Eli Coleman ([@EliC23](https://github.com/EliC23))


## Run Locally

Follow the below listed instructions to successfully install and run this project on your local machine.

### 1. Clone the Repository.

```
git clone https://github.com/will-german/csci-400-ecommerce
cd csci-400-ecommerce
```

### 2. Create a Virtual Environment

MacOS
```
python3 -m venv ./venv
```

Windows
```
python -m venv ./venv
```

### 3. Setup Environment Variables

Create a new file ".env" in your root directory. The following variables are required to run the application locally:

```SECRET_KEY```, ```DEBUG```, ```ALLOWED_HOSTS```, ```SENDGRID_API_KEY```, ```STRIPE_PUBLISHABLE_KEY```, ```STRIPE_SECRET_KEY```


### 4. Activate the Virtual Environment

Your dependencies will be installed within the virtual environment. Installing outside of this environment will install dependencies globally.

**MacOS/Unix**
```
source venv/bin/activate
```

**Windows**
```
venv\Scripts\activate
```

### 5. Install Requirements
```
pip install -r requirements.txt
```

### 6. Migrate
```
python manage.py migrate
```

### 7. Collect Static Files
```
python manage.py collectstatic
```

### 8. Create a Superuser
```
python manage.py createsuperuser
```

### 9. Run the Server
```
python manage.py runserver
```


## Features

- Responsive User Interface
- Content Management System
- Permissions and Authentication
- Cross Browser Compatible ([Chrome](https://www.google.com/chrome/dr/download/?brand=SJWC&ds_kid=43700080875129437&gad_source=1&gclid=CjwKCAjwyfe4BhAWEiwAkIL8sLpkq4L7oAGTvaPU7PcEt4Jk86vi8KcU_vlUuPpSctIL4oFrGntD6BoC5rMQAvD_BwE&gclsrc=aw.ds), [Firefox](https://www.mozilla.org/en-US/firefox/), [Edge](https://www.microsoft.com/en-us/edge/download?form=MA13FJ), [Safari](https://www.apple.com/safari/))
- PCI Compliant Payment Gateway ([Stripe Checkout](https://stripe.com/payments/checkout?utm_campaign=AMER_US_en_Google_Search_Brand_Checkout_EXA-20550770147&utm_medium=cpc&utm_source=google&ad_content=673946537954&utm_term=stripe%20checkout&utm_matchtype=e&utm_adposition=&utm_device=c&gad_source=1&gclid=CjwKCAjwyfe4BhAWEiwAkIL8sN7F492SlsLIQf-xIFHkeZob2JCNHLSx8TU9qslXDaAH2ux3Pbz-LRoC_5EQAvD_BwE))
- SMTP Email Service ([SendGrid](https://sendgrid.com/en-us/solutions/email-api?utm_source=google&utm_medium=cpc&utm_term=sendgrid&utm_campaign=SendGrid_G_S_NAMER_Brand_Tier1&cq_plac=&cq_net=g&cq_pos=&cq_med=&cq_plt=gp&gad_source=1&gclid=CjwKCAjwyfe4BhAWEiwAkIL8sDRFEiT0ZI2BM1NW_ZLWswR-MOAZDDFyuILgqaBlUBw98g3-942zbBoCF7kQAvD_BwE))


## License

[MIT License](https://choosealicense.com/licenses/mit/)

Copyright (c) 2024 William Spencer German

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.