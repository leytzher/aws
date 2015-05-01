# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 19:59:07 2015

@author: user
"""

# AWS Utility functions
# Author: Leytzher Muro



def amazonSearchByKeywords(keywords,awsKeyId,awsSecretAccessKey,awsAffiliateId):
    import base64, hashlib, hmac, time
    from urllib import urlencode, quote_plus
    base_url = "http://webservices.amazon.com/onca/xml"
    url_params = dict(
        Service='AWSECommerceService', 
        Operation='ItemSearch', 
        Keywords= keywords,
        SearchIndex='All',
        AWSAccessKeyId=awsKeyId,
        AssociateTag = awsAffiliateId,
        ResponseGroup='Large')
    

    #Can add Version='2009-01-06'. What is it BTW? API version?


    # Add a ISO 8601 compliant timestamp (in GMT)
    url_params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # Sort the URL parameters by key
    keys = url_params.keys()
    keys.sort()
    # Get the values in the same order of the sorted keys
    values = map(url_params.get, keys)

    # Reconstruct the URL parameters and encode them
    url_string = urlencode(zip(keys,values))

    #Construct the string to sign
    string_to_sign = "GET\nwebservices.amazon.com\n/onca/xml\n%s" % url_string

    # Sign the request
    signature = hmac.new(
        key=awsSecretAccessKey,
        msg=string_to_sign,
        digestmod=hashlib.sha256).digest()

    # Base64 encode the signature
    signature = base64.encodestring(signature).strip()

    # Make the signature URL safe
    urlencoded_signature = quote_plus(signature)
    url_string += "&Signature=%s" % urlencoded_signature

    #print "%s?%s\n\n%s\n\n%s" % (base_url, url_string, urlencoded_signature, signature)
    print "%s?%s\n" % (base_url, url_string)
    return base_url+"?"+url_string

################


from bs4 import BeautifulSoup
import pandas as pd

def xml2df(xml_doc):
    f = open(xml_doc, 'r')
    soup = BeautifulSoup(f)

    name_list=[]
    text_list=[]
    attr_list=[]

    def recurs(soup):
        try:
            for j in soup.contents:
                try:
                    #print j.name
                    if j.name!=None:
                        name_list.append(j.name)
                except:
                    pass
                try:
                    #print j.text
                    if j.name!=None:
                        #print j.string
                        text_list.append(j.string)
                except:
                    pass
                try:
                    #print j.attrs
                    if j.name!=None:
                        attr_list.append(j.attrs)
                except:
                    pass
                recurs(j)
        except:
            pass

    recurs(soup)

    attr_names_list = [q.keys() for q in attr_list]
    attr_values_list = [q.values() for q in attr_list]

    columns = hstack((hstack(name_list),
                      hstack(attr_names_list)) )
    data = hstack((hstack(text_list),
                   hstack(attr_values_list)) )

    df = pd.DataFrame(data=matrix(data.T), columns=columns )

    return df
