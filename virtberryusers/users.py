#!/usr/bin/python3
import json
from hashlib import pbkdf2_hmac
import binascii

PathToNormalConfigFile = "/etc/virtberry/config.json"
PathToUsersConfigFile = "/etc/virtberry/users.json"

class User:
    def __init__(self, userid):
        self.username = userid
        self.password = get_user_attributes(self.username, "pass")
        self.is_active_var = get_user_attributes(self.username, "active")
        self.is_anonymous_var = get_user_attributes(self.username, "anonymous")
        self.is_authenticated_var = False
        self.permissions_var = get_user_attributes(self.username, "permissions")

    def check_permissions_read(self, permissionname):
        for permission in self.permissions_var:
            if permission["role"] == permissionname:
                return permission["read"]

        # if we get here we did not found the permissionname in the config file
        return False

    def check_permissions_write(self, permissionname):
        for permission in self.permissions_var:
            if permission["role"] == permissionname:
                return permission["write"]

        # if we get here we did not found the permissionname in the config file
        return False

    def check_pass(self, password):
        self.is_authenticated_var = check_password(self.password, password)
        print("get here")


    def check_pass_return(self, password):
        return check_password(self.password, password)
        print("get here")

    def get_user_name(self):
        return self.username

    def printdata(self):
        print("self.username {}".format(self.username))
        print("self.password {}".format(self.password))
        print("self.is_authenticated {}".format(self.is_authenticated_var))
        print("self.is_active {}".format(self.is_active_var))

    def set_password(self, value):
            hashedpass = hash_password(value)
            set_user_attributes(self.username ,"pass", hashedpass)

    def get_id(self):
        return "{}".format(self.username)

    def is_authenticated(self):
            return self.is_authenticated_var

    @property
    def is_active(self):
            return self.is_active_var

    @property
    def is_anonymous(self):
            return self.is_anonymous_var

def check_if_user_exist(userid):
    with open(PathToUsersConfigFile) as file:
        data = json.load(file)
        users = data["users"]
        for user in users:
            if user["username"] == userid:
                return True

        return False

def set_user_attributes(userid ,attr, value):
    with open(PathToUsersConfigFile,"r") as file:
        data = json.load(file)
        for user in data["users"]:
            if user["username"] == userid:
                new = {}
                new.setdefault(attr, value)
                print(new)
                user.update(new)
                with open("/etc/virtberry/config.json","w") as file:
                    json.dump(data, file, indent=4)

def get_user_attributes(userid ,attr):
    with open(PathToUsersConfigFile,"r") as file:
        data = json.load(file)
        for user in data["users"]:
            if user["username"] == userid:
                return user.get(attr)



def get_user_pass_salt():
    with open(PathToNormalConfigFile,"r") as file:
        data = json.load(file)
        return data["salt"]


def hash_password(password):
    passhash = pbkdf2_hmac("sha256", bytes(password, encoding="UTF-8"), bytes(get_user_pass_salt(), encoding="UTF-8"), 200000)
    passhash = binascii.hexlify(passhash)
    return passhash.decode()

def check_password(hash, password):
    if hash_password(password) == hash:
        return True
    else:
        return False


DerUser = User("admin")


print(DerUser.check_permissions_read("users"))
print(DerUser.check_permissions_write("users"))
