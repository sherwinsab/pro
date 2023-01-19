from twilio.rest import Client
import os

def sendsms():
    account_sid = os.environ('ACbd373e62581246849c1d7d98f3f1f560')
    auth_token = os.environ('5ce15071bacc9cc0909ea8fc8813a44b')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                        body=f"HotWheels, Your New Car Has Arrived At The Showroom",
                                        from_='+14109364038',
                                        to='+917560893894'
                                    )

    print("Welldone")