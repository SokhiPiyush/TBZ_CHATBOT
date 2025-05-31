# TBZ_CHATBOT

This repository contains a basic Rasa chatbot for TravelBullz. The bot collects travel preferences such as destination country, cities to visit, number of nights in each city, number of passengers and travel date. Options are presented using clickable buttons where possible.

## Setup
1. Install Rasa Open Source (`pip install rasa`).
2. Run the action server:
   ```bash
   rasa run actions
   ```
3. In a separate terminal, start the bot:
   ```bash
   rasa shell
   ```
