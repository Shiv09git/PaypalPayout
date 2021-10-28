# from http import client
# from create_payouts import CreatePayouts
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
import os
import sys
from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment


from paypalpayoutssdk.payouts import PayoutsPostRequest
from paypalhttp import HttpError
from paypalhttp.encoder import Encoder
from paypalhttp.serializers.json_serializer import Json
from payout1.paypal_client import PayPalClient
# from paypal_client import PayPalClient
# import json
import random
import string
# Creating Access Token for Sandbox
# client_id = os.environ.get("PAYPAL-CLIENT-ID")
# client_secret = os.environ.get("PAYPAL-CLIENT-SECRET")
# # Creating an environment
# environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
# client = PayPalHttpClient(environment)



from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment
from django.conf import settings

from paypalpayoutssdk.payouts import PayoutsItemGetRequest

from paypalpayoutssdk.payouts import PayoutsGetRequest

# payout_batch_id=''

class PayPalClient:
    def __init__(self):
        print('In PayPalClient')
        self.client_id =  settings.CLIENTID
        self.client_secret = settings.CLIENTSECRET
        
        """Set up and return PayPal Python SDK environment with PayPal Access credentials.
           This sample uses SandboxEnvironment. In production, use
           LiveEnvironment."""
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance in an environment with access credentials. 
        Use this instance to invoke PayPal APIs, provided the credentials have access. """
        self.client = PayPalHttpClient(self.environment)
        print(self.client)

        

def PAL(self):
    obj = PayPalClient()
    return JsonResponse({"status":"OK"})


print(settings.CLIENTID)
print(settings.CLIENTSECRET)

######## 1 #############
class CreatePayouts(PayPalClient):
    """ Creates a payout batch with 5 payout items
    Calls the create batch api (POST - /v1/payments/payouts)
    A maximum of 15000 payout items are supported in a single batch request"""
    # amount='10.00'
    @staticmethod
    def build_request_body(include_validation_failure=False):
        senderBatchId = str(''.join(random.sample(
            string.ascii_uppercase + string.digits, k=7)))
        amount = "10.00" if include_validation_failure else "1.00"
        return \
            {
                "sender_batch_header": {
                    "recipient_type": "EMAIL",
                    "email_message": "SDK payouts test txn",
                    "note": "Enjoy your Payout!!",
                    "sender_batch_id": senderBatchId,
                    "email_subject": "This is a test transaction from SDK"
                },
                "items": [{
                    "note": "Your 1$ Payout!",
                    "amount": {
                        "currency": "USD",
                        "value": amount
                    },
                    "receiver": "payout-sdk-1@paypal.com",
                    "sender_item_id": "Test_txn_1"
                }]
            }
    
    def create_payouts(self, debug=False):
        # global payout_batch_id
        request = PayoutsPostRequest()
        request.request_body(self.build_request_body(False))
        response = self.client.execute(request)
        # request.session['aaaa']= response.result.batch_header.payout_batch_id
        print('@@@@@@@@100:-' + response.result.batch_header.payout_batch_id)
        # batch_id=response.result.batch_header.payout_batch_id
        
        if debug:
            print("Status Code: ", response.status_code)
            print("Payout Batch ID:- " +
                  response.result.batch_header.payout_batch_id)
            print("Payout Batch Status: " +
                  response.result.batch_header.batch_status)
            print("Links: ")
            
            # batch_id=response.result.batch_header.payout_batch_id
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(
                    link.rel, link.href, link.method))

            # To toggle print the whole body comment/uncomment the below line
            # json_data = self.object_to_json(response.result)
            # print "json_data: ", json.dumps(json_data, indent=4)
        print('@@@@@@@@119:-' + response.result.batch_header.payout_batch_id)
        
        return response


def cpo(self):
    create_response = CreatePayouts().create_payouts(True)
    # print('@@@@@@@@:-' + CreatePayouts().client.execute(PayoutsPostRequest()).response.result.batch_header.payout_batch_id)
    # create_responsee = GetPayouts().get_payouts(True)
    return JsonResponse({"status": create_response.status_code})
# print('@@@@@@@@:-' + response.result.batch_header.payout_batch_id)



    # def get_payouts(self, payout_batch_id, debug=False):
    #     request = PayoutsGetRequest(payout_batch_id)
    #     request.page(1)
    #     request.page_size(10)
    #     request.total_required(True)

    #     try:
    #         response = self.client.execute(request)

    #         if debug:
    #             print(response.result)
    #             print("Status Code: ", response.status_code)
    #             print("Payout Batch ID:-- " +
    #                 response.result.batch_header.payout_batch_id)
    #             print("Payout Batch Status: " +
    #                 response.result.batch_header.batch_status)
    #             print("Items count: ", len(response.result.items))
    #             print("First item id: " + response.result.items[0].payout_item_id)
    #             print("Links: ")
    #             for link in response.result.links:
    #                 print('\t{}: {}\tCall Type: {}'.format(
    #                     link.rel, link.href, link.method))

    #             # To toggle print the whole body comment/uncomment the below line
    #             #json_data = self.object_to_json(response.result)
    #             #print "json_data: ", json.dumps(json_data, indent=4)

    #         return response

    #     except HttpError as httpe:
    #         # Handle server side API failure
    #         encoder = Encoder([Json()])
    #         error = encoder.deserialize_response(httpe.message, httpe.headers)
    #         print("Error: " + error["name"])
    #         print("Error message: " + error["message"])
    #         print("Information link: " + error["information_link"])
    #         print("Debug id: " + error["debug_id"])

    #     except IOError as ioe:
    #         #Handle cient side connection failures
    #         print(ioe.message)

# def cpo(self):
#     create_response = CreatePayouts().create_payouts(True)
#     # create_responsee = GetPayouts().get_payouts(True)
#     return JsonResponse({"status": create_response.status_code})
    # ,'stat':create_responsee.status_code


############## 2 ###########
class GetPayouts(PayPalClient):

    
    """ Retries a Payout batch details provided the batch_id
     This API is paginated - by default 1000 payout items are retrieved
     Use pagination links to navigate through all the items, use total_required to get the total pages"""
    def get_payouts(self, payout_batch_id, debug=False):
        request = PayoutsGetRequest(payout_batch_id)
        request.page(1)
        request.page_size(10)
        request.total_required(True)

        try:
            response = self.client.execute(request)

            if debug:
                print(response.result)
                print("Status Code: ", response.status_code)
                print("Payout Batch ID: " +
                    response.result.batch_header.payout_batch_id)
                print("Payout Batch Status: " +
                    response.result.batch_header.batch_status)
                print("Items count: ", len(response.result.items))
                print("First item id: " + response.result.items[0].payout_item_id)
                print("Links: ")
                for link in response.result.links:
                    print('\t{}: {}\tCall Type: {}'.format(
                        link.rel, link.href, link.method))

                # To toggle print the whole body comment/uncomment the below line
                #json_data = self.object_to_json(response.result)
                #print "json_data: ", json.dumps(json_data, indent=4)

            return response
        except HttpError as httpe:
            # Handle server side API failure
            encoder = Encoder([Json()])
            error = encoder.deserialize_response(httpe.message, httpe.headers)
            print("Error: " + error["name"])
            print("Error message: " + error["message"])
            print("Information link: " + error["information_link"])
            print("Debug id: " + error["debug_id"])

        except IOError as ioe:
            #Handle cient side connection failures
            print(ioe.message)


def gpo(self):
    global payout_batch_id
    # create_response = GetPayouts().get_payouts(payout_batch_id,True)
    create_response = GetPayouts().get_payouts(True)
    return JsonResponse({"status": create_response})





class GetPayoutItem(PayPalClient):

    """ Retrieves the details of an individual Payout item provided the item_id"""
    def get_payout_item(self, payout_item_id, debug=False):
        request = PayoutsItemGetRequest(payout_item_id)

        try:
            response = self.client.execute(request)

            if debug:
                print("Status Code: ", response.status_code)
                print("Payout Item ID: " + response.result.payout_item_id)
                print("Payout Item Status: " + response.result.transaction_status)
                print("Links: ")
                for link in response.result.links:
                    print('\t{}: {}\tCall Type: {}'.format(
                        link.rel, link.href, link.method))

                # To toggle print the whole body comment/uncomment the below line
                #json_data = self.object_to_json(response.result)
                #print "json_data: ", json.dumps(json_data, indent=4)

            return response
        except HttpError as httpe:
            # Handle server side API failure
            encoder = Encoder([Json()])
            error = encoder.deserialize_response(httpe.message, httpe.headers)
            print("Error: " + error["name"])
            print("Error message: " + error["message"])
            print("Information link: " + error["information_link"])
            print("Debug id: " + error["debug_id"])

        except IOError as ioe:
            #Handle cient side connection failures
            print(ioe.message)

def pitmid(self):
    create_response = GetPayoutItem().get_payout_item(True)
    return JsonResponse({"status": create_response})





def paypal_payout(request):
    # create_response = CreatePayouts().create_payouts(True)
    # return JsonResponse({"status": create_response.status_code})
    amount = str('10.00')
    email = "sb-0kluk8294119@personal.example.com"
    body = {
        "sender_batch_header": {
            "recipient_type": "EMAIL",
            "email_message": "SDK payouts test txn",
            "note": "Enjoy your Payout!!",
            "sender_batch_id": "Test_SDK_1",
            "email_subject": "This is a test transaction from SDK"
        },
        "items": [{
            "note": "Your 1$ Payout!",
            "amount": {
                "currency": "USD",
                "value": amount
            },
            "receiver": email,
            "sender_item_id": "Test_txn_1"
        }]
    }
    payout_request = PayoutsPostRequest()
    payout_request.request_body(body)
    try:
        # Call API with your client and get a response for your call
        # response = client.execute(request)
        response = PayPalClient().client.execute(request)
        # If call returns body in response, you can get the deserialized version from the result attribute of the response
        batch_id = response.result.batch_header.payout_batch_id
        return JsonResponse ({"batch_id":batch_id})
    except HttpError as httpe:
        # Handle server side API failure
        encoder = Encoder([Json()])
        error = encoder.deserialize_response(httpe.message, httpe.headers)
        print("Error: " + error["name"])
        print("Error message: " + error["message"])
        print("Information link: " + error["information_link"])
        print("Debug id: " + error["debug_id"])
        print("Details: ")
        for detail in error["details"]:
            print("Error location: " + detail["location"])
            print("Error field: " + detail["field"])
            print("Error issue: " + detail["issue"])
    
    except IOError as ioe:
        # Handle cient side connection failures
        print(ioe.message)
    
    return JsonResponse({"status":"something is wrong"})



# class PayPalClient:
#     def __init__(self):
#         self.client_id = os.environ["PAYPAL_CLIENT_ID"] if 'PAYPAL_CLIENT_ID' in os.environ else "<<PAYPAL-CLIENT-ID>>"
#         self.client_secret = os.environ[
#             "PAYPAL_CLIENT_SECRET"] if 'PAYPAL_CLIENT_SECRET' in os.environ else "<<PAYPAL-CLIENT-SECRET>>"
#
#         """Setting up and Returns PayPal SDK environment with PayPal Access credentials.
#            For demo purpose, we are using SandboxEnvironment. In production this will be
#            LiveEnvironment."""
#         self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
#
#         """ Returns PayPal HTTP client instance with environment which has access
#             credentials context. This can be used invoke PayPal API's provided the
#             credentials have the access to do so. """
#         self.client = PayPalHttpClient(self.environment)
#
#     def object_to_json(self, json_data):
#         """
#         Function to print all json data in an organized readable manner
#         """
#         result = {}
#         if sys.version_info[0] < 3:
#             itr = json_data.__dict__.iteritems()
#         else:
#             itr = json_data.__dict__.items()
#         for key, value in itr:
#             # Skip internal attributes.
#             if key.startswith("__"):
#                 continue
#             result[key] = self.array_to_json_array(value) if isinstance(value, list) else \
#                 self.object_to_json(value) if not self.is_primittive(value) else \
#                     value
#         return result
#
#     def array_to_json_array(self, json_array):
#         result = []
#         if isinstance(json_array, list):
#             for item in json_array:
#                 result.append(self.object_to_json(item) if not self.is_primittive(item) \
#                                   else self.array_to_json_array(item) if isinstance(item, list) else item)
#         return result
#
#     def is_primittive(self, data):
#         return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)