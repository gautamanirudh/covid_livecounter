from plyer import notification
from bs4 import BeautifulSoup
import requests,time
import yagmail,keyring

html_doc = requests.get(r"https://www.mohfw.gov.in/")

soup = BeautifulSoup(html_doc.text, 'html.parser')

def notify(title,message,timeout):
    try:
        if desktopNotification==True:
            notification.notify(
                title = title,
                message = message,
                app_icon =  "./icon.ico",
                timeout = timeout
                
            )
        else:
            print("Set desktopNotification = True for desktop alert")
    
    except:
        print("Make sure plyer is install, try running pip install plyer")
        


def sendmail(content,to,fromEmail,fromEmailPass):
    try:
        if emailNotification == True:
            import yagmail


            receiver = to
            body = "Current status of people affected due to corona virus in India\nSource of information https://www.mohfw.gov.in/ \n"+content
            
            yag = yagmail.SMTP(fromEmail,fromEmailPass)
            yag.send(
                to=receiver,
                subject="Live Covid Count",
                contents=body
                
            )
            print("Email sent successfully!")

        else:
            print("set emailNotification = True for email alert")
    except:
        print("Error: Make sure you are connected to the internet\nMake sure keyring is installed successfully, try running pip install keyring")
        print("Make sure email and password entered are correct!")



states = ["Madhya Pradesh", "Delhi"]
# Add states you want to track in above states list from reference given below
# Andhra Pradesh
# Bihar
# Chhattisgarh
# Delhi
# Gujarat
# Haryana
# Himachal Pradesh
# Karnataka
# Kerala
# Madhya Pradesh
# Maharashtra
# Odisha
# Puducherry
# Punjab
# Rajasthan
# Tamil Nadu
# Telengana
# Chandigarh
# Jammu and Kashmir
# Ladakh
# Uttar Pradesh
# Uttarakhand
# West Bengal

if __name__ == "__main__":
        
    desktopNotification = True #Only for windows
    emailNotification = True
    fromEmail = "enter your email address"
    toEmail = "Email address, where you want to recieve notifications"
    fromEmailPass = "password of 'fromEmail' email"
    schedule = True   # Set it to False if you dont want to schedule this script for scheduleTimeHr hours
    scheduleTimeHr = 2  
    notifyTimeOut = 10 #seconds for which windows alert stay on screen
    while(True):
        for tableBody in soup.find_all('tbody')[1:]:
            emailmsg = ""
            for row in tableBody.find_all('tr'):
            
                templt = row.get_text().strip().split('\n')
                for state in states:
                    if state in templt:
                        print(state)
                        notify(f"{templt[1]} ",f"Number of Indians affected is {templt[2]}",notifyTimeOut)
                        time.sleep(notifyTimeOut)
                        emailmsg += f"{templt[1]} ::"+ f"Number of Indians affected is {templt[2]}\n"
                if "Total number of confirmed cases in India" in templt:
                    emailmsg += f"{templt[0]} ::" + f"{int(templt[1][:3])+int(templt[3])}\n"
                   
                    notify(f"{templt[0]} ::" ,f" {int(templt[1][:3])+int(templt[3])}\n",notifyTimeOut)
                    time.sleep(notifyTimeOut)
                # print(templt)
        sendmail(emailmsg,toEmail,fromEmail,fromEmailPass)
        if(not schedule):
            break
        else:
            time.sleep(scheduleTimeHr*3600)
        

        
    


