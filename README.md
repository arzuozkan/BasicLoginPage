# BasicLoginPage
The purposes of the login page development is pentesting for the any vulnerability and finding how to patch them.

# Development Phase
## Login, Register and Profile Pages
![image](https://user-images.githubusercontent.com/48025290/184535497-1f20d385-2706-4aff-a09c-573cc1fcf691.png)

## Modules
* Flask-login, user session management and authentication
* Flask-SQLAlchemy, user information storage and database operations

# Vulnerability Scanning Phase

## 1. Flask Weak Secret Key

The secret key can be found when it is weak and predictable by using `flask-unsign` tool. The output of the tool includes decoding cookie content and secret key. After changing the cookie data, another session becomes accessible.

![unsign](https://user-images.githubusercontent.com/48025290/185180415-277e6d8a-28ce-4f11-9799-5dedfec98ad7.png)

The user_id part of the decoded cookie is changed to 3 and signed with a previosly found secret key.

![sign](https://user-images.githubusercontent.com/48025290/185186491-c852ee85-0275-4036-a138-c6eddf5ee96f.png)

Attacker can access other users session with tampered cookie.

As mitigation, secret key must random and long enough. The commands shown in the image can be given as an example of secret key generation.

![image](https://user-images.githubusercontent.com/48025290/185179799-3f8cb239-66c4-4ef8-9b79-49f34c985dc4.png)


- [ ] TODO: coming soon
