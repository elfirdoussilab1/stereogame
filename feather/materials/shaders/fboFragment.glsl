uniform sampler2D sTexture;

varying vec2 vTexCoord;

void main() {
    gl_FragColor = texture2D(sTexture, vTexCoord);
}