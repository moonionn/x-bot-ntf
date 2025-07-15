<div align="center">

<a href="./AVATAR.md"><img alt="LOGO" src="/images/md/avatar.png" width="300" height="300" /></a>

# x_bot_ntf

A Discord Bot for Twitter Notifications

[![](https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)

[**English**](./README.md) | [**繁體中文**](./R### 3. Run the bot

````shell
python bot.py
```_zh.md)

</div>

## 📝Introduction

x_bot_ntf is a Discord bot that leverages the [tweety-ns module](https://github.com/mahrtayyab/tweety) to provide real-time tweet updates from specific Twitter users directly to your Discord server. Simply configure the Twitter users and Discord channels you want to monitor, and x_bot_ntf will automatically forward tweets to the designated channels, ensuring you never miss important updates.🐦

## ✨Features

- 🐦 **Real-time Twitter Monitoring**: Automatically track and forward tweets from specified Twitter users to Discord channels
- 🌍 **Tweet Translation**: Translate tweets using Gemini AI with dual translation styles (direct + natural) and detailed explanations
- 🤖 **Auto Translation**: Automatically translate tweet links posted in designated channels without manual commands
- 📱 **Rich Embed Support**: Display tweets with images, videos, and formatted content
- ⚙️ **Easy Management**: Simple commands to add/remove tracked users and manage auto-translation channels
- 🔧 **Flexible Configuration**: Customizable settings for check intervals, notification preferences, and more
- 📊 **User Management**: Pagination-based user list management with detailed statistics
- 🛡️ **Error Handling**: Robust error recovery and automatic retry mechanisms
- 🎨 **Modern UI**: Beautiful, responsive embed designs with avatar support

<details>
   <summary>

### Screenshots

   </summary>
👇Whenever a followed user posts a new tweet, your server will receive an instant notification.

![](/images/md/screenshot.png)

</details>

<details>
   <summary>

### Commands

   </summary>

#### 🐦 Twitter Tracking Commands

👉 `.add @username #channel` - Add a Twitter user to be tracked in a specific channel

👉 `.remove @username #channel` - Remove a Twitter user from tracking in a specific channel

👉 `.list` - List all tracked Twitter users on the current server

#### 🌍 Translation Commands

👉 `/translate <tweet_url>` - Manually translate a tweet

**Supported URL formats:**
- `https://twitter.com/username/status/1234567890`
- `https://x.com/username/status/1234567890`

#### 🤖 Auto Translation Commands

👉 `/autotranslate add_channel #channel` - Enable auto translation for a channel

👉 `/autotranslate remove_channel #channel` - Disable auto translation for a channel

👉 `/autotranslate list_channels` - List all channels with auto translation enabled

👉 `/autotranslate status` - Check the status of translation functionality

#### 📊 Advanced Management Commands

👉 `/add notifier` `username` `channel` | `mention` `type` `media_type` `account_used`

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `username` | str | The username of the twitter user you want to turn on notifications for |
| `channel` | discord.TextChannel | The channel to which the bot delivers notifications |
| `mention` | discord.Role | The role to mention when notifying |
| `type` | str | Whether to enable notifications for retweets & quotes |
| `media_type` | str | Whether to enable notifications that include media, or only enable notifications that include media |
| `account_used` | str | The twitter client used by the bot to monitor the user's tweets |

👉 `/remove notifier` `channel` `username`

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `channel` | str | The channel id which set to delivers notifications |
| `username` | str | The username of the twitter user you want to turn off notifications for |

👉 `/list users` | `account` `channel`

- List all twitter users whose notifications are enabled on the current server

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `account` | str | The client name that you want to filter |
| `channel` | str | The channel name that you want to filter |

👉 `/sync`

- Sync the notification of new Twitter account with database.  If you change the twitter account used by bot, please use this command

👉 `/customize message` `channel` `username` | `default`

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `channel` | str | The channel id which set to delivers notifications |
| `username` | str | The username of the twitter user you want to set customized message |
| `default` | bool | Whether to use default setting _(default is false)_ |

Custom notification messages are in `f-string format`, currently supporting 4 special variables for use, which will be explained below.

- `{action}` : poster's action, include `tweeted`, `retweeted` and `quoted`
- `{author}` : poster's display name
- `{mention}` : the role to mention when sending to discord
- `{url}` : the link of the tweet

Using the default notification as an example, if the message is customized to the following format (supporting Discord's markdown format):

```plaintext
{mention}**{author}** just {action} here:
{url}
````

The notification will be sent in this format when a tweet is posted (here is a real-world example):

```plaintext
@Ping_SubTweet ﾅﾁｮﾈｺ just tweeted here:
https://twitter.com/nyachodayo/status/1869000108697960952
```

</details>

## 📥Installation

Before running the bot, you need to install the necessary modules.

```shell
pip install -r requirements.txt
```

## ⚡Usage

**📢This tutorial applies to version 0.5 or higher. For settings of older versions, please refer to the README files of the respective historical versions.**

### [⬆️View Version Upgrade Guides](./UPGRADE_GUIDE.md)

### 1. Create and configure the .env file

```env
BOT_TOKEN=YourDiscordBotToken
TWITTER_TOKEN=NameForYourTwitterToken:YourTwitterAccountAuthToken
DATA_PATH=./data
```

> [!NOTE]  
> The `NameForYourTwitterToken` here can be freely defined. It is only used as an alias to specify the account when entering commands and does not need to match the Twitter account name.

#### Example

```env
BOT_TOKEN=FAKE1234567890ABCDEFGHIJKLMNO.PQRSTUVWXYZ1234567890.ABCDEFGHIJKLMNOPQRSTUVWXYZ123456
TWITTER_TOKEN=Account1:12345abcde67890fghij12345klmnop67890qrstuv,Account2:abcdef123456ghijkl7890mnopqrst123456uvwx
DATA_PATH=./data
```

You can retrieve your auth token from cookies, or you can explore other methods to obtain it.

### 2. Configure the configs.yml file

Create `configs.yml` and copy the contents of `configs.example.yml` into it, and edit it to your liking.

> [!IMPORTANT]
> All configuration instructions here are synchronized with the latest version. For users of the old version, please refer to the old README.

#### Base

| Parameter                          | Description                                                      | Restriction                                                                                            |
| ---------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `prefix`                           | The prefix for bot commands, only effective for prefix commands. | None, but recommended to choose a simple and easily identifiable prefix and avoid using empty strings. |
| `activity_name`                    | The activity name displayed by the bot.                          | None.                                                                                                  |
| `activity_type`                    | The activity type displayed by the bot.                          | `playing`, `streaming`, `listening`, `watching` and `competing` only.                                  |
| `users_list_pagination_size`       | `list users` command's pagination size.                          | Only accepts integers, and it is not recommended to use too large or too small values.                 |
| `users_list_page_counter_position` | `list users` command's pagination counter position.              | `title` and `footer` only.                                                                             |

Custom activity name is in `f-string` format, currently supporting 1 special variable for use, which will be explained below.

- `{count}` : the number of users currently being monitored, it will be updated in real time

#### Timer & Counter

| Parameter                    | Description                                                                                                                                                                                                                                                                                                                                                                                                                  | Unit    |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `tweets_check_period`        | The check frequency for the posts, it is not recommended to set this value too low to avoid rate limiting. Default value: `10`, Safety value: `18` [(why is this value?)](https://github.com/mahrtayyab/tweety/wiki/FAQs#twitter-new-limits), not recommended below `10`. If the account controlled by Tweetocrd is the same as the account you usually use, please increase the value appropriately to avoid rate limiting. | seconds |
| `tweets_updater_retry_delay` | Retry Interval when Tweets Updater encounters exceptions.                                                                                                                                                                                                                                                                                                                                                                    | minutes |
| `tasks_monitor_check_period` | Interval at which to check if each tasks is functioning properly, and if a task has stopped, attempt a restart.                                                                                                                                                                                                                                                                                                              | minutes |
| `tasks_monitor_log_period`   | Interval at which to output the list of currently running tasks to the execution log.                                                                                                                                                                                                                                                                                                                                        | hours   |
| `auth_max_attempts`          | The maximum number of attempts to log in to the Twitter account, if the number of failures exceeds this number, the bot will be forced to stop running.                                                                                                                                                                                                                                                                      | times   |

#### Control Account Behavior

| Parameter                    | Description                                                                                                      |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `auto_change_client`         | If a new client is specified for an exisiting user, automatically use the new client to monitor the user.        |
| `auto_turn_off_notification` | If all notifications for a user are disabled, decide whether to unfollow the user.                               |
| `auto_unfollow`              | If all notifications for a user is disabled, decide whether to disable notification for the user (twitter side). |

#### Database

| Parameter                        | Description                                                                                                                                                                                                               |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `auto_repair_mismatched_clients` | Whether the system should automatically use the first client defined in the current environment variables to replace invalid `client_used` values in the database when they are not defined in the environment variables. |

#### Embed Style

| Parameter | Description                                                              |
| --------- | ------------------------------------------------------------------------ |
| `type`    | Determine the type of embed, supported types: `built_in` / `fx_twitter`. |

##### built_in:

| Parameter           | Description                                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fx_image`          | Whether to use FxTwitter's combined image when there are multiple images, friendly for iOS systems that cannot display multiple image embeddings. |
| `video_link_button` | Determine whether to use a link button as a prompt when the media is a video.                                                                     |
| `legacy_logo`       | If set to `true`, the footer will use Twitter's legacy bluebird logo instead of the new X emblem.                                                 |

##### fx_twitter:

| Parameter             | Description                                                                                                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `domain_name`         | The domain name to be used when sending tweet links, can be `fxtwitter` or `fixupx`.                                                                                                  |
| `original_url_button` | Add a link button at the bottom of the embed that directs to the original tweet. This can resolve the issue where clicking an FxTwitter URL does not open the app on certain devices. |

#### Message

| Parameter         | Description                                                                                                                                                                              |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default_message` | Set default message format globally, the format is the same as the customized message, use f-string and support 4 special variables. For details, please refer to [Commands](#commands). |

#### Translation Settings

| Parameter                             | Description                                    | Restriction                                                                                                 |
| ------------------------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `translation.gemini_api_key`          | Your Gemini API key for translation services.  | Required for translation functionality. Get from [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `translation.default_target_language` | Default target language for translations.      | Default: "繁體中文" (Traditional Chinese)                                                                   |
| `translation.auto_translate_channels` | List of channel IDs for automatic translation. | Array of Discord channel IDs (e.g., [1234567890, 0987654321])                                               |

**Example translation configuration:**

```yaml
translation:
  gemini_api_key: "your_gemini_api_key_here"
  default_target_language: "繁體中文"
  auto_translate_channels: []
```

### 3. Set up environment variables

You also need to set up environment variables for the bot. You can either create a `.env` file or set them in your system:

```env
DISCORD_TOKEN=YourDiscordBotToken
TWITTER_USERNAME=YourTwitterUsername
TWITTER_PASSWORD=YourTwitterPassword
GEMINI_API_KEY=YourGeminiAPIKey
```

### 3. Run and invite the bot to your server

```shell
python bot.py
```

#### Permissions Setup

🔧Bot Permissions Setup (Permissions Integer): `2147666944`

| Enable | Permissions                 |
| ------ | --------------------------- |
| ✔️     | Read Messages/View Channels |
| ✔️     | Send Messages               |
| ✔️     | Embed Links                 |
| ✔️     | Attach Files                |
| ✔️     | Mention Everyone            |
| ✔️     | Use Slash Commands          |

> [!NOTE]  
> Please generate an invitation link with the default permissions on the [Discord Developer Portal](https://discord.com/developers/applications) rather than inviting the bot first and then manually adjusting its permissions.

#### Privileged Gateway Intents Setup

| Enable | Intents                |
| ------ | ---------------------- |
| ❌     | Presence Intent        |
| ❌     | Server Members Intent  |
| ✔️     | Message Content Intent |

> [!NOTE]
> If you want to host the bot on a server, here is a recommended service that is basically free: [fly.io](https://fly.io) _(update: fly.io has stopped offering free plans to new users)_

> [!TIP]
> Alternatively, you can try this virtual hosting service provided by Taiwanese students: [FreeServer](https://freeserver.tw/index.html)

<details>
   <summary><b>⚙️some configuration files you may need if you use fly.io</b></summary>

- dockerfile

```dockerfile
FROM python:3.11.11
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot/
CMD python bot.py
```

- fly.toml

```toml
app = "YOUR_APP_NAME"
primary_region = "YOUR_APP_REGION"

[env]
  DATA_PATH = "/data"

[mounts]
  source = "YOUR_APP_VOLUME_NAME"
  destination = "/data"
```

</details>

### 4. Run the bot

```shell
python bot.py
```

### 5. Have fun

Now you can go back to Discord and use the commands to set up your bot:

**For Twitter tracking:**

- Use `.add @username #channel` to track Twitter users
- Use `.list` to see all tracked users

**For translation features:**

- Use `/translate <tweet_url>` for manual translation
- Use `/autotranslate add_channel #channel` to enable auto translation
- Post tweet links in auto-translation channels for automatic translation

For detailed usage instructions, see the [Usage Guide](../USAGE_GUIDE.md) and [Quick Start Guide](../QUICK_START.md).

## 💪Contributors

This project exists thanks to all the people who contribute.

This project also benefits from the creative contributions of artists who provide our logo.

<a href="./AVATAR.md"><img alt="LOGO" src="/images/md/MarcoDK.png" width="64" height="64" /></a>
