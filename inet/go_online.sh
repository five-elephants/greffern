#!/bin/sh

#PRICE_ID=136  # 90 min, 1 GB
PRICE_ID=235   # 30 Tage, 300 MB

curl --cookie cookies --cookie-jar cookies --head https://web.vodafone.de/sbb/welcome
curl --cookie cookies --cookie-jar cookies --user-agent "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)" --data "priceId=$PRICE_ID&pytId=1&backButton.x&nextButton.x" https://web.vodafone.de/sbb/processProductPaymentForm
curl --cookie cookies --cookie-jar cookies --user-agent "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)" --data "backButton.x&nextButton.x" https://web.vodafone.de/sbb/createSubscriptionDirect