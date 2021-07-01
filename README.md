# mbed_final

1. My design is to let the BBcat follow a polyline until the BBcar can't find the line on the table and then enter the next mode. 
The method to follow a polyline is line regression. Calculate for the angle and the distance difference between the regression line and middle point. 
Then if the openmv cannot find the line for 2 seconds, the BBcar will enter the Apriltags mode.

2. The apriltags mode is detect the tilt angle and then let the car to choose keep going or rotate for a few angle. The goal is let the car prercisely in the front of the Apriltags. Then the car will enter the last mode. 

3. The last mode is to detect a obstable and avoid it. The car will keep going until the ping detect something and the distance is smaller than 20 centimeter. And then stop the car and rotate for avoid the obstacle. And at this mode, the XBEE will deliver the information back to PC. 


