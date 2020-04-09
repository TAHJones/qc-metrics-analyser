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

To deploy Avengers Top Trumps to GitHub Pages from its [GitHub repository](https://github.com/TAHJones/avengers-top-trumps) do the following:

1. Log into GitHub.
2. From the list of repositories on the screen, select **avengers-top-trumps**.
3. Alternatively select **Repositories** from the menu items at the top of the page, then select **avengers-top-trumps**.
4. From the menu items at the top of the page, select **Settings**.
5. Scroll down to the **GitHub Pages** section.
6. Under **Source** click on the drop-down menu and select **Master Branch**.
7. On selecting Master Branch the page is automatically refreshed, Avengers Top Trumps is now deployed.
8. In the **GitHub Pages** section the URL for the deployed website will now be available.

To clone Avengers Top Trumps from its [GitHub repository](https://github.com/TAHJones/avengers-top-trumps) and run on your local environment do the following:

1. Follow this link to the Avengers Top Trumps [GitHub repository](https://github.com/TAHJones/avengers-top-trumps).
2. Under the repository name, click "Clone or download".
3. In the **Clone with HTTPs** pop up window, copy the URL address for the Avengers Top Trumps repository.
4. In your local IDE open your preferred terminal.
5. Navigate to the location where the cloned repository will be downloaded.
6. Type ```git clone``` followed by the Avengers Top Trumps URL address as follows:

```
git clone https://github.com/TAHJones/avengers-top-trumps
```

7. Press Enter and the cloned repository will be created.

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