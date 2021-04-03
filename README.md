# Accompany AI Chat (AI_chatbot_platform)

Backend: https://github.com/EasonC13/AI_chatbot_platform

Front-end: https://github.com/EasonC13/AI_Chatbot_website

Chinese_Word_Generator_API: https://github.com/EasonC13/Chinese_Word_Generator_API

(Please Checkout demo Branch)

Demo Video: https://youtu.be/-Bq76zVv7GI

## How To Run?

### 0. Please Use demo branch for demo

```
git checkout demo
```

### 1. install dependency:

```
pip install -r requirements.txt
```

### 2. copy app/core/config_example.py to app/core/config.py and Edit the config file.

```
cp app/core/config_example.py app/core/config.py
```


### 3. Edit the config.py.

(1) You might need to [add Google API Key from this tutorial](https://cloud.google.com/docs/authentication/getting-started).<br>
And use that key at GOOGLE_APPLICATION_CREDENTIALS in config.py

(2) the part of Operator_bot_Token, TELEGRAM_API_ID, TELEGRAM_API_HASH is not necessary to set if you seeking a demo like [Demo Video](https://youtu.be/ES2mmcrhS10)

(3) You might need a MongoDB if you don't have it yet, please follow [the tutorial from MongoDB's Manual](https://docs.mongodb.com/manual/installation/) to install MongoDB at your host.

(3) if you want to have the link to chinese model generate(CH_GENERATE_API_URL), please use `https://chatbot.eason.tw/api/developer/middle-ware/generate-text` for now (demo purpose).

Or train and host a chinese (zh-tw) language generate model API from [Chinese_Word_Generator_API_example](https://github.com/EasonC13/Chinese_Word_Generator_API)

API should have the following format:

```
curl -X 'GET' \
  'https://{host}/?input_text={input_text}[{emotion}]&nsamples={need_samples_amount}' \
  -H 'accept: application/json'
```

the response example is like the following:


```
curl -X 'GET' \
  'https://{host}/?input_text=你好世界[lovely]&nsamples=5' \
  -H 'accept: application/json'
```

```
[
  {
    "candidate": "回覆你喔",
    "coherence": 0.5
  },  
  {
    "candidate": "😘😘",
    "coherence": 0.8
  },
  {
    "candidate": "你好!",
    "coherence": 0.8
  },
  {
    "candidate": "世界真小",
    "coherence": 0.5
  },
  {
    "candidate": "😊",
    "coherence": 0.6
  }
]
```

Coherence is the score of the fluency of the response. If you don’t have a model to judging coherence, just use 0.5 directly.

### 4. Install and Bulid front-end

Please [clone front end from another GitHub Repo](https://github.com/EasonC13/AI_Chatbot_website) at root.

```
cd AI_chatbot_platform
git clone https://github.com/EasonC13/AI_Chatbot_website.git
mv AI_Chatbot_website front-end
```

Please change the google cloud login client-id to your own at `front-end/public/index.html` at line 49 follwing [this tutorial](https://developers.google.com/identity/sign-in/web/sign-in).

And then go inside it and build it. (Recommand Demo Branch since we havn't merge it.)

```
cd front-end
git checkout demo
npm i
npm run build
```

### 5. Create tmp folder at app/

```
mkdir app/tmp
```

### 6. Use the following command to run it:

```
cd app
uvicorn app:app --port {API_PORT} --host 0.0.0.0 --workers 8
```

> Or You can just open the app/main_dev.ipynb and run all cells, it also work.
