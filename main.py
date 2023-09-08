from src import *

class ai_manager():
    def __init__(self,data_directory: Optional[str]=False):
        self.data_directory = data_directory
        self.driver = callUcDriver(headless=True,data_directory=data_directory)
        print("Driver created succesfully..")
    def sign_in(self,email: Optional[str] = None,password:Optional[str] = None) -> bool:
        if self.data_directory == False:
            ##get url
            print("Login starting")
            self.driver.get("https://chat.openai.com/auth/login")

            ##find login button and click it
            login_button = self.wait_element(self.driver,By.XPATH,"//button[@data-testid='login-button']",click=True,trys=2)
            if not login_button: print("There was a problem in clicking to the login button, please turn off headless mode and report the bug. "); return False

            ##get email and password inputs and fill it
            email_input = self.wait_element(self.driver,By.XPATH,"//input[@name='username']",click=True,trys=3)
            if not email_input: print("Could not click on the email section, the operation is cancelled."); return False
            email_input.send_keys(email)
            print("Email written, processing the next step.")

            self.wait_element(self.driver,By.XPATH,"//button[@type='submit']",click=True,trys=2)

            password_input = self.wait_element(self.driver,By.XPATH,"//input[@name='password']",click=True,trys=3)
            if not password_input: print("Could not click on the password section, the operation is cancelled."); return False
            password_input.send_keys(password)
            print("Password written, signing in is completed.")
        else:
            ##get url if logged in
            print("Logging in")
            self.driver.get("https://chat.openai.com/")
            logged_in = self.wait_element(self.driver,By.XPATH,"//textarea",click=False,trys=3)
            if not logged_in: print("Something went wrong in logged in, please turn off the headless mode and report the bug."); return False

        ##accept the pop-up if it appears
        self.wait_element(self.driver,By.XPATH,"//button[@as='button']",click=False,trys=1,sleep=3)
        buttons = self.driver.find_elements(By.XPATH,"//button[@as='button']")
        if len(buttons) > 4:
            buttons[-1].click()

        time.sleep(1.5)
        print("Logging in success !")
        return True
    def send_prompt(self,prompt:str,response_wait_time:int = 10) -> bool:
        ##send the promp to ai and recieve the answer
        prompt_textarea = self.wait_element(self.driver, By.XPATH, "//textarea[@id='prompt-textarea']", click=True, trys=2)
        if not prompt_textarea: print("There was a problem in the login section, please turn off headless mode and report the bug."); return False
        prompt_textarea.send_keys(prompt)
        prompt_textarea.send_keys(Keys.ENTER)

        print("Your answer is preparing...")
        ##wait for dear gpt to answer
        time.sleep(response_wait_time)

        ##not taking last answer caues it is a textarea which is we are typing our question
        answer =  self.driver.find_elements(By.XPATH,'//header/following-sibling::div')[:-1][-1].text
        print("The answer of your prompt is :\n",answer)
        print("\n")
        return True
    @staticmethod
    def wait_element(driver: webdriver,element_type,element:str,click: bool = False,trys: int = 1,sleep: int = 20)-> Union[False,webdriver.webelement]:
        while trys>0:
            try:
                if click:
                    WebDriverWait(driver, sleep).until(EC.presence_of_element_located((element_type,element))).click()
                else:
                    WebDriverWait(driver, sleep).until(EC.presence_of_element_located((element_type, element)))

                return driver.find_element(element_type, element)
            except:
                    trys-=1
        print(f"Element {element} could not be clicked.")
        return False

if __name__ == "__main__":
    print("You can use chrome profile to avoid logging in again and again. You can find the relevant section in the comment lines of the source code.")
    print("Do not forget that you will only log in with your chat gpt account, you will need to use a existing profile  for different login paths.")
    #   EN : To use the existing chrome profile you are logged in to or the existing one, you can give the path of the profile to the ai_manager class using the data_directory variable.
    #   If you encounter any errors, do not forget to open an issiue.
    #   exmple : ai_manager(data_directory="/home/linuxkerem/.config/chromium") ( the name of the folder is not important )
    #   TR  : Daha onceden kullandiginiz yada yeni olusturdugunuz bir chrome logu kullanarak giris yapma isleminden kurtulabilirsiniz, boylece her seferinde tekrar giris yapmak durumunda kalmazsiniz.
    #   yapmaniz gereken tek sey ai_manager sinifi cagirilirken degisken olarak data_directory degiskenini vermek olacaktir.
    # ornek : ai_manager(data_directory="/home/linuxkerem/.config/chromium") ( klasor isimi onemsiz )


    while True:
        choice = input("1- Log in with GPT account\n2- Use existing profile\nPlease make a choice: ")
        if choice == "1":
            mng = ai_manager()
            email = input("Please provide a email to login :")
            password = input("Please proivde a password to login :")
            break
        elif choice == "2":
            data_directory = input("Please give the path of the chrome profile you will use : ")
            mng = ai_manager(data_directory=data_directory)

            break
        else:
            print("\nPlease choose one of the options ( for exit, use Ctrl + C )")

    mng.sign_in()
    print("\n")
    while True:
        choice = input("1-Give a prompt for an answer\n2-Exit\nPlease make a choice : ")
        if choice == "1":
            prompt = input("Give your prompt: ")
            mng.send_prompt(prompt)
        elif choice == "2":
            print("Thanks for using my app, bye !")
            mng.driver.quit()
            break
        else:
            print("\nPlease choose one of the options ( for exit, use Ctrl + C )")