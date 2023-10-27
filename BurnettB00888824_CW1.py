""" Inventory codebase for Simply Screws ltd. 
    Author: Jack Burnett. B-code: B00888824
    
    !!! OLD data_file.txt DATA FILE USED !!!
    
    Python interpreter used: 3.6.0 64-bit
        3.6 needed for both matplotlib and f-strings to function

    Important details:
    - Unit of stock = 50 screws
    - A "screw combo" in this codebase means a screw "category" of
      material, head-type and length e.g brass, slot, 20
    - lst_screws_list is a list of lists, lst_screws_list[x] contains
      details of a specific screw combo
      e.g ['brass', 'slot', '20', '35', '20', '10', '4.00']
    - lst_screws_list[x][n] shows a specific value, where:
    [x][0]: MATERIAL
    [x][1]: HEAD TYPE
    [x][2]: LENGTH (mm)
    [x][3]: STOCK OF 50s
    [x][4]: STOCK OF 100s
    [x][5]: STOCK OF 200s
    [x][6]: COST PER BOX OF 50s (£) i.e unit price
"""
import os  # Used to remove file after update
import matplotlib.pyplot as plt  # Used to draw a bar chart 
# Global variables
UNIT_OF_STOCK = 50  # How many screws are considered to be 1 unit
MATERIALS_LIST = ["brass", "steel"]
HEAD_TYPES_LIST = ["slot", "star", "pozidriv"]
LENGTHS_LIST = ["20", "40", "60"]
# REFACTORED, populates SCREW_COMBO_LIST
# SCREW_COMBO_LIST = []
# for material in MATERIALS_LIST:  
#     for head in HEAD_TYPES_LIST:
#         for length in LENGTHS_LIST:
#             SCREW_COMBO_LIST.append([material, head, length])
SCREW_COMBO_LIST = [[material, head, length] for material in MATERIALS_LIST \
                    for head in HEAD_TYPES_LIST for length in LENGTHS_LIST]
# SCREW_COMBO_LIST contains all possible combinations of screws
SPECIAL_DISCOUNT = 0.9  # Discount on combo with highest stock
                        # 0.9 = 10% off, 0.8 = 20% off etc
special_discount_screw = ["", "", ""]  # Material, Head, Length
# ^ Holds the highest-stocked screw combo after feature(5) is accessed
                                  
def main():
    # Full inventory list used in functions:
    lst_screws_list = file_to_list_of_lists()
    
    # Kills program if we didn't get to open the file
    if lst_screws_list == []:
        return
    
    selection = 0
    # MAIN MENU
    while selection != 7:
        selection = 0
        print("\nMain menu: \n" \
              "1. Print report of available screw types\n" \
              "2. Print report of screws by length\n" \
              "3. Print report of screws of inputted length\n" \
              "4. Increase or decrease stock in file\n" \
              "5. View and/or apply special discount\n" \
              "6. View a bar chart of units of screws by length\n" \
              "7. Exit the program")
        while selection not in [1, 2, 3, 4, 5, 6, 7]:
            selection = input_integer("Type '1','2','3','4','5','6' or '7': ")
        print("")  # Line break
        if selection == 1:
            # Do task 1
            show_screw_types(lst_screws_list)
        elif selection == 2:
            # Do task 2
            show_total_units_of_length(lst_screws_list)
        elif selection == 3:
            # Do task 3
            length = "0"
            while length not in LENGTHS_LIST:
                length = input(f"Input length (mm) from " \
                               f"{list_to_string(LENGTHS_LIST)}: ")
            print("")
            show_screw_types_with_length(length)
        elif selection == 4:
            # Do task 4
            check_stock_level(lst_screws_list)
        elif selection == 5:
            # Do task 5
            check_highest_stock_level(lst_screws_list)
        elif selection == 6:
            # Do task 6
            units_in_lengths_barchart(lst_screws_list)

    # print(f"New discount applied to {special_discount_screw}")  # Test
    print("Ending........")
    
    # main end


def file_to_string_list():  
    """ Writes each line in data_file.txt as
        a string in a list, removing the comments.
        Returns empty list if file not found.
        (data file -> list of strings)
        Return type: list[str]
    """
    # list = []  # removed as part of refactor below
    try: # Open file in try-catch block
        screws_file = open("data_file.txt", "r")
        # REFACTORED, reads file and puts line into list
        # while line!='':
        #     if line[0]!='#':
        #         screwsList.append(line)
        #     line = screwsFile.readline().rstrip('\n')
        # -------------------------------------------------------------
        # for line in screwsFile:
        #     if line[0]!='#':
        #         screwsList.append(line)
        list = [line.rstrip('\n') for line in screws_file if line[0]!='#']
        screws_file.close()
    except FileNotFoundError:
        print("Couldn't open stock file, try changing the directory" \
              " in the file_to_string_list() function")
        return []
    return list

def file_to_list_of_lists():  
    """ Uses file_to_string_list() to get a list of strings
        from the data, then converts each string to a list.
        (data file -> list of lists)
        Return type: list[list]
     """
    list = file_to_string_list()  
    list = [item.split(',') for item in list]  
    return list

def show_screw_types(list):  # Basic, Feature 1
    """ Prints a summary of the current inventory, with each combo in
        its own section, as well as a summation of the total inventory.
        Can now also act as a general screw-list report output function.
        Input type: list[list]
        Return type: N/A
    """
    inv_value = inv_value_disc = inv_units = 0
    for screw_type in list:
    # screw_type e.g: ['brass', 'slot', '20', '35', '20', '10', '4.00']
        total_units = int(screw_type[3]) + int(screw_type[4])*2 \
                      + int(screw_type[5])*4
        inv_units += total_units
        total_value = total_units*float(screw_type[6])
        inv_value += total_value
        total_value_disc = total_value - ((int(screw_type[4])*2*0.1 \
                           + int(screw_type[5])*4*0.15)*float(screw_type[6]))
        inv_value_disc += total_value_disc

        # REMOVED print(f"Screw ID: {list.index(screw_type) + 1}")
        # Screw ID was a potential identifier that I ended up not using
        print(f"Screw combo: {screw_type[0].title()}, {screw_type[1]} head, " \
              f"Length (mm): {screw_type[2]}, Cost per unit: £{screw_type[6]}")
        print(f"50-Boxes: {screw_type[3]}, 100-Boxes: {screw_type[4]}, "\
              f"200-Boxes: {screw_type[5]}")
        print(f"Combo units (100-box=2, 200-box=4) = {total_units} units")
        print(f"Combo value without discounts = £{total_value:,.2f}")
        print(f"Combo value with bulk discount = £{total_value_disc:,.2f}\n")

    if len(list) == len(SCREW_COMBO_LIST):
        # Only outputs this block if the list being worked on
        # is the full inventory list of screws
        print(f"Inventory units (100-box=2, 200-box=4): {inv_units} units")
        print(f"Inventory value without discounts: £{inv_value:,.2f}")
        print(f"Inventory value with bulk discount: £{inv_value_disc:,.2f}\n")

def show_total_units_of_length(list):  # Basic, Feature 2
    """ Writes a report showing the total
        number of units in stock in each length category
        Input type: list[list]
        Return type: N/A
    """
    # dict = {x:"cvcu", y:"hw08eh2io0"}
    # TESTED: Compared results for total units to show_screw_types()
    # result: 3176 units = 859 + 1207 + 1110. Working ^_^
    for length in LENGTHS_LIST:
        print(f"Stock of screws of length: {length} mm")
        box_50_amount = sum(int(screw[3]) for screw in list \
                        if screw[2]==length)
        box_100_amount = sum(int(screw[4]) for screw in list \
                        if screw[2]==length)
        box_200_amount = sum(int(screw[5]) for screw in list \
                        if screw[2]==length)
        total_units = box_50_amount + box_100_amount*2 + box_200_amount*4
        print(f"50-boxes: {box_50_amount}, 100-boxes: {box_100_amount}" \
            f", 200-boxes: {box_200_amount}")
        print(f"Total units (100-box=2, 200-box=4): {total_units} units\n")
        
def show_screw_types_with_length(length):  # Basic, Feature 3
    """ Prints list of screw combos with a user defined length.
        Input type: str
        Return type: N/A
    """
    full_list = file_to_list_of_lists()  # Gets full list, will reduce below:
    length_sorted_list = [screw for screw in full_list if screw[2]==length]
    show_screw_types(length_sorted_list)

def input_screw_combo():
    """ Function to process the user inputting a single screw combo.
        (Just added in case I want to update a function to use this)
        Return type: list[str]
    """
    material = ""
    head = ""
    length = ""
    # Repeatedly asks for inputs until the user gets it right. 
    while material not in MATERIALS_LIST:
        material = input(f"Input the material you want from " \
                         f"{MATERIALS_LIST}: ")
    while head not in HEAD_TYPES_LIST:
        head = input(f"Input the head-type you want from " \
                     f"{HEAD_TYPES_LIST}: ")
    while length not in LENGTHS_LIST:
        length = input(f"Input the length (mm) you want from " \
                       f"{LENGTHS_LIST}: ")
    print(f"Chosen: {[material, head, length]}\n")
    return [material, head, length]

def check_stock_level(list):  # Adv, feature 4
    """ Checks to see if a user-inputted screw combo has stock left.
        Moves to update stock level if stock exists
        Input types: list[list]
        Return type: N/A
    """
    user_list = input_screw_combo()
    # Find the inputted screw combo in the inventory screw list
    matched_screw = [screw for screw in list \
                    if user_list[0] == screw[0] \
                    and user_list[1] == screw[1] \
                    and user_list[2] == screw[2]][0]
    # print(matched_screw)  # test
    show_screw_types([matched_screw])
    box_size = ""
    print("Which box size would you like?")
    while box_size not in ["50", "100", "200"]:
        box_size = input("Input '50' for small box, "\
                         "'100' for medium, '200' for large: ")
    # Get index for given box size
    box_index = 3 if box_size == "50" else 4 if box_size == "100" else 5
    
    update_file(list, matched_screw, box_index)  # File change function

def update_file(list, matched_screw, box_index):
    """ Changes a value in the inventory file list, after asking if
        this is for increasing or decreasing stock
        Input types: list[list], list[str], int
        Return type: N/A
    """
    inc_or_dec = ""
    change = 0
    while inc_or_dec not in ["increase","decrease"]:
        print("Would you like to increase, or decrease the stock for a sale?")
        inc_or_dec = input("Type 'increase' or 'decrease': ").lower()
        
    if inc_or_dec == 'increase':
        print("Increasing:")
    else:
        # Check to see if that combo has boxes left in the requested box-size
        if list[(list.index(matched_screw))][box_index] != "0":
            # print(f"{matched_screw}, {box_index}, ")  # test
            print("We have that screw in that box size!")
            print("Decreasing:")
        else:
            print("Unfortunately, we don't have that in stock")
            return  # Gets us out of the file writing function immediately
        

    temp_file = open("temp_data_file.txt", "w")
    temp_file.truncate()  # removes all lines from file
    temp_file.write("#Listing showing screw stock details\n#MATERIAL, HEAD" \
                    " TYPE, LENGTH, STOCK(IN BOXES OF 50,100,200)," \
                    " COST PER BOX of 50 (Â£)\n")  # The comment lines on top
    for screw in list:  # Screw in master list
        if screw != matched_screw:
            temp_file.write(f"{list_to_string(screw)}\n")
            
        else:  # This is the rewrite block:
            if inc_or_dec=='increase':
                change = input_integer( \
                        "Input no. of boxes you want to increase this by: ")
                matched_screw[box_index] = str(int( \
                                            matched_screw[box_index])+change)
                temp_file.write(f"{list_to_string(matched_screw)}\n")
                
            else:  # Sale
                matched_screw = process_sale(matched_screw, box_index)
                temp_file.write(f"{list_to_string(matched_screw)}\n")
                
    temp_file.close()
    # Delete the original data_file.txt file.
    os.remove('data_file.txt')
    # Rename the temporary file.
    os.rename('temp_data_file.txt', 'data_file.txt')
        
def process_sale(matched_screw, box_index):
    """ Uses params from update_file() to process possible outcomes
        for sales.
        Input type: list[str], int
        Return type: list[str]
    """
    change = input_integer( \
            "Input no. of boxes you want to decrease this by: ")
    # If we are trying to sell more than we have:
    if change > int(matched_screw[box_index]):
        print("We don't have enough boxes to fulfil that order")
        print(f"Would you like to sell {int(matched_screw[box_index])}" \
              f" boxes instead?")
        choice = ""
        while choice not in ['y', 'n']:
            choice = input("Input 'y' for yes, 'n' for no: ").lower()
            
        disc = 1    
        if choice == 'n':  # returns the original screw with no change
            print("No sale")
            return matched_screw
        else:
            change = int(matched_screw[box_index])  # equal to remaining boxes
            # Discounts:
            if box_index == 4:
                disc *= 0.9
            elif box_index == 5:
                disc *= 0.85
            if special_discount_screw == [matched_screw[0], \
                                          matched_screw[1],matched_screw[2]]:
                print("This screw is on special discount!!")
                disc*=SPECIAL_DISCOUNT  # Apply special discount if it's there
            unit_price_times_box = float(matched_screw[6])*(2**(-3+box_index))
            print(f"Cost of sale: £" \
                  f"{change*disc*unit_price_times_box:,.2f}")
            #2**(-3+box_index) will give either 2**0 =1, 2**1 =2, or 2**2 =4
            matched_screw[box_index] = "0"  # Sold them all ^_^
            return matched_screw
    else:  # Full sale confirmation
        print(f"Are you sure you want to sell {change} boxes of " \
              f"{matched_screw[0]}-{matched_screw[1]}-{matched_screw[2]} ?")
        choice = ""
        while choice not in ['y', 'n']:
            choice = input("Input 'y' for yes, 'n' for no: ").lower()
        
        disc = 1
        if choice == 'n':
            print("No sale")
            return matched_screw
        else:
            # Discounts:
            if box_index == 4:
                disc *= 0.9
            elif box_index == 5:
                disc *= 0.85
            if special_discount_screw == [matched_screw[0], \
                                          matched_screw[1],matched_screw[2]]:
                print("This screw is on special discount!!")
                disc*=SPECIAL_DISCOUNT  # Apply special discount if it's there
            unit_price_times_box = float(matched_screw[6])*(2**(-3+box_index))
            print(f"Cost of sale: £" \
                  f"{change*disc*unit_price_times_box:,.2f}")
            #2**(-3+box_index) will give either 2**0 =1, 2**1 =2, or 2**2 =4
            change_str = str(int(matched_screw[box_index])-change)
            matched_screw[box_index] = change_str
            return matched_screw
        
def list_to_string(list):
    """ Converts a list[str] to a single string to fit into data_file.txt
        e.g ["brass", "slot", "40"] -> "brass,slot,40"
        Input type: list[str]
        Return type: str
    """
    out = ""
    for str in list:
        if str != list[-1]:  # Not the last list item -> add a comma
            out += str+","
        else:
            out += str  # Last item -> no comma
    return f"{out}"
        
def input_integer(msg):
    """ General int input handler with a message param
        Input type: str
        Return type: int
    """
    integer = 0
    while True:
        try:
            integer = int(input(f"{msg}"))
            break
        except:
            print("You have to type an integer, not anything else :D")
    return integer

def check_highest_stock_level(list):  # Adv, feature 5
    """ Finds the screw combo with the highest amoount of units.
        Asks user if they want to remove current discount if it exists.
        Can apply the special discount by assigning the combo to
        special_discount_screw via apply_special_discount().
        Input type: list[list]
        Return type: N/A
    """
    global special_discount_screw  # Uses global variable on assignment
    highest_units_total = 0
    highest_combo = ["", "", ""]
    
    for screw in list:  # Gets the combo with the most units
        total_units = int(screw[3]) + int(screw[4])*2 \
                      + int(screw[5])*4
        #print(f"test,{total_units},{highest_units_total},{highest_combo}")
        if total_units > highest_units_total:
            highest_units_total = total_units
            highest_combo = [screw[0], screw[1], screw[2]]
            
    # If there is a discount already, asks user to remove or keep it
    if special_discount_screw != ["","",""]:
        user_input = input(f"Type 'y' to remove the current discount " \
                    f"that is currently on {special_discount_screw}, and " \
                    f"apply a new one to a different screw combo\n" \
                    f"Or type anything else to not do that: ").lower()
        
        if user_input == 'y':
            print("Removing discount....")
            # Runs the apply option function
            special_discount_screw = apply_special_discount(highest_combo)
            
        else:  # No changes are made if the user doesn't remove the discount
            print("Discount was left as it was")
    else:  # If no discount exists, runs the apply option function
        special_discount_screw = apply_special_discount(highest_combo)
        
def apply_special_discount(highest_combo):  # Adv, feature 5
    """ Applies the special discount from check_highest_stock_level()
        if the user requests to do so
        Input type: list[str]
        Return type: list[str]
    """
    user_input = input(f"Type 'y' to apply a {100-(SPECIAL_DISCOUNT*100)}" \
                    f" % discount to {highest_combo}\n" \
                    f"Or type anything else to not do that: ").lower()
    if user_input == 'y':
        print(f"Discount was applied to {highest_combo}")
        return highest_combo
    else:
        print("No discount was applied...")
        return ["","",""]
            
def units_in_lengths_barchart(list):  # Adv, feature 6
    """ Prints a bar chart showing the number of units available,
        with a bar being a length of screw.
        Input type: list[list]
        Return type: N/A
    """
    box_50_amount = 0  # Units in each box size
    box_100_amount = 0
    box_200_amount = 0
    units_list = []  # Will contain number of units in each length
    
    for length in LENGTHS_LIST:
        box_50_amount = sum(int(screw[3]) for screw in list \
                        if screw[2]==length)
        box_100_amount = sum(int(screw[4]) for screw in list \
                        if screw[2]==length)
        box_200_amount = sum(int(screw[5]) for screw in list \
                        if screw[2]==length)
        total_units = box_50_amount + box_100_amount*2 + box_200_amount*4
        units_list.append(total_units)
    plt.bar(LENGTHS_LIST, units_list, color="grey", edgecolor="blue")
    plt.xlabel("Lengths of screws (mm)")
    plt.xticks(rotation=10)
    plt.ylabel("Number of units (50 screws/unit)")
    plt.show()

main()