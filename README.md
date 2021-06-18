# Alexa-base-CRM
- Alexa-based CRM. CRM stands for customer relationship management. It helps you manage and maintain customer relationships, track sales leads, marketing, and pipeline, and deliver actionable data and all these functions will manage through Alexa by giving voice over commands.
- Amazon S3 Bucket:- An Amazon S3 bucket is a public cloud storage resource available in Amazon Web Services' (AWS) Simple Storage Service (S3), an object storage offering. Upload lambda function on Amazon S3 bucket, copy the object url from your Amazon S3 bucket and paste it to lambda function.
- Choose compatile programming language for your lambda function and insert suitable API's in different intent handlers as per requirement. 
- In order to use custom libraries in your lambda function you need to place folder of those custom libraries in the root folder of the zip and upload the zip into your Amazon S3 bucket.
- You need to keep lambda_function.py in your root folder of the zip file.
- Queries which you can ask Alexa
- 1. User : Alexa, open CRM management.
- 2. User : Alexa, fetch me details of product {product_name} 
-Alexa will fetch all the details related to the product that you requested.
- 3. User : Alexa, add product {product_name} with  {product_price} and {product_unit} unit.
-Alexa will add product to your CRM.
- 4. User : Alexa, list the activities associated with {person_name}
-Alexa will fetch the list of activities which is related to the particular customer.
- 5. User : Alexa, add a person with {person_name}  {person_phone_number} and {person_email}
-Alexa can add person/customer to your CRM.
- 6. User : Alexa, add deal with {deal_title} and worth {deal_value}
-Alexa can add deal of organization with some other organization with title and value. 
- 7. User : fetch me details of deal {deal_name}
-Alexa can fetch you the details of particular deal which you want
- 8. User : Alexa, delete {deal_name} deal
-Alexa will delete the particular deal.
- 9. User : Alexa, i want to delete {name} record
-If person is no longer your organization custumer you can simply delete the record the customer from CRM.
- 10. User : Alexa, i want to delete {dealname} deal
-If the deal of the organization is over you can delete deal from your CRM y simply giving voice based commands to Alexa.
- 11. User : Alexa, details of recent assigned activity of user {name}.
-Alexa can fetch you the activities which is assigned to the particular user.

