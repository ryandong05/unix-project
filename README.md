# unix-project
Final project for Unix F24:
The goal of this project is to create a media player system on a Raspberry Pi that
streams Netflix through Kodi. When the user closes the Netflix session in Kodi, the
Raspberry Pi captures data about the watched content and sends it to a
Python-based machine learning script. This script uses a pre-trained
recommendation model to generate personalised movie recommendations based on
the user's viewing history. The recommendations are then sent to the user's email.
