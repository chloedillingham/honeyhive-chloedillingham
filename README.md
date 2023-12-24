# GPT-4 Playground

This is a playground interface for OpenAI GPT-4. It allows you to interact with chat completions with both text and images. It allows you so stream responses. It also allows you to go back and edit messages, which regenerates a response. 

## Set up

1. clone the repository
 ```git clone git@github.com:chloedillingham/honeyhive-chloedillingham.git ```
2.  in the repo directory, create a python virtual environment and activate it.
 ```python3 -m venv env```
 ```source env/bin/activate ```
3. install prerequisites 
 ```pip install -r requirements.txt```

## Configure your environment 
1. Create a file named `.env` in the root directory of the project.
2. Open the `.env` file and add your OpenAI API key like this:
 ```OPENAI_API_KEY='your_openai_api_key_here'```
 Replace `your_openai_api_key_here` with your actual OpenAI API key.

3. Save the `.env` file. The application will use this key to interact with OpenAI's API.
## Run it!

 ```python openai-api.py```


## Contact

You can reach me for questions at `chloeldillingham@gmail.com`