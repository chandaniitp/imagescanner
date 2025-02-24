import requests

# Define the Apache version
version = "2.4.41"

# Construct the CVE API URL
cve_api_url = f"https://cveawg.mitre.org/api/cve?cpe=cpe:/a:apache:http_server:{version}"

# Send the GET request
response = requests.get(cve_api_url)
print(response)  # Print response object for status code

# Parse the JSON response
data = response.json()
print(data)  # Print the raw JSON data

# Check if the totalResults field exists and if it has any results
if data.get("totalResults", 0) > 0:
    print(f"Result count: {data['totalResults']}")
else:
    print("No results found")
