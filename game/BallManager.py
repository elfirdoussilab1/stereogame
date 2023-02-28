class BallManager:
    def __init__(self, balls):
        
        self.balls = list(balls) # liste des projectiles qui se trouvent dans la scène

    def getBalls(self):
        return self.balls
        
    def addBall(self, ball):
        self.balls.append(ball) 

    def removeBall(self, ball):
        
        self.balls.remove(ball)

        ball.destroy()
        
          