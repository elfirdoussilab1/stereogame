uniform sampler2D sTextures[8];

varying vec2 vTexCoord;

void main() {
    // getting the screen coordinates (0,0) is the bottom left corner
    float x = gl_FragCoord.x - 0.5;
    float y = gl_FragCoord.y - 0.5;
    
    // The view indices for the current pixel
    float Ri = mod(3.0 * x + y + 8.0, 8.0);
    float Gi = mod(3.0 * x + y + 9.0, 8.0);
    float Bi = mod(3.0 * x + y + 10.0, 8.0);
    
    // init pixel colors to black
    float r = 0.0;
    float g = 0.0;
    float b = 0.0;

    float r0 = texture2D(sTextures[0], vTexCoord).r;
    float g0 = texture2D(sTextures[0], vTexCoord).g;
    float b0 = texture2D(sTextures[0], vTexCoord).b;

    float r1 = texture2D(sTextures[1], vTexCoord).r;
    float g1 = texture2D(sTextures[1], vTexCoord).g;
    float b1 = texture2D(sTextures[1], vTexCoord).b;

    float r2 = texture2D(sTextures[2], vTexCoord).r;
    float g2 = texture2D(sTextures[2], vTexCoord).g;
    float b2 = texture2D(sTextures[2], vTexCoord).b;

    float r3 = texture2D(sTextures[3], vTexCoord).r;
    float g3 = texture2D(sTextures[3], vTexCoord).g;
    float b3 = texture2D(sTextures[3], vTexCoord).b;

    float r4 = texture2D(sTextures[4], vTexCoord).r;
    float g4 = texture2D(sTextures[4], vTexCoord).g;
    float b4 = texture2D(sTextures[4], vTexCoord).b;

    float r5 = texture2D(sTextures[5], vTexCoord).r;
    float g5 = texture2D(sTextures[5], vTexCoord).g;
    float b5 = texture2D(sTextures[5], vTexCoord).b;

    float r6 = texture2D(sTextures[6], vTexCoord).r;
    float g6 = texture2D(sTextures[6], vTexCoord).g;
    float b6 = texture2D(sTextures[6], vTexCoord).b;

    float r7 = texture2D(sTextures[7], vTexCoord).r;
    float g7 = texture2D(sTextures[7], vTexCoord).g;
    float b7 = texture2D(sTextures[7], vTexCoord).b;


    // VIEW 0
    if(Ri == 0.0) {
        r = r0;
        g = g1;
        b = b2;
    }

    if(Ri == 1.0) {
        r = r1;
        g = g2;
        b = b3;
    }

    if(Ri == 2.0) {
        r = r2;
        g = g3;
        b = b4;
    }

    if(Ri == 3.0) {
        r = r3;
        g = g4;
        b = b5;
    }

    if(Ri == 4.0) {
        r = r4;
        g = g5;
        b = b6;
    }

    if(Ri == 5.0) {
        r = r5;
        g = g6;
        b = b7;
    }

    if(Ri == 6.0) {
        r = r6;
        g = g7;
        b = b0;
    }

    if(Ri == 7.0) {
        r = r7;
        g = g0;
        b = b1;
    }

    gl_FragColor = vec4(r, g, b, 1.0);
}