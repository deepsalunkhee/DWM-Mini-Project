# WhatsApp Chat Analyzer

WhatsApp Chat Analyzer is a tool that helps you analyze and visualize statistics from your WhatsApp chat data. You can gain insights into message frequencies, word usage, media sharing, and more. This project is built using Python and Streamlit.

## Getting Started

To get started with the WhatsApp Chat Analyzer, follow these steps:

### Prerequisites

You'll need the following prerequisites to run the project:

- Python (3.7 or higher)
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- emoji (Python library)
- [Urlextract](https://pypi.org/project/urlextract/)
- [WordCloud](https://pypi.org/project/wordcloud/)

You can install the required Python libraries using pip:

```bash
pip install streamlit pandas matplotlib seaborn emoji urlextract wordcloud
```

### Running the Application

1. Clone this GitHub repository to your local machine:

```bash
git clone <https://github.com/deepsalunkhee/DWM-Mini-Project>
```

2. Navigate to the project directory:

```bash
cd WhatsApp-Chat-Analyzer
```

3. Run the Streamlit application:

```bash
streamlit run chat_analyzer.py
```

4. Upload your WhatsApp chat data file in the Streamlit app to start the analysis.

## Usage

- Upload your WhatsApp chat data in a text format (typically a .txt file).
- Choose the user you want to analyze (individual user or "Overall" for group analysis).
- Click the "Show Analysis" button to view the statistics and visualizations.

## Features

- Total message count analysis.
- Word count analysis.
- Media sharing analysis.
- Links shared analysis.
- Busiest users in the chat.
- Wordcloud visualization.
- Most common words analysis.
- Emoji analysis.
- Monthly and daily message timeline.
- Weekly and monthly activity maps.