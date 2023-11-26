# Stocks Profits Tracker (+ Notion API Integration with Python)
You can track live US stock prices in your personal notion dashboard and a single Python script.

![Cover.png](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/amu31tn9r9d6jfonp7n3.png)

# Integration Guide

## 1. Duplicating Template:

**Click on the `Duplicate` button in the top right of the notion page.**

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8flwra12sjqqhhewjxx7.png)

ℹ️ Ignore if you’ve already completed this step. Notion may ask you to login into your notion account to successfully duplicate.

## 2.  Creating Notion Integration:

### What is a Notion Integration?

A notion integration allows a user to run automations using tools like programming languages like Python, Javascript, etc. 

> 🤔 **You don’t have to worry too much about this if you’re confused, this is just a simple explanation that will help you get a general idea.**
> 

---

**Follow these steps to create a notion integration:**

1. Click on this link → https://notion.so/my-integrations/ (**once you open this link in your browser, the website may ask you to login to your notion account**)
2. You’ll be presented with this webpage, click on `+ New Integration` button (big black button)
    
![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7wop4ntbxxdzhwz8wz0x.png)
    
3. You’ll then be presented with a form to fill in the `Basic Information:` , you can set the below values:
    1. Type → `Internal`
    2. Associated Workspace → **Choose your notion account’s workspace**
    3. Name →  `Stocks Profits Tracker`
    4. Logo → No need, ignore this
    
    Finally, Click on the `Submit →` (black button)
    
4. You’ll next be presented with a webpage called `Secrets` , you will have to click `show` and `copy` the notion integration secret token and keep it safely aside
    
    
> Copy & Paste the above 🔑 `Notion Integration Secret Key` somewhere 🔒 safe because it will be used in the 🐍 python script.
    

## 3. Connect Notion Integration to Template:

1. Click on the three dots `...` in the top right corner of the duplicate notion template
2. Click on `+ Add Connections` at the end of the the drop down, search for and click the notion integration you’ve created in step 2 ( `Stock Profits Tracker`)
    

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/i4tf41c2hdsom3epfgyl.png)
    

## 4. Populating Stock Prices in ‘Stock Profit Tracker’ Database:

You can add the following values for every stock symbol(tick) you want to add:

1. `Name` → Stock Symbol (like MSFT)
2. `Amount Invested` → Add the amount you bought the stock units with
3. `Price/Unit` → This value will be updated by the Notion Integration (add a default `0.1` so that the python script can update it)
4. `Number of units bought` → Add the number of stock units you bought

**Leave the `Status` & `Net Profit` because when the `Price/Unit` gets updated by automation, these values will change automatically.**


💡 The default notion database contains a few stock market symbols like MSFT, NFLX, TSLA, AAPL, HOOD, etc. (use them as example while adding new stock units)




🚨 **Don’t change the column names  or database name in the `Stocks Profits Tracker` database, doing so will make it impossible to update the columns using the python script.**



## 5. Running Python Script:

**The final part of the integration is about running a python script that will update the real stock prices for all the stock units you have in the database.**

---

1. **Clone this GitHub repository**
2. **Save the secret notion integration token in the `my_variables.yml` file**
    
    ```bash
    MY_NOTION_SECRET_TOKEN: paste-your-notion-integration-token-here
    ```
    
3. **Install the python requirements and dependency libraries by running the command in your terminal**
    
    ```bash
    python3 -m pip3 install -r requirements.txt
    ```
    
4. **Finally run this command in your terminal to start the live `Price/Unit` update process**
    
    ```bash
    python3 main.py
    ```
    

That’s it!

If all the steps are followed properly, your notion database should be getting live stock price and net profit updates when python server is running on your machine.
