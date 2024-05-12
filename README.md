# chat-with-weburls
A versatile chatbot designed to interact with websites, extract information, and engage users through an intuitive Streamlit-based GUI. Leveraging LangChain and compatible with advanced language models like GPT-4, it offers a seamless blend of web navigation and conversational AI.
Access it here [LangStream WebBot URL](https://webnavigator.streamlit.app/) or [URL2](https://chatwithwebsites.onrender.com/)

## App Architecture / Logic
<img width="1313" alt="image" src="https://github.com/DeepankDixit/LangStream-WebBot/assets/22991058/0486ee9d-96bb-4c59-8624-fdee66833f9b">

### Installing the Dependencies

1. Clone the repository to your local machine
2. Run `pip install -r requirements.txt` to install the required dependencies
3. Get your OpenAI API key and save it in the `.env` file in the project directly
`OPENAI_API_KEY="your_secret_api_key"`

## How to run it locally

1. Run the `app.py` file from the project directly using `streamlit run app.py`
2. This will launch the app in your web browser.
3. You can load multiple websites and click on Process. 
4. Once the processing is complete, you can ask questions about the websites in natural language.

## App walkthrough

1. App UI
<img width="1271" alt="image" src="https://github.com/DeepankDixit/LangStream-WebBot/assets/22991058/60439b1d-3684-4044-871a-c4d973ba1053">


2. Enter the website URLs with which you want to chat - [Cisco Identity Services Engine Administrator Guide, Release 3.3](https://www.cisco.com/c/en/us/td/docs/security/ise/3-3/admin_guide/b_ise_admin_3_3/b_ISE_admin_33_troubleshooting.html#concept_01E90718274343D287DAB79B12FAE740), [Frequently Asked Questions About ArcaneDoor](https://www.tenable.com/blog/cve-2024-20353-cve-2024-20359-frequently-asked-questions-about-arcanedoor), [ISE Guest Access Prescriptive Deployment Guide](https://community.cisco.com/t5/security-knowledge-base/ise-guest-access-prescriptive-deployment-guide/ta-p/3640475)

<img width="1608" alt="image" src="https://github.com/DeepankDixit/LangStream-WebBot/assets/22991058/426f5bde-b939-4d02-974d-bfe9c7c77957">

The bot is now activated.

<img width="1490" alt="image" src="https://github.com/DeepankDixit/LangStream-WebBot/assets/22991058/831a5080-579a-4254-b204-58c94ed6cabc">

3. Enter your queries and engage in the conversation. Remember that the bot has memory, so it will remember the conversation exchanged during an entire session.
e.g., "Can you help me stepwise with troubleshooting unexpected radius authentication issues in ISE 3.3?"

<img width="1132" alt="image" src="https://github.com/DeepankDixit/LangStream-WebBot/assets/22991058/ff05dfe0-3400-42a8-9677-31b1db3a688f">

"I am trying to configure Guest Access for ISE. What should be my switch configuration. Give me the commands"

<img width="1069" alt="image" src="https://github.com/DeepankDixit/LangStream-WebBot/assets/22991058/0d4a9a07-5394-40ea-a884-27d457fac99c">
<img width="1008" alt="image" src="https://github.com/DeepankDixit/LangStream-WebBot/assets/22991058/cc5e3639-4c53-4a37-b109-9147c9e640f0">

"what is the CVE id associated with ArcaneDoor?"

<img width="1038" alt="image" src="https://github.com/DeepankDixit/LangStream-WebBot/assets/22991058/a88cd09a-a479-46d6-a5f9-c870e517abfa">

