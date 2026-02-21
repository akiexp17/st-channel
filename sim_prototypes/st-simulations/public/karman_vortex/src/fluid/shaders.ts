export const baseVertexShader = `
precision highp float;
attribute vec2 aPosition;
varying vec2 vUv;
varying vec2 vL;
varying vec2 vR;
varying vec2 vT;
varying vec2 vB;
uniform vec2 texelSize;

void main () {
    vUv = aPosition * 0.5 + 0.5;
    vL = vUv - vec2(texelSize.x, 0.0);
    vR = vUv + vec2(texelSize.x, 0.0);
    vT = vUv + vec2(0.0, texelSize.y);
    vB = vUv - vec2(0.0, texelSize.y);
    gl_Position = vec4(aPosition, 0.0, 1.0);
}
`;

export const displayShaderSource = `
precision highp float;
precision highp sampler2D;
varying vec2 vUv;
uniform sampler2D uTexture;
uniform vec2 obstacleCenter;
uniform float obstacleRadius;
uniform float aspectRatio;

void main () {
    vec3 color = texture2D(uTexture, vUv).rgb;
    // Draw the obstacle
    vec2 p = vUv - obstacleCenter;
    p.x *= aspectRatio;
    if (length(p) < obstacleRadius) {
        // Neon cyan/magenta coloring for the pole
        color = vec3(0.1, 0.8, 0.9);
    }
    gl_FragColor = vec4(color, 1.0);
}
`;

export const splatShaderSource = `
precision highp float;
precision highp sampler2D;
varying vec2 vUv;
uniform sampler2D uTarget;
uniform float aspectRatio;
uniform vec3 color;
uniform vec2 point;
uniform float radius;

void main () {
    vec2 p = vUv - point.xy;
    p.x *= aspectRatio;
    vec3 splat = exp(-dot(p, p) / radius) * color;
    vec3 base = texture2D(uTarget, vUv).xyz;
    gl_FragColor = vec4(base + splat, 1.0);
}
`;

export const constantInflowShaderSource = `
precision highp float;
precision highp sampler2D;
varying vec2 vUv;
uniform sampler2D uTarget;
uniform vec3 inflowColor;
uniform vec2 inflowVelocity;
uniform float isVelocity; // 1.0 if writing to velocity texture, 0.0 if dye

void main () {
    vec3 base = texture2D(uTarget, vUv).xyz;
    
    // Create an invisible wind inflow on the left side
    float mask = step(vUv.x, 0.05); // Left edge
    
    // Only apply wind velocity, do not inject color (so no 'blue wall' appears)
    vec3 newVal = mix(base, isVelocity > 0.5 ? vec3(inflowVelocity, 0.0) : base, mask * 0.2);
    gl_FragColor = vec4(newVal, 1.0);
}
`;


export const advectionShaderSource = `
precision highp float;
precision highp sampler2D;
varying vec2 vUv;
uniform sampler2D uVelocity;
uniform sampler2D uSource;
uniform vec2 texelSize;
uniform vec2 dyeTexelSize;
uniform float dt;
uniform float dissipation;

void main () {
    vec2 coord = vUv - dt * texture2D(uVelocity, vUv).xy * texelSize;
    vec4 result = texture2D(uSource, coord);
    float decay = 1.0 + dissipation * dt;
    gl_FragColor = result / decay;
}
`;

export const divergenceShaderSource = `
precision highp float;
precision highp sampler2D;
varying highp vec2 vUv;
varying highp vec2 vL;
varying highp vec2 vR;
varying highp vec2 vT;
varying highp vec2 vB;
uniform sampler2D uVelocity;
uniform vec2 obstacleCenter;
uniform float obstacleRadius;
uniform float aspectRatio;

void main () {
    // Check obstacle
    vec2 p = vUv - obstacleCenter;
    p.x *= aspectRatio;
    if (length(p) < obstacleRadius) {
        gl_FragColor = vec4(0.0);
        return;
    }

    float L = texture2D(uVelocity, vL).x;
    float R = texture2D(uVelocity, vR).x;
    float T = texture2D(uVelocity, vT).y;
    float B = texture2D(uVelocity, vB).y;

    if (vL.x < 0.0) L = -texture2D(uVelocity, vR).x;
    if (vR.x > 1.0) R = -texture2D(uVelocity, vL).x;
    if (vT.y > 1.0) T = -texture2D(uVelocity, vB).y;
    if (vB.y < 0.0) B = -texture2D(uVelocity, vT).y;

    float div = 0.5 * (R - L + T - B);
    gl_FragColor = vec4(div, 0.0, 0.0, 1.0);
}
`;

export const pressureShaderSource = `
precision highp float;
precision highp sampler2D;
varying highp vec2 vUv;
varying highp vec2 vL;
varying highp vec2 vR;
varying highp vec2 vT;
varying highp vec2 vB;
uniform sampler2D uPressure;
uniform sampler2D uDivergence;
uniform vec2 obstacleCenter;
uniform float obstacleRadius;
uniform float aspectRatio;

void main () {
    vec2 p = vUv - obstacleCenter;
    p.x *= aspectRatio;
    if (length(p) < obstacleRadius) {
        gl_FragColor = vec4(0.0);
        return;
    }

    float L = texture2D(uPressure, vL).x;
    float R = texture2D(uPressure, vR).x;
    float T = texture2D(uPressure, vT).x;
    float B = texture2D(uPressure, vB).x;
    float C = texture2D(uDivergence, vUv).x;
    
    if (vL.x < 0.0) L = texture2D(uPressure, vR).x;
    if (vR.x > 1.0) R = texture2D(uPressure, vL).x;
    if (vT.y > 1.0) T = texture2D(uPressure, vB).x;
    if (vB.y < 0.0) B = texture2D(uPressure, vT).x;

    float pressure = (L + R + B + T - C) * 0.25;
    gl_FragColor = vec4(pressure, 0.0, 0.0, 1.0);
}
`;

export const gradientSubtractShaderSource = `
precision highp float;
precision highp sampler2D;
varying highp vec2 vUv;
varying highp vec2 vL;
varying highp vec2 vR;
varying highp vec2 vT;
varying highp vec2 vB;
uniform sampler2D uPressure;
uniform sampler2D uVelocity;
uniform vec2 obstacleCenter;
uniform float obstacleRadius;
uniform float aspectRatio;

void main () {
    vec2 p = vUv - obstacleCenter;
    p.x *= aspectRatio;
    if (length(p) < obstacleRadius) {
        gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
        return;
    }

    float L = texture2D(uPressure, vL).x;
    float R = texture2D(uPressure, vR).x;
    float T = texture2D(uPressure, vT).x;
    float B = texture2D(uPressure, vB).x;

    vec2 velocity = texture2D(uVelocity, vUv).xy;
    velocity.xy -= vec2(R - L, T - B);
    gl_FragColor = vec4(velocity, 0.0, 1.0);
}
`;
