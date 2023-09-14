# National UFO Reporting Center (NUFORC) Sighting Tool

## NUFORC Overview
According to their website, "the National UFO Reporting Center was founded in 1974 by noted UFO investigator Robert J. Gribble. The Center’s primary function over the past five decades has been to receive, record, and to the greatest degree possible, corroborate and document reports from individuals who have been witness to unusual, possibly UFO-related events.  Throughout its history, the Center has processed over 170,000 reports, and has distributed its information to thousands of individuals" (https://nuforc.org/about-us/).

## NUFORC UFO Sighting Tool Overview
This tool was created for the purpose of pulling back UFO sighting data from the NUFORC datatables provided at _https://nuforc.org/databank/_ from the past 6 months. This tool pulls back relevant information, such as sighting date, location, shape, and summary. 

## NUFORC UFO Sighting Tool Technology Stack
This project uses Python, Flask, HTML, and CSS to create an HTML template that displays the JSON object with the past 6 months of sighting data.

## Run the Project
To run the project, <a href="https://www.python.org/downloads/">Python</a> and <a href="https://flask.palletsprojects.com/en/2.3.x/installation/">Flask</a> will need to be downloaded and installed.

To start the project, complete the following:
  1. Clone the project
    ```shell
      git clone https://github.com/BrittanyClarke/ufo-sighting.git
    ```
  2. Navigate to the project's main directory
    ```shell
      cd ufo-sighting/
    ```
  3. Run the project with Flask
    ```shell
      flask --app ufo-sight run
    ```
  4. Navigate to http://127.0.0.1:5000/ on your browser
  5. Voilà! View UFO sighting from the past 6 months in a JSON object. For more specific filters, please see the _Routes_ section below

## Routes
This application has 3 routes, and they are as follows:
  - /
    - Example usage: http://127.0.0.1:5000/ will display all sightings from the past 6 months
  - /date
    - This route takes a date as a ddmmyyy-formatted parameter
    - Example usage: http://127.0.0.1:5000/date?ddmmyyyy=09022023 will display all sightings from the date of 09/02/2023
  - /location
      - This route takes a country as a location parameter
      - Example usage: http://127.0.0.1:5000/location?country=USA will display all sightings from the USA
