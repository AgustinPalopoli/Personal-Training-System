# Distinctiveness and Complexity
I think the webpage is considered to satisfy the distinctiveness and complexity requirements for several reasons. Firstly, its design incorporates a unique and visually appealing layout using a minimalist approach. In every css file there is a code that assures mobile-responsive style.

Additionally, the webpage demonstrates the use of a variety of models and many functions in the back-end that allow the differents types of users to make many things. Admins are able to assign routines to user and they are able to see them and save information about the weights quantity.In the other hand JavaScript its used in the frond-end side of the users so they have a dinamic experience.

In summary, the webpage's unique design, coupled with its comprehensive content and advanced functionality, fulfills the distinctiveness and complexity requirements. It aims to leave a lasting and fun impression on users while offering a user-friendly gym experience.

# Content

**Functions**
- Create accounts with permissions
- Register, login and logout
- In case of forgoting the password the user can change it with a mail that will be sent to their email
- Permission decorator in views to avoid cross url access
- Admin accounts can do the following:
  - List, add, modify and delete a exercise (it conisist in a type, muscle, name, set, repetitions, rest, weight, image)
  - List, add, modify and delete a routine (it conisist in a name, type of the user who will see it, which biological sex is it directed to)
  - List, add, delete, modify the password, change from a free account to a preimun and the saved weight of a user
  - Upload a txt file fill with phrase
  - List, add, delete and modify a "chalkboard" (in the chalkboard the admin assigns a user 5 routines and a message with a personal sentence or a random phrase)
- Premiun user accounts can do the following:
  - In the index they can see they personal 5 routines (next to random images generated with ia) and the message
  - See all the exercises of a routine and do progressively the exercise (you can make a set, click the rest button and a countdown appears when it finishes its add 1 to the counter of set. When you finish all the exercises a message appears). See the weight the user lift (blank if its equal to none) and if you click a input field with a save button will apear so you can change the ammount of weight. Click a button to load the image of the exercise.
  - See all the exercises that use weights and a input field with the ammount the user lift (blank if its equal to none)
  - See stretching exercises
- Free user accounts can do the following:
  - In the index they can see pre-load routines (next to random images generated with ia)
  - See all the exercises of a routine and do progressively the exercise (you can make a set, click the rest button and a countdown appears when it finishes its add 1 to the counter of set. When you finish all the exercises a message appears). Click a button to load the image of the exercise.
  - See the benefits of becoming Premiun and how to contact the staff
  
**Style**
- Inicio contains all the static files for the index page
- css contains all the css files
- imagenes contains all the images of the exercises
- imageDesign contains all the images for the design
- js contains the js needed in the user side
- sonido contains the sound that plays when a rest end or the last exercise its finished
  
**Templatetags**
- Contains a python file that have two filter for the templates. One give a random int to select a random image of desing. The other retunr a bool value if a time is equal to 0:00:00
  
**Template**
- base_ templates contains the base that will be extended in the rest of the templates
- admin_  templates contains all the templates used in the admin side
- inicio is the index template
- iniciar_sesion is the log in template
- redireccion is a template that redirect the user depending on the rol
- resetear_ templates contains all the templates used when you are changing your password
- usuario_ templates contains all the templates used in the premiun user side
- usuario_g_ templates contains all the templates used in the free user side

# How to run the application

1. This aplication use postgre so it need the appropriate connection
2. Put a email in settings.py in the variable EMAIL_HOST_USER
3. In that email get a password for an app and paste it in EMAIL_HOST_PASSWORD
4. Create a super user
5. Log in as normal and create an admin account

# Additional information

This webpage was develop for a personal trainer and he is going to use it for work.

Sorry for my poor english. I learned how to have a conversation about the weather but they didnt teach me how to explain code in english. Also sorry about the video I couldnt show all the functions of the webpage in it.