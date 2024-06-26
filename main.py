from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from dotenv import load_dotenv
import json
load_dotenv()
SLACK_TOKEN = os.getenv("SLACK_TOKEN")

# User IDS for the users
USER_IDS = json.loads(os.getenv("USER_IDS"))
# List of specific public/private channels to fetch messages from
SPECIFIED_CHANNELS = json.loads(os.getenv("SPECIFIED_CHANNELS"))
# SPECIFIED_DMS_AND_GROUPS = json.loads(os.getenv("SPECIFIED_DMS_AND_GROUPS"))
# create the client
client = WebClient(token=SLACK_TOKEN)


def get_all_channels_and_groups():
    try:
        # Fetch all public channels
        public_channels = client.conversations_list(
            types='public_channel')['channels']
        public_channels_info = [
            {'name': channel['name'], 'id': channel['id']} for channel in public_channels]

        # Fetch all private channels
        private_channels = client.conversations_list(
            types='private_channel')['channels']
        private_channels_info = [
            {'name': channel['name'], 'id': channel['id']} for channel in private_channels]

        # Fetch all group chats (multiparty direct messages)
        group_chats = client.conversations_list(types='mpim')['channels']
        group_chats_info = [{'name': chat['name'], 'id': chat['id']}
                            for chat in group_chats]

        # Fetch all direct messages
        dms = client.conversations_list(types='im')['channels']
        dms_info = [{'id': dm['id'], 'user': dm['user']} for dm in dms]
        return {
            'public_channels': public_channels_info,
            'private_channels': private_channels_info,
            'group_chats': group_chats_info,
            'dms': dms_info
        }
        # return {
        #     'public_channels': len(public_channels_info),
        #     'private_channels': len(private_channels_info),
        #     'group_chats': len(group_chats_info),
        #     'dms': len(dms_info)
        # }

    except SlackApiError as e:
        print(f"Error fetching channels and groups: {e.response['error']}")
        return None


def get_user_message_counts(channel_id, user_ids):

    user_message_counts = {user_id: 0 for user_id in user_ids}

    try:
        # Fetch the channel messages
        response = client.conversations_history(channel=channel_id)
        messages = response['messages']

        # Include replies by fetching thread replies
        for message in messages:
            user = message.get('user')
            if user in user_message_counts:
                user_message_counts[user] += 1

            # Check if the message has replies
            if 'thread_ts' in message:
                thread_response = client.conversations_replies(
                    channel=channel_id, ts=message['thread_ts'])
                thread_messages = thread_response['messages']
                for thread_message in thread_messages:
                    thread_user = thread_message.get('user')
                    if thread_user in user_message_counts:
                        user_message_counts[thread_user] += 1
                user_message_counts[thread_user] -= 1

    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")

    return user_message_counts


def get_channel_name(channel_id):
    try:
        response = client.conversations_info(channel=channel_id)
        channel_name = response['channel']['name']
        return channel_name
    except SlackApiError as e:
        print(f"Error fetching channel name: {e.response['error']}")
        return None
    
def get_channel_info(channel_id):
    try:
        response = client.conversations_info(channel=channel_id)
        channel = response['channel']
        return channel
    except SlackApiError as e:
        print(f"Error fetching channel name: {e.response['error']}")
        return None


def get_user_name(user_id):
    try:
        response = client.users_info(user=user_id)
        user_name = response['user']['real_name']
        return user_name
    except SlackApiError as e:
        print(f"Error fetching user name: {e.response['error']}")
        return None

def get_dm_messages():
     # Fetch list of direct message channels
    try:
        im_result = client.conversations_list(types="im")
        ims = im_result['channels']
    except SlackApiError as e:
        print(f"Error fetching direct messages: {e.response['error']}")
        return
    
    # Iterate through direct message channels and count messages between the two users
    for im in ims:
        im_id = im['id']
        info = get_channel_info(im_id)
        if info.get('user') == USER_IDS[1]:
            data = get_user_message_counts(im_id, USER_IDS)
            print(f"In DM {im_id}")
            for d in data.keys():
                print(f"User: {get_user_name(d)} ({d})  sent: {data[d]} messages")
            print("")


if __name__ == "__main__":
    get_dm_messages()
    
    for channel in SPECIFIED_CHANNELS:
        data = get_user_message_counts(channel, USER_IDS)
        print(f"Numbesr of Message Sent to Channel: {get_channel_name(channel)} ({channel}) -> ")
        for d in data.keys():
            print(f"User: {get_user_name(d)} ({d})  sent: {data[d]} messages")
        print("")
        
        
    # for dm in SPECIFIED_DMS_AND_GROUPS:
    #     data = get_user_message_counts(dm, USER_IDS)
    #     print(f"Numbesr of Message Sent to DM: {dm} -> ")
    #     for d in data.keys():
    #         print(f"User: {get_user_name(d)} ({d})  sent: {data[d]} messages")
    #     print("")
        
    # print(get_all_channels_and_groups())
