<h1 id="top"> Package Routing Application </h1>

Python application for optimizing package delivery according to time and distance constraints.

<h1 id="index"> Index </h1>
 <ol type="i">
   <li><a href="#features">Application Features</a></li>
   <li><a href="#user_interface">User Interface</a></li>
   <li><a href="#delivery_constraints">Delivery Constraints</a></li>
   <li><a href="#notable_concepts">Notable Concepts Involved</a></li>
   <li><a href="#package_data">Package Input Data</a></li>
   <li><a href="#location_data">Location Data</a></li>
   <li><a href="#algorithm">Algorithm Overview</a></li>
   <li><a href="#results">Results</a></li>
 </ol> 
 
<h1 id="features"> Application Features </h1>
<p>
 <ul>
  <li>Graphical User interface that animates the delivery process.</li>
  <li>Console readout to provide narrative of each delivery step.</li>
  <li>User can check the status of package at a given time.</li>
  <li>User can add additional packages to any of the defined locations.</li>
  <li>Animations options can be adjusted to the user's preferences.</li>
 </ul>
 <br>
<p align="center">
 <a href="#top">Back To Top</a>
</p>

<h1 id="notable_conepts"> Notable Concepts </h1>
<p>
 <ul>
  <li>Space-time complexity is evaluated using Big O notation throughout the entire program (see code).</li>
  <li>A Greedy Algorithm was implemented for determining the next package delivery.</li>
  <li>A hash table was implemented for storing the packages.</li>
  <li>Tkinter was used to develop the GUI.</li>
 </ul>
 <br>
<p align="center">
 <a href="#top">Back To Top</a>
</p>

<h1 id="user_interface"> User Interface </h1>
<p align="center">
  <kbd>
    <img src="MediaFiles/Video.gif" width="600">
  </kbd>
  <br>
  The user interface animatings the delivery process. <br>
  It also allows the user to customize the package status checks, add additional packages, and toggle animation options. <br>
  The user interface was created using Tkinter.
  <br><br>
  <a href="#top">Back To Top</a>
  <br><br>
</p>

<h1 id="delivery_constraints"> Delivery Constraints and Assumptions </h1>
<p>
 <ul>
  <li>40 Packages must be delivered by the end of the day.</li>
  <li>2 trucks are available for delivery - they cannot travel more than a combined 140 miles.</li>
  <li>Each truck can only hold 16 packages.</li>
  <li>Each package has a destination that it must be delivered to and a deadline for when it must arrive by.</li>
  <li>Each location has a distance provided to each of the other possible locations available for delivery.</li>
  <li>Each truck drives an average of 18 miles per hour and spends no time loading or unloading packages.</li>
  <li>A package could be delayed, rerouted, or have other packages that it must travel with.</li>
 </ul>
 <br>
<p align="center">
 <a href="#top">Back To Top</a>
</p>

<h1 id="package_data"> Package Data </h1>
<p align="center">
  <kbd>
    <img src="MediaFiles/Packages.png" width = "1000">
  </kbd>
 <br>
  All the necessary package information is inputted into the program as the above .csv file.
  <br><br>
  <a href="#top">Back To Top</a>
</p>

<h1 id="location_data"> Location Data </h1>
<p align="center">
  <kbd>
    <img src="MediaFiles/Locations.png" width = "1000">
  </kbd>
 <br>
  All the necessary location information is inputted into the program as the above .csv file.
  <br><br>
  <a href="#top">Back To Top</a>
</p>

<h1 id="algorithm"> Algorithm / Delivery Walkthrough </h1>

 
 <strong> Delivery Process (Greedy Algorithm) </strong>
 <ol>
  <li>All packages with deadlines are loaded on to the first truck.</li>
  <li>If there is still room, packages going to the same destination as a loaded package gets loaded on the truck.</li>
  <li>The current truck location is then analyzed to determine the closest delivery location for a loaded package.</li>
  <li>The truck travels to the location and unloads the package (Steps 3 and 4 repeat).</li>
  <li>Once new packages with deadlines are available, the truck returns to the hub to load them.</li>
  <li>Truck 1 delivers all the remaining packages that it has loaded.</li>
  <li>Truck 2 begins loading all packages at the hub until it is full.</li>
  <li>It then uses the earlier described greedy algorithm to delivery its packages.</li>
  <li>When truck 2 is empty, it returns to the hub for more packages.</li>
  <li>Once all packages are delivered, the delivery process is complete.</li>
 </ol>
 <br>

<p align="center">
 <br>
  <strong> Truck 1 Delivery Route </strong>
  <br>
  <kbd>
    <img src="MediaFiles/Truck1.png" width = "600">
  </kbd>
 <br>
  The result of truck 1's delivery route can be seen above.
 <br>
 
 <p align="center">
 <br>
 <strong> Truck 2 Delivery Route </strong>
 <br>
 <kbd>
    <img src="MediaFiles/Truck2.png" width = "600">
  </kbd>
 <br>
 The result of truck 2's delivery route can be seen above.
 <br>
 
 <p align="center">
 <br>
 <strong> Status Report at 10:00 AM </strong>
 <br>
 <kbd>
    <img src="MediaFiles/Status_10AM.png" width = "600">
  </kbd>
 <br>
 The status of all packages at 10:00AM can be seen above.
 <br>
 
 <p align="center">
 <br>
 <strong> Status Report at 13:00 PM </strong>
 <br>
 <kbd>
    <img src="MediaFiles/Status_13PM.png" width = "600">
  </kbd>
 <br>
 The status of all packages at 13:00PM can be seen above.
 
  <br>
  <p align="center">
  <a href="#top">Back To Top</a>
</p>

<h1 id="results"> Results </h1>
<p>
All constraints are respected, and the total mileage at the end of the delivery process is 115 miles. For a complete narrative of each step of the delivery process, see the following link: 
</p>
<a href="MediaFiles/ConsoleOutput.txt">Delivery Application Console Output</a>
<br><br>
<p align="center">
 <a href="#top">Back To Top</a>
</p>
