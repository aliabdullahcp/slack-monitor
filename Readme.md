# Slack API

# Context.
1. Each Direct Message, Group Chat, Private Channel or Public channel has a channel ID.
2. You can get the channel ID opening that specific group chat/DM or channel. Click on the title at the top. In `About` Section. You can find it at the bottom. (Check Screenshot1.png for reference.)

3. You will also require User ID of users. Check the Screenshot2.png for reference. `You can add multiple member ids`


### How to run
1. Make sure you have python installed on your machine [See Here](https://www.python.org/downloads/)
2. Rename the `.env.example` file to `.env` file.
3. Update the `.env` files values with your desired Channel IDs and UserIDs
4. Open the terminal/powershell in the same folder and run the following command
```
python main.py
```