# PipableLLM

The above repository is the flask implementation for Pipable LLM. The instruction to use this repository is as follows:

1. Clone the repository
2. Enter the repository

   ``cd PipableLLM``
3. Create two directories `checkpoints` and `datasets`

   ``mkdir checkpoints datasets``
4. Install the requirements using

   ``pip install -r requirements.txt``
5. Download the checkpoints from [here](https://drive.google.com/file/d/1jzMW7kqXlZB8vp8Y1RAHyKBNX1TVBIos/view?usp=sharing) using this [script](./utilities/download_weights.py) and place them in the `checkpoints` folder.
6. Run the development server

   ``flask --app server run``

The server will be running on **localhost:5000** or **127.0.0.1:5000**

> Test out the APIs using this [notebook](./playground.ipynb).

## Endpoints

The following are the endpoints available for use right now:

1. `/generate` - Using this endpoint, you can generate text from the LLM for your queries.

   **Request Type**: POST

   **Request Body**

   ```json
   {
       "context": "<DETAILS ABOUT TABLE>",
       "question": "<QUERY TO PERFORM IN SIMPLE ENGLISH>"
   }
   ```
   **Response Body**

   ```json
   {
       "output": "<GENERATED TEXT>"
   }
   ```
2. `/train` - The use of this endpoint, is to fine the LLM for Supervised Fine Tuning.

   The dataset needs to be a json file with the following format (notice that the two json are seperate by a new line limiter),

   ```json
       {
           "context": "<CREATE TABLE STATEMENTS FOR TABLES INVOLVED IN THE QUERY>",
           "question": "<QUERY TO PERFORM IN SIMPLE ENGLISH>",
           "answer": "<THE SQL QUERY FOR THE QUESTION>"
       }
       {
           "context": "<CREATE TABLE STATEMENTS FOR TABLES INVOLVED IN THE QUERY>",
           "question": "<QUERY TO PERFORM IN SIMPLE ENGLISH>",
           "answer": "<THE SQL QUERY FOR THE QUESTION>"
       }
   ```
   **Request Type**: POST

   **Request Body**

   ```json
   {
       "dataset_path": "<PATH TO DATASET>"
   }
   ```
   **Response Body**

   ```json
   {
       "status": "",
       "message": ""
   }
   ```
