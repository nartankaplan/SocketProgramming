# SocketProgramming
Including client and server, basic game named "Stock Market Forecasting Application"  using socket programming. In practice, the server randomly selects a  stock and the client tries to estimate the price of this stock within a  certain tolerance number which is 5%.


This process takes place between a server and a client on the same machine (local). When the client estimates the 
price of a stock selected by the server, the server gives feedback to the client 
according to the correctness of its prediction.

## Case 1: User wins at first prediction
![image](https://github.com/user-attachments/assets/43d6dc3f-037a-4019-800a-d57f6701719b)
If the both server and client logs are being followed, after the client is started as well as 
the server, the server randomly choses stock and sends the stock name to client. After 
that, client asks the user to make a predict. If the user make the right guess, client sends 
the correct guess to the server and server checks if it is right. After being verification, 
server sends message to the client that the answers is correct. At the end, the 
connection between client socket is being closed.

## Case 2: User wins at second precition
![image](https://github.com/user-attachments/assets/7fb9e8da-5966-4e3b-b33b-06e44b408cd1)
After the user enter’s the first input wrong (or out range of tolerance number 5%) server 
sends messsage to make another guess to user. Also gives hint to make the user’s 
predict more correctively. To illustrate, if the input number is less than the stock’s price, 
server sends message “Higher”. If the input number is higher than the stock’s price, 
server sends hint message “Lower” to client. In screenshot of case 2, user input “4200” 
which is less than the actual stock price “4400” the answer is correct since there is a 
tolerance range 5%.  

## Case 3:  User wins at third prediction
![image](https://github.com/user-attachments/assets/dbf9d991-42d4-4179-8c40-ad568e9e4b77)
Like previous case, the only difference between case 2 and 3 is making annother attemp 
in other words, user is making another prediction. After having correct guess. Like 
previous ones, server sends message to client that the answer is correct or in tolerance 
range.  

## Case 4: User loses
![image](https://github.com/user-attachments/assets/5033e774-e457-47ba-b0eb-a91be67c7460)
After making 3 predictions and all the 3 of them is incorrect or out range of tolerance 
range, server sends the correct price of the related stock name and at the client side, 
“Game Over. Too many attempts. Correct price: <correct price> ” message is being 
printed. 

## Case 5: Invalid input from user
![image](https://github.com/user-attachments/assets/c0cb5647-3ac8-45fd-8b39-62a57aa3c71c)
If user enters rather integer or float, server does not accepts the input and sends a 
message to client that the input is wrong “Invalid input. Please enter a valid number.”

## Case 6: Input "End"
![image](https://github.com/user-attachments/assets/7ecb2acd-9152-4971-ba64-6f57b4bd5a35)
If user enters “end” or “END” as a input. The client socket is being closed.


