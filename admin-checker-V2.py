import requests
import argparse
import hashlib

def hash_content(content):
    """Create a hash of response content to compare easily."""
    return hashlib.sha256(content).hexdigest()

def check_admin_endpoints(urls, admin_cookie, other_cookie):
    headers_admin = {"Cookie": admin_cookie}
    headers_other = {"Cookie": other_cookie}

    results = []

    for url in urls:
        url = url.strip()
        if not url:
            continue

        try:
            admin_response = requests.get(url, headers=headers_admin, verify=False, timeout=10)
        except requests.RequestException as e:
            results.append({"url": url, "admin_status": f"Error: {e}", "other_status": "Skipped", "content_match": "N/A"})
            continue

        if admin_response.status_code == 200:
            try:
                other_response = requests.get(url, headers=headers_other, verify=False, timeout=10)
            except requests.RequestException as e:
                results.append({
                    "url": url,
                    "admin_status": admin_response.status_code,
                    "other_status": f"Error: {e}",
                    "content_match": "N/A"
                })
                continue

            admin_hash = hash_content(admin_response.content)
            other_hash = hash_content(other_response.content)

            content_match = "Yes" if admin_hash == other_hash else "No"

            results.append({
                "url": url,
                "admin_status": admin_response.status_code,
                "other_status": other_response.status_code,
                "content_match": content_match
            })
        else:
            results.append({
                "url": url,
                "admin_status": admin_response.status_code,
                "other_status": "Skipped (admin no access)",
                "content_match": "N/A"
            })

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if admin-only endpoints are accessible to another role, including content comparison.")
    parser.add_argument("-f", "--file", required=True, help="File containing list of admin URLs (one per line)")
    parser.add_argument("--admin-cookie", required=True, help="Admin role cookie string (e.g. 'sessionid=ADMIN123')")
    parser.add_argument("--other-cookie", required=True, help="Other role cookie string (e.g. 'sessionid=USER456')")

    args = parser.parse_args()

    with open(args.file, "r") as f:
        urls = f.readlines()

    results = check_admin_endpoints(urls, args.admin_cookie, args.other_cookie)

    print(f"{'URL':50} {'Admin Status':15} {'Other Status':15} {'Content Match?':15}")
    print("-" * 95)
    for r in results:
        print(f"{r['url']:50} {str(r['admin_status']):15} {str(r['other_status']):15} {r['content_match']:15}")
