# added notes for main parts for those who don't understand

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import requests
import json

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
    
    def setup_window(self):
        self.setWindowTitle("Roblox User Lookup")
        self.setGeometry(100, 100, 500, 400)
        
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        # label for input
        label = QtWidgets.QLabel("Enter username or ID:")
        layout.addWidget(label)
        
        # input box
        self.input_box = QtWidgets.QLineEdit()
        self.input_box.setPlaceholderText("type username or ID")
        layout.addWidget(self.input_box)
        
        # search button
        button = QtWidgets.QPushButton("Search")
        button.clicked.connect(self.search_user)
        layout.addWidget(button)
        
        # text display
        self.text_box = QtWidgets.QTextEdit()
        self.text_box.setReadOnly(True)
        layout.addWidget(self.text_box)
        
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def search_user(self):
        query = self.input_box.text()
        
        if not query:
            self.text_box.setText("Error: empty input")
            return
        
        # check if its a number or username
        if query.isdigit():
            user_id = query
        else:
            # convert username to id
            user_id = self.get_id_from_username(query)
            if user_id is None:
                self.text_box.setText("Error: user not found")
                return
        
        # get all the data
        self.get_user_data(user_id)
    
    def get_id_from_username(self, username):
        try:
            url = "https://users.roblox.com/v1/usernames/users"
            payload = {"usernames": [username]}
            response = requests.post(url, json=payload, timeout=10)
            data = response.json()
            
            if data.get("data") and len(data["data"]) > 0:
                return str(data["data"][0]["id"])
            return None
        except:
            return None
    
    def get_follower_count(self, user_id):
        try:
            url = f"https://friends.roblox.com/v1/users/{user_id}/followers/count"
            response = requests.get(url, timeout=10)
            data = response.json()
            return data.get("count")
        except:
            return "error"
    
    def get_friends_count(self, user_id):
        try:
            url = f"https://friends.roblox.com/v1/users/{user_id}/friends/count"
            response = requests.get(url, timeout=10)
            data = response.json()
            return data.get("count")
        except:
            return "error"
    
    def get_following_count(self, user_id):
        try:
            url = f"https://friends.roblox.com/v1/users/{user_id}/followings/count"
            response = requests.get(url, timeout=10)
            data = response.json()
            return data.get("count")
        except:
            return "error"
    
    def get_groups_count(self, user_id):
        try:
            url = f"https://groups.roblox.com/v1/users/{user_id}/groups/roles"
            response = requests.get(url, timeout=10)
            data = response.json()
            groups = data.get("data", [])
            return len(groups)
        except:
            return "error"
    
    def get_user_data(self, user_id):
        try:
            url = f"https://users.roblox.com/v1/users/{user_id}"
            response = requests.get(url, timeout=10)
            user_data = response.json()
            
            username = user_data.get("name", "unknown")
            display_name = user_data.get("displayName", "unknown")
            created = user_data.get("created", "unknown")
            banned = user_data.get("isBanned", False)
            verified = user_data.get("verified", False)
            
            # get the numbers
            followers = self.get_follower_count(user_id)
            friends = self.get_friends_count(user_id)
            following = self.get_following_count(user_id)
            groups = self.get_groups_count(user_id)
            
            # put it all together
            result = f"Username: {username}\n"
            result += f"Display Name: {display_name}\n"
            result += f"User ID: {user_id}\n"
            result += f"Created: {created}\n"
            result += f"Banned: {banned}\n"
            result += f"Verified: {verified}\n"
            result += f"\n"
            result += f"Followers: {followers}\n"
            result += f"Following: {following}\n"
            result += f"Friends: {friends}\n"
            result += f"Groups: {groups}\n"
            
            self.text_box.setText(result)
        except Exception as e:
            self.text_box.setText(f"Error: {str(e)}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
