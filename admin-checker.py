import requests
import argparse

def check_admin_endpoints(urls, admin_cookie, other_cookie):
    headers_admin = {"Cookie": admin_cookie}
    headers_other = {"Cookie": other_cookie}

    results = []

    for url in urls:
        url = url.strip()
        if not url:
            continue

        # Step 1: Check with admin
        try:
            admin_response = requests.get(url, headers=headers_admin, verify=False, timeout=10)
        except requests.RequestException as e:
            results.append({"url": url, "admin_status": f"Error: {e}", "other_status": "Skipped"})
            continue

        if admin_response.status_code == 200:
            # Step 2: Check with other role
            try:
                other_response = requests.get(url, headers=headers_other, verify=False, timeout=10)
                results.append({
                    "url": url,
                    "admin_status": admin_response.status_code,
                    "other_status": other_response.status_code
                })
            except requests.RequestException as e:
                results.append({"url": url, "admin_status": admin_response.status_code, "other_status": f"Error: {e}"})
        else:
            results.append({
                "url": url,
                "admin_status": admin_response.status_code,
                "other_status": "Skipped (admin no access)"
            })

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if admin-only endpoints are accessible to another role.")
    parser.add_argument("-f", "--file", required=True, help="File containing list of admin URLs (one per line)")
    parser.add_argument("--admin-cookie", required=True, help="Admin role cookie string (e.g. 'sessionid=ADMIN123')")
    parser.add_argument("--other-cookie", required=True, help="Other role cookie string (e.g. 'sessionid=USER456')")

    args = parser.parse_args()

    # Read URLs from file
    with open(args.file, "r") as f:
        urls = f.readlines()

    results = check_admin_endpoints(urls, args.admin_cookie, args.other_cookie)

    print(f"{'URL':50} {'Admin':15} {'Other Role':15}")
    print("-" * 85)
    for r in results:
        print(f"{r['url']:50} {str(r['admin_status']):15} {str(r['other_status']):15}")
