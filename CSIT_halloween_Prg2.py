import json
import math
import heapq
import requests

def calculate_score(record):
    # Unpack necessary fields
    rating = record.get("rating", 0.0)
    distance = record.get("distance_from_me", 0.0)
    record_id = record.get("id", 0)
    
    # Calculate score
    score = (rating * 10 - distance * 0.5 + math.sin(record_id) * 2) * 100 + 0.5
    final_score = round(score / 100, 2)  # Round to 2 decimal places
    
    return final_score

def sort_and_select_top_k():
    # Load the validated data
    input_file_name = "validated_dataset.json"
    output_file_name = "topk_results.json"
    
    try:
        with open(input_file_name, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: {input_file_name} not found.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in validated dataset.")
        return

    # Add calculated scores to each record
    for record in data:
        record["score"] = calculate_score(record)
    
    # Sort data based on the multiple criteria
    top_k_records = sorted(
        data, 
        key=lambda x: (x["score"], x["rating"], x["distance_from_me"], x["restaurant_name"]), 
        reverse=True  # Sorting in descending order for all except restaurant_name (default asc for str)
    )[:10]

    # Format output to match specified structure
    output_data = [
        {
            "id": record["id"],
            "restaurant_name": record["restaurant_name"],
            "rating": record["rating"],
            "distance_from_me": record["distance_from_me"],
            "score": record["score"]
        }
        for record in top_k_records
    ]
    
    # Save the top 10 records to a JSON file
    with open(output_file_name, 'w') as file:
        json.dump(output_data, file, indent=4)
    
    print(f"Top 10 records saved to {output_file_name}")

# Call the function
sort_and_select_top_k()

def api_testSolution():
    # API endpoint URL
    api_url = os.getenv("API_URL") + "/test/check-topk-sort"
    

    try:
        with open("topk_results.json", "r") as file:
            topresults = json.load(file)
    except FileNotFoundError:
        print("Error: topk_results.json.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in topk_results.json.")
        return

    # Prepare the payload with the required format
    payload = {"data": topresults}

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
