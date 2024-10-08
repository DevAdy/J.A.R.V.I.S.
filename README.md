# J.A.R.V.I.S : 🧠
<centre>![JARVIS AI](/jarvis.jpg)</centre>
<p align="center">
  <small><small><em>Image source: <a href="https://at.pinterest.com/pin/715439090790098312/">Pinterest</a></em></small></small>
</p>

This project implements an AI-powered voice assistant using Flask, Groq API for text generation, and Google Cloud Text-to-Speech for voice synthesis. This assistant can transcribe audio input, generate responses, and convert those responses to speech. Additionally it has silence detection to detect silence and stop recording. 

It has a modern and intuitive Web interface, ensuring an exceptional user experience by running on the client-side. It also tracks user and AI transcriptions live on the web interface. 
## Features :eyes:
 - Audio transcription using Whisper model via Groq API
 - AI response generation using LLaMa 3 model via Groq API
 - Text-to-speech conversion using Google Cloud TTS
 - Silence detection in audio input (Refine w.r.t Surroundings)
 - Web interface for interaction and tracking transcriptions
 - Expose the local Flask server over the internet with Ngrok to access anywhere in the world.

## Prerequisites :ninja:
 - **Python 3.7+** : Make sure Python is installed. You can download it from the [official Python website](https://www.python.org/downloads/).

 - **Flask**: Install Flask using pip or requirements.txt above.

 - **Groq API key (Llama 3 & Whisper)**: Sign up at Groq to obtain an API key for Llama 3 and Whisper. Follow their documentation for integration details.

 - **Google Cloud credentials (TTS)**: Set up a Google Cloud account and enable the Text-to-Speech API. Download your service account credentials JSON file and set the **GOOGLE_APPLICATION_CREDENTIALS** environment variable in .env to the path of the json file downloaded from the service key.
    - Note: You may also need the Google Cloud SDK to authenticate and manage your Google Cloud projects. Follow the [Google Cloud SDK installation guide](https://cloud.google.com/sdk/docs/install) if needed.

 - **Ngrok (for public URL access)**: Download and install Ngrok from [ngrok.com](https://ngrok.com)

## Setup:🗣
### 1. Clone the repository:
```bash
git clone https://github.com/DevAdy/J.A.R.V.I.S..git
cd <project-directory>
```
### 2. Install the required packages:
```bash
pip install -r requirements.txt
```
### 3. Set up environment variables: Create a .env file in the project root and add the following:
```bash
GROQ_API_KEY=your_groq_api_key
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/google_credentials.json
```
  - Ensure you have the necessary Google Cloud credentials file for Text-to-Speech.

### 4. Set up Ngrok:
 - Download and install Ngrok from <https://ngrok.com/.> or in the cmd:
    ```
    choco install ngrok
    ```
    - To install with choco you need to install Chocolatey:
    
        If you don't have Chocolatey installed, you can do so by running the following in your terminal (as an administrator):
        ```bash
        @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
        ```
        For more details, visit the [official Chocolatey setup guide](https://docs.chocolatey.org/en-us/choco/setup/).
 - Run the following command in the terminal to add your authtoken to the default ngrok.yml configuration file.
    ```bash
     ngrok config add-authtoken <your_ngrok_auth_token>
    ```

## Running the Application 🏃‍♂️
### 1. Start the Flask server:
```bash
python app.py
```

### 2. Expose the server to the internet using Ngrok:
```
ngrok http <LOCAL-PORT> <Default:5000>
```

 - After running this, Ngrok will provide a public URL (e.g., https://<random-string>.ngrok.io). You can use this URL to access the voice assistant from any device anywhere in the world.

### 3.Access the application:
Open a web browser and navigate to the Ngrok public URL to access the voice assistant interface.

## Usage 👣
 - Allow microphone access for the webpage.
 - Click the Human Circle to start recording.
 - Speak your query or command.
 - The assistant will transcribe your audio, generate a response, and play it back as speech.
 - It also shows the live transcipt and the previous transcripts of both USER and AI
 - Click again on the Human circle to record your voice for continuing the conversation with the AI.
 - You can say 'Thank you.' to end the conversation with the AI.
 - It stops recording when silence is detected.

 ## Project Structure 🦚
 - **app.py**: Main Flask application
 - **assistant.py**: AI assistant class implementation
 - **templates/index.html**: Web interface
 - **static/**: JavaScript and CSS files
 - **requirements.txt**: Python dependencies

 ## Contributing 🫶
We welcome contributions to enhance this project! Whether you want to fix bugs, add features, or improve documentation, your input is invaluable. To get started, please fork the repository, create a new branch for your changes, and submit a pull request with a clear description of your modifications. Make sure to follow our coding standards and include tests where applicable.

Together, we can make this project even better! Please follow these steps:
 - Fork the repository
 - Create a new branch (git checkout -b feature/improvement)
 - Make your changes
 - Commit your changes (git commit -am 'Add new feature')
 - Push to the branch (git push origin feature/improvement)
 - Create a new Pull Request
 ## License 👊
Distributed under the MIT License. See LICENSE.txt for more information.

## Contact 💬
If you have any questions, suggestions, or feedback, feel free to reach out! You can contact me via email at <aditya.b.career@gmail.com> or connect with me on [LinkedIn](https://www.linkedin.com/in/aditya-b-27466921a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app ). I look forward to hearing from you!
Let's learn together!

## Acknowledgments 🙏
 - [Groq API for AI model and STT access](https://groq.com/)
 - [Google Cloud for Text-to-Speech capabilities](https://cloud.google.com/free/?utm_source=google&utm_medium=cpc&utm_campaign=japac-IN-all-en-dr-BKWS-all-core-trial-EXA-dr-1605216&utm_content=text-ad-none-none-DEV_c-CRE_644159077391-ADGP_Hybrid+%7C+BKWS+-+EXA+%7C+Txt+-GCP-General-core+brand-main-KWID_43700074766895886-kwd-6458750523&userloc_9061994-network_g&utm_term=KW_google%20cloud&gad_source=1&gclid=EAIaIQobChMIt5acua76iAMVscc8Ah2tiAfIEAAYASAAEgJHt_D_BwE&gclsrc=aw.ds)
 - [Flask for the web framework](https://flask.palletsprojects.com/en/3.0.x/)
 - [Ngrok for public URL access](https://ngrok.com/)
 - [Chocolatey for choco](https://docs.chocolatey.org/en-us/choco/setup/)
 



