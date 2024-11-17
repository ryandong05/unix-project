# Netflix Kodi Media Center Software
Creating a media player that streams Netflix through a home theater platform and sends personalized recommendations to user's email based on their viweing history.

## Table of Contents
- About the Project
- System Functionality
- Features
- Installation
- Usage
- Contributing
- License
- Contact

## About the Project
The goal of this project is to design and implement a media player system using a Raspberry Pi to
streams Netflix through Kodi. When the user closes the Netflix session in Kodi, the
Raspberry Pi captures data about the watched content and sends it to a
Python-based machine learning script. This script uses a pre-trained
recommendation model to generate personalized movie recommendations based on
the user's viewing history. These recommendations are sent directly to the user via email, providing a seamless entertainement experience. The project will be presentated by two students and demonstrated on a Rasperry Pi running Kodi with the Netflix add-on. During the presentation, Netflix content will be streamed via Kodi. Once the user stops their session, the recommendation model, running through a python script, will be triggered on the Raspberry Pi, and a sample email containning recommended movies will be sent to the user's inbox. 

## System Functionality 

**1. Netflix streaming via Kodi** 

The Raspberry Pi is configured as a multimedia streaming device using Kodi, a popular open-source media center application. Kodi serves as the interface for accessing and playing Netflix content. Users can browse, select, and stream their favorite movies or TV shows directly on their Raspberry Pi-powered media player.

**2. Data Collection on Session Close**

Once the user finishes watching their Netflix content and exits their streaming session within Kodi, the Raspberry Pi initiates a process to capture viewing data. This data includes:

* Movie or TV show title
* Genre(s)
* Durattion watched (partial or full viewing)
* Date and time of viewing

This will be done either through Kodi's API or a custom plugin. The system will detect when the user finishes a Netflix session, triggering the recommendation process.

**3. Machine Learning Recommendations Model**
The system utilizes a Python-based machine learning script that employs a pre-trained recommendation model stored on the
Raspberry Pi. This model will generates recommendations by analyzing the user's viewing history/data and
is optimized to run efficiently on the Raspberry Pi’s limited resources. The recommendation model is designed to adapt over time, providing increasingly personalized suggestions as the user's viewing patterns evolve.

**4. Email Integration**
A Python script will use *smtplib* or an email service like
SendGrid to send the generated recommendations to the user’s email address. Once the recommendation are created, the system automatically compiles them into a structured and easy-to-use format. The email includes:

* A brief list of top recommended movies or shows.
* Descriptions, genres, and duration  of each recommendation.
* Links for quick access to the content.

## Features
**1. Streaming Capabilities**
* Smooth playback of Netflix content on Kodi with Raspberry Pi as the hardware platform
* Kodi interface for browsing and selecting content

**2. Data Capture**
* Automated detection and collection of viewing history upon session closure
* Reliable storage of metadata for analysis

**3. Personalized Recommendations**
* Machine learning-driven recommendations tailored to the user's preferences
* Dynamic adaptation to changing tastes (like genres) and new data

**4. Email Integration**
* Automated email delivery of recommendation to the user
* Clear and accessible email format

## Installation

**1. Clone the repository**

run the command :

git clone https://github.com/ryandong05/unix-project.git

**2. Navigate to the project directory**

run the command :

    cd unix-project

**3. Install dependencies:**

run the command :

    npm install

or

    pip install -r requirements.txt

**4. Run the project**

run the command :

    npm start

or

    python app.py

## Usage

**1. Selecting a Movie or TV Show**  

 Users can effortlessly browse or search for their desired movies or TV shows. Once a selection is made, the system ensures a smooth playback experience, allowing users to fully immerse themselves and enjoy their chosen content.

**2. Personal Entertainement Systems**

The system serves as a compact home media player, offering personalized recommendations. Users can easily search for movies or TV shows that pique their interest, enchancing their entertainment experience.

**3. Data-Driven Content Discovery**

User benefit from AI-powered insights into their preferences, enabling them to discover hidden gems and new releases that aligns with their tastes.

**4. Flexibible Environment**

The system can be customized for different environments, making it suitable for multi-user setups such as families or individual use.

## Contributing
Guidelines for contributing to the project:

* Fork the repositery
* Create a new branch for your feature:

        git checkout - b feature /new-feature

* Commit your changes:

        git commit -m "Add new feature"

* Push to the branch:

        git push origin feature/new-feature

* Submit a pull request

## License 
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

* Project Maintainer: Ryan Dong & Yakin Succès
* Email: [ryan insert ya email] & yakinsucces24@gmail.com
* Github: ryandong05 & YakinSucces



