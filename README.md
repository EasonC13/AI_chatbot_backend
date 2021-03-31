# AI_chatbot_platform

Backend: https://github.com/EasonC13/AI_chatbot_platform

Front-end: https://github.com/EasonC13/AI_Chatbot_website

(Please Checkout Dev Branch)

Demo Video: https://youtu.be/ES2mmcrhS10

# How To Run?

0. install dependency:

```
pip install -r requirements.txt
```

1. copy app/core/config_example.py to app/core/config.py and Edit the config file.

```
cp app/core/config_example.py app/core/config.py
```

2. Edit the config.py.

You might need to [add Google API Key from this tutorial](https://cloud.google.com/docs/authentication/getting-started).<br>
And use that key at GOOGLE_APPLICATION_CREDENTIALS in config.py

if you want to have a ch-generate-url, please contact me at pricean01@gmail.com. Or use a language generate API like the following format:

```
curl -X 'GET' \
  'https://{host}/?input_text={input_text}[{emotion}]&nsamples={need_samples_amount}' \
  -H 'accept: application/json'
```

the response format is like the following:


```
curl -X 'GET' \
  'https://{host}/?input_text=Hello World[lovely]&nsamples=5' \
  -H 'accept: application/json'
```

```
[
  {
    "candidate": "Reply Text",
    "coherence": 0.5
  },  
  {
    "candidate": "😘😘",
    "coherence": 0.8
  },
  {
    "candidate": "Greeting!",
    "coherence": 0.8
  },
  {
    "candidate": "The world is so small",
    "coherence": 0.5
  },
  {
    "candidate": "😊",
    "coherence": 0.6
  }
]
```

Coherence is the score of the fluency of the response. If you don’t have a model to judging coherence, just use 0.5 directly.

3. Use the following command to run it:

```
cd app
uvicorn app:app --port {API_PORT} --host 0.0.0.0 --workers 8
```

3. Bulid front-end

If you want use front-end as well. <br>
Please [clone front end from another GitHub Repo](https://github.com/EasonC13/AI_Chatbot_website) at root.

```
cd AI_chatbot_platform
git clone https://github.com/EasonC13/AI_Chatbot_website.git
mv AI_Chatbot_website front-end
```

And change the google cloud login credentials to your own at `front-end/public/index.html` at line 49.

And then go inside it and build it. (Recommand Demo Branch since we havn't merge it.)

```
cd front-end
git checkout demo
npm i
npm run build
```
