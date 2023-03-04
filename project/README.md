# eBike Booking
#### Video Demo:  https://www.youtube.com/watch?v=8NaNPrb6_QI
#### Description:

###### Intro

This is a webapp for a school that offer students to rent ebikes during the week. It is designed to be as easy as possible
for the students to use, as well as easy to maintain regarding any issues with the bikes. Every user has an account that allows you to
book bikes and keep track of current and recent bookings. It also features an admin account that also have an admin page with an overview over
all bookings and reports made by users.

The webapp is made using flask in python alongside html, SQL and CSS. The different pages has their own function in the application.py and is easily sorted alphabeticlly. The HTML pages uses a standard layout in which they all extend with their different content. SQL is used to store date and records of bookings, users and reports.

###### Application

To achive fast and easy booking I figured there has to be an account system. Therefor the page requires a login to work. I used the login function from problem set 9. I did the same for the registration page, but added some extra features. First of all, there are more inputs such as name and mail. The mail has to be from the given distributer and it also have to be included in a csv file thats in the static folder. This is meant to be the list of all students and emplyees mails that has been given to them respectivly. One does not get to register if you dont have a valid mail in the list.

Once logged in you get to the index page where the current week is shown. Since the system is designed to be low maintanance and self driven, the currrent week is automaticilly updated useing the datetime library. The index function the queries for the status of the bikes and sends it to the html file that generates the grid with clickable boxes. These boxes are design to get an easy overview of which bikes are availeble and not, and on which day. If it is available it is green and clickable, if not, it is red and not clickable.

If you want to book a bike, simply click on the button that represent the day and bike you would like. This takes you to the confirmation page where you are asked if you would like to book the bike at the given date. The function uses one of the helpers function to return the correct date given the day of booking. You will also have the possibility to cancel the confirmation and it will not be booked. When confirmed, you will be put back to the main page and can now see that the button for the day and bike you just booked is red.

In the profile tab, accesible on the top bar, you will have an overview of the current active bookings. Active bookings are simply bookings coming up. Further, there is a table that shows yor history of bookings. And lastly, some statistics of your bookings and the ability to change password on the account. The avtive bookings, historical bookings and statistics are all generated in html with date from flask which are queried through SQL. Using "SELECT .... FROM bookings WHERE userid = ...." and COUNT. Simple queries that gets the job done.

Users also have the possibility to report issues with their bikes. Lets say the chain is loose or lacks grease, you will be able to click the "report issue" button on the top right corner. Then you will have to select the bike and write a short description of what the issue is. When done you click submit and the report will be sent to an admin.

Hardcoded in the script, there is an admin user that will also access the admin page. If regular users try to access this page they wil automaticlly be redirected to the index page, or login page if not logged in. On this page you will have access to all the bookings, you will see who booked when and which bike. This is to give the responsible an overview and control over the renting of bikes. They will also have access to all the reports that are in the database. Those reports will be queried for and given to the html file so that all are shown. If the admin sees that the report reports an issue that takes the bike out of operation, there is a button to deactivate/activate the bike. If deactivated, the status in the datebase will be switched for the given bike and it will no longer be available for booking on the main page -> all buttons will be and stay red untill activated again by the admin.

To log out you simply click the log out button and you will be returned to the login page and session is cleared.

###### Database

To store the information about users, bookings, bike status and reports, I used a local file SQL database. The database consists of four tables that are linked together via primary and foreign keys. Users is the table where accounts are stored, it contains values from each of the paramater promted on registration as well as an account id. This id is a primary key that links the account to bookings and reports. Booking is a table with records of all the bookings made. Every bookings has its uniqe booking ID which is also the primary key. It also contains the user id of the user who did the booking, the bike id of which bike was booked as well as day, week, month, year and time. Bookings links to users with the user id key.

Reports is a table thats stores all the issues reported. It has a uniqe report id for each new report as well as user id of the user submitting the report and bike id of the bike concerning the issue. There is also text message that is the description sent in by the user. Furthermore there is just date and time for when the report was submitted.

Lastly there is a bike table where each bike has a status and an id. This table is linked up to every other table via the bike id key. This is mainly to handle the status and availability of the bikes. But also to give information to the other tables that may have use for the status.

###### HTML pages

The HTML pages ueses a standard layout that every other HTML file extends. There is one extension of the title of the page and one for the main contents of the page. The bar is either the logged in version or the not logged in version. In each case showing different options on the top bar. The design of the page is very easy and uses the Bootstrap extension which is quite easy to use. Most of the HTML files uses input given from the python functions to generate tables with information. All data is queried in the function and then sent to html file to iterate over to make tables of wanted content.
