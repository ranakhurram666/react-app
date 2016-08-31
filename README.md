**How to Run app(gif Zone):**
-----------------------------
In project directory run command: **python server.py**
to run the app.

**Functioalities of app(gif Zone):**
------------------------------------
**Front-end:** React, Bootstrap, css, HTML, jQuery

**Back-end:** Flask(Python)

**Summary:-**
-------------
	This is an app for gif images. In this app user can upload gif images from 2 sources
	and search image. More details are following.
	
**Description:-**
-----------------

1. User can Login and Signup.

2. User can upload gif images. Images will be uploaded from 2 sources.
	a. Local Machine  b. Online Url

3. Image uploaded from local machine will directly upload.
   And image through Url will be downloaded first and then will be
   upload to server.

4. One .png image will be made on server side
   by extracting 1st frame of original gif image.
   I used PIL(Python Image Library for that) for this purpose.

5. When user clicks on gif image, image will be stop(.png will be uploaded at that time).
   When user clicks again it will again start animating(.gif will be uploaded at that time).

6. User can search image by category, tags, description and
   title of image.

7. User can edit and delete images. 

8. User can Logout.
