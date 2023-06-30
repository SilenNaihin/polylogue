# polylogue

Polylogue is an AI-powered Discord bot designed to engage in real-time conversations. It understands and contributes to discussions, facilitating engaging communication, and fostering a more interactive community environment.

Bot that can get added by a user to a voice chat they are currently in !logue. The bot listens to the conversation that is going on, and transcribes the speech using an api route /transcribe. Every 10 seconds, it calls the /create api and passes in all of the transcribed text. After it gets a response, it calls the /create api once again. If the /create api decides, it will call a function that raises the bots hand. If a user then does something with the bot, the /speak api to speak the output of the text.
