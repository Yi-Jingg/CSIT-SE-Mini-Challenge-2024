import requests
import time
import json
import re
import glob

auth_token = None

def api_get():
    global auth_token
    api_url = "https://u8whitimu7.execute-api.ap-southeast-1.amazonaws.com/prod/register"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        
        if 'data' in data:
            auth_token = data['data'].get("authorizationToken")
            token_expiry = data['data'].get("tokenExpiryAt")

            if auth_token:
                print("Authorization Token:", auth_token)
                print("Token Expiry:", token_expiry)
            else:
                print("Authorization token not found in response.")
        else:
            print("Error: 'data' key not found in response.")
    else:
        print(f"Failed to retrieve data: {response.status_code} - {response.text}")
api_get()

def api_post():
    global auth_token  # Use the global variable
    if auth_token is None:
        print("Error: No authorization token available. Call api_get() first.")
        return
    headers = {
        "authorizationToken": auth_token,
        "Content-Type": "application/json"
    }

    # Initialize pagination variables
    next_id = ""  # Start with an empty next_id for the first request
    dataset_urls = [] 

    # Loop to retrieve paginated data until next_id is empty
    while True:
        payload = {
            "next_id": next_id
        }
        response = requests.post(
            "https://u8whitimu7.execute-api.ap-southeast-1.amazonaws.com/prod/download-dataset",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            response_data = response.json()
            
            if "data" in response_data:
                data = response_data["data"]
                
                # Retrieve dataset URL from data
                if "dataset_url" in data:
                    dataset_url = data["dataset_url"]
                    
                    # Download the dataset using the URL
                    dataset_response = requests.get(dataset_url)
                    if dataset_response.status_code == 200:
                        # Save the dataset file
                        file_name = f"dataset_{next_id or 'start'}.json"  # Name based on next_id
                        with open(file_name, "wb") as file:
                            file.write(dataset_response.content)
                        print(f"Dataset saved as {file_name}")
                        
                        # Collect the URL for tracking purposes (if needed)
                        dataset_urls.append(dataset_url)
                        
                    else:
                        print(f"Failed to download dataset from {dataset_url}: {dataset_response.status_code}")
                        break
                    
                else:
                    print("Error: Dataset URL missing in response data.")
                    break
                
                # Update next_id for pagination; break if empty
                next_id = data.get("next_id", "")
                if not next_id:
                    print("No more data to retrieve. Pagination completed.")
                    break

            else:
                print("Error: Response does not contain 'data' field.")
                break

        elif response.status_code == 429:
            # Handle rate limiting with retry after
            retry_after = int(response.headers.get("Retry-After", 5))  # Default to 5 seconds if header not present
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            # Handle other possible errors
            print(f"Failed to retrieve dataset: {response.status_code} - {response.text}")
            break

# Call the function
api_post()

def is_valid_record(record):
    # Check that the id is an integer
    record_id = record.get("id")
    if not isinstance(record_id, int):
        return False
    
    # Get the restaurant name
    restaurant_name = record.get("restaurant_name")
    # Check that the restaurant name is a valid string
    if not isinstance(restaurant_name, str) or not restaurant_name.strip() or re.search(r'[^a-zA-Z\s]', restaurant_name):
        return False

    # Check that the rating is a valid float
    rating = record.get("rating")
    if not isinstance(rating, float) or not (1.00 <= rating <= 10.00) or rating < 0:
        return False

    # Check that the distance is a valid float
    distance = record.get("distance_from_me")
    if not isinstance(distance, float) or not (10.00 <= distance <= 1000.00) or distance < 0 :
        return False

    return True

def cleanData():

    file_pattern = "dataset_*.json"
    output_file_name = "validated_dataset.json"
    all_validated_data = []

    # Process each dataset file matching the pattern
    for input_file_name in glob.glob(file_pattern):
        print(f"Processing {input_file_name}...")
        try:
            with open(input_file_name, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"Error: {input_file_name} not found.")
            continue
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {input_file_name}.")
            continue

        # Validate records and add to all_validated_data list
        validated_data = [record for record in data if is_valid_record(record)]
        all_validated_data.extend(validated_data)

    # Save all validated records to a single JSON file
    with open(output_file_name, 'w') as file:
        json.dump(all_validated_data, file, indent=4)
    
    print(f"All validated data saved to {output_file_name}")

# Call the function
cleanData()
    
def api_testSolution():
    # API endpoint URL
    api_url = "https://u8whitimu7.execute-api.ap-southeast-1.amazonaws.com/prod/test/check-data-validation"
    
    # Load the data from validated_dataset.json
    try:
        with open("validated_dataset.json", "r") as file:
            validated_records = json.load(file)
    except FileNotFoundError:
        print("Error: validated_dataset.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in validated_dataset.json.")
        return

    # Prepare the payload with the required format
    payload = {"data": validated_records}

    # Submit the data to the API
    try:
        print("Submitting data to the API...")
        response = requests.post(api_url, json=payload)

        # Check response status
        if response.status_code == 200:
            print("Submission successful:", response.json())
        else:
            print(f"Failed to submit data: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"An error occurred while submitting the dataset: {e}")

# Call the api_testSolution function
api_testSolution()
