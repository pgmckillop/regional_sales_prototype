import pandas as pd
from matplotlib import pyplot as plt

# Import the data into a DataFrame
sales = pd.read_csv('regional_sales.csv')
sales2 = pd.read_csv('regional_sales_2.csv')


# Modularised main menu
def main_menu():
    print()
    print("\t\t**** Welcome to the Dashboard ****")
    print("\t\t*** ENTER A MENU CHOICE NUMBER ***")
    print()
    print('1) Return all current data')
    print('2) Return data for a specific region')
    print('3) Perform enhanced search')
    print('4) Highest Team sales over time')
    print('5) Total Period Sales')
    print('6) Single Team sales over time')
    print('7) Teams sales over time')
    print('9) Exit the program')
    choice = int(input("\n  Enter a menu number: "))
    return choice


# Return all data in the regional_sales DataFrame
def all_data():
    print(sales)


# Regional data analysis
def average_regional_sales(region_selected, start_date_selected, end_date_selected):
    # Split - Apply
    sales_filters = sales.loc[:, 'Id':'Region']
    # Split - Apply
    sales_range = sales.loc[:, start_date_selected:end_date_selected]
    # Combine into the data filtered by region and dates
    result = pd.concat([sales_filters, sales_range], axis=1, join='inner')
    result = result.where(sales_filters["Region"] == region_selected)
    # Cast as a DataFrame
    result = pd.DataFrame(result)
    # Munge empty cells as good practice
    result.dropna(inplace=True)
    # Show the data in the terminal

    # PLOTTING
    average_sales = sales_range.mean()
    plt.style.use('ggplot')
    average_sales.plot(kind='bar', title='average regional sales')
    plt.show()
    return result


# *****************************************************************
# MENU OPTION 3: ENHANCED SEARCH
# *****************************************************************
# For the enhanced search feature I am going to modularise the code
# to the Highest practical extent given the time allowed in line with the planning
# documentation
# I will do this to make the code more secure, robust and maintainable.
# If I have time I will Modularise, perhaps not exactly in this order:
#   1.  Provision to print a list of valid region names to improve the UX when filtering
#           and reduce user errors.
#   2.  Ditto for product types
#   3.  Ditto for the Sales Teams
#   4.  Function to return a validated region name
#   5.  Function to return a validated product type name
#   6.  Function to return a validated Sales Team
#   7.  Functions to return validated start and end dates
#   8.  Class to hold the validated data needed for the enhanced search:
#           Region, Type of product, Sales Team.
#   9.  Function to populate the Class object instance with validated data harvested
#   10. Function to carry out the search and show the outcome
#
# In a perfect world, I would then refactor the code for Menu option 2 to use these features.
# I would also would modularise features into separate files and folders. I won't have time to do that, I think.


# 1. List of regions
def print_valid_regions():
    regions = sales2["Region"].values
    unique_regions = list(set(regions))
    print('The available regions are: ')
    for r in unique_regions:
        print(f"\t{r}")


# 2. List of product types
def print_valid_product_types():
    types = sales2["Type"].values
    unique_types = list(set(types))
    print("The available product types are: ")
    for t in unique_types:
        print(f"\t{t}")


#   3.  list of Sales Teams
def print_valid_sales_teams():
    teams = sales2['Sales_Team'].values
    unique_teams = list(set(teams))
    print("The available Sales Teams are: ")
    for t in unique_teams:
        print(f"\t{t}")


#   SPARE for Development
# 3X. Range of customer ratings
def print_customer_rating_range():
    rating_min = sales2["Customer_Rating"].min()
    rating_max = sales2["Customer_Rating"].max()
    print(f"You can select a customer rating between {rating_min} and {rating_max}")


# 4. Get valid region from the user
def get_region():
    # Check loop
    while True:
        # Call the modularised method from 1. above
        # to offer best chance and good UX
        print_valid_regions()
        # get value and convert to lower
        selected_region = input("Enter the name of the Region to check: ").lower()
        # Check if in the dataframe
        if selected_region not in sales2["Region"].str.lower().values:
            # inform user of error
            print("Invalid Region name entered")
        else:
            # confirm and break
            print()
            print(f"{selected_region} selected")
            break
    # return function value
    return selected_region


# 5. Get the product type from the user
#       Same strategy. No comments needed
def get_product_type():
    while True:
        print_valid_product_types()
        selected_type = input("Enter the name of the Product Type to check: ").lower()
        if selected_type not in sales2["Type"].str.lower().values:
            print("Invalid Product Type")
        else:
            print()
            print(f"{selected_type} selected")
            break
    return selected_type


#   6.  Get Sales team
def get_sales_team():
    while True:
        print_valid_sales_teams()
        selected_team = input("Enter the name os the Sales Team to check: ").lower()
        if selected_team not in sales2['Sales_Team'].str.lower().values:
            print("Invalid Sales Team name")
        else:
            print()
            print(f"You selected the {selected_team} Sales Team")
            break
    return selected_team


# SPARE for Development
# 6X Get Customer rating
#       Same principle being used, but now trapping a ValueError
#       if value entered is not an integer using try .. except
def get_customer_rating():
    while True:
        print_customer_rating_range()
        try:
            user_input = input("Please enter a customer rating (integer): ")
            selected_rating = int(user_input)  # Attempt to convert the input to an integer

            # Check if the entered rating exists in the DataFrame column
            if selected_rating in sales2['Customer_Rating'].values:
                print(f"Valid rating {selected_rating} entered.")
                return selected_rating
            else:
                print("Rating not found. Please enter a valid rating.")

        except ValueError:
            print("Invalid input. Please enter an integer value.")


#   7.    Get valid Start and End dates
#   Part 1 Start Date
def get_start_date():
    while True:
        selected_start_date = input("Enter a start data in the format 01-Mmm: ")
        if selected_start_date not in sales2.columns:
            print("ERROR: Start date not found")
        else:
            print(f"{selected_start_date} set as Start Date.")
            break
    return selected_start_date


#   Part 2 End Date
def get_end_date():
    while True:
        selected_end_date = input("Enter an end date in the format 01-Mmm: ")
        if selected_end_date not in sales2.columns:
            print("ERROR: End date not found")
        else:
            print(f"{selected_end_date} set as End Date")
            break
    return selected_end_date


#   9.  Class to manage the data for the enhanced search
#       so that it can be handled as a single object
class EnhancedSearchData:
    def __init__(self,
                 region_selected,
                 product_type_selected,
                 sales_team_selected,
                 start_date_selected,
                 end_date_selected):
        self.region_selected = region_selected
        self.product_type_selected = product_type_selected
        self.sales_team_selected = sales_team_selected
        self.start_date_selected = start_date_selected
        self.end_date_selected = end_date_selected


#   9. Get all the data needed for processing the enhanced search option
#       The data entered by the user will instantiate an object of
#       Class EnhancedSearchData
def harvest_enhanced_search_data():
    try:
        set_region = get_region()
        set_type = get_product_type()
        set_team = get_sales_team()
        set_start = get_start_date()
        set_end = get_end_date()

        search_data = EnhancedSearchData(set_region, set_type, set_team, set_start, set_end)

        re = search_data.region_selected
        ty = search_data.product_type_selected
        st = search_data.sales_team_selected
        sd = search_data.start_date_selected
        ed = search_data.end_date_selected

        print(f"You selected Region {re}, Type {ty}, Team {st}, between {sd} and {ed}")

        return search_data
    except:
        print("Something went wrong in the process_enhanced_search_data procedure")


#   10. Process the enhanced search
#       call this method from menu option 3.
def process_enhanced_search():
    # get the data from the user using the modularised method
    search_data = harvest_enhanced_search_data()
    # SPLIT

    # Left Hand Side
    filters = sales2.loc[:, 'Region':'Customer_Rating']
    # TODO: Debug
    print(filters)

    # Right hand side
    sales2_data = sales2.loc[:, search_data.start_date_selected:search_data.end_date_selected]
    print(sales2_data)

    # APPLY and COMBINE
    # Filter the data using the data  object
    result = pd.concat([filters, sales2_data], axis=1, join='inner').where(
        (filters['Region'].str.lower() == search_data.region_selected) &
        (filters['Type'].str.lower() == search_data.product_type_selected) &
        (filters['Sales_Team'].str.lower() == search_data.sales_team_selected))

    # Create a DataFrame we can use
    lhs = pd.DataFrame(filters)

    lhs = lhs.where((lhs["Region"].str.lower() == search_data.region_selected) & (
            lhs["Type"].str.lower() == search_data.product_type_selected))
    lhs.dropna(inplace=True)

    print("Class Data")
    print(search_data.region_selected)

    print('This is rhs')
    print(lhs)

    result = pd.DataFrame(result)

    # Remove null values and reconfigure
    result.dropna(inplace=True)

    # Do we have data to show?
    if not result.empty:
        print("There is data meeting the parameters set.")
        print(result)
        # get the mean values
        average_sales = sales2_data.mean()
        # Plot with matplotlib
        average_sales.plot(kind='bar')
        # enhance the plot
        title_string = (f"Plot for {search_data.region_selected} of {search_data.product_type_selected} "
                        f"for Sales Team {search_data.sales_team_selected}")
        plt.title = title_string
        plt.xlabel('Time period')
        plt.ylabel('Average sales')
        plt.style.use('fivethirtyeight')
        plt.show()
    else:
        print("There is no data to show for the parameters set.")


# *****************************************************************
# MENU OPTION 4: Team with the highest sales over time
# *****************************************************************

# Function to calculate the Sales_Team with the highest sales over a period
def highest_team_sales(sales_start_date, sales_end_date):
    # get column indeces
    start_index = sales2.columns.get_loc(sales_start_date)
    end_index = sales2.columns.get_loc(sales_end_date)

    # Trap date order error
    if start_index > end_index:
        raise ValueError("Start date must be before end date")

    # Sum the sales for each Sales_Team across the specified period
    sales_columns = sales2.columns[start_index:end_index + 1]
    sales2['Total_Sales'] = sales2[sales_columns].sum(axis=1)

    # Identify the Sales_Team with the highest total sales
    highest_sales_team = sales2.groupby('Sales_Team')['Total_Sales'].sum().idxmax()
    highest_sales_value = sales2.groupby('Sales_Team')['Total_Sales'].sum().max()

    # Print the formatted message before returning the values
    print(f"The Team with the highest sales is {highest_sales_team} with sales of {highest_sales_value}")

    # Return the name of the Sales_Team with the highest sales and the values
    # This is not strictly needed, but it is worth implementing now
    return highest_sales_team, highest_sales_value


def process_highest_team_sales():
    start_point = get_start_date()
    end_point = get_end_date()

    # Call the analysis method
    highest_team_sales(start_point, end_point)


# *****************************************************************
# MENU OPTION 5: Total sales over time
# *****************************************************************

"""
   This is a good way to make a block of comments.
   
   Calculates the total sales across all Sales_Teams between the specified start and end dates.

   Parameters:
   - start_date: str, the start date in the format 'dd-Mmm' (e.g., '01-Jan')
   - end_date: str, the end date in the format 'dd-Mmm' (e.g., '01-Dec')

   Returns:
   - A formatted string displaying the total sales in the specified period.
   
   Can be used in code by calling the print(total_sales_over_time()) instruction
"""


# Calculate and return a formatted message
# def total_sales_over_time(start_of_period, end_of_period):
#     # Ensure the start_date comes before the end_date
#     start_index = sales2.columns.get_loc(start_of_period)
#     end_index = sales2.columns.get_loc(end_of_period)
#     # very simple check. Error not handled
#     if start_index > end_index:
#         return "Start date must be before the end date."
#
#     # Calculate the total sales for the specified period
#     sales_columns = sales2.columns[start_index:end_index + 1]
#     total_sales = sales2[sales_columns].sum().sum()  # Double sum to get total of all sales
#
#     # Format and return the message
#     message = f"The total sales value between {start_of_period} and {end_of_period} was {total_sales}"
#     return message


def show_period_total_sales(start_date=None, end_date=None):
    """
    Asks the user for start_date and end_date, calculates the total sales for each
    of the months selected, and displays a bar chart titled "Period Total Sales".
    """
    # Since we can't use input() in this environment, we'll simulate it with function parameters
    if start_date is None:
        start_date = input("Enter the start date (format dd-Mmm, e.g., 01-Jan): ")
    if end_date is None:
        end_date = input("Enter the end date (format dd-Mmm, e.g., 01-Dec): ")

    # Validate the start_date and end_date
    if start_date not in sales2.columns or end_date not in sales2.columns:
        print("Invalid date(s) provided. Please ensure the dates match the column names.")
        return

    # Ensure the start_date comes before the end_date
    start_index = sales2.columns.get_loc(start_date)
    end_index = sales2.columns.get_loc(end_date)
    if start_index > end_index:
        print("Start date must be before the end date.")
        return

    # Calculate the total sales for each month in the selected period
    sales_columns = sales2.columns[start_index:end_index + 1]
    total_sales_by_month = sales2[sales_columns].sum()

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.style.use('fivethirtyeight')
    total_sales_by_month.plot(kind='bar', color='skyblue')
    plt.title("Period Total Sales")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Get the dates needed and then call the method.
def process_total_sales_over_time():
    start_of_period = get_start_date()
    end_of_period = get_end_date()

    # Call the method above
    show_period_total_sales(start_of_period, end_of_period)


# *****************************************************************
# MENU OPTION 6: Plot Single team sales values over time
# *****************************************************************
def show_single_team_sales(team_selected, start_date, end_date):
    """
    Displays the monthly sales for a selected team between the specified start and end dates as a bar chart.
    """
    # Validate the start_date and end_date

    # Ensure the start_date comes before the end_date
    start_index = sales2.columns.get_loc(start_date)
    end_index = sales2.columns.get_loc(end_date)
    if start_index > end_index:
        print("Start date must be before the end date.")
        return

    # Filter the DataFrame for the selected team
    team_data = sales2[sales2['Sales_Team'].str.lower() == team_selected]

    if team_data.empty:
        print(f"No data found for {team_selected}. Please check the team name.")
        return

    # Extract the sales data for the specified period
    sales_columns = sales2.columns[start_index:end_index + 1]
    monthly_sales = team_data[sales_columns].sum()

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.style.use('ggplot')
    plt.bar(monthly_sales.index, monthly_sales, color='blue')
    plt.title(f"Monthly Sales for {team_selected.upper()} from {start_date} to {end_date}")
    plt.xlabel('Month')
    plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
    plt.ylabel('Sales')
    plt.show()


def process_show_single_team_sales():
    team_selected = get_sales_team()
    start_date_selected = get_start_date()
    end_date_selected = get_end_date()

    # Use the function to display the data.
    show_single_team_sales(team_selected, start_date_selected, end_date_selected)


# *****************************************************************
# MENU OPTION 7: All team sales over time
# *****************************************************************
def all_team_sales(start_date, end_date):
    """
    Displays a bar chart with the dates on the x-axis and shows the total sales for all the teams
    using side-by-side columns for the specified period.
	"""
    # Ensure the start_date comes before the end_date
    start_index = sales2.columns.get_loc(start_date)
    end_index = sales2.columns.get_loc(end_date)
    if start_index > end_index:
        print("Start date must be before the end date.")
        return

    # Extract the sales data for the specified period
    sales_columns = sales2.columns[start_index:end_index + 1]
    df_period_sales = sales2.groupby('Sales_Team')[sales_columns].sum().T

    # Plotting
    plt.figure(figsize=(14, 8))
    plt.style.use('ggplot')
    df_period_sales.plot(kind='bar', width=0.8, figsize=(14, 8))
    plt.title(f"Total Sales by Team from {start_date} to {end_date}")
    plt.xlabel('Month')
    plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
    plt.ylabel('Total Sales')
    plt.legend(title='Sales Team')
    plt.tight_layout()  # Adjust the layout to make room for the rotated x-axis labels
    plt.show()


def process_all_team_sales():
    start_date = get_start_date()
    end_date = get_end_date()
    # Call the function
    all_team_sales(start_date, end_date)


# *****************************************************************
# MENU OPTION 8: Rank sales over time
# *****************************************************************
def print_sales_ranking(start_date, end_date):
    """
    Calculates the total sales for each Sales_Team between start_date and end_date,
    and prints each team in rank order of the sales values descending.
    """
    # Validate the start_date and end_date
    if start_date not in sales2.columns or end_date not in sales2.columns:
        print("Invalid date(s) provided. Please ensure the dates match the column names.")
        return

    # Ensure the start_date comes before the end_date
    start_index = sales2.columns.get_loc(start_date)
    end_index = sales2.columns.get_loc(end_date)
    if start_index > end_index:
        print("Start date must be before the end date.")
        return

    # Extract the sales data for the specified period and sum it up for each team
    sales_columns = sales2.columns[start_index:end_index + 1]
    team_sales = sales2.groupby('Sales_Team')[sales_columns].sum().sum(axis=1).sort_values(ascending=False)

    # Print each team and their sales in rank order
    print("Sales Team Rankings:")
    for rank, (team, sales) in enumerate(team_sales.items(), start=1):
        print(f"{rank}. {team}: {sales}")


def process_print_sales_ranking():
    start_date = get_start_date()
    end_date = get_end_date()

    # call the function
    print_sales_ranking(start_date, end_date)

# **********************************************************
# **********************************************************
# **********************************************************
# Main Menu loop
# Display menu when application launches
# **********************************************************


x = main_menu()

# Control loop to allow menu display
while x == 1 or x == 2 or x == 3 or x == 4 or x - - 5 or x == 6 or x == 7 or x == 9:
    if x == 1:
        print()
        all_data()
    elif x == 2:
        print()
        # Get the region wanted
        region = input("Please enter the name of the region you would like to check: ")
        # Allow for casing differences
        region = region.lower()
        # Check valid region
        if region in sales2["Region"].str.lower().values:
            while True:
                start_date = input("PLEASE ENTER A START DATE AS 01-Mmm: ")
                # Check valid start date
                if start_date not in sales2.columns:
                    print("ERROR: Start date not found")
                else:
                    while True:
                        end_date = input("PLEASE ENTER AN END DATE AS 01-Mmm: ")
                        # check valid end date
                        if end_date not in sales2.columns:
                            print("ERROR: End date not found")
                        else:
                            # Use the modularised analysis method
                            average_regional_sales(region, start_date, end_date)
                            break
                    break
            break
        else:
            print("region not in the data set")
    elif x == 3:
        # Enhanced search
        print()
        print("Enhanced search selected")
        process_enhanced_search()
    elif x == 4:
        # Team performance
        print()
        print("Team performance selected")
        process_highest_team_sales()
    elif x == 5:
        # Region performance
        print()
        print("Region performance selected")
        print(process_total_sales_over_time())
    elif x == 6:
        # Plot team sales over time
        print()
        print("Single Team sales analysis selected")
        process_show_single_team_sales()
    elif x == 7:
        # all teams sales analysis
        print()
        print("All teams sales analysis selected")
        process_all_team_sales()
    elif x == 8:
        # Rank the sales for teams by date
        print()
        print("Rank Team sales selected")
        process_print_sales_ranking()
    elif x == 9:
        # Exit application
        print("")
        print("----------")
        print("Exit option selected. Leaving the application")
        print("----------")
        print()
        break
    x = main_menu()
