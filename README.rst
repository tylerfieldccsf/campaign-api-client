NetFile Campaign API Sync Client
================================
Open source Python library to synchronize a local database with the Campaign API data provided by NetFile, Inc.
This is a command line utility, written in Python, that allows a user to interact with NetFile, Inc.'s public Campaign API.

Usage
-----
1) Create config.json file based on config.json.example file
    * Create copy of config.json.example file named config.json
    * Update the DB_USER, DB_PASSWORD with values used by your local installation of PostgreSQL database
    * Update the API_USER, API_PASSWORD values with credentials provided from NetFile
2) Use the campaign_api_client.py file as a command line utility to perform necessary operations
    * For list of available commands: `python campaign_api_client.py --help`
3) Create local postgres database that will contain the synchronized Campaign data
    * Create a local postgres database that matches the DB_NAME value in config.json file. (The default is 'campaign-api-sync')
    * Create schema the first time
        example: `python campaign_api_client.py --database create`
    * Rebuild the schema (drop all tables and re-create from SQL schema file)
        example: `python campaign_api_client.py --database rebuild`
4) View available Sync Feeds and Sync Topics:
    * example: `python campaign_api_client.py --feed`
5) Create a new Sync Subscription for a Sync Feed. The subscription can be maintained over the long term if desired, and does not need to be re-created. Command arguments are an existing Feed Name and user provided Subscription Name:
    * example: `python campaign_api_client.py --create-subscription FilingActivity_V101 Test_Filing_Activity_Sub`
6) Create a new Sync Session associated with a Sync Subscription by providing the subscription ID as input argument. The lifecycle of the Sync Session is only for a single Sync cycle, and will be set to completed when finished, or canceled if necessary.
    * example: `python campaign_api_client.py --session create 48aae322-a0be-42c3-b010-61534a8aa964`
7) Once the Sync Session is created, synchronize the Feed Topics to the local database by providing the session ID and topic name
    * example 1: `python campaign_api_client.py --sync-topic 05af361b-6c4b-489f-9673-4cfe7f189ddd activities`
    * example 2: `python campaign_api_client.py --sync-topic 05af361b-6c4b-489f-9673-4cfe7f189ddd activity-elements`
    * **Note: The local database should now have the latest data available through the API.**
8) Optionally Cancel the Sync Session. User provides the Session ID. No reads of the Sync Session will be recorded on the back-end.
    * example: `python campaign_api_client.py --session cancel ebcb9151-067e-47de-be67-20e256b79d73 1`
9) Complete the Sync Session when done with desired Sync Topics. User provides the Session ID
    * example: `python campaign_api_client.py --session complete 05af361b-6c4b-489f-9673-4cfe7f189ddd 1`
    * **Note: The Sync process is now Complete**
10) Optionally Cancel the Sync Subscription. User provides the Subscription ID

    * example: `python campaign_api_client.py --cancel-subscription 48aae322-a0be-42c3-b010-61534a8aa964 1`

**Provided and supported by NetFile, Inc. The largest provider of Campaign and SEI services in California.**

More information:

- [Website] (https://www.netfile.com)