from feather.materials.textureMaterial import TextureMaterial
from feather.shapes.cube import Cube
from feather.texture import Texture
import random

allEffects = {1:'disparition',2:'teleport',3:'bomb',4:'x3',5:'superbat', 6:'increaseEyeDistance', 7:'decreaseEyeDistance', 8:'switchViews'}

class MysteryBox(Cube):
    

    # battlex is the attribute size_x of the battlefield, and same thing for battley and battlez
    def __init__(self,name, battlefield, scene = None):
        Cube.__init__(self, name,True, scene)
        self.battlex, self.battley, self.battlez = battlefield.getSizex(), battlefield.getSizey(), battlefield.getSizez()
        boxMat = TextureMaterial(Texture("./assets/question.jpeg"))
        self.setMaterial(boxMat)
        self.setPosition(
            random.uniform(-self.battlex / 1.5, self.battlex / 1.5),
            random.uniform(-self.battley / 1.5, self.battley / 1.5),
            random.uniform(-self.battlez / 1.5, self.battlez / 1.5)
        )

    def isCollision(self, ball):
        ballposition = ball.getPosition()
        x,y,z = ballposition.x, ballposition.y, ballposition.z
        position = self.getPosition()
        bx, by, bz = position.x,position.y,position.z

        collisionRadius = 1.5

        if abs(bx-x)<= collisionRadius and abs(by-y)<= collisionRadius and abs(bz-z)<= collisionRadius:
            return True
        return False
    
    def onHit(self,ball):
        x,y,z = self.battlex, self.battley, self.battlez
        self.setPosition(random.uniform(-x+2, x-2), random.uniform(-y + 2, y-2), random.uniform(-3, 3))
        effect = random.randint(1,8)
        #effect = 3
        ball.applyEffect(allEffects[effect])

