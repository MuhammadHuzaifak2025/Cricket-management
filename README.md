# Django Cricket Management System

This is a Django-based Cricket Management System that provides various APIs for managing users, players, teams, coaches, and matches. It includes endpoints for creating and managing users, adding players and coaches, creating teams and matches, and viewing player and team data.

## Features

- User Management
  - Create a new user
  - Login user
- Player Management
  - Create a new player
  - Get player data
  - Add player to a team
- Team Management
  - Create a new team
  - Get team data
- Coach Management
  - Create a new coach
- Match Management
  - Create a new match
  - View all matches
- Utility
  - Generate temporary teams with fake data
  - Perform a virtual toss
-  Real-time Match Updates
  - WebSocket support for live match details (Not Completed yet)

## DataBase Erd Diagram:
![image](https://github.com/MuhammadHuzaifak2025/Cricket-management/assets/115894335/09bb712d-9ee7-47b8-979d-3691bd351e98)

Models
The system uses several models:

User: Default Django User model for authentication.
Player: Represents a cricket player.
Team: Represents a cricket team.
Coach: Represents a coach of a team.
Match: Represents a match between two teams.
Innings: Represents an innings in a match.
BallEvent: Represents an event (like a run or wicket) in a match.

Extentions:
Postman
Github Copilot
Websocketking

Contributor:
Muhammad Huzaifa (Owner).

## Thank You

Thank you for using the Django Cricket Management System! We hope this system meets your needs for managing cricket matches, teams, and players, and provides a seamless experience with real-time updates through WebSockets. Your feedback is invaluable, so please feel free to reach out with any suggestions or issues you encounter. Happy coding and enjoy the game!

Best regards,

Muhammad Huzaifa
