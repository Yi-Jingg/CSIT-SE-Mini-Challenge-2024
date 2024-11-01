# CSIT Software Engineering Mini Challenge 2024

This repository contains solutions for the CSIT Software Engineering Mini Challenge 2024, which is divided into two main parts:

1. **Cleaning and Retrieving Data from a Database API**
2. **Sorting and Selecting the Top Entries Based on Multiple Criteria**

## Challenge Overview

The challenge focuses on working with a dataset via API, cleaning and sorting it based on specific criteria, and generating the top-ranked results based on a calculated score.

### Prerequisites
- **Python** (version 3.x)
- **API Authorization Token**: Required for API access

---

## Part 1: Database Cleanup and Retrieval

This part of the challenge involves paginating through a dataset provided via an API, collecting and cleaning the records.

### API Details

- **Payload Parameter**:
  - `next_id` (String): Used for paginating through the dataset. Begin with an empty `next_id`. Continue sending the last received `next_id` until the API response contains an empty `next_id`, indicating the end of the dataset.

- **Headers**:
  - `authorizationToken` (String): Required for API access. Replace with a valid token.
  - `Content-Type`: Set to `"application/json"`.

### Solution Steps

1. Connect to the API and initiate the first request with an empty `next_id`.
2. Loop through the paginated data, appending results to a dataset until `next_id` is empty.
3. Validate and clean the retrieved data as needed for further processing.

---

## Part 2: Sorting and Ranking the Cleaned Data

In this part, the goal is to sort the cleaned data according to specific criteria and select the top 10 entries. The criteria are as follows:

### Sorting Criteria
1. **Score**: Calculated using the formula:
   \[
   \text{score} = (\text{rating} \times 10 - \text{distance} \times 0.5 + \sin(\text{id}) \times 2) \times 100 + 0.5
   \]
   - `final_score = round(score / 100, 2)`
2. **Rating**: Sort in descending order.
3. **Distance**: Sort in descending order.
4. **Restaurant Name**: Sort alphabetically in ascending order.

### Solution Steps

1. Compute the `final_score` for each entry using the provided formula.
2. Sort entries by `final_score`, followed by `rating`, `distance`, and `restaurant name` (in that order of priority).
3. Select the top 10 entries and save them to a JSON file, `topk_results.json`.
