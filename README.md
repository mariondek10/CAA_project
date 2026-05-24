# CAA_project

Overall Architecture
GPS (9600 baud) ──┐
├── Grove HUB ── Port C (UART2) ── M5Stack Core2
logic:
Switch to GPS baud → read NMEA → parse coordinates → calculate speed

## M5stack functionalities :

When turned on, the m5stack will allow the user to config a wifi, for the utulisation to be more easy, the m5stack directly connects the default config if no other wifi set.

after it, je gps search but the session starts only when the user decides.

Here are the controls :

Bouton A (left) : Start (is stopped) / Pause (if running) / resume (if paused).

Bouton C (right) : Stop (ending session, if start pressed, a new session begins).

The speed shown on the screen is an average, it is more smooth this way and avoid the jumps.

## dashboard

## implementation

google cloud
docker
deployed on https://bike-backend-387007830650.europe-west6.run.app
