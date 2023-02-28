uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
    
attribute vec3 aVertex;
attribute vec2 aTexCoord;

varying vec2 vTexCoord;
varying vec3 vPosition;
varying vec3 vPositionW;

void main() {
    vTexCoord = aTexCoord;
    vPosition = aVertex;
    vPositionW = vec3(uPMatrix * uMVMatrix * vec4(aVertex, 1.0));

    gl_Position = (uPMatrix * uMVMatrix)  * vec4(aVertex, 1.0);
}