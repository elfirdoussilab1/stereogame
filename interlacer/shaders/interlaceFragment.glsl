uniform sampler2D sTextures[8];

varying vec2 vTexCoord;

void main() {
    // getting the screen coordinates (0,0) is the bottom left corner
    int x = int(gl_FragCoord.x - 0.5);
    int y = int(gl_FragCoord.y - 0.5);

    // The view indices for the current pixel
    int Ri = mod(3 * x + y + 7, 8.0);
    int Gi = mod(3 * x + y + 8, 8.0);
    int Bi = mod(3 * x + y + 9, 8.0);

    // setting colors according to the view indices
    float r = texture2D(sTextures[Ri], vTexCoord).r;
    float g = texture2D(sTextures[Gi], vTexCoord).g;
    float b = texture2D(sTextures[Bi], vTexCoord).b;
    
    gl_FragColor = vec4(r, g, b, 1.0);
}