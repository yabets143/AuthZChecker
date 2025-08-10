# AuthZChecker
A simple Python CLI tool that verifies if admin-only endpoints are improperly accessible by other user roles. It accepts a list of URLs and compares the HTTP response status codes when accessed with admin versus non-admin cookies, helping identify potential authorization bypass or privilege escalation vulnerabilities in web applications.

Usage example:
python check_admin_access.py -f admin_urls.txt --admin-cookie "sessionid=ADMIN123" --other-cookie "sessionid=USER456"


# version 2

How to run it (same as before):

python check_admin_access.py -f admin_urls.txt --admin-cookie "sessionid=ADMIN123" --other-cookie "sessioni
