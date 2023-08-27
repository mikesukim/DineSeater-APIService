# DineSeater APIService
This readme doc is in progress.

Please contact mikesungunkim@gmail.com for any inquiries.

## APIs
### POST DeviceTokenRegistration 
___
#### Description
Register FCM's Device_token to SNS for push notification.
#### Request
- header
 `Authorization : <id_token>` 
- url 
 `POST <lambda_host_domain>/<stage>/business/device_token_registration`
- body
  ```Json
   {"device_token" : "<device_token>"}
  ```
#### Response
```Json
 {"message" : "The incoming token has expired"}
```
```Json
 {"message" : "device_token is registered"}
```
## Contributing
TBA
## License
TBA
