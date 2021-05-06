# PROJECT NAME - SELSEY KITCHEN

This is the third Milestone Project undertaken as part of the course for the Full stack developer certification from Code Institute. The purpose is to build a build a full-stack site that allows users to manage a common dataset about a particular domain.


![](screenshots/responsive_image.PNG)

<a href="http://rk-selsey-kitchen.herokuapp.com/" target="_blank">Deployed project domain</a>

### UX - 
Selsey Kitchen is a recipe website for people interested in sharing recipes and getting inspired to try new recipes. It allows the user to add, delete and update a set of recipes and has a useful search option. The website also shared relevant news and blogs from other cooking websites in addition to promoting a range of premium kitchen knives for users and visitors.

### WIREFRAMES -

1. <a href="https://github.com/RoVsEk23/selsey_kitchen/blob/master/wireframes/desktop_wireframes.pdf" target="_blank">Desktop wireframe (Github link)</a>
2. <a href="https://github.com/RoVsEk23/selsey_kitchen/blob/master/wireframes/mobile_wireframes.pdf" target="_blank">Mobile wireframe (Github link)</a>

### TECHNOLOGY -

`Languages used -` 
HTML5, CSS3, jQuery, Python

`Frameworks, Libraries, Etc. -`
Gitpod, GIT, GitHub, Materialize, MongoDB, Flask, Jinja, Heroku,  Werkzeug, Mockplus

`Testing -`
Chrome DevTools,W3C Markup Validator, W3C CSS Validator, PEP8, JShint

### LAYOUT -

#### 1. DESKTOP

##### LANDING PAGE

<img src="screenshots/desktop_landing_page_1.PNG" width="300"> <img src="screenshots/desktop_landing_page_2.PNG" width="300"> <img src="screenshots/desktop_landing_page_3.PNG" width="300">

##### DASHBOARD, ADD RECIPES, UPDATE RECIPES

<img src="screenshots/desktop_dashboard.PNG" width="300"> <img src="screenshots/desktop_add_recipe.PNG" width="300"> <img src="screenshots/desktop_update_recipes.PNG" width="300">

##### MANAGE CATEGORIES, DELETE CONFIRMATION

<img src="screenshots/desktop_admin_manage_categories.PNG" width="300"> <img src="screenshots/desktop_delete_confirmation.PNG" width="300"> 


#### 2. MOBILE

##### LANDING PAGE

<img src="screenshots/mobile_landing_page_1.PNG" width="200"> <img src="screenshots/mobile_landing_page_2.PNG" width="200"> <img src="screenshots/mobile_landing_page_3.PNG" width="200"> <img src="screenshots/mobile_landing_page_4.PNG" width="200"> 

##### DASHBOARD, ADD RECIPES, UPDATE RECIPES

<img src="screenshots/mobile_dashboard.PNG" width="200"> <img src="screenshots/mobile_add_recipe.PNG" width="200"> <img src="screenshots/mobile_update_recipes.PNG" width="200"> 

##### MANAGE CATEGORIES, DELETE CONFIRMATION, LOG IN

<img src="screenshots/mobile_admin_manage_categories.PNG" width="200"> <img src="screenshots/mobile_delete_confirmation.PNG" width="200"> <img src="screenshots/mobile_log_in.PNG" width="200"> 


### DESIGN -

##### GENERAL FEATURES - 

1. I have tried to making the navigation simple and consistent throughtout the site.

2. I have tried to make the pages visually appealing.

3. Flash messages for every action that the user or admin does. Defensive programming by modal on delete actions.

4. The header provides easy navigation to various pages and also the drop down menu for mobile.

5. The footer has links to social media and my personal Github page.

##### PAGES - 

1. Header and footer remains the same throughout the site.

2. The landing page displays relevant articles followed by search and recipe cards. This is followed by a carousel display of products that the site owner wants to promote. The admin has been provided privilege to update or delete any recipe directly from the homepage. This feature is not provided to general users or visitors.

3. The register and log in pages has been kept simple and redirects to the user dashboard on creation or logging in.

4. The user dashboard is a collapsible popout of the various recipes that the user has uploaded. There are update and delete options on every recipe.

5. The add and update recipe forms are almost identical. The user has the option of not uploading an image to the recipe on the first time entry. A placeholder image will be used initially. But the user must upload an image if the intend to update the recipe. This functionality helps the user to update a recipe quickly even if they dont have an image handy to upload. But to maintain full access to the recipe they must upload an image.

6. The admin has a manage categories page available where categories can be added, edited, or deleted.


##### FEATURES TO ADD IN FUTURE - 

1. Pagination for recipes on home page and dashboard.

2. Recipe to open in a seperate page from the card layout.

3. Ability for User to delete their profile.

4. User profile form added to dashboard with relevant user information.


### TESTING -

#### 1. CODE VALIDATION

A. HTML VALIDATION

1. Parsing errors on all pages built with jinja templating.

B. CSS VALIDATION

<img src="screenshots/CSS_validator.PNG" width="1000"> 

C. GOOGLE MOBILE TEST

<img src="screenshots/Google_mobile_test.PNG" width="1000"> 

D. PEP8

<img src="screenshots/PEP8_python_validator.PNG" width="1000"> 














