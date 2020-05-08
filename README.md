<h1 id="top"> Package Routing Application </h1>

Python application for optimizing package delivery according to time and distance constraints.

<h1 id="index"> Index </h1>
 <ol type="i">
   <li><a href="#features">Features</a></li>
   <li><a href="#user_interface">User Interface</a></li>
   <li><a href="#delivery_constraints">Delivery Constraints</a></li>
   <li><a href="#package_data">Package Input Data</a></li>
   <li><a href="#location_data">Location Data</a></li>
   <li><a href="#algorithm">Algorithm Overview</a></li>
   <li><a href="#results">Results</a></li>
 </ol> 
 
<h1 id="features"> Features </h1>
<p>
 <ol>
  <li>Graphical User interface that animates the delivery process.</li>
  <li>Console readout to provide narrative of each delivery step.</li>
  <li>User can check the status of package at a given time.</li>
  <li>User can add additional packages to any of the defined locations.</li>
  <li>Animations options can be adjusted to the user's preferences.</li>
  <li>Space-time complexitiy is evaluated using Big O notation throughout the entire program (see code).</li>
 </ol>
 <br>
<p align="center">
 <a href="#top">Back To Top</a>
</p>

<h1 id="user_interface"> User Interface </h1><br>
<p align="center">
  <kbd>
    <img src="MediaFiles/Video.gif" width="600">
  </kbd>
  <br><br>
  The user interface animatings the delivery process. <br>
  It also allows the user to customize the package status checks, add additional packages, and toggle animation options. <br>
  The user interface was created using Tkinter.
  <br><br>
  <a href="#top">Back To Top</a>
  <br><br>
</p>

<h1 id="delivery_constraints"> Delivery Constraints and Assumptions </h1>
<p>
 <ol>
  <li>40 Packages must be delivered by the end of the day.</li>
  <li>2 trucks are available for delivery - they cannot travel more than a combined 140 miles.</li>
  <li>Each package has a destination that it must be delivered to and a deadline for when it must arrive by.</li>
  <li>Each location has a distance provided to each of the other possible locations available for delivery.</li>
  <li>Each truck drives an average of 18 miles per hour and spends no time loading or unloading packages.</li>
  <li>A package could be delayed, rerouted, or have other packages that it must travel with.</li>
 </ol>
 <br>
<p align="center">
 <a href="#top">Back To Top</a>
</p>

<h1 id="package_data"> Package Data </h1>
<p align="center">
  <kbd>
    <img src="MediaFiles/Packages.png" width = "1000">
  </kbd>
 <br><br>
  All the necessary package information is inputted into the program as the above .csv file.
  <br><br>
  <a href="#top">Back To Top</a>
</p>

<h1 id="location_data"> Location Data </h1>
<p align="center">
  <kbd>
    <img src="MediaFiles/Locations.png" width = "1000">
  </kbd>
 <br><br>
  All the necessary location information is inputted into the program as the above .csv file.
  <br><br>
  <a href="#top">Back To Top</a>
</p>

<h1 id="algorithm"> Algorithm / Delivery Walkthrough </h1>
<p align="center">
 <h2> Truck 1 Delivery Route </h2>
  <kbd>
    <img src="MediaFiles/Truck1.png" width = "600">
  </kbd>
 <br><br>
 The reports table view displays the number of each appointment type broken up by month. <br>
 Additional reports are available that show the schedule and total the number of hours for each consultant.
  <br><br>
 <h2> Truck 2 Delivery Route </h2>
 <kbd>
    <img src="MediaFiles/Truck2.png" width = "600">
  </kbd>
 <br><br>
 The reports table view displays the number of each appointment type broken up by month. <br>
 Additional reports are available that show the schedule and total the number of hours for each consultant.
  <br><br>
  <a href="#top">Back To Top</a>
</p>

<h1 id="results"> Results </h1>
<p>
 <br>
<p align="center">
 <a href="#top">Back To Top</a>
</p>
