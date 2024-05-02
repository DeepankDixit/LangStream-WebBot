# LangStream-WebBot
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
<img width="1115" alt="image" src="https://github.com/DeepankDixit/LangStream-WebBot/assets/22991058/6af7dfb2-e7dd-47a9-85ca-25056254cce0">

2. Enter the website URL with which you want to chat - [Cisco ISE 3.2 CLI Reference Guide](https://www.cisco.com/c/en/us/td/docs/security/ise/3-2/cli_guide/b_ise_CLI_Reference_Guide_32/b_ise_CLIReferenceGuide_32_chapter_01.html#wp4862170690). The bot is now activated.

or [Cisco Hypershield At a Glance](https://www.cisco.com/c/en/us/products/collateral/security/hypershield-aag.html)

<img width="781" alt="image" src="https://github.com/DeepankDixit/LangStream-WebBot/assets/22991058/b08eda4e-6174-4121-a124-f6966c292fac">

3. Enter your queries and engage in the conversation. Remember that the bot has memory, so it will remember the conversation exchanged during an entire session.
e.g., "I accidentally changed the ISE system time from cli, and broke the deployment. How can I fix it?"

<img width="800" alt="image" src="https://github.com/DeepankDixit/LangStream-WebBot/assets/22991058/13ead5a3-3d86-4def-ab87-e4ce67b72842">

<img width="771" alt="image" src="https://github.com/DeepankDixit/LangStream-WebBot/assets/22991058/e0b4f0f6-5ff1-4687-9a24-50485c257ab9">
