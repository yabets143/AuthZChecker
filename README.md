# AuthZChecker
A simple Python CLI tool that verifies if admin-only endpoints are improperly accessible by other user roles. It accepts a list of URLs and compares the HTTP response status codes when accessed with admin versus non-admin cookies, helping identify potential authorization bypass or privilege escalation vulnerabilities in web applications.
