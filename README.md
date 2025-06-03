
# *** This project is no longer being maintained.  It is listed as reference for anyone who wishes to have a look. *** 

### Daedalus_Wallet_CSV_Print_Utility

Daedalus Wallet - A python print script to print your Daedalus wallet(s) as a csv

Platform: Windows

Tested on Daedalus Mainnet 2.2.0

This is a python script to output your Daedalus wallet(s) as a csv file.  One should always double check the output with the Daedalus wallet.  The wallets print in the order of their wallet id and not their wallet name.  Also be aware that the script has to get the tansaction time from the blockchain as it was not stored locally. So, it may take a little bit of time.

Use at your own risk. No warranties are express or implied.  This was just a little side project of mine.

Enjoy! 
Jim G.

---
This Python script is a well-structured tool for exporting transaction and reward data from Cardano Daedalus wallets into a CSV file. It interacts directly with the wallet's underlying SQLite database files and uses an external API to gather complete transaction details.

Here is a detailed analysis of the code.

### Overall Purpose and Functionality

The primary goal of this script is to provide users with a transaction history report for their Daedalus wallets, suitable for record-keeping or tax purposes.

The script accomplishes this through several key steps:
1.  **Locates Wallet Data:** It first prompts the user for the path to their Daedalus wallet directory. To improve user experience, it saves this path in a local file (`storedData.txt`) so it doesn't have to be entered every time the script is run.
2.  **Identifies Wallets:** It scans the directory for wallet database files (`.sqlite`), separating them by era (the older "Byron" and the current "Shelley").
3.  **User Selection:** The script presents a menu of the wallets it found, allowing the user to select a single wallet or all of them for export.
4.  **Data Extraction:** For the selected wallet(s), it connects to the SQLite database to pull transaction metadata (`tx_meta`) and staking rewards (`delegation_reward`).
5.  **Timestamp Retrieval:** Since the local database does not store the final transaction timestamp, the script uses the transaction ID (`tx_id`) to make an API call to the public Cardano Explorer. This call fetches the official timestamp for each transaction.
6.  **CSV Export:** It formats the collected data—including the timestamp, wallet name, transaction direction (sent/received), and amount—into a CSV format. This data is printed to the console and saved to a `.csv` file in a user-specified output folder.

---
## Analysis
### Code Structure

The script is organized into a series of functions, each handling a specific part of the process. The execution flows from the `main()` function.

* `main()`: The main entry point and control loop for the program. It calls the other functions in sequence and handles the overall program flow and basic error catching.
* `getWalletPath()` & `writeStoredData()`: These functions manage the location of the wallet data directory. `getWalletPath` cleverly checks for a saved path in `storedData.txt` to avoid asking the user repeatedly. It uses `ast.literal_eval()` to safely parse the stored data, which is a secure and excellent choice.
* `dirInfo()` & `retreiveWalletName()`: `dirInfo` uses the `glob` module to find all wallet files and then uses `retreiveWalletName` to query each database file to get the human-readable name the user assigned to the wallet.
* `menu()`: This function builds and displays the interactive menu that allows the user to make their selection. It's the primary UI of the script.
* `importData()`: This is the core data processing function. It executes the main SQL query to get transaction data from the database, handles the file creation logic (including creating a single file for all wallets), and calls other functions to get rewards and timestamps.
* `retreieveRewardAmount()`: Executes a specific SQL query to get the total staking rewards from the `delegation_reward` table.
* `retreivetime2(tx_id)`: Takes a transaction ID, constructs a URL, and uses the `requests` library to call the Cardano Explorer API. It includes a `while` loop to retry the request if the server is busy, which is a robust way to handle intermittent network errors.

---

### Technical Strengths and Suggestions for Improvement

The script is quite effective and demonstrates a good understanding of database interaction, API calls, and file I/O in Python. As a computer science educator, you might appreciate the following points.

#### Strengths:
* **Modularity:** The code is well-organized into functions, making it easy to understand and maintain.
* **User-Friendliness:** Remembering the wallet path is a thoughtful feature that greatly improves usability.
* **Robustness:** The retry mechanism in the API call function (`retreivetime2`) is a great example of defensive programming.
* **Security:** The use of `ast.literal_eval` instead of the more dangerous `eval()` for reading the stored path is a critical security best practice.
---
* **API Dependency:** The script's reliance on a public API is its main vulnerability. If the API URL changes, is discontinued, or becomes unreliable, the script will break. The author correctly notes this in the comments. Unfortunately, without the timestamp in the local database, this dependency is necessary.
