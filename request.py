import requests

def get_vulnerabilities(package_name, package_version):
    # NVD API endpoint for searching CVEs
    url = f"https://services.nvd.nist.gov/rest/json/cves/1.0"
    
    # Query parameters for NVD API (we filter by package name and version)
    params = {
        "keyword": package_name,
        "version": package_version,
        "resultsPerPage": 5,  # You can increase this number to get more results
        "startIndex": 0
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Failed to retrieve vulnerabilities for {package_name} {package_version}")
        return []

    data = response.json()
    vulnerabilities = []

    for item in data.get('vulnerabilities', []):
        cve_id = item['cve']['CVE_data_meta']['ID']
        description = item['cve']['description']['description_data'][0]['value']
        url = f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}"
        vulnerabilities.append({
            "cve_id": cve_id,
            "description": description,
            "url": url
        })
    
    return vulnerabilities

def main():
    package_name = "tar"  # Change this to your desired package name
    package_version = "1.34+dfsg-1.2+deb12u1"  # Change to your specific version

    vulnerabilities = get_vulnerabilities(package_name, package_version)
    
    if vulnerabilities:
        print(f"Found {len(vulnerabilities)} vulnerabilities for {package_name} {package_version}:")
        for vuln in vulnerabilities:
            print(f"- {vuln['cve_id']}: {vuln['description']}")
            print(f"  URL: {vuln['url']}")
    else:
        print(f"No vulnerabilities found for {package_name} {package_version}")

if __name__ == "__main__":
    main()
