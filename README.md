# Breanna Bisnott ECSE3038 Lab 4 Submission
### Would you rather?
Would you rather be gluten intolerant or allergic to seafood for the rest of your life? 

![gf bread](https://github.com/breannabisnott/ECSE3038_lab4/assets/158131996/bfd8b102-eeed-4703-b384-ce16fcac42b5)

The purpose of this code is for a lab assignment on building POST request handlers with FastAPI

## `get_profile()`
The server application allows a user to create only one user profile. The get request handler only ever returns a singular JSON object.

## `post_profile()`
Your server should allow for an incoming POST request that accepts a JSON body as described above. The structure of the JSON request should match the example illustrated by the "Example Request" in *fig.2.*  The server response should be structured as the the "Expected Response" in *[fig.2](https://www.notion.so/lab-959a3128adfb4ed99fcb5868d90a0f94?pvs=21).* 
The `last_updated` attribute should be generated by the web application and can be formatted any way you choose (it MUST include both date and time), as long as it reflects the time at the time of the request. The `last_updated` attribute should not be sent to the web application by the client.
(Here’s that really good idea I had) The profile’s `last_updated` attribute’s value should update every time the web application successfully handles a tank POST, PUT and DELETE request. The value should reflect the date and time that any of those three requests is successful.
**The route should also return status code that indicates that an object was successfully created.**

## `get_tank()`
This route returns a list of 0 or more objects. If a POST request was successfully made to the /tank route previously, the GET route should return an array of the POSTed tank object.

## `get_tank_id()`
This route returns a single JSON object of tank that is associated with the id passed as input in the route. If the API is unable to locate the object that has the id specified, the API  responds with an appropriate response message and status code.

## `post_tank()`
This route accepts a JSON object structured as depicted below. On success, the web application responds with the same JSON object that was posted with the addition of an `id` attribute. This `id` is to be generated by the API. 
The route also returns a status code that indicates that an object was **successfully created**.

## `patch_tank()`
The server allows a client to alter the parts of one of the tanks after it has been POSTed. The server allows the requester to make a JSON body with any combination of the three attributes and update them as necessary (The client is NOT allowed to edit the `id` attribute). 
The route also returns a status code that indicates that an object was **successfully altered**.
If the API is unable to locate the object that has the id specified, the API responds with an appropriate response message and status code.

## `delete_tank()`
The web application allows the client to delete any previously POSTed object. The web application does not send back any message to the client once the objects have been deleted. There is, however, a suitable status code that indicates **success** and that an **empty response is sent**.
If the API is unable to locate the object that has the id specified, the API responds with an appropriate response message and status code.

### This was exhausting & emotionally draining :D!
