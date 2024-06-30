# Heron Data with Streamlit

Heron Data has expanded its features! This service is hosted by Streamlit cloud service to calculate and transform area under curve data for mass spectrometrists. Once a Skyline CSV is uploaded with raw area under the curve data, this python script will transform the data into pivot tables and then display a `Download` button for a xlsx file complete with Pie Charts. 

# How To Run Locally

Make sure you have python3 installed. Then, install [streamlit here](https://streamlit.io/). Then, clone repo and run the following command in the terminal `streamlit run heron_auc_home.py`


# Additional Links
This is sub-service of the `herondata.app` which can be found at this [github repo](https://github.com/Step-henC/heron-data-internet)

# Future Steps

Eventually this code will be refactored into a Django project and launched on Vercel. Doing so will allow me to use Vercel as a reverse proxy and host this project (that will be a Django project) within a subdirectory of the home project at herondata.app. As oppose to two separate websites, as it is currently.

Also, it will be ideal to include Selenium tests and dockerize this project for those without local python installation. Pending future funding.