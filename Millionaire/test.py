import requests

host = "http://localhost:5000/service"

response = requests.get("%s/%s" % (host, "0")).json()
print(response)

# Does not exist in List - testing for error message
response = requests.get("%s/%s" % (host, "10000")).json()
print(response)

response = requests.delete("%s/%s" % (host, "0")).json()
print(response)

# Does not exist in List - testing for error message
response = requests.delete("%s/%s" % (host, "1000000")).json()
print(response)

response = requests.put("%s/%s" % (host, "5000"), data={
    "level": 2,
    "fragetext": "Is this a good test?",
    "antwortmoeglichkeit": ["Yes", "Maybe", "No", "Perfect game"],
    "antwort": "3"
}).json()
print(response)


response = requests.patch("%s/%s" % (host, "1"), data={
    "level": 1,
    "fragetext": "How are you?",
    "antwortmoeglichkeit": ["Yes", "Maybe", "No", "Perfect game"],
    "antwort": "3"
}).json()
print(response)

# Does not exist in List - testing for creating question
response = requests.patch("%s/%s" % (host, "10000"), data={
    "level": 3,
    "fragetext": "Is this a good question?",
    "antwortmoeglichkeit": ["Yes", "Maybe", "No", "Perfect game"],
    "antwort": "2"
}).json()
print(response)