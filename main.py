import json
import openai
import os
import sqlite3
from time import time
fdir = os.path.dirname(__file__)

def getPath(fname):
    return os.path.join(fdir, fname)

sqliteDbPath = getPath("muesumDATA.sqlite")
setupSqlPath = getPath("createTable.sql")
setupSqlDataPath = getPath("populateTable.sql")

if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath)

sqliteCon = sqlite3.connect(sqliteDbPath)
sqliteCursor = sqliteCon.cursor()

with open(setupSqlPath) as setupSqlFile:
    setupSqlScript = setupSqlFile.read()

with open(setupSqlDataPath) as setupSqlDataFile:
    setupSQlDataScript = setupSqlDataFile.read()

sqliteCursor.executescript(setupSqlScript)
sqliteCursor.executescript(setupSQlDataScript)

def runSql(query):
    result = sqliteCursor.execute(query).fetchall()
    return result

configPath = getPath("config.json")
print(configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openai.api_key = config["openaiKey"]
openai.organization = config["orgId"]

def getChatGptResponse(content):
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    responseList = []
    for chunk in response:
        if 'content' in chunk.choices[0].delta:
            responseList.append(chunk.choices[0].delta.content)

    result = "".join(responseList)
    return result

commonSqlOnlyRequest = " Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not explain it!"
strategies = {
    "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    "single_domain_double_shot": (
        setupSqlScript +
        " Who doesn't have a way for us to text them? " +
        " \nSELECT p.person_id, p.name\nFROM person p\nLEFT JOIN phone ph ON p.person_id = ph.person_id AND ph.can_recieve_sms = 1\nWHERE ph.phone_id IS NULL;\n " +
        commonSqlOnlyRequest
    )
}

questions = [
    "Which artifacts were restored in 2022?"
]

def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    return value

for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    for question in questions:
        print(question)
        error = "None"
        queryRawResponse = None
        friendlyResponse = None
        try:
            sqlSyntaxResponse = getChatGptResponse(strategies[strategy] + " " + question)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print(sqlSyntaxResponse)
            queryRawResponse = str(runSql(sqlSyntaxResponse))
            print(queryRawResponse)
            friendlyResultsPrompt = f'I asked a question "{question}" and the response was "{queryRawResponse}". Please, just give a concise response in a more friendly way? Please do not give any other suggestions or chatter.'
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print(friendlyResponse)
        except Exception as err:
            error = str(err)
            print(err)

        questionResults.append({
            "question": question,
            "sql": sqlSyntaxResponse,
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })

    responses["questionResults"] = questionResults

    with open(getPath(f"response_{strategy}_{int(time())}.json"), "w") as outFile:
        json.dump(responses, outFile, indent=2)

sqliteCursor.close()
sqliteCon.close()
print("Done!")
