<h1 align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/Pm0yBXj/qc-metrics-analyser.png" alt="qc metrics analyser title">
  </a>
</h1>

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/BjjcL0g/qc-metrics-image-links.png" alt="qc metrics analyser site">
  </a>
</div>

## Introduction

[QC Metrics Analyser](https://qc-metrics-analyser.herokuapp.com/) is a website that can be used by Next Generation Sequencing (NGS) users using Illumina's sequencing chemistries and instruments. The site has been primarily designed for employees of the Royal Marsden Hospital working within the Molecular Diagnostics department. The department uses Illumina's sequencing technologies to detect acquired genetic mutations in patients tumour samples. Patients found to have clinically actionable mutations can then be assigned to an appropriate clinical trial for treatment.

Each NGS sequencing run generates a set of 'Sequencing Metrics' which can be used to assess the quality of the sequencing data produced. These sequencing metrics are useful for QC purposes. Firstly to ensure the quality of individual runs remain high and secondly to monitor the performance of the sequencing instruments over time.

The website records and displays four types of QC metric data:

1. Yield - Shows the expected number of nucleotide bases sequenced for the run. Typically this is measured in gigabases.

2. Cluster Density - Shows the number of clusters detected for the sequencing run.

3. Clusters Passing Filter - Shows the percentage of clusters passing the signal purity filter.

4. Q30 Score  - Shows the percentage of bases that have a Q-score above or equal to 30; Q30 is a probability of incorrect base calling of 1 in 1000. A quality score, or Q-score, is a prediction of the probability of an incorrect base call. A higher Q-score implies that a base call is higher quality and more likely to be correct.

In addition the website records the following related run information:

1. Sequencing Chemistry - The type of chemistry used can be Mid150, Mid300 or High300. This effects the amount of sequencing that can be performed and therefore the expected yield.

2. Sequencing Experiment - The type of experiment performed can be Capture, Exome or Genome. This determines the amount of sequencing required and effects the type of chemistry used and therefore the expected yield.


## UX

This site is designed to be used by laboratory technicians and clinical scientists working within the Molecular Diagnostics department. Laboratory technicians who set up the sequencing experiments will have standard user accounts and will be able to enter new run data and review previous run data for their own runs. Clinical scientists who analyse the sequencing data will have user accounts with admin privileges so will be able to review runs for multiple users and have a general overview of sequencing run performance.

There are three type of user with three different levels of access to the QC Metrics Analyser website:

- Unregistered Users - Users of the site that don't have a user account, who can view run information on the homepage but cannot select, edit, add or delete run qc data.

- Registered Users - Users of the site that have created a user account page, who can view, filter, edit and delete their own run data.

- Registered Users with Admin Privileges - Users of the site with a user account with admin privileges, who are able to view, filter, edit or delete run qc data for other users. They are also able to view, edit or delete user accounts.


### User Requirements

The user requirements for QC Metrics Analyser are as follows:

- The site is easy and intuitive to use.

- The site provides basic information about NGS qc data for new users.

- The site has different levels of access/security depending on the users status which will be dependent on their training and job role.

- Unregistered users are able to view basic run information but not edit or delete it. They must be able to create a user account using the sign-in in page.

- Registered users must be able to use a unique user name to log into their user account. Once successfully logged in, the user must be able to view, filter, edit and delete their own run information.

- Registered users with admin privileges must be able to use a unique user name to log into their user account. Once logged in as a user they must be able to verify their admin status by using a unique email address. Once successfully logged in with admin privileges they must be able to view, filter, edit or delete run information for individual users. They must also be able to view, edit or delete individual user accounts.


### User Stories

As an unregistered user:

1. I want to be able to access the run qc data as easily as possible.

2. I want to be able to see an overview of the data for each type of qc metric.

3. I may not have a strong scientific in NGS sequencing and I may require additional information to help understand the qc metric data.

4. I may not be familiar with the layout of the site so it must be easy and intuitive to use.

5. I only want to be able to view the data. I don't want to be able to accidentally change or delete qc metric data.

6. I may be a new NGS user and need to create a user account so I can add, edit and delete my own run qc data.


As a registered user:

1. I want to be able to log in to my account as quickly and easily as possible.

2. I want to be able to see an overview of my own data for type of qc metric.

3. I want to be able to add new run qc data to the database.

4. I want to be able to edit or delete existing run qc data.

5. I only want to be able to access my own run qc data. I don't want to be able to access other users data or user account information.

6. I want to be able to filter my own data using specific criteria.

7. I want to be able to log out of my account quickly and easily when my session is over.


As a registered user with admin privileges:

1. I want to be able to log in to my account as quickly and easily as possible.

2. I want to be able to choose to log in as either a regular user or as a user with admin privileges.

3. I want confirmation that I have logged in with or without admin privileges.

4. I want to be able to choose to either edit run qc data or user accounts.

5. I want to be able to view, edit or delete run qc data for individual users.

6. I want to be able to filter run qc data for individual users according to  specific criteria.

7. I want to be able to edit or delete user accounts for individual users.

8. I want to be able to log out of my account quickly and easily when my session is over.


As a NHS organisation:

1. I want the run qc data to be stored securely.

2. I want there to be different levels of access to the sites database to ensure only staff with the appropriate training can perform the appropriate tasks.

3. I want registered users to have unique identifiers so there is traceability.

4. I want users with admin privileges to have additional security measures (login with email).

5. I want users with admin privileges to be able to edit/delete user run information and user accounts to ensure the database remains up-to-date and accurate.


### Wireframes

Wireframes for this project were created using [Balsamiq](https://balsamiq.com/) and can be found [here](https://github.com/TAHJones/qc-metrics-analyser/tree/master/wireframes).

#### Site Layout on Desktop, Tablet & Mobile Devices

The layout of most pages of the site are similar for mobile, tablet and desktop devices. However the main homepage and individual users homepage which display the run qc data do have some significant layout changes between desktop/tablet and mobile screen sizes.

Desktop or Tablet Layout:

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/LzVwPTH/homepage.png" alt="desktop and tablet layout">
  </a>
</div>
<br>

On the desktop or tablet layout both the modal image-links are arranged in pairs. The first section contains four modal links for line charts and the second section contains two modal links for pie charts.

Mobile Layout:

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/vYPsS2Z/homepage-mobile.png" alt="mobile layout">
  </a>
</div>
<br>

On mobile layout each modal image-links to stacked individually on top of each other. The navbar changes into a collapsible dropdown menu which is displayed by clicking the hamburger icon.


### How to Use the QC Metrics Analyser Website

#### Using the Site as an Unregistered User

##### Step 1 - Viewing Sequencing Run QC Data
On the homepage unregistered users can see an overview of qc metric data by clicking on one of the six modal image-links on the page.

1. Viewing Linechart Data - A line-chart for yield, cluster density, clusters passing filter and Q30 score can be displayed by clicking on one of the four modal image-links in the 'Sequencing Run Metrics' section.

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/PGgvn1v/select-image-link-modal.png" alt="selecting linechart modal image link">
  </a>
</div>
<br>

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/mGYNM0P/linechart-modal.png" alt="linechart modal">
  </a>
</div>
<br>

2. Viewing Piechart Data - A pie-chart for sequencing chemistry or sequencing experiment can be displayed by clicking on one of the two modal image-links in the 'Other Sequencing Metrics' section.

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/q14GGZT/select-image-link-modal-2.png" alt="selecting piechart modal image link">
  </a>
</div>
<br>

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/wshGt5T/piechart-modal.png" alt="piechart modal">
  </a>
</div>
<br>

##### Step2 - Creating a User Account
Unregistered users can access the sign-up page by clicking on the green 'Sign Up' button located on the right of the header or footer navbar. On the sign-up page unregistered users can create an account by entering a unique username into the sign up form then clicking on the green 'Sign Up' form button. If the selected username already exists the following warning message will be displayed; "username 'selected username' already exists, enter a unique username or login".

#### Using the Site as a Registered User

##### Step 1 - Logging into a User Account
On the homepage registered users can access the log-in page by clicking on the blue 'Login' button located on the right of the header or footer navbar. On the log-in page registered users can access their account by entering their unique username into the login form on the login page. When successfully logged in the user is directed to the user homepage.

##### Step 2 - Viewing User Run QC Data
On the user homepage registered users can see an overview of their own qc metric data by clicking on one of the six modal image-links on the page. A line-chart for yield, cluster density, clusters passing filter and Q30 score can be displayed by clicking on one of the four modal image-links in the 'Sequencing Run Metrics' section. A pie-chart for sequencing chemistry or sequencing experiment can be displayed by clicking on one of the two modal image-links in the 'Other Sequencing Metrics' section.

##### Step 3 - Adding New Run QC Data
Once successfully logged in the user can add a new sequencing run data by clicking on the 'Add Run' link If any of the fields are left empty the submission will fail and the message 'Please fill in this field' will appear below the first empty field encountered.. On the add-run page the user can add new run data into the Add-New-Run form and submit it to the database by clicking on the yellow 'Add Run' form button. If any of the fields are left empty the submission will fail and the message 'Please fill in this field' will appear below the first empty field encountered.

##### Step 4 - Managing Existing User Run QC Data
Once successfully logged in the user can manage their existing run qc data by clicking on the 'Manage Runs' link located on the header or footer navbar.

1. Selecting a Run - On the manage-runs page the user can either select an individual run directly from the dropdown menu then click on the blue 'Select' button or filter a group of runs using the series of dropdown menus provided then click on the blue 'Filter Runs' button.

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/vjKJfz3/manage-runs-1.png" alt="selecting run">
  </a>
</div>
<br>

2. Viewing Filtered Runs - If the user chooses to filter run data then a filtered list of runs will be displayed. The user must then select one run from the list using the dropdown list provided.

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/Wz2nNQV/manage-runs-2.png" alt="viewing filterd runs">
  </a>
</div>
<br>

2. Viewing Selected Run - Once an individual run has been selected the runs pool number, yield, cluster density, pass filter value, Q30 score, chemistry and experiment type will all be displayed on the page. The user will now have the option to delete or update the selected run.

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/3T9yzGc/manage-runs-3.png" alt="viewing selected run">
  </a>
</div>
<br>

3. Deleting Selected Run - Once an individual run has been selected click on the red 'Delete' button that appears at the bottom of the page. On the delete-run page the selected run is displayed as a list along with a yes/no check box to confirm the deletion of the run. Once the user has selected 'yes' they can delete the run from the database by clicking on the red 'Delete' button. If the user clicks on the 'Delete' button without slecting the 'yes' checkbox first the following message is displayed; "To delete Pool_XXX select Yes then click Delete". Once the run has been successfully deleted the following message will be displayed; "Pool_XXX has been successfully deleted".

4. Updating Selected Run - Once an individual run has been selected click on the yellow 'Update' button that appears at the bottom of the page. On the update-run page the selected run data is displayed in the update-run form. The data in each form field can be edited and these changes can be saved to the database by clicking on the yellow 'Update' button beneath the form. Once the run has been successfully updated the following message will be displayed; "Pool_XXX has been successfully updated". If any of the fields are left empty the submission will fail and the message 'Please fill in this field' will appear below the first empty field encountered.

##### Step 5 - Ending User Session
When the user wants to end their session they can click on the blue 'Logout' button located on the right of the header or footer navbar. This directs the user to the logout page which informs the user that they have successfully logged out and provides a link to return to the sites main homepage.

#### Using the Site as a Registered User with Admin Privileges

##### Step 1 - Logging into an Admin Account
On the homepage registered users can access the log-in page by clicking on the blue 'Login' button located on the right of the header or footer navbar. On the log-in page registered users can access their account by entering their unique username into the login form on the login page. If the user has admin privileges they are directed to the admin-or-user page where they can choose to continue as either a regular user or as an admin-user. If the later option is chosen then the user is prompted to provide their email address as further confirmation of their identity. Once successfully logged the admin-user is directed to the admin page where they can choose to manage user run data or manage user accounts.

##### Step 2 - Managing User Run Data as Admin-User
1. Selecting User Runs - On the manage-user-runs page the admin user can either select all the runs for an individual user by using the default filter run settings and then selecting a user from the dropdown menu. Alternatively they can adjust the filter run settings to select the type of runs displayed, then select a user from the dropdown menu. Once the appropriate settings have been made the run data can be displayed by clicking on the blue 'Select' button.

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/D76Fhps/manage-user-runs-1.png" alt="selecting user runs">
  </a>
</div>
<br>


2. Viewing User Runs - The selected user runs (filtered or unfiltered) are displayed as a list. The pool number, yield, cluster density, pass filter value and Q30 score is displayed for each run. The admin-user must select one run from the list using the dropdown list provided and clicking on the blue 'Select' button.

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/0j0pntR/manage-user-runs-2.png" alt="viewing user runs">
    <img src="https://i.ibb.co/P4z4Yd9/manage-user-runs-2.png" alt="viewing user runs">
  </a>
</div>
<br>

3. Viewing Selected User Run - Once an individual user run has been selected the runs pool number, yield, cluster density, pass filter value, Q30 score, chemistry and experiment type will all be displayed on the page. The admin-user will now have the option to delete or update the selected run.

<div align="center">
  <a href="https://qc-metrics-analyser.herokuapp.com/" target="_blank">
    <img src="https://i.ibb.co/prXbR2K/manage-user-runs-3.png" alt="viewing selected run">
  </a>
</div>
<br>

4. Deleting Selected Run - Once an individual user run has been selected click on the red 'Delete' button that appears at the bottom of the page. On the delete-run page the selected user run is displayed as a list along with a yes/no check box to confirm the deletion of the run. Once 'yes' has been selected the run can be deleted from the database by clicking on the red 'Delete' button. If the 'Delete' button is clicked without selecting the 'yes' checkbox first the following message is displayed; "To delete Pool_XXX select Yes then click Delete". Once the run has been successfully deleted the following message will be displayed; "Pool_XXX has been successfully deleted".

5. Updating Selected User Run - Once an individual user run has been selected click on the yellow 'Update' button that appears at the bottom of the page. On the update-run page the selected user run data is displayed in the update-run form. The data in each form field can be edited and these changes can be saved to the database by clicking on the yellow 'Update' button beneath the form. Once the run has been successfully updated the following message will be displayed; "Pool_XXX has been successfully updated". If any of the fields are left empty the submission will fail and the message 'Please fill in this field' will appear below the first empty field encountered.

##### Step 3 - Managing User Accounts as Admin-User
1. Selecting a User Account - On the select-user page the admin user can select a user account by selecting a username from the dropdown menu then clicking on the blue 'select' button.

2. Viewing Selected User Account - Once an individual user account has been selected the users name, membership status, date joined and time joined are displayed on the page. The admin-user will now have the option to delete or update the selected user account.

3. Deleting Selected User Account - Once a user account has been selected click on the red 'Delete' button that appears at the bottom of the page. On the delete-user page the selected user run is displayed as a list along with a yes/no check box to confirm the deletion of the user. Once 'yes' has been selected the user can be deleted from the database by clicking on the red 'Delete' button. If the 'Delete' button is clicked without selecting the 'yes' checkbox first the following message is displayed; "To delete user account for 'selected user' select Yes then click Delete". Once the user has been successfully deleted the following message will be displayed; "User account for 'selected user' has been successfully deleted".

4. Updating Selected User Account - Once an individual user account has been selected click on the yellow 'Update' button that appears at the bottom of the page. On the update-run page the selected user information is displayed in the update-run form. The data in each form field can be edited and these changes can be saved to the database by clicking on the yellow 'Update' button beneath the form. Once the user information has been successfully updated the following message will be displayed; "User account for 'selected user' has been successfully updated". If any of the fields are left empty the submission will fail and the message 'Please fill in this field' will appear below the first empty field encountered.

##### Step 4 - Ending Admin-User Session
When the admin-user wants to end their session they can click on the blue 'Logout' button located on the right of the header or footer navbar. This directs the admin-user to the logout page which informs the user that they have successfully logged out and provides a link to return to the sites main homepage.

## Technologies Used

- HTML
- CSS
- Javascript
- [Bootstrap](https://getbootstrap.com/docs/)
- [Chart.js](https://www.chartjs.org/)
- [mongoDB](https://www.mongodb.com/)
- Python
- [Flask](https://palletsprojects.com/p/flask/)
- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)

## Testing

Information regarding testing can be found in separate [testing.md](https://github.com/TAHJones/qc-metrics-analyser/tree/master/testing/testing.md) file.

## Deployment

Still to be added...

## Credits

### Content

Data used during the creation of this site was artifical so as not to breach NHS information governance rules.

### Media

Images were obtained from:
- [Vecteezy](https://www.vecteezy.com/)

Images were edited using [GIMP](https://www.gimp.org/).

The color scheme was inspired by the NHS logo. It is intended to create a cool scientific / clinical feel.

## Acknowledgements

- The project is inspired by the site creators day job, where he saw a need for an easy way for sequencing users to record, organise and review the qc data generated for NGS sequencing runs.

- Special thanks to my Code Institute Mentor [Simen Daehlin](https://github.com/eventyret) for his coding expertise, patience and generosity with his time.