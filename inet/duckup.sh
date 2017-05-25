#!/bin/sh

echo url="https://www.duckdns.org/update?domains=greffern&token=d27fc66f-847d-49e4-8fd5-54ed6b4f71b6&ip=" | curl -k -o ~/duck.log -K -
