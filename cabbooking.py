import time
import math

# Main DB to store Driver Details
def Master_Data_Driver(Driver_Name, Driver_Contact_no, Driver_x_y_coordinates, Driver_Status, Vehicle_no,
                       Vehicle_Model_Name, Driver_Trip_Status):
    global Master_Driver
    Master_Driver[Driver_Contact_no] = [Driver_Name, Driver_x_y_coordinates, Driver_Contact_no, Driver_Status,
                                        Vehicle_no, Vehicle_Model_Name, Driver_Trip_Status]

# Main DB to store Rider Details
def Master_Data_Rider(Customer_Name, Customer_ContactNO, Status, Cust_x_y_coordinates):
    global Master_Rider
    Master_Rider[Customer_ContactNO] = [Customer_Name, Status, Cust_x_y_coordinates, Customer_ContactNO]

# Driver class
class Driver():
    def __init__(self, Driver_Name, Driver_Contact_no, Driver_Current_x_y_coordinates_in_ListFormat, Vehicle_no,
                 Vehicle_Model_Name, Driver_Status):
        self.Driver_Name = Driver_Name
        self.Driver_Contact_no = Driver_Contact_no
        self.Driver_x_y_coordinates = Driver_Current_x_y_coordinates_in_ListFormat
        self.Vehicle_Model_Name = Vehicle_Model_Name
        self.Vehicle_no = Vehicle_no
        self.Driver_Status = Driver_Status
        self.Driver_Trip_Status = False
        Master_Data_Driver(self.Driver_Name, self.Driver_Contact_no, self.Driver_x_y_coordinates, self.Driver_Status,
                           self.Vehicle_no, self.Vehicle_Model_Name, self.Driver_Trip_Status)

    # Driver account login interface
    def Driver_Account_Login_Page(self):
        print(
            f"-----------------------------\nHello, {self.Driver_Name}.Welcome to your account.Please find the account details below.\n-----------------------------\nName : {self.Driver_Name} \nContactNo : {self.Driver_Contact_no} \nVehicle No : {self.Vehicle_no}\nVehicle Model Name: {self.Vehicle_Model_Name}\nCab location : {self.Driver_x_y_coordinates}")
        if self.Driver_Status:
            print("Current Status : Available to accept a ride-----------------------------")
        else:
            print("Current Status : Unavailable to accept a ride\n-----------------------------")
    
        while True:
            try:
                x = int(input(
                    f"Please select an option from below and given option number as input \n 1.To change your Status \n 2.To update your Cabs location \n 3.To exit from your account and go to Main interface\n"))
                break
            except Exception:
                print("XXXX - Wrong input. Please try again - XXXX")
            
        if x == 1:
            self.Driver_Status_Updation()

        elif x == 2:
            self.Driver_Location_Updation()

        elif x == 3:
            Main_Interface()

        else:
            print("XXXX - Wrong input. Please try again - XXXX")
            self.Driver_Account_Login_Page()
        
    # Function to update availability status of driver
    def Driver_Status_Updation(self):
        global Master_Driver
        if Master_Driver[self.Driver_Contact_no][6] == True:
            print(
                "----------------------------------------------------\nYou currently have an ongoing trip. You can only change your status once your trip is completed. Please try when this trip ends.\n----------------------------------------------------")
            self.Driver_Account_Login_Page()
        else:
            y = input("Please enter AVAILABLE OR UNAVAILABLE : ").upper()
            if y == "UNAVAILABLE":
                Master_Driver[self.Driver_Contact_no][3] = False
                self.Driver_Status = False
                print(
                    "Your current status is : UNAVAILABLE, \n To recieve bookings please change your status.Thank you")
                print("----------------------------------------------------")
                self.Driver_Account_Login_Page()
            elif y == "AVAILABLE":
                Master_Driver[self.Driver_Contact_no][3] = True
                self.Driver_Status = True
                print(
                    "Your current status is : AVAILABLE, \n You will be assigned to the nearest rider as soon as a new booking requirement comes.\n Thank You")
                print("----------------------------------------------------")
                self.Driver_Account_Login_Page()
            else:
                print("XXXX - Wrong input. Please try again - XXXX")
                self.Driver_Status_Updation()
    
    # Function to update driver location
    def Driver_Location_Updation(self):
        if Master_Driver[self.Driver_Contact_no][6] == True:
            print(
                "----------------------------------------------------\nYou cannot update coordinates while your current trip is not ended.\n Please try after customer ends the trip\n----------------------------------------------------")
            self.Driver_Account_Login_Page()

        else:
            while True:
                try:
                    self.Driver_x_y_coordinates = list(
                        map(float, input("To update your location -> Please enter x , y coordinates with spaces").split()))
                    if self.Driver_x_y_coordinates == [] or self.Driver_x_y_coordinates[0] == None or \
                            self.Driver_x_y_coordinates[1] == None:
                        raise Exception()
                    break
                except Exception:
                    print("XXXX - Wrong input. Please try again - XXXX")
            Master_Driver[self.Driver_Contact_no][1] = self.Driver_x_y_coordinates
            print("Cool, Your new coordinates have been updated sucessfully.")
            self.Driver_Account_Login_Page()

# Rider class
class Rider(Driver):
    def __init__(self, Cust_name, Cust_Contact_no, Cust_x_y_coordinates):
        self.Cust_name = Cust_name
        self.Cust_Contact_no = Cust_Contact_no
        self.Cust_x_y_coordinates = Cust_x_y_coordinates
        self.Trip_Details = {}
        self.Trip_ID = None
        self.Search_Status = None
        self.Cust_Status = True
        self.Cur_Driver_Key = None
        Master_Data_Rider(self.Cust_name, self.Cust_Contact_no, self.Cust_Status, self.Cust_x_y_coordinates)

    # Rider account login interface
    def Rider_Account_Login_Page(self):
        print(
            f"----------------------------------------------------\nHello, {self.Cust_name}.Welcome to your account.Please find your account details below.\n----------------------------------------------------")
        print(
            f"Name : {self.Cust_name}\nContact No : {self.Cust_Contact_no}\nYour current Position : {self.Cust_x_y_coordinates} ")
        while True:
            try:
                no = int(input(
                    "Please select an option from below. Please choose option number as your input \n 1 - New Booking \n 2 - History of all previous rides \n 3 - End current ongoing trip  \n 4 - Exit from your account\n"))
                break
            except Exception:
                print("XXXX - Wrong input. Please try again - XXXX")

        if no == 1:
            self.Booking()

        if no == 2:
            self.History()

        if no == 3:
            self.End_Trip()

        if no == 4:
            Main_Interface()
        else:
            print("XXXX - Wrong input. Please try again - XXXX")
            self.Rider_Account_Login_Page()
    
    # Function to search the nearest available Driver
    def Availability_Search(self):
        global Master_Driver
        flag = 0
        for key, value in Master_Driver.items():
            if value[3] == True:
                Distance_Calculator = math.sqrt(
                    ((Master_Driver[key][1][0] - Master_Rider[self.Cust_Contact_no][2][0]) ** 2) + (
                                (Master_Driver[key][1][1] - Master_Rider[self.Cust_Contact_no][2][1]) ** 2))
                if Distance_Calculator > 10:
                    flag = 1
                    continue
                else:
                    value[3] = False
                    value[6] = True
                    return key
        return flag

    # Function to book a nearest driver for the rider
    def Booking(self):
        global Master_Driver
        while True:
            try:
                self.Cust_x_y_coordinates = list(map(float, (input(
                    "----------------------------------------------------\nPlease enter your current cordinates x , y with spaces ").split())))
                if self.Cust_x_y_coordinates == [] or self.Cust_x_y_coordinates[0] == None or self.Cust_x_y_coordinates[
                    1] == None:
                    raise Exception
                break
            except Exception:
                print("XXXX - Wrong input. Please try again - XXXX")
        Master_Rider[self.Cust_Contact_no][2] = self.Cust_x_y_coordinates
        self.Search_Status = self.Availability_Search()

        if Master_Rider[self.Cust_Contact_no][1] == False:
            print(
                "----------------------------------------------------\nYou cannot book another ride while your current ride is still ongoing.\n Please end the trip to finish current ride and book another\n----------------------------------------------------")
            self.Rider_Account_Login_Page()
        elif self.Search_Status == 0:
            print(
                "----------------------------------------------------\nNo Cab Drivers are available at this time.Please try after sometime.We regret the inconvenice caused\n----------------------------------------------------")
            self.Rider_Account_Login_Page()
        elif self.Search_Status == 1:
            print(
                "----------------------------------------------------\nThere are no nearest Cabs available.Please try after Sometime\n----------------------------------------------------")
            self.Rider_Account_Login_Page()
        else:
            global x
            global Current_Live_Booking_Data
            Master_Rider[self.Cust_Contact_no][1] = False
            Master_Driver[self.Search_Status][5] = True
            Master_Driver[self.Search_Status][3] = False
            self.Trip_ID = int(str(self.Cust_Contact_no)[6:10])
            for y in self.Trip_Details.keys():
                if self.Trip_ID == y:
                    self.Trip_ID += 1

            Current_Live_Booking_Data[self.Trip_ID] = {"Trip_ID": self.Trip_ID,
                                                       "Driver_Name": Master_Driver[self.Search_Status][0],
                                                       "Rider_name": self.Cust_name,
                                                       "Vehicle_No": Master_Driver[self.Search_Status][4], "Date": x}
            self.Trip_Details[self.Trip_ID] = {"Trip_ID": self.Trip_ID,
                                               "Driver_Name": Master_Driver[self.Search_Status][0],
                                               "Vehicle_No": Master_Driver[self.Search_Status][4],
                                               "Driver_Contact_no": Master_Driver[self.Search_Status][2], "Date": x}
            print("Your Booking is confirmed \n", "your Trip_ID is : ", self.Trip_ID, "\n", "Your Driver name is : ",
                  Master_Driver[self.Search_Status][0], "\n", "Vehicle_No : ", Master_Driver[self.Search_Status][4],
                  "\n", "Driver_Contact_no :", Master_Driver[self.Search_Status][2], "\n", "Date : ", x)
            self.Cur_Driver_Key = self.Search_Status
            self.Rider_Account_Login_Page()
    
    # Function to end Rider trip
    def End_Trip(self):
        if Master_Rider[self.Cust_Contact_no][1] == True:
            print(
                "----------------------------------------------------\nThere is no ogoing trip to end.\n----------------------------------------------------")
            self.Rider_Account_Login_Page()
        else:
            Master_Rider[self.Cust_Contact_no][1] = True
            Master_Driver[self.Cur_Driver_Key][3] = True
            Master_Driver[self.Cur_Driver_Key][5] = False
            Current_Live_Booking_Data.pop(self.Trip_ID)

            print(
                "----------------------------------------------------\nYour Trip is ended.Thank you.\n----------------------------------------------------")
            self.Rider_Account_Login_Page()