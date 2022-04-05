# Discord-Crypto-wallet

Hello! This is a discord crypto wallet!

**Pros and cons:**
| Feature  | Exists |
| -------- | ------ |
| 2FA  | ✅  |
| Multiple users  | ✅  |
| JSON RPC error handling  | ✅  |
| Multiple wallets per users  | ❌  |


**Setup:**
1. Paste your discord bot token into the ``DiscordToken``file
2. Get the ``serviceAccountKey.json`` file from google FireStore, [guide](https://clemfournier.medium.com/how-to-get-my-firebase-service-account-key-file-f0ec97a21620)
3. Change RPC password/username/host in the ``bot.py`` file
4. Test it out ussing slash commands (Be sure to see if you can recieve funds and enable 2FA)
5. Enjoy!


**Maintaning the bot:**
1. If you get a undefined error report from a user or if you see one in the terminal please report it to me, and I'll push a fix!
2. Update the bot regularly!
3. Please post suggestions, bug fixes, bug reports and etc in issues!

**Testing the bot for yourself:**
I have currently set it up to work with Optical Bitcoin [oBTC], you may test it out in my [discord server](https://discord.gg/3BKBr8ZRm2) or by [inviting it](https://discord.com/oauth2/authorize?client_id=944217990734434365&permissions=517677111616&scope=bot%20applications.commands)
