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

Yield

Cluster Density

Clusters Passing Filter

Q30 Score

In addition the website records the following related run information:

Sequencing Chemistry

Sequencing Experiment


## UX

This site is designed to be used by laboratory technicians and clinical scientists working within the Molecular Diagnostics department. Laboratory technicians who set up the sequencing experiments will have standard user accounts and will be able to enter new run data and review previous run data for their own runs. Clinical scientists who analyse the sequencing data will have user accounts with admin privileges so will be able to review runs for multiple users and have a general overview of sequencing run performance.

There are three type of user with three different levels of access to the QC Metrics Analyser website:

#### Unregistered Users
Users of the site that don't have a user account can access an overview of sequencing run qc data on the homepage but cannot select, edit, add or delete run qc data. Run data can be accessed by clicking on one of the six modal image links. The first four modals display line charts for the four main qc metrics of yield, cluster density, clusters passing filter and q30 score. The data is plotted sequentially by run number (Pool No.). The last two modals display pie charts that divide run data into sequencing chemistry type or sequencing experiment type. Unregistered users can create an account using the sign up page. To create an account they must entering a unique username into the sign up form on the sign up page.

#### Registered Users
Users of the site that have created a user account can access their account using the login page. To login the user must entering their unique username into the login form on the login page. When successfully logged in the user view, filter, edit and delete their own run data.

#### Registered Users with Admin Privileges
Users of the site with a user account with admin privileges can access their account using the login page. To login the user must entering their unique username into the login form on the login page. Once successfully logged in they are given the choice to continue as a standard user or as a user which admin privileges. If they choose the later they are asked to verfiy their account by entering their email address. Once successfully logged in, users with admin privileges are able to view, filter, edit or delete run qc data for individual users. They are also able to view, edit or delete individual user accounts.


### User Requirements

User requirements for QC Metrics Analyser are:

1. It's easy and intuitive to use.
2. Unregistered users of the site can view a summary of qc metric data and can create a user account.
3. Registered users can login to view, filter, update, edit and delete their own data.
4. Registered users with admin privileges can view, filter, edit or delete user data.
5. Registered users with admin privileges can view, edit or delete user accounts.



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