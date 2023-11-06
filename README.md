# Live Chat ETL Project 🔴💭

This GitHub repository hosts the code for a live chat ETL (Extract, Transform, Load) project for my Iron Hack's Data Analysis bootcamp. The primary goal of this project is to scrape live chats, perform sentiment analysis, identify hate speech, and then store the processed data in a MongoDB database. If you're interested in working with real-time chat data and exploring the sentiment and language used within these chats, this project can serve as a helpful reference.

## Index

1. [Project Overview🔎](#project)
1. [Technologies Used👩‍💻](#techs)
1. [How to Use This Repository📒](#howto)
1. [Limitations🛑](#limitations)
1. [Contributions👥](#contributions)
1. [License ©](#license)

<a name="project"/>

## Project Overview🔎

The project follows an ETL pipeline that consists of the following steps:

1. **Extraction (E)**: I use various technologies like `chat_downloader` and `selenium` to scrape live chats from YouTube and Twitch, as well as scraping the top streamers from each platform from playboard and twitchstats.

2. **Transformation (T)**: The scraped chat data is then processed and analyzed for sentiment and hate speech using the `pysentimiento` library. Sentiment analysis helps understand the emotional tone of the chat, while hate speech detection helps identify harmful or abusive language.

3. **Load (L)**: Finally, the cleaned and processed data is stored in a MongoDB database for further analysis, reporting, or other downstream applications.

<a name="techs"/>

## Technologies Used👩‍💻

This project leverages the following technologies and libraries:

- **Python**: The primary programming language used for implementing the ETL pipeline and conducting the analysis.

- **Selenium**: A web automation tool used to interact with websites and retrieve chat data from websites that don't provide a direct API.

- **Joblib**: A Python library to process parallel tasks. Only for main.py.

- **MongoDB**: A NoSQL database used for storing the processed chat data.

- **chat_downloader**: A Python library for downloading chat messages from various platforms and live streams. [Documentation](https://github.com/xenova/chat-downloader).

- **pysentimiento**: A Python library for sentiment analysis that offers pre-trained models for analyzing text data. [Documentation](https://github.com/pysentimiento/pysentimiento).

<a name="howto"/>

## How to Use This Repository📒

To get started with this project, follow these steps:

1. **Clone the Repository**: Begin by cloning this repository to your local machine.

```python
git clone https://github.com/kohkitos/live-chat-etl-project.git
```

2. **Install Dependencies**: Make sure you have Python and the required libraries (chat_downloader, Selenium, and pysentimiento) installed on your system. You can use `pip` to install these dependencies.

```python
pip install chat_downloader selenium pysentimiento
```

3. **Configure MongoDB**: Ensure that you have a MongoDB database set up and configure the connection details in the project settings.

4. **Scraping and Analysis**: Modify the scraping and analysis scripts as needed for your specific use case. The provided code is a starting point and can be customized to suit your requirements.

5. **Run the ETL Pipeline**: Execute the ETL pipeline to scrape live chats, perform sentiment analysis, and load the data into MongoDB.

6. **Explore the Data**: Use the stored data in MongoDB for further analysis, reporting, or any other data-driven tasks.

<a name="limitations"/>

## Limitations🛑

While this project aims to provide a useful ETL pipeline for live chat data analysis, there are a few limitations to be aware of:

1. **Limited Computing Resources**: The development and testing of this project were conducted on a non-powerful PC, which may have led to the creation of optimized, but less computationally intensive versions of certain functions. As a result, some processes may be less efficient than they could be on more powerful hardware.

2. **Hate Speech Analysis Accuracy**: The hate speech analyzer, powered by the `pysentimiento` library, provides a good estimate of hate speech within the chat data. However, it's important to note that the accuracy of hate speech detection is not perfect. There may be instances where real hate speech goes undetected, or non-hate speech content is misclassified as hate speech. This limitation is inherent to most automated text analysis tools and should be considered when using the results.

3. **Scraping Platform Dependence**: The effectiveness of chat scraping heavily relies on the specific platforms from which you collect data. Changes in the website structure or updates to their chat interfaces may affect the scraping functionality, leading to potential issues with data retrieval. Regular maintenance and adaptation may be required to accommodate platform changes.

4. **Resource Intensive**: Depending on the source and volume of chat data, the ETL pipeline can be resource-intensive, requiring significant processing power and memory. Be mindful of the system requirements when using this project for larger-scale data processing.

Please keep these limitations in mind when using or further developing this project, and consider potential enhancements or adaptations to better suit your specific needs and hardware capabilities.

<a name="contributions"/>

## Contributions👥

Contributions to this project are welcome. If you have ideas for improvements, bug fixes, or additional features, feel free to submit a pull request.

<a name="license"/>

## License ©

This project is licensed under the GNU Affero General Public License v3.0. You can find the details in the [LICENSE](LICENSE) file.


Enjoy working with live chat data and have fun exploring the world of sentiment analysis and hate speech detection!


