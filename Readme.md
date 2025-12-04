# Tic Tac Toe AI Game

This repository contains a Tic Tac Toe game with three AI difficulties:
- **Easy** — plays using a Reinforcement Learning (RL) agent (uses learned Q-values).
- **Medium** — runs a short self-play training session (warm-up) and then uses the RL agent.
- **Hard** — perfect-play AI using the Minimax algorithm.

The AI stores its learned Q-values and training experience to disk so it improves over time.

## Demo Video
Tic Tac Toe Demonstration: [Meeting Recording](https://teams.microsoft.com/l/meetingrecap?driveId=b%21rYSbpyc59UmqpjTOXwwJE1JrpA83JDFPlJSDxFsVxNU8Ir6ZoSmQS6iYo5Vv_D4E&driveItemId=01KPAHYJDRR34XKX27GNELCTGPHF2QSVVG&sitePath=https%3A%2F%2Fbyupathwayworldwideprod-my.sharepoint.com%2F%3Av%3A%2Fg%2Fpersonal%2Fdjigu_byupathway_edu%2FIQBxjvl1X18zSLFMzzl1CVamAd43s9by3V7-tx3PLxoBNtQ&fileUrl=https%3A%2F%2Fbyupathwayworldwideprod-my.sharepoint.com%2Fpersonal%2Fdjigu_byupathway_edu%2FDocuments%2FRecordings%2FTic%2520Tac%2520Toe-20251204_042852-Meeting%2520Recording.mp4%3Fweb%3D1&threadId=19%3Ameeting_MzBjMGZmN2QtYzhhMy00MDJhLWE4YjgtMDc1MWVhN2Y2ODZi%40thread.v2&organizerId=92c31936-c937-45e7-a261-4fe74b92ebd8&tenantId=42804ae1-d2e9-40b7-a4a3-45811234298b&callId=f7e37af3-e267-4673-8a54-f0b100a72dc2&threadType=Meeting&meetingType=MeetNow&subType=RecapSharingLink_RecapCore)

## Files
- `tic_tac_toe.py` — main Python game and AI implementation.


## Requirements
- Python 3.8+
- Packages: `numpy`  
  Install with:
  ```bash
  pip install numpy
